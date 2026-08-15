//let current = 0;
//
//const slides = document.getElementById("slides");
//const total = slides.children.length;
//const dotsContainer = document.getElementById("dots");
//
//// create dots
//for (let i = 0; i < total; i++) {
//  const dot = document.createElement("div");
//  dot.classList.add("dot");
//  dot.onclick = () => goToSlide(i);
//  dotsContainer.appendChild(dot);
//}
//
//const dots = document.querySelectorAll(".dot");
//
//function update() {
//  slides.style.transform = `translateX(-${current * 100}%)`;
//
//  dots.forEach(d => d.classList.remove("active"));
//  dots[current].classList.add("active");
//}
//
//function nextSlide() {
//  current = (current + 1) % total;
//  update();
//}
//
//function prevSlide() {
//  current = (current - 1 + total) % total;
//  update();
//}
//
//function goToSlide(i) {
//  current = i;
//  update();
//}
//
//// autoplay
//setInterval(nextSlide, 5000);
//
//// init
//update();



const slides = document.getElementById("slides");
const dotsContainer = document.getElementById("dots");

if (slides && dotsContainer) {
    let current = 0;
    const total = slides.children.length;

    for (let i = 0; i < total; i++) {
        const dot = document.createElement("div");
        dot.classList.add("dot");
        dot.onclick = () => goToSlide(i);
        dotsContainer.appendChild(dot);
    }

    const dots = document.querySelectorAll(".dot");

    function update() {
        slides.style.transform = `translateX(-${current * 100}%)`;
        dots.forEach(d => d.classList.remove("active"));
        dots[current].classList.add("active");
    }

    function nextSlide() {
        current = (current + 1) % total;
        update();
    }

    function prevSlide() {
        current = (current - 1 + total) % total;
        update();
    }

    function goToSlide(i) {
        current = i;
        update();
    }

    setInterval(nextSlide, 5000);
    update();
}