document.addEventListener('DOMContentLoaded', function () {
  const elements = document.getElementsByClassName("DOT");

  for (let i = 0; i < elements.length; i++) {
    const el = elements[i];
    el.innerHTML = el.innerHTML.replace(/\./g, '.<br>');
  }
});