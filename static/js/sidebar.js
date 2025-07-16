const toggleButton = document.getElementById('toggle-btn')
const sidebar = document.getElementById('sidebar')

function toggleSidebar(){
    sidebar.classList.toggle('open')
    toggleButton.classList.toggle('rotate')

    Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
        ul.classList.remove('show')
        ul.previousElementSibling.classList.remove('rotate')
    })
}

function toggleSubMenu(button){
    button.nextElementSibling.classList.toggle('show')
    button.classList.toggle('rotate')

    if (!sidebar.classList.contains('open')){
        sidebar.classList.toggle('open')
        toggleButton.classList.toggle('rotate')
    }
}