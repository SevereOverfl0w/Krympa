$('#shortenForm').submit(function(e){
    e.preventDefault();
    var form = $(this);
    postData = form.serializeArray();
    var formURL = form.attr('action');
    $.ajax({
        url: formURL,
        type: 'POST',
        data: postData,
        success: function(data, textStatus, jqXHR){
            form.children('.errors').remove();
            if ( data.status === 'error' ){
                var word = Object.keys(data.response.errmsg).length == 1 ? 'error' : 'errors';
                var errordiv = '<div class="errors"><h2 class="form-error-title">Oops. The following ' + word + ' occurred.</h2><ul>';
                for (var key in data.response.errmsg){
                    errordiv += '<li class="form-error">' + key + ': ' + data.response.errmsg[key] + '</li>';
                }
                errordiv += '</ul></div>';
                $('#shortenForm').prepend(
                    errordiv
                    );
            } else if ( data.status === 'success' ){
                form.fadeOut(function(){
                    $('#urlInput').val( data.response.short );
                    form.fadeIn();
                });
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(textStatus)
        }
    });
});
