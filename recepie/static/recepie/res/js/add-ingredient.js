(function ($) {
  'use strict';
  window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = $('.needs-validation') //document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    $('#id_post-content').attr('required');
    $('#id_post-image').removeAttr('required');
    var validation = Array.prototype.filter.call(forms, function (form) {
      form.addEventListener('submit', function (event) {
        $(':hidden').each(function() {
          $('#id_post-image').removeAttr('required');
        })
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})(jQuery);