(function ($) {
  $(document).ready(function () {
    var ordenDeTrabajoField = $("#id_orden_de_trabajo");
    var clienteField = $("#id_cliente");

    ordenDeTrabajoField.change(function () {
      var ordenDeTrabajoId = $(this).val();
      if (ordenDeTrabajoId) {
        $.ajax({
          url: "/api/orden-de-trabajo/" + ordenDeTrabajoId + "/",
          success: function (data) {
            clienteField.val(data.cliente_nombre);
          },
          error: function () {
            console.log("Error al obtener los datos de la orden de trabajo.");
          },
        });
      } else {
        clienteField.val("");
      }
    });
  });
})(django.jQuery);
