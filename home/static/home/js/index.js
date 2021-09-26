var alertPlaceholder = document.getElementById('liveAlertPlaceholder')
var alertTrigger = document.getElementById('liveAlertBtn')

function bsalert(message, type) {
    var wrapper = document.createElement('div')
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'

    alertPlaceholder.append(wrapper)
}

if (alertTrigger) {
    alertTrigger.addEventListener('click', function() {
        bsalert('Nice, you triggered this alert message!', 'success')
    })
}

function start_file_processing(data = {}) {
    $.ajax({
        type: "PUT",
        url: "/upload/files/",
        data: JSON.stringify(data), // now data come in this function
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        dataType: "json",
        success: function(data, status, jqXHR) {
            alert("Upload Successful, you can browse anything you want while I process the file on a different Thread!!!"); // write success in " "
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

function clear_sku_form() {
    $("#sku-search").val("");
    $("#product_name").val("");
    $("#product_description").val("");
}

$("#sku-search-button").click(function() {
    var sku = $("#sku-search").val();
    if (!sku) {
        bsalert('SKU Field cannot be blank!', 'danger');
        clear_sku_form();
        return;
    }
    $.get(`data/products/?sku=${sku}`, function(data) {
        if (!data.product) {
            bsalert('No matching query!', 'info');
            clear_sku_form();
            return;
        }
        if (data.product.name && data.product.description) {
            $("#product_name").val(data.product.name);
            $("#product_description").val(data.product.description);
        }
    });
});


$("#reset").click(function() {
    $("#reset").html = 'Destroying...';
    $.get(`data/delete/`, function(data) {
        alert("You just deleted everything, refresh the page now :(")
    });
    $("#reset").html = 'Everything Destroyed!';
    location.reload();
});

$("#save-product").click(function() {
    var sku = $("#sku-search").val();
    if (!sku) {
        bsalert('SKU Field cannot be blank!', 'danger');
        clear_sku_form();
        return;
    }
    var product_name = $("#product_name").val();
    var product_description = $("#product_description").val();

    if (sku && product_description && product_name) {
        var data = { "product_sku": sku, "product_name": product_name, "product_description": product_description }
        $.ajax({
            type: 'POST',
            url: '/data/products/',
            data: JSON.stringify(data),
            success: function(data) { bsalert('Changes saved successfully!!', 'success'); },
            contentType: "application/json",
            dataType: 'json'
        });
    }
});

$(document).ready(function() {
    $('#example').DataTable();
});