document.addEventListener('DOMContentLoaded', function () {
    const btnCart = document.querySelector('.container-cart-icon');
    const containerCartProducts = document.querySelector('.container-cart-products');
    const productsList = document.querySelector('.container-items');
    const allProducts = [];

    const valorTotal = document.querySelector('.total-pagar');
    const cartEmpty = document.querySelector('.cart-empty');

    // Función para mostrar los productos en el carrito
    function showHTML() {
        // Actualiza la interfaz del carrito con los productos
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

            const btnQuitar = document.createElement('button');
            btnQuitar.classList.add('btn-quitar');
            btnQuitar.innerHTML = '<i class="fas fa-times"></i>';

            // Evento de clic para el botón "Quitar"
            btnQuitar.addEventListener('click', function () {
                if (product.quantity > 1) {
                    // Disminuir la cantidad del producto en el carrito
                    product.quantity--;
                } else {
                    // Eliminar el producto del carrito si la cantidad es 1
                    const index = allProducts.indexOf(product);
                    if (index !== -1) {
                        allProducts.splice(index, 1);
                    }
                }

                // Actualizar la interfaz del carrito
                showHTML();
            });

            const imagenProductoCarrito = document.createElement('img');
            imagenProductoCarrito.src = product.img;

            const descriptionProductoCarrito = document.createElement('p');
            descriptionProductoCarrito.textContent = product.description;

            const familiaOlfativa = document.createElement('p');
            familiaOlfativa.textContent = `Familia Olfativa: ${product.familia_olfativa}`;

            const notasSalida = document.createElement('p');
            notasSalida.textContent = `Notas de Salida: ${product.notas_salida}`;

            const notasCorazon = document.createElement('p');
            notasCorazon.textContent = `Notas de Corazón: ${product.notas_corazon}`;

            const notasFondo = document.createElement('p');
            notasFondo.textContent = `Notas de Fondo: ${product.notas_fondo}`;

            // Agregar los elementos al contenedor del producto en el carrito
            infoCartProduct.appendChild(btnQuitar); // Agregar el botón "Quitar"
            infoCartProduct.appendChild(imagenProductoCarrito);
            infoCartProduct.appendChild(descriptionProductoCarrito);
            infoCartProduct.appendChild(familiaOlfativa);
            infoCartProduct.appendChild(notasSalida);
            infoCartProduct.appendChild(notasCorazon);
            infoCartProduct.appendChild(notasFondo);
            cartProduct.appendChild(infoCartProduct);
            containerCartProducts.appendChild(cartProduct);
        });

        // Añadir el botón "Vaciar Carrito" al contenedor del carrito solo si hay productos
        if (totalProducts > 0) {
            const btnVaciarCarrito = document.createElement('button');
            btnVaciarCarrito.id = 'btnVaciarCarrito';
            btnVaciarCarrito.classList.add('btncom');
            btnVaciarCarrito.textContent = 'Vaciar';

            // Evento de clic para el botón de vaciar carrito
            btnVaciarCarrito.addEventListener('click', function () {
                // Vaciar el array de productos
                allProducts.length = 0;

                // Actualizar la interfaz del carrito
                showHTML();

                // Cerrar el carrito después de vaciarlo
                containerCartProducts.classList.add('hidden-cart');
            });

            // Agregar el botón al contenedor del carrito
            containerCartProducts.appendChild(btnVaciarCarrito);
        }

        valorTotal.textContent = `$${total.toFixed(2)}`;

        // Oculta el mensaje de carrito vacío si hay productos en el carrito
        if (totalProducts > 0) {
            cartEmpty.style.display = 'none';
        } else {
            cartEmpty.style.display = 'block';
        }
    }

    btnCart.addEventListener('click', () => {
        containerCartProducts.classList.toggle('hidden-cart');
    });

    productsList.addEventListener('click', e => {
        if (e.target.classList.contains('btn-add-cart')) {
            const productDetails = e.target.closest('.item-details');
            const productDescription = productDetails.getAttribute('data-product-description');
            const productPrice = productDetails.getAttribute('data-product-price');
            const productImg = productDetails.getAttribute('data-product-img');
            const familiaOlfativa = productDetails.getAttribute('data-familia-olfativa');
            const notasSalida = productDetails.getAttribute('data-notas-salida');
            const notasCorazon = productDetails.getAttribute('data-notas-corazon');
            const notasFondo = productDetails.getAttribute('data-notas-fondo');

            const infoProduct = {
                quantity: 1,
                description: productDescription,
                price: productPrice,
                img: productImg,
                familia_olfativa: familiaOlfativa,
                notas_salida: notasSalida,
                notas_corazon: notasCorazon,
                notas_fondo: notasFondo,
            };

            const existingProduct = allProducts.find(product => product.description === infoProduct.description);

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
});