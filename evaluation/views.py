from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView, UpdateView, FormView, CreateView, DetailView, DeleteView

from users.models import Agent
from evaluation.models import Evaluation, CaseType, Criteria, EvaluationTimeline, EvaluationMistakes
from evaluation.forms import AgentCaseSelectionForm, EvaluationForm


# Create your views here.
def start_evaluation_view(request):
    if request.method == 'POST':
        form = AgentCaseSelectionForm(request.POST, user = request.user)
        if form.is_valid():
            request.session['reviewed_agent_id'] = form.cleaned_data['agent'].id
            request.session['agent_name'] = form.cleaned_data['agent'].__str__()
            request.session['case_type'] = form.cleaned_data['case_type'].id
            request.session['case_type_name'] = form.cleaned_data['case_type'].case_type
            return redirect('finalize-evaluation')
    else:
        form = AgentCaseSelectionForm(user = request.user)
    return render(request, 'evaluation/start-evaluation.html', {'form': form})
class EvaluationCreateView(CreateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'evaluation/continue-evaluation.html'
    success_url = reverse_lazy('overview')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['case_type_id'] = self.request.session.get('case_type')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case_type_id = self.request.session.get('case_type')
        context['case_type'] = CaseType.objects.get(id=case_type_id)
        return context

    def form_valid(self, form):
        agent_id = self.request.session.get('reviewed_agent_id')
        case_type_id = self.request.session.get('case_type')

        agent = Agent.objects.get(id=agent_id)
        case_type = CaseType.objects.get(id=case_type_id)
        evaluator = Agent.objects.get(id=self.request.user.id)

        # calculate score
        score = 1
        for field_name, criteria in form.criteria_mapping.items():
            if form.cleaned_data.get(field_name):
                score -= criteria.scoredown
        score = max(score, 0)

        # calculate seconds for EvaluationTimeline
        total_time = 0
        start_time = self.request.session.get('evaluation_start_time')
        if start_time:
            start_time = parse_datetime(start_time)
            end_time = timezone.now()
            total_time = (end_time - start_time).total_seconds()

        evaluation = form.save(commit=False)

        evaluation.agent = agent
        evaluation.case_type = case_type
        evaluation.evaluator = evaluator
        evaluation.score = score
        if case_type.ftr_yn:
            evaluation.ftr = form.cleaned_data.get('ftr')

        if case_type.case_type == 'Zendesk':
            evaluation.contact_category = form.cleaned_data.get('contact_category')
        # insert Evaluation into the Evaluation model
        evaluation.save()

        # insert Mistakes into the Mistakes model
        for field_name, criteria in form.criteria_mapping.items():
            if form.cleaned_data.get(field_name):
                EvaluationMistakes.objects.create(
                    evaluation=evaluation,
                    criteria=criteria)

        # insert handling time into the Timeline model
        EvaluationTimeline.objects.create(
            evaluation=evaluation,
            modifier=evaluator,
            handling_time_seconds=total_time
        )

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.request.session['evaluation_start_time'] = timezone.now().isoformat()
        return super().get(request, *args, **kwargs)

class EditEvaluationView(UpdateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name='evaluation/continue-evaluation.html'
    success_url = reverse_lazy('overview')
    slug_field = 'uuid_field'
    slug_url_kwarg = 'uuid_field'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['case_type_id'] = self.object.case_type.id
        return kwargs

    def get_initial(self):
        initial = super().get_initial()

        mistakes = self.object.evaluationmistakes_set.all()
        for mistake in mistakes:
            field_name = f'criteria_{mistake.criteria.id}'
            initial[field_name] = True

        if self.object.case_type.ftr_yn:
            initial['ftr'] = self.object.ftr

        if self.object.case_type == 'Zendesk':
            initial['contact_category'] = self.object.contact_category

        return initial

    def form_valid(self, form):
        evaluation = form.save(commit=False)

        evaluation.modifier = self.request.user
        evaluation.modification_date = timezone.now()
        score = 1
        for field_name, criteria in form.criteria_mapping.items():
            if form.cleaned_data.get(field_name):
                score -= criteria.scoredown
        evaluation.score = max(score,0)

        if evaluation.case_type.ftr_yn:
            evaluation.ftr = form.cleaned_data.get('ftr')

        if evaluation.case_type == 'Zendesk':
            evaluation.contact_category = form.cleaned_data.get('contact_category')

        evaluation.save()

        # delete and reinsert the mistakes
        evaluation.evaluationmistakes_set.all().delete()
        for field_name, criteria in form.criteria_mapping.items():
            if form.cleaned_data.get(field_name):
                EvaluationMistakes.objects.create(evaluation=evaluation,criteria=criteria)

        total_time = 0
        start_time = self.request.session.get('evaluation_start_time')
        if start_time:
            start_time = parse_datetime(start_time)
            end_time = timezone.now()
            total_time = (end_time - start_time).total_seconds()

        EvaluationTimeline.objects.create(
            evaluation=evaluation,
            modifier=self.request.user,
            handling_time_seconds=total_time)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.request.session['evaluation_start_time'] = timezone.now().isoformat()
        return super().get(request, *args, **kwargs)


class EvaluationListView(ListView):
    model = Evaluation
    template_name = 'evaluation/overview.html'
    context_object_name = 'evaluations'

    def get_queryset(self):
        if self.request.user.role.work_title == 'Analyst':
            Evaluation.objects.filter(agent=self.request.user).order_by('-evaluation_date')
        elif self.request.user.role.work_title == 'Senior Analyst':
            Evaluation.objects.filter(evaluator=self.request.user).order_by('-evaluation_date')
        else:
            return Evaluation.objects.filter(agent__team=self.request.user.team).order_by('-evaluation_date')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluations = self.get_queryset()

        for evaluation in evaluations:
            evaluation.score_percent = f'{evaluation.score * 100:.0f}'

        context['evaluations'] = evaluations
        return context


class EvaluationDetailsView(DetailView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'evaluation/continue-evaluation.html'
    slug_field = 'uuid_field'
    slug_url_kwarg = 'uuid_field'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        evaluation = self.get_object()

        initial = {}
        for mistake in evaluation.evaluationmistakes_set.all():
            field_name = f'criteria_{mistake.criteria.id}'
            initial[field_name] = True

        if evaluation.case_type.ftr_yn:
            initial['ftr'] = evaluation.ftr

        if evaluation.case_type == 'Zendesk':
            initial['contact_category'] = evaluation.contact_category

        form = EvaluationForm(
            instance=evaluation,
            initial = initial,
            user=self.request.user,
            case_type_id=evaluation.case_type.id
        )

        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

        context['form'] = form
        context['case_type'] = evaluation.case_type
        context['view_only'] = True

        return context

class DeleteEvaluationView(DeleteView):
    model = Evaluation
    form_class = EvaluationForm
    slug_field = 'uuid_field'
    slug_url_kwarg = 'uuid_field'
    success_url = reverse_lazy('overview')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class SearchEvaluationView(ListView):
    pass

class ReAuditView:
    pass

