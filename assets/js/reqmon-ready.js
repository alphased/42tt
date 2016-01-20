$(function() {
    xhrRequests = undefined;

    var abort = function() {
        if (typeof xhrRequests !== "undefined") {
            xhrRequests.abort();
        }
    }

    var reload = function() {
        $('form#requests_form').submit();
    }

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
        xhrRequests = $.ajax({
            url: "/requests/updates",
            type: "GET",
            dataType: "json",
            data: { last:     $('#requests_form input#last').val(),
                    priority: $('#requests_form select#priority').val() },
            success: function(json) {
                var counter, rest, reverse;

                $('#requests_form input#last').val(json.latest);
                if (json.requests.length != 0) {
                    counter = $('#requests_form input#new')
                    counter.val(function(index, value) {
                        return parseInt(value) + json.requests.length;
                    });
                    rest = document.title.match(/^(?:\(\d+\))(.*)$/);
                    document.title = ["(", counter.val(), ") ",
                                      (rest != null) ? rest[1] : document.title].join("");
                    reverse = parseInt($('#requests_form select[name=reverse]').val());

                    json.requests.forEach(function(element, index, array) {
                        var timestamp = new Date(element.timestamp);
                        var text = "<li><p><span>" + timestamp.toUTCString() + "</span> " +
                                          "<span>" + element.method + "</span> " +
                                          "<span>" + element.path + "</span></p></li>";
                        if (reverse == 0) {
                            if ($('#requests > li').length >= 10) {
                                $("#requests > li:first-child").remove();
                            }
                            $("#requests").append(text);
                        } else {
                            if ($('#requests > li').length >= 10) {
                                $("#requests > li:last-child").remove();
                            }
                            $("#requests").prepend(text);
                        }
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

    $('form#requests_form #reverse').on("change", reload);
    $('form#requests_form #priority').on("change", reload);
    $(window).on('beforeunload', abort);
    $(window).on('focus', reset);
    $(document).on('click keydown touchstart', reset);
})
