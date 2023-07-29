function table_function() {
    $(document).ready(function() {

        var table = $('#example').DataTable({

            lengthChange: false,

            buttons: [{ extend: 'copy', className: 'btn btn-primary' },
                { extend: 'excel', className: 'btn btn-primary' },
                { extend: 'pdf', className: 'btn btn-primary' },
                { extend: 'colvis', className: 'btn btn-primary' }
            ],
            'order': [
                [0, 'desc']
            ],


        });

    });

};

table_function();