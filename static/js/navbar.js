// Mobile menu toggle functionality
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

function toggleSubmenu(section) {
    const submenu = document.getElementById(section + '-submenu');
    const icon = document.getElementById(section + '-icon');

    submenu.classList.toggle('hidden');
    icon.classList.toggle('rotate-180');
}