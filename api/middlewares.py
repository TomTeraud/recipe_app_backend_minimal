from django.urls import reverse



class ModifyQueryParamsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the Django admin interface
        if request.path.startswith(reverse('admin:index')):
            return self.get_response(request)

        # Modify query parameters for other requests
        default_lang = 'lv'
        lang = request.GET.get('lang')
        if lang:
            modified_lang = f'name_{lang}'
        else:
            modified_lang = f'name_{default_lang}'

        request.GET = request.GET.copy()
        request.GET['lang'] = lang
        request.GET['language'] = modified_lang

        response = self.get_response(request)
        return response
