import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader

from django.views.generic import View
from .models import Participant
import datetime


def index(request):
    return render(request, 'signup/index.html')


def register(request):
    if request.method == "POST":
        participant = Participant()
        participant.name = request.POST.get('username', '')
        participant.school_id = request.POST.get('pass', 0)
        participant.qq_number = request.POST.get('qq_number', 0)
        participant.faculty = request.POST.get('xy', '')
        try:
            if len(str(participant.name)) > 10:
                participant.name = participant.name[:10]
            if len(str(participant.school_id)) > 12:
                participant.school_id = participant.school_id[:12]
            if len(str(participant.qq_number)) > 15:
                participant.qq_number = participant.qq_number[:13]
            sid = str(participant.school_id)
            ne = str(participant.name)
            now = datetime.datetime.now()
            if len(sid) != 12 or int(sid[0:4]) not in range(now.year-4, now.year+1) or int(sid[8:10]) not in range(1, 21) or int(sid[10:12]) not in range(1, 61):
                participant.remark = 1
            elif not all('\u4e00' <= char <= '\u9fff' for char in ne):
                participant.remark = 1
            elif len(str(participant.qq_number)) not in range(5, 14):
                participant.remark = 1
            else:
                participant_list = Participant.objects.filter(remark=0)
                for pat in participant_list:
                    print("id: " + str(pat.id))
                    print("sid: " + str(pat.school_id) + "*")
                    print("sid: " + str(participant.school_id) + "*")
                    if str(pat.school_id) == str(participant.school_id):
                        print("Skip")
                        participant.remark = 5
                        break
        except Exception:
            participant.remark = 7
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
    participant_count = Participant.objects.filter(remark=0).count()
    return render(request, 'signup/lottery.html', {'totTeam': participant_count})

