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

/* Paginator */
function getPageList(totalPages, page, maxLength){
    function range(start, end){
      return Array.from(Array(end - start + 1), (_, i) => i + start);
    }
  
    var sideWidth = maxLength < 9 ? 1 : 2;
    var leftWidth = (maxLength - sideWidth * 2 - 3) >> 1;
    var rightWidth = (maxLength - sideWidth * 2 - 3) >> 1;
  
    if(totalPages <= maxLength){
      return range(1, totalPages);
    }
  
    if(page <= maxLength - sideWidth - 1 - rightWidth){
      return range(1, maxLength - sideWidth - 1).concat(0, range(totalPages - sideWidth + 1, totalPages));
    }
  
    if(page >= totalPages - sideWidth - 1 - rightWidth){
      return range(1, sideWidth).concat(0, range(totalPages- sideWidth - 1 - rightWidth - leftWidth, totalPages));
    }
  
    return range(1, sideWidth).concat(0, range(page - leftWidth, page + rightWidth), 0, range(totalPages - sideWidth + 1, totalPages));
  }
  
  $(function(){
    var numberOfItems = $(".container-items .item").length;
    var limitPerPage = 12; //How many card items visible per a page
    var totalPages = Math.ceil(numberOfItems / limitPerPage);
    var paginatorSize = 15; //How many page elements visible in the paginator
    var currentPage;
  
    function showPage(whichPage){
      if(whichPage < 1 || whichPage > totalPages) return false;
  
      currentPage = whichPage;
  
      $(".container-items .item").hide().slice((currentPage - 1) * limitPerPage, currentPage * limitPerPage).show();
  
      $(".paginator li").slice(1, -1).remove();
  
      getPageList(totalPages, currentPage, paginatorSize).forEach(item => {
        $("<li>").addClass("page-item").addClass(item ? "current-page" : "dots")
        .toggleClass("active", item === currentPage).append($("<a>").addClass("page-link")
        .attr({href: "javascript:void(0)"}).text(item || "...")).insertBefore(".next-page");
      });
  
      $(".previous-page").toggleClass("disable", currentPage === 1);
      $(".next-page").toggleClass("disable", currentPage === totalPages);
      return true;
    }
  
    $(".paginator").append(
      $("<li>").addClass("page-item").addClass("previous-page").append($("<a>").addClass("page-link").attr({href: "javascript:void(0)"}).text("◄")),
      $("<li>").addClass("page-item").addClass("next-page").append($("<a>").addClass("page-link").attr({href: "javascript:void(0)"}).text("►"))
    );
  
    $(".container-items").show();
    showPage(1);
  
    $(document).on("click", ".paginator li.current-page:not(.active)", function(){
      return showPage(+$(this).text());
    });
  
    $(".next-page").on("click", function(){
      return showPage(currentPage + 1);
    });
  
    $(".previous-page").on("click", function(){
      return showPage(currentPage - 1);
    });
  });

  // Checkbox
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        
  checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
          if (this.checked) {
              checkboxes.forEach(otherCheckbox => {
                  if (otherCheckbox !== this) {
                      otherCheckbox.disabled = true;
                  }
              });
          } else {
              checkboxes.forEach(otherCheckbox => {
                  otherCheckbox.disabled = false;
              });
          }
      });
  });

/* Link index 
const images = document.querySelectorAll(".imgcar img");

images.forEach((image) => {
    image.addEventListener("click", () => {
        const link = image.getAttribute("data-link");
        if (link) {
            window.location.href = link;
        }
    });
});
*/
