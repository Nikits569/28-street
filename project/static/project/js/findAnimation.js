const openBtn = document.getElementById('searchOpen');
const overlay = document.querySelector('.search-overlay');
const input = overlay.querySelector('input');

function openSearch() {

    overlay.classList.add('active');

    openBtn.style.opacity = '0';
    openBtn.style.pointerEvents = 'none';

    setTimeout(() => {
        input.focus();
    }, 150);
}

function closeSearch() {

    overlay.classList.remove('active');

    openBtn.style.opacity = '1';
    openBtn.style.pointerEvents = 'auto';
}

openBtn.addEventListener('click', openSearch);

/* закрытие при потере фокуса */
input.addEventListener('blur', () => {

    // маленькая задержка для плавности
    setTimeout(() => {
        closeSearch();
    }, 150);

});