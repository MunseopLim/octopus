from django.shortcuts import render
from resources.models import Resources
from datetime import datetime


def index(request):
    print("[runner.views.index] begin: " + str(datetime.now()))
    print("[runner.views.index] session: " + request.session._session_key)
    resource_list = Resources.objects.filter(disabled=False)
    print("[runner.views.index] end: " + str(datetime.now()))
    return render(request, "pages/runner_index.html", {"resources": resource_list})
