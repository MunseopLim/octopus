from django.shortcuts import render
from resources.models import Resources
from datetime import datetime

# Create your views here.
def index(request):
    print("[runner.tester.index] begin: " + str(datetime.now()))
    print("[runner.tester.index] session: " + request.session._session_key)
    resource_list = Resources.objects.filter(disabled=False)
    print("[runner.tester.index] end: " + str(datetime.now()))
    return render(request, "pages/tester_index.html", {"resources":resource_list})
