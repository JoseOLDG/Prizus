document.addEventListener('DOMContentLoaded', function() {
    const btnCart = document.querySelector('.container-cart-icon');
    const containerCartProducts = document.querySelector('.container-cart-products');
    const productsList = document.querySelector('.container-items');
    const allProducts = [];

    const valorTotal = document.querySelector('.total-pagar');
    const countProducts = document.querySelector('#contador-productos');
    const cartEmpty = document.querySelector('.cart-empty');
    const cartTotal = document.querySelector('.cart-total');

    // Función para mostrar los productos en el carrito
    function showHTML() {
        // Actualiza la interfaz del carrito con los productos
        // ...

        // Actualiza el valor total y el contador de productos
        let total = 0;
        let totalProducts = 0;

        // Limpia el contenido actual del carrito
        containerCartProducts.innerHTML = '';

        allProducts.forEach(product => {
            total += product.quantity * parseFloat(product.price.slice(1));
            totalProducts += product.quantity;

            // Crear elementos HTML para mostrar los productos en el carrito
            const cartProduct = document.createElement('div');
            cartProduct.classList.add('cart-product');

            const infoCartProduct = document.createElement('div');
            infoCartProduct.classList.add('info-cart-product');

            const cantidadProductoCarrito = document.createElement('span');
            cantidadProductoCarrito.textContent = product.quantity; // Mostrar la cantidad

            const imagenProductoCarrito = document.createElement('img'); // Crear una etiqueta <img> para la imagen
            imagenProductoCarrito.src = product.img; // Establecer la URL de la imagen

            const tituloProductoCarrito = document.createElement('p');
            tituloProductoCarrito.textContent = product.title; // Mostrar el nombre del producto

            const descriptionProductoCarrito = document.createElement('p');
            descriptionProductoCarrito.textContent = product.description; // Mostrar la descripción del producto

            const precioProductoCarrito = document.createElement('span');
            precioProductoCarrito.textContent = product.price; // Mostrar el precio

            // Agregar los elementos al contenedor del producto en el carrito
            infoCartProduct.appendChild(imagenProductoCarrito); // Agregar la imagen al carrito
            infoCartProduct.appendChild(tituloProductoCarrito);
            infoCartProduct.appendChild(descriptionProductoCarrito);
            infoCartProduct.appendChild(precioProductoCarrito);
            cartProduct.appendChild(infoCartProduct);
            containerCartProducts.appendChild(cartProduct);
        });

        valorTotal.textContent = `$${total.toFixed(2)}`;
        countProducts.textContent = totalProducts;

        // Oculta el mensaje de carrito vacío si hay productos en el carrito
        if (totalProducts > 0) {
            cartEmpty.style.display = 'none';
        } else {
            cartEmpty.style.display = 'block';
        }

        // ...
    }

    btnCart.addEventListener('click', () => {
        containerCartProducts.classList.toggle('hidden-cart');
    });

    productsList.addEventListener('click', e => {
        if (e.target.classList.contains('btn-add-cart')) {
            const productDetails = e.target.closest('.item-details');
            const productName = productDetails.getAttribute('data-product-name');
            const productDescription = productDetails.getAttribute('data-product-description');
            const productPrice = productDetails.getAttribute('data-product-price');
            const productImg = productDetails.getAttribute('data-product-img'); // Obtener la URL de la imagen

            const infoProduct = {
                quantity: 1,
                title: productName,
                description: productDescription,
                price: productPrice,
                img: productImg, // Agregar la URL de la imagen al objeto
            };

            const existingProduct = allProducts.find(product => product.title === infoProduct.title);

            if (existingProduct) {
                existingProduct.quantity++;
            } else {
                allProducts.push(infoProduct);
            }

            // Mostrar el carrito al agregar un producto
            containerCartProducts.classList.remove('hidden-cart');

            showHTML(); // Actualiza la interfaz del carrito al agregar productos
        }
    });

    // ...
});