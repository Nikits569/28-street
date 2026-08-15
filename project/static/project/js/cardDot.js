const container = document.getElementById('about');
const text = container.textContent;

// Разбиваем по точке с пробелом (или просто по точке)
const parts = text.split('.').filter(part => part.trim().length > 0);

// Создаем новые абзацы
container.innerHTML = parts.map(part => `<p>${part.trim()}.</p>`).join('');