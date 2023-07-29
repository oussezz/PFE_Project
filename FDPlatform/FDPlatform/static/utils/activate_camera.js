function activate(d) {
    $.ajax({
        type: 'GET',
        url: '/activate_camera',
        data: { 'data': d },
        success: function(data) {
            // display a success message and refresh the page
            $('#example').DataTable().destroy();
            $('#bd').html(data);
            table_function();
        },
        // replace with the URL of your server-side script
        error: function() {
            alert('Error activating camera.');
        },
    });
};