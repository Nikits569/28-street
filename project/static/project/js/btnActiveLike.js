function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

window.addEventListener('DOMContentLoaded', () => {
  let cook_like = getCookie('BOX_like');
  if (cook_like) {
    let classList_like = decodeURIComponent(cook_like).split(',');
    for (let className of classList_like) {
      className = className.trim(); // Убираем лишние пробелы
      let elements_like = document.getElementsByClassName(className);
      for (let el_like of elements_like) {
        if (el_like.tagName.toLowerCase() === 'input' && el_like.type === 'checkbox' && el_like.classList.contains('myCheckboxLike')) {
          el_like.checked = true;
        }
      }
    }
  }
});