import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader

from django.views.generic import View
from .models import Participant


def index(request):
    return render(request, 'signup/index.html')


def register(request):
    if request.method == "POST":
        participant = Participant()
        participant.name = request.POST.get('username', '')
        participant.school_id = request.POST.get('pass', '')
        participant.qq_number = request.POST.get('qq_number', '')
        participant.faculty = request.POST.get('xy', '')
        if participant.name != '' and participant.school_id != '' and participant.faculty != '' and participant.qq_number != '':
            participant.save()
        return HttpResponseRedirect("list.html")
    else:
        return render(request, 'signup/register.html')


def par_list(request):
    participant_list = Participant.objects.order_by('-id')
    context = {
        'participant_list': participant_list,
    }
    return render(request, 'signup/list.html', context)


def lottery(request):
    participant_count = Participant.objects.filter(remark='Accepted').count()
    return render(request, 'signup/lottery.html', {'totTeam': participant_count})

