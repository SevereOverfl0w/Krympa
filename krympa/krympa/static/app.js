$('#shortenForm').submit(function(e){
    postData = $(this).serializeArray();
    var formURL = $(this).attr('action');

    $.ajax({
        url: formURL,
        type: 'POST',
        data: postData,
        success: function(data, textStatus, jqXHR){
            if ( data.status === 'error' ){
                console.log(data.response.errmsg);
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
