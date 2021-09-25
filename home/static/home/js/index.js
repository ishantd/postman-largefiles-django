function start_file_processing(data = {}) {
    $.ajax({
        type: "PUT",
        url: "/upload/files/",
        data: JSON.stringify(data), // now data come in this function
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        dataType: "json",
        success: function(data, status, jqXHR) {

            alert("success"); // write success in " "
        },

        error: function(jqXHR, status) {
            // error handler
            console.log(jqXHR);
            alert('fail' + status.code);
        }
    });
}
$('#csvfile').fileupload().on('fileuploaddone', function(e, data) { console.log("STAT");
    start_file_processing(); });