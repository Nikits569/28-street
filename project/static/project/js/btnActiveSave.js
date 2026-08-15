function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

window.addEventListener('DOMContentLoaded', () => {
  let cook = getCookie('BOX');
  if (cook) {
    let classList = decodeURIComponent(cook).split(',');
    for (let className of classList) {
      className = className.trim();
      let elements = document.getElementsByClassName(className);
      for (let el of elements) {
        if (el.tagName.toLowerCase() === 'input' && el.type === 'checkbox' && el.classList.contains('myCheckbox')) {
          el.checked = true;
        }
      }
    }
  }
});