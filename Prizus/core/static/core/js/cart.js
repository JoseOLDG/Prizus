document.addEventListener('DOMContentLoaded', function() {
    const btnCart = document.querySelector('.container-cart-icon');
    const containerCartProducts = document.querySelector('.container-cart-products');
    const productsList = document.querySelector('.container-items');
    const allProducts = [];

    const valorTotal = document.querySelector('.total-pagar');
    const countProducts = document.querySelector('#contador-productos');
    const cartEmpty = document.querySelector('.cart-empty');
    const cartTotal = document.querySelector('.cart-total');

    btnCart.addEventListener('click', () => {
        containerCartProducts.classList.toggle('hidden-cart');
    });

    productsList.addEventListener('click', e => {
        if (e.target.classList.contains('btn-add-cart')) {
            const productDetails = e.target.closest('.item-details');
            const productName = productDetails.getAttribute('data-product-name');
            const productDescription = productDetails.getAttribute('data-product-description');
            const productPrice = productDetails.getAttribute('data-product-price');

            const infoProduct = {
                quantity: 1,
                title: productName,
                description: productDescription,
                price: productPrice,
            };

            const existingProduct = allProducts.find(product => product.title === infoProduct.title);

            if (existingProduct) {
                existingProduct.quantity++;
            } else {
                allProducts.push(infoProduct);
            }

            showHTML();
        }
    });

    function showHTML() {
        // Actualiza la interfaz del carrito con los productos
        // ...

        // Actualiza el valor total y el contador de productos
        let total = 0;
        let totalProducts = 0;

        allProducts.forEach(product => {
            total += product.quantity * parseFloat(product.price.slice(1));
            totalProducts += product.quantity;
        });

        valorTotal.textContent = `$${total.toFixed(2)}`;
        countProducts.textContent = totalProducts;

        // ...
    }

    // ...
});