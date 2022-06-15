 $(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-product").modal("show");
      },
      success: function (data) {
        $("#modal-product .modal-content").html(data.html_form);
        
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    var formData = new FormData(this)
    $.ajax({
      url: form.attr("action"),
      data: formData,
      type: form.attr("method"),
      dataType: 'json',
      cache: false,
      processData: false,
      contentType: false,
      success: function (data) {
        if (data.form_is_valid) {
          $("#product-table tbody").html(data.html_product_list);
          $("#modal-product").modal("hide");
        }
        else {
          $("#modal-product .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* load formset */

  var loadformset=function(){
    var newElement = $('div.form-container:last').clone(true);
    var total = $('#id_' + 'form' + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    
    total++;
    $('#id_' + 'form' + '-TOTAL_FORMS').val(total);
    $('div.form-container:last').after(newElement);
  }

  var removeformset=function(){
     var total = $('#id_' + 'form' + '-TOTAL_FORMS').val();
     if (total>1){
     total=total-1;
     $('div.form-container:last').remove();
     $('#id_' + 'form' + '-TOTAL_FORMS').val(total);
   }
   else{
    alert('you need at least one document as proof of ownership')
   }
  }

  /* Binding */

  // Create Product
  $(".js-add-product").click(loadForm);
  $("#modal-product").on("submit", ".js-product-create-form", saveForm);

  // Update Product
  $("#product-table").on("click", ".js-update-product", loadForm);
  $("#modal-product").on("submit", ".js-product-update-form", saveForm);

  //Delete Product
  $("#product-table").on("click", ".js-delete-product", loadForm);
  $("#modal-product").on("submit", ".js-product-delete-form", saveForm);

  //load formset
  $("#modal-product").on("click", ".js-add-formset", loadformset);
  //remove one formset
  $("#modal-product").on('click', ".js-remove-formset", removeformset)

});