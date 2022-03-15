from django.shortcuts import render
from django.views import View
from datetime import datetime
from ticketLog.models import Sections, Days, Ticket


# Create your views here.
class Home(View):
    def get(self, request):
        print(Days.choices)
        return render(request, "home.html", {"days": Days.choices, "sections": Sections.choices})

    def post(self, request):
        print(Days.choices)
        # extract form data from POST
        # convert datetime-local string to a Python datetime
        d = datetime.strptime(request.POST['dateTime'], '%Y-%m-%dT%H:%M')  # replace the first argument
        # instantiate and save a Ticket
        dayWeek = d.strftime("%A")
        a = Ticket(datetime=d, section=request.POST['section'], dayOfWeek=dayWeek)
        a.save()
        # to get day of the week, use strftime("%A")
        # like
        # a = datetime.now()
        # print(a.strftime("%A"))
        # also you can use the class Days like a dictionary
        # print(Days["Monday"]) #prints "M", just like print(Days.Monday)
        # render a response, identical to the page rendered by get
        return render(request, "home.html", {"days": Days.choices, "sections": Sections.choices})


class History(View):
    def get(self, request):
        return render(request, "history.html", {"days": Days.choices, "sections": Sections.choices})

    def post(self, request):
        # extract day and section from POST
        day = request.POST['dateTime']
        section = request.POST['sections']
        dayWeek = day.strftime("%A")
        # query (filter) for tickets
        T = Ticket.objects.filter(dayOfWeek=dayWeek, section=section).values()
        # render a response (with a table of matching tickets)
        return render(request, "history.html", {"days": Days.choices, "sections": Sections.choices, "ticket": T})
