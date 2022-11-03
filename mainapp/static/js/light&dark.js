let body = document.querySelector('body')
let mode = document.querySelector('.modemoon')
let icon = document.querySelector('.fa-moon')


mode.addEventListener('click', ()=>{
    body.classList.toggle('dark')
    if(body.classList.contains('dark'))
        icon.classList.replace('fa-moon', 'fa-sun')
    else
        icon.classList.replace('fa-sun', 'fa-moon')  
})