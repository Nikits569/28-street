function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


const box = getCookie('BOX');

const decoded = decodeURIComponent(box);
const BOX = decoded.split(',');

document.querySelectorAll('.myCheckbox').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            if (!BOX.includes(this.name)) {
                BOX.push(this.name);
            }
        } else {
            const index = BOX.indexOf(this.name);
            if (index !== -1) {
                BOX.splice(index, 1);
            }
        }
        document.cookie = `BOX=${encodeURIComponent(BOX.join(','))}; path=/;`;
    });
})
