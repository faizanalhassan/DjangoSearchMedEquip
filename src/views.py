from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from .ResourceHandler import add_resource, users_resources, Thread
from .DriverHandler import LOGS
from . import settings
user_id = 0


class ResponseStrings:
    SUCCEED = "Succeed."
    FAILED = "Failed."


def verify_session_id(request):
    if "user_id" not in request.session or request.session["user_id"] not in users_resources:
        raise Http404


def main(request):
    global user_id
    request.session["user_id"] = user_id
    user_id += 1
    messages.success(request, add_resource(request.session["user_id"]))
    context = {
        "LOGS": LOGS,
        "ResponseStrings": ResponseStrings,
    }
    return render(request, "main.html", context)


def update_last_connected(request):
    verify_session_id(request)
    result = []
    for driver_handler in users_resources[request.session["user_id"]]:
        driver_handler.update_last_connected()
        result.append({
            "searching": str(driver_handler.run_search),
            "logs": driver_handler.logs
        })
    print(result)
    return JsonResponse(result, safe=False)


def search_query(request):
    verify_session_id(request)
    query = request.GET.get("query")
    if query is None or query == '':
        return HttpResponse("Failed")
    for driver_handler in users_resources[request.session["user_id"]]:
        if driver_handler.run_search:
            return HttpResponse(ResponseStrings.FAILED + " Already Searching.")
    for driver_handler in users_resources[request.session["user_id"]]:
        Thread(target=driver_handler.start_search, args=(query,)).start()
    return HttpResponse(ResponseStrings.SUCCEED)


def stop_search(request):
    verify_session_id(request)
    stopped = False
    for driver_handler in users_resources[request.session["user_id"]]:
        if driver_handler.run_search:
            driver_handler.run_search = False
            stopped = True
    if stopped:
        return HttpResponse(ResponseStrings.SUCCEED)
    else:
        return HttpResponse(ResponseStrings.FAILED + " Search is not running.")


def file_urls(request):
    verify_session_id(request)
    urls = []
    for driver_handler in users_resources[request.session["user_id"]]:
        filname = driver_handler.filename
        file_url = settings.MEDIA_URL + filname
        urls.append({
            "name": filname,
            "url": file_url
        })
    return JsonResponse(urls, safe=False)
