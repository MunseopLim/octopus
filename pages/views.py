from django.shortcuts import render
from resources.models import Resources
from tester.tester import tester
from datetime import datetime


def index(request):
    print("[pages.views.index] begin: " + str(datetime.now()))
    resource_list = Resources.objects.filter(disabled=False)
    test = tester(resource_list)
    result = test.run()
    print("[pages.views.index] end: " + str(datetime.now()))
    return render(
        request, "pages/index.html", {"resources": resource_list, "more_info": result}
    )
