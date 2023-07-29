document.getElementById("deleteAlert").style.display = "none";

function AjaxDeletionFunction(id_camera) {
    $.ajax({
        type: "GET",
        url: "/delete_camera/" + id_camera,
        success: function(data) {
            // display a success message and refresh the page
            $('#example').DataTable().destroy();
            $('#bd').html(data);
            table_function();
        },
        error: function() {
            alert('Error deleting camera.');
        },
    });
    $('#exampleModal').modal('hide');

    //show the alert
    document.getElementById("deleteAlert").style.display = "block";
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 3000);
}