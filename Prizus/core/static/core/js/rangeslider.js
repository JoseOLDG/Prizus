$(document).ready(function () {
    $("#range-slider").ionRangeSlider({
        type: "double", // Dos sliders
        grid: true,
        min: 0, // Valor mínimo
        max: 500000, // Valor máximo
        from: 0, // Valor inicial para el primer slider
        to: 500000, // Valor inicial para el segundo slider
        skin: "square",
        prefix: "$",
    });

    
});
