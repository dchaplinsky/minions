from django_jinja import library


@library.global_function
def updated_querystring(request, params):
    """Updates current querystring with a given dict of params, removing
    existing occurrences of such params. Returns a urlencoded querystring."""
    original_params = request.GET.copy()
    for key in params:
        if key in original_params:
            original_params.pop(key)
    original_params.update(params)
    return original_params.urlencode()


@library.filter
def ua_pluralize(value, bit1="", bit2="", bit3="", bit4=""):
    try:
        if value % 100 in (11, 12, 13, 14):
            return bit3
        if value % 10 == 1:
            return bit1
        if value % 10 in (2, 3, 4):
            return bit2
        else:
            return bit3
    except:
        raise TemplateSyntaxError
