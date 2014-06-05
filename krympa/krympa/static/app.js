$('#shortenForm').submit(function(e){
    postData = $(this).serializeArray();
    var formURL = $(this).attr('action');

    $.ajax({
        url: formURL,
        type: 'POST',
        data: postData,
        success: function(data, textStatus, jqXHR){
            if ( data.status === 'error' ){
                var errordiv = '<div class="errors"><h2 class="form-error-title">Oops. The following error(s) occurred.</h2><ul>';
                for (var key in data.response.errmsg){
                    errordiv += '<li class="form-error">' + key + ': ' + data.response.errmsg[key] + '</li>';
                }
                errordiv += '</ul></div>';
                $('#shortenForm').prepend(
                    errordiv
                    );
            } else if ( data.status === 'success' ){
                $('#urlInput').val( data.response.short )
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(textStatus)
        }
    });
    e.preventDefault();
});
