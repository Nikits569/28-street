document.addEventListener("DOMContentLoaded", function () {
    const sliders = document.querySelectorAll('.slider');

    sliders.forEach(slider => {
        const radios = slider.querySelectorAll('input[type="radio"]');
        if (radios.length <= 1) return;

        let current = 0;

        setInterval(() => {
            radios[current].checked = false;
            current = (current + 1) % radios.length;
            radios[current].checked = true;
        }, 10000);
    });
});