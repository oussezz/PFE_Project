$(document).ready(function() {
    document.getElementById("addAlert").style.display = "none";


    $('#addCameraForm').submit(function(e) {
        e.preventDefault(); // prevent the form from submitting normally

        // send the form data via AJAX
        $.ajax({
            type: 'POST',
            url: '/add_camera', // replace with the URL of your server-side script
            data: $(this).serialize(),
            success: function(data) {
                // display a success message and refresh the page
                $('#cameraName').val(''); // clear the input field
                $('#cameraIP').val(''); // clear the input field
                $('#example').DataTable().destroy();
                $('#bd').html(data);
                table_function();
            },

            error: function() {
                alert('Error adding camera.');
            }
        });

        $('#addCameraModal').modal('hide'); // hide the modal
        //show the alert
        document.getElementById("addAlert").style.display = "block";
        setTimeout(function() {
            $('.alert').fadeOut('slow');
        }, 3000);
    });


});
$(document).ready(function() {
    document.getElementById("editAlert").style.display = "none";
    $('#editCameraForm').submit(function(e) {
        e.preventDefault(); // prevent the form from submitting normally

        // send the form data via AJAX
        $.ajax({
            type: 'POST',
            url: '/streaming_server_cameras', // replace with the URL of your server-side script
            data: $(this).serialize(),
            success: function(data) {
                // display a success message and refresh the page
                $('#example').DataTable().destroy();
                $('#bd').html(data);
                table_function();
            },

            error: function() {
                alert('Error editing camera.');
            }
        });

        $('#EditCameraModal').modal('hide'); // hide the modal
        //show the alert
        document.getElementById("editAlert").style.display = "block";
        setTimeout(function() {
            $('.alert').fadeOut('slow');
        }, 3000);
    });
});