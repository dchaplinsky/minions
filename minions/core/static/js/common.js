$(function() {
    $(".search-form-q").typeahead({
        minLength: 2,
        items: 100,
        autoSelect: false,
        source: function(query, process) {
            $.get($(".search-form-q").data("endpoint"), {
                    "q": query
                })
                .done(function(data) {
                    process(data);
                })
        },
        matcher: function() {
            return true;
        },
        sorter: function(items) {
            return items
        },
        highlighter: function(instance) {
            return instance;
        },
        updater: function(instance) {
            return $(instance).data("sugg_text")
        },
        afterSelect: function(item) {
            var form = $(".search-form-q").closest("form");
            form.submit();
        }
    });
});
