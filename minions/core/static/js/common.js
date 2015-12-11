$(function() {
    $("#search-q").typeahead({
        minLength: 2,
        autoSelect: false,
        source: function(query, process) {
            $.get($("#search-q").data("endpoint"), {
                    "q": query
                })
                .success(function(data) {
                    process(data);
                })
        },
        matcher: function() {
            // Big guys are playing here
            return true;
        },
        afterSelect: function(item) {
            var form = $("#search-q").closest("form");
            form.find("input[name=is_exact]").val("on");

            form.submit();
        }
    });

    $(function () {
        $('.tooltip-anchor').tooltip();
    })
});