const link = window.location.href;
const trimmed = link.endsWith('/') ? link.slice(0, -1) : link;
const lastPartWithParams = trimmed.substring(trimmed.lastIndexOf('/') + 1);
const lastPart = lastPartWithParams.split('?')[0]; // Убираем query-параметры

if (lastPart) {
    const elements = document.querySelectorAll(`.borderImage.${CSS.escape(lastPart)}`);

    if (elements.length > 0) {
        for (let el of elements) {
            if (el.classList.contains(lastPart)) {
                el.style.backgroundColor = 'rgb(242, 177, 199)';
                el.querySelector('.filterImageDefault').style.opacity = 0;
                el.querySelector('.filterImageHover').style.opacity = 1;
                break;
            }
        }
    }
}