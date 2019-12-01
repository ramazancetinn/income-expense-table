$(document).ready( function () {
    
    // Datepicker Settings
    /* rewrite the today button function to select today's date */
    $.datepicker._gotoToday = function (id) { $(id).datepicker('setDate', new Date()).datepicker('hide').blur(); };
    /* jQuery datepicker function used for selecting date */
    $("#fromdatepicker").datepicker({
        showAnim: "slideDown",
        showButtonPanel: true,
        showOptions: { direction: "up" },
        dateFormat: "yy-mm-dd",
        maxDate: 0
    });
    $("#todatepicker").datepicker({
        showAnim: "slideDown",
        showButtonPanel: true,
        showOptions: { direction: "up" },
        dateFormat: "yy-mm-dd",
        maxDate: 0
    });

    function singleSelect() {
    var checkBox = document.getElementById("customCheckDisabled");
    var toDiv = document.getElementById("toDataPickerDiv");
    if (checkBox.checked == true){
        toDiv.hidden = true
    } else {
        toDiv.hidden = false
    }
    }
    
    // Income-Expense Tables
    $('#incomeTable').DataTable({
        "language": {
            "search": "Arama:",
            "info": "_PAGE_. sayfa",
            "infoEmpty": "Gösterilecek veri yok.",
            "lengthMenu": "Toplam _MENU_ veri göster",
            "emptyTable": "Herhangi bir veri bulunmamaktadır!",
            "zeroRecords": "Böyle bir sonuç yok.",
            "paginate": {
                "previous": 'Önceki',
                "next":     'Sonraki',
            } 
          }
    });
    $('#expenseTable').DataTable({
        "language": {
            "search": "Arama:",
            "info": "_PAGE_. sayfa",
            "infoEmpty": "Gösterilecek veri yok.",
            "lengthMenu": "Toplam _MENU_ veri göster",
            "emptyTable": "Herhangi bir veri bulunmamaktadır!",
            "zeroRecords": "Böyle bir sonuç yok.",
            "paginate": {
                "previous": 'Önceki',
                "next":     'Sonraki',
            } 
          }
    });

} );


