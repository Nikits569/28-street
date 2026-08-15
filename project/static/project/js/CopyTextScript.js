
const textElement = document.getElementById('copyText');

textElement.addEventListener('click', () => {
  const text = textElement.innerText;

  navigator.clipboard.writeText(text).then(() => {
    alert('Текст скопійован!');
  }).catch(err => {
    alert('Помилка при копіюванні ' + err);
  });
});
