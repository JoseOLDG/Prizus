// Index img redireccion
document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".imgcar img");

    images.forEach((image) => {
        image.addEventListener("click", () => {
            const link = image.getAttribute("data-link");
            if (link) {
                window.location.href = link;
            }
        });
    });
});
