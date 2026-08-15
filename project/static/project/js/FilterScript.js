const scrollBlock = document.getElementById('blockFilter');

// Горизонтальная прокрутка для колесика мыши (ПК)
scrollBlock.addEventListener('wheel', function (e) {
  e.preventDefault();
  scrollBlock.scrollLeft += e.deltaY;
}, { passive: false });

// Переменные для отслеживания свайпа
let isTouching = false;
let touchStartX = 0;
let scrollStartX = 0;

// Начало касания
scrollBlock.addEventListener('touchstart', function (e) {
  isTouching = true;
  touchStartX = e.touches[0].clientX;
  scrollStartX = scrollBlock.scrollLeft;
}, { passive: true });

// Движение пальцем
scrollBlock.addEventListener('touchmove', function (e) {
  if (!isTouching) return;

  const touchX = e.touches[0].clientX;
  const deltaX = touchStartX - touchX;
  scrollBlock.scrollLeft = scrollStartX + deltaX;
}, { passive: true });

// Завершение касания
scrollBlock.addEventListener('touchend', function () {
  isTouching = false;
});