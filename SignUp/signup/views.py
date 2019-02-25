import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.template import loader

from django.views.generic import View
from .models import Participant, Contest, Team
from datetime import datetime, timedelta

from .fetch_data import fetch_data


def index(request):
    contest = Contest.objects.order_by('-start_time')[0]
    now = datetime.now().timestamp()
    context = {
        'contest': contest,
        'now': now,
    }
    return render(request, 'signup/index.html', context)


def register(request):
    contest = Contest.objects.order_by('-start_time')[0]
    if datetime.now().timestamp() > contest.end_time.timestamp() or datetime.now().timestamp() < contest.start_time.timestamp():
        return HttpResponseRedirect("list.html")
    context = {
        'contest': contest
    }
    team = Team()
    if request.method == "POST":
        if contest.type == 0:
            participant = Participant()
            participant.name = request.POST.get('username', '').replace(' ', '')
            participant.school_id = request.POST.get('pass', '').lstrip('-')
            participant.qq_number = request.POST.get('qq_number', '').lstrip('-')
            participant.faculty = request.POST.get('xy', '')
            participant.contest = contest

            team.name = participant.name
            team.contest = contest

            participant = check_participant(participant)
            team.save()
            participant.team = team
            participant.save()
        else:
            team.name = request.POST.get('teamname', '').strip(' ').lstrip('*')
            if team.name == '' or team.name.__len__() > 30:
                team.name = team.name[:30]
                team.remark = 1
            team.contest = contest

            participant1 = Participant()
            participant1.name = request.POST.get('username1', '').replace(' ', '')
            participant1.school_id = request.POST.get('pass1', '').lstrip('-')
            participant1.qq_number = request.POST.get('qq_number1', '').lstrip('-')
            participant1.faculty = request.POST.get('xy1', '')
            participant1.contest = contest
            participant1 = check_participant(participant1)

            participant2 = Participant()
            participant2.name = request.POST.get('username2', '').replace(' ', '')
            participant2.school_id = request.POST.get('pass2', '').lstrip('-')
            participant2.qq_number = request.POST.get('qq_number2', '').lstrip('-')
            participant2.faculty = request.POST.get('xy2', '')
            participant2.contest = contest
            if participant2.name != '' and participant2.school_id != '' and participant2.qq_number != '':
                participant2 = check_participant(participant2)

            participant3 = Participant()
            participant3.name = request.POST.get('username3', '').replace(' ', '')
            participant3.school_id = request.POST.get('pass3', '').lstrip('-')
            participant3.qq_number = request.POST.get('qq_number3', '').lstrip('-')
            participant3.faculty = request.POST.get('xy3', '')
            participant3.contest = contest
            if participant3.name != '' and participant3.school_id != '' and participant3.qq_number != '':
                participant3 = check_participant(participant3)

            team.save()
            participant1.team = team
            participant1.save()
            if participant2.name != '' and participant2.school_id != '' and participant2.qq_number != '':
                participant2.team = team
                participant2.save()
            if participant3.name != '' and participant3.school_id != '' and participant3.qq_number != '':
                participant3.team = team
                participant3.save()

        return HttpResponseRedirect("list.html")
    else:
        return render(request, 'signup/register.html', context)


def par_list(request):
    contest = Contest.objects.order_by('-start_time')[0]
    if datetime.now().timestamp() < contest.start_time.timestamp():
        return HttpResponseRedirect("index.html")
    team_list = Team.objects.order_by('-id').filter(contest=contest)
    valid_team_list = [team for team in team_list if team.remark == 0 or team.remark == 4]
    valid_team_count = valid_team_list.__len__()
    participant_list = Participant.objects.order_by('-id').filter(contest=contest)
    valid_participant_list = participant_list.filter(Q(remark=0) | Q(remark=4))
    valid_participant_count = valid_participant_list.count()
    if datetime.now().timestamp() > contest.end_time.timestamp():
        participant_list = valid_participant_list
        team_list = valid_team_list
    context = {
        'contest': contest,
        'participant_list': participant_list,
        'team_list': team_list,
        'valid_participant_count': valid_participant_count,
        'valid_team_count': valid_team_count,
        'now': datetime.now().timestamp()
    }
    return render(request, 'signup/list.html', context)


def lottery(request):
    contest = Contest.objects.order_by('-start_time')[0]
    if contest.type == 0:
        participant_count = Participant.objects.filter(Q(contest=contest), Q(remark=0) | Q(remark=4)).count()
    else:
        participant_count = [t for t in Team.objects.filter(contest=contest) if t.remark == 0 or t.remark == 4].__len__()
    context = {
        'contest': contest,
        'totTeam': participant_count
    }
    return render(request, 'signup/lottery.html', context)


@login_required
def scrollboard(request):
    contest = Contest.objects.order_by('-start_time')[0]
    mp = fetch_data(contest.contest_id)
    start_time = mp['start_time']
    pro_num = mp['pro_num']
    frozen_time = start_time + timedelta(hours=4)
    context = {
        'contest': contest,
        'pro_num': pro_num,
        'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'frozen_time': frozen_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render(request, 'signup/scrollboard.html', context)


def login(request):
    return HttpResponseRedirect("/index.html")


def check_participant(participant):
    try:
        if len(str(participant.name)) > 10:
            participant.name = participant.name[:10]
        if len(str(participant.school_id)) > 12:
            participant.school_id = participant.school_id[:12]
        if len(str(participant.qq_number)) > 15:
            participant.qq_number = participant.qq_number[:13]
        sid = str(participant.school_id)
        ne = str(participant.name)
        now = datetime.now()
        if now.month < 8:
            now = now.replace(year=now.year-1)
        if len(str(participant.name)) > 5:
            participant.remark = 1
        elif len(sid) != 12 or int(sid[0:4]) not in range(now.year - 4, now.year + 1) \
                or int(sid[8:10]) not in range(1, 21) or int(sid[10:12]) not in range(1, 61):
            participant.remark = 1
        elif not all('\u4e00' <= char <= '\u9fff' for char in ne):
            participant.remark = 1
        elif len(str(participant.qq_number)) not in range(5, 14):
            participant.remark = 1
        else:
            contest = Contest.objects.order_by('-start_time')[0]
            participant_list = [par for par in Participant.objects.filter(Q(contest=contest), Q(remark=0) | Q(remark=4)) if par.team.remark == 0 or par.team.remark == 4]
            for pat in participant_list:
                if str(pat.school_id) == str(participant.school_id):
                    participant.remark = 5
                    break
            Participant.objects.filter(Q(contest=contest), Q(school_id=participant.school_id), Q(remark=3)).update(remark=6)
    except Exception:
        participant.remark = 7
    return participant
