$(document).ready(function(){



  var table=$('#example23').DataTable( {

         // para realizar los picklist de los filtros al pie de la tabla
          initComplete: function () {
              this.api().columns().every( function () {
                  var column = this;
                  var select = $('<select><option value=""></option></select>')
                      .appendTo( $(column.footer()).empty() )
                      .on( 'change', function () {
                          var val = $.fn.dataTable.util.escapeRegex(
                              $(this).val()
                          );

                          column
                              .search( val ? '^'+val+'$' : '', true, false )
                              .draw();
                      } );

                  column.data().unique().sort().each( function ( d, j ) {
                      if(d.indexOf("method=")==-1 & d.indexOf("href=")==-1){
                          select.append( '<option value="'+d+'">'+d+'</option>' )
                      }
                  } );
              } );
              //Para agregar search al dar click en cualquier dato de la tabla.
              var api=this.api();

              api.$('td').click(function(){
                  //evitamos la línea que contiene acciones.
                  if(this.innerHTML.search("</i>")==-1){
                      //agregamos la línea a la búsqueda.
                      api.search(this.innerText.match(/[0-9]/)!==null? "\""+this.innerText+"\"":this.innerText).draw();
                  }

              });

          },




          //que no sea responsive
          responsive:false,

          dom: 'Bflript',
          processing:true,

          //botones para exportar información
          buttons: [
    {extend:'copy',exportOptions:{columns:':visible.print-col'}}, {extend:'csv',exportOptions:{columns:':visible.print-col'}}, {extend:'excel',exportOptions:{columns:':visible.print-col'}},{extend:'pdfHtml5',orientation:'landscape',pageSize:'LETTER',exportOptions:{columns:':visible.print-col'}}, {extend:'print',orientation:'landscape',pageSize:'LETTER',exportOptions:{columns:':visible.print-col'}},{extend:'colvis',columns:':gt(0)'}
    ],
    lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
    columDefs:[{
    targets:-1,
    visible:false
    }]
    ,
    //cambiar el texto de los mensajes mostrados en la tabla.
    language:{
        processing:     "Procesando...",
        lengthMenu:     "Mostrar _MENU_ registros",
        zeroRecords:    "No se encontraron resultados",
        emptyTable:     "Ningún dato disponible para esta consulta",
        info:           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        infoEmpty:      "Mostrando registros del 0 al 0 de un total de 0 registros",
        infoFiltered:   "(filtrado de un total de _MAX_ registros)",
        infoPostFix:    "",
        search:         "Buscar:",
        url:            "",
        infoThousands:  ",",
        loadingRecords: "Cargando...",
        paginate: {
            first:    "Primero",
            last:     "Último",
            next:     "Siguiente",
            previous: "Anterior"
        },
        aria: {
            sortAscending:  ": Activar para ordenar la columna de manera ascendente",
            sortDescending: ": Activar para ordenar la columna de manera descendente"
        }
    },
});

$('#container').css('display','block');
    table.columns.adjust().draw();


});

//reajustar la tabla de acuerdo a los filtros y columnas ocultas.
