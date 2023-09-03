
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('#read_button')) {
        button = document.querySelector('#read_button')
        button.addEventListener('click', () => {
            window.location.pathname = '/read'
        })
    }

    if (document.querySelector('#reading_list_button')) {
        button = document.querySelector('#reading_list_button')
        button.addEventListener('click', () => {
            window.location.pathname = '/unread'
        })
    }
})