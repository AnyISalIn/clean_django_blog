from django.shortcuts import render_to_response


def page404(request):
    response = render_to_response('error.html', {'status_code': 404, 'message': '你来到了没有知识的荒原 :('})
    response.status_code = 404
    return response
