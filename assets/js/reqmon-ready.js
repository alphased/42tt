$(function() {
    var reset = function(event) {
        var counter, rest;
        counter = $('#requests_form input#new');
        if (counter.val() !=0 ) {
            rest = document.title.match(/^(?:\(\d+\))(.*)$/);
            document.title = (rest != null) ? rest[1] : document.title;
            counter.val(0);
        }
    }

    var update = function() { 
        $.ajax({
            url: "/requests/updates",
            type: "GET",
            dataType: "json",
            data: { last : $('#requests_form input#last').val()},
            success: function(json) {
                var counter, rest
                $('#requests_form input#last').val(json.latest);
                if (json.requests.length != 0) {
                    counter = $('#requests_form input#new')
                    counter.val(function(index, value) {
                        return parseInt(value) + json.requests.length;
                    });
                    rest = document.title.match(/^(?:\(\d+\))(.*)$/);
                    document.title = ["(", counter.val(), ") ",
                                      (rest != null) ? rest[1] : document.title].join("");
                    
                    json.requests.forEach(function(element, index, array) {
                        var timestamp = new Date(element.timestamp);
                        var text = "<li><p><span>" + timestamp.toUTCString() + "</span> " +
                                          "<span>" + element.method + "</span> " +
                                          "<span>" + element.path + "</span></p></li>";
                        $("#requests > li:last-child").remove();
                        $("#requests").prepend(text);
                    });
                }
            },
            error: function(xhr, errmsg, err) {},
            complete: function(xhr, errmsg, err) {
                window.setTimeout(update, 200);
            }
        });
    }
    window.setTimeout(update, 200);

    $(document).on('click keydown touchstart', reset);
    $(window).on('focus', reset);
})