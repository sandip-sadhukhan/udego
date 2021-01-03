const sidenavButton = document.getElementById('sidemenu-button')
const sideBar = document.getElementById('sidenav')

const toggleNavber = () => {
    if(sideBar.classList.contains('d-none')){
        sideBar.className = 'col-md-3'
    }else{
        sideBar.className = 'd-none d-sm-none d-md-block col-md-3'
    }
}

sidenavButton.addEventListener('click', toggleNavber)