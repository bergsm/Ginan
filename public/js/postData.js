$('#submitButton').click(function () {
    //alert('clicked')
    $.ajax({
        url: "/test-page",
        type: "POST",
        dataType: 'json',
        data: JSON.stringify({
            starting_url: $('#inputURL').val(),
            crawl_limit: $('#crawlLimit').val(),
            search_type: $("input[name='data[searchType]']:checked").val(),
	    keywordInput: $('#keywordInput').val()
        }),
        contentType: "application/json;charset=UTF-8",
        cache: false,
        timeout: 5000,
        complete: function () {
            //called when complete
            console.log('process complete');
        },

        success: function (data) {
            console.log(data);
            console.log('process sucess');
        },

        error: function () {
            console.log('process error');
        },
    });
});
