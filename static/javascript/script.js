const sidebar_btn = document.querySelector('#sidebar_btn');
const sidebar = document.querySelector('.sidebar');
const close_sidebar = document.querySelector('#close_sidebar');

close_sidebar.addEventListener('click', () => {
    sidebar.classList.remove('open_sidebar')
})

sidebar_btn.addEventListener('click', () => {
    sidebar.classList.toggle('open_sidebar')
})


