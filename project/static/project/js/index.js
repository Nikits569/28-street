<script>
  document.getElementById('image').addEventListener('click', function () {
    const image = document.getElementById('image');
    const search = document.getElementById('search');

    image.style.display = 'none';           // Скрываем изображение
    search.style.display = 'block';         // Показываем строку поиска
    setTimeout(() => {
      search.classList.add('show');         // Плавное появление (через opacity)
    }, 10); // даём время браузеру применить display перед добавлением класса
  });
</script>
