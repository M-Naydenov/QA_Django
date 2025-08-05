from django import forms
from django.forms import ModelForm

from evaluation.models import CaseType, Evaluation
from users.models import Agent


class AgentCaseSelectionForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none(), label = 'Agent:')
    case_type = forms.ModelChoiceField(queryset=CaseType.objects.none(), label = 'Case Type:')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['agent'].queryset = Agent.objects.filter(team=user.team, is_active=True, role__work_title__in=['Analyst','Senior Analyst'])
            self.fields['case_type'].queryset = CaseType.objects.filter(team=user.team)

        self.fields['agent'].widget.attrs['class'] = 'selector'
        self.fields['case_type'].widget.attrs['class'] = 'selector'

class EvaluationForm(ModelForm):
    def __init__(self, *args, **kwargs ):
        self.user = kwargs.pop('user', None)
        case_type_id = kwargs.pop('case_type_id', None)
        super().__init__(*args, **kwargs)

        self.criteria_mapping = {}

        if case_type_id:
            case_type = CaseType.objects.get(pk=case_type_id)
            case_criteria = case_type.criteria_set.all()

            for c in case_criteria:
                print("Adding field:", f'criteria_{c.id}', c.criteria)
                field_name = f'criteria_{c.id}'
                helptext = f'{c.scoredown*100:.0f}%'

                if c.ftr_scoredown:
                    helptext += ' (affects FTR)'

                self.fields[field_name] = forms.BooleanField(initial=False,
                                                             required=False,
                                                             label=c.criteria,
                                                             help_text=helptext,
                                                             widget=forms.CheckboxInput(attrs={'class':'criteria'}),
                                                             )
                self.criteria_mapping[field_name] = c

            if case_type.ftr_yn:
                self.fields['ftr'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(),
                                                        label='First time resolution:')
            if case_type.case_type == 'Zendesk':
                self.fields['contact_category'] = forms.CharField(widget=forms.TextInput(attrs={
                    'placeholder': 'Zendesk Contact category...'
                }),
                    required=True)

    class Meta:
        model = Evaluation
        fields = [
            'summary',
            'score_reason',
            'case',
            'account_name',
            'contact_date',
        ]

        widgets = {
            'summary':forms.Textarea(attrs={'placeholder':'Provide a description of the contact...'}),
            'score_reason':forms.Textarea(attrs={'placeholder':'Provide a reason for the scoring...'}),
            'case': forms.TextInput( attrs={'placeholder':'Customer identification...'}),
            'account_name': forms.TextInput(attrs={'placeholder':'Case identification...'}),
            'contact_date': forms.DateInput(attrs={'type':'date'}),
        }