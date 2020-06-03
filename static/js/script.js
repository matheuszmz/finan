$(document).ready(function(){
    $('#id_valor').mask('#.##0,00', {reverse: true});

    $(document).on('click', '.confirm-delete', function () {
        $("#confirmDeleteModal").attr("caller-id", $(this).attr("id"));
    });

    $(document).on('click', '#confirmDeleteButtonModal', function () {
        var caller = $("#confirmDeleteButtonModal").closest(".modal").attr("caller-id");
        window.location = $("#".concat(caller)).attr("href");
    });

});

function MudarEstado(el) {
    var display = document.getElementById(el).style.display;
    if (display == "none")
        document.getElementById(el).style.display = 'block';
    else
        document.getElementById(el).style.display = 'none';
}
