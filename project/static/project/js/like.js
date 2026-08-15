
const box_like = getCookie('BOX_like');

const decoded_like = decodeURIComponent(box_like);
const BOX_like = decoded_like.split(',');

const box_like_total = getCookie('BOX_like_total');
let TOTAL_BOX;

if (box_like_total) {
    const decoded_total = decodeURIComponent(box_like_total);
    const parsedObject = JSON.parse(decoded_total);
    TOTAL_BOX = parsedObject; // ← без let
} else {
    TOTAL_BOX = {}; // ← без let
}

document.querySelectorAll('.myCheckboxLike').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        let elements = Array.from(document.getElementsByClassName('likesText'));
        let textLike = elements.find(el => el.classList.contains(this.name));
        if (this.checked) {
            if (!BOX_like.includes(this.name)) {
                BOX_like.push(this.name);
                TOTAL_BOX[this.name] = Number(textLike.textContent)+1;
                textLike.textContent = Number(textLike.textContent)+1;

            }
        } else {
            const index_like = BOX_like.indexOf(this.name);
            if (index_like !== -1) {
                BOX_like.splice(index_like, 1);
                TOTAL_BOX[this.name] = Number(textLike.textContent)-1;
                textLike.textContent = Number(textLike.textContent-1)

            }
        }
        const jsonString = JSON.stringify(TOTAL_BOX);
        const encoded = encodeURIComponent(jsonString);

        document.cookie = `BOX_like=${encodeURIComponent(BOX_like.join(','))}; path=/;`;
        document.cookie = `BOX_like_total=${encoded}; path=/;`;
    });
})
