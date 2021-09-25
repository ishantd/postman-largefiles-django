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
$('#csvfile').fileupload({
    progressall: function(e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .bar').css(
            'width',
            progress + '%'
        );
        $('#progress .bar').attr({
            "aria-valuenow": progress + '%',
        });
        $('#progress .bar').text(
            progress + '%'
        );
    }
}).on('fileuploaddone', function(e, data) {
    start_file_processing();
});