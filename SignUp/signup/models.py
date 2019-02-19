from django.db import models

# Create your models here.


class Contest(models.Model):
    TYPE = (
        (0, "个人赛"),
        (1, "组队赛"),
    )
    name = models.CharField(max_length=30)
    contest_time = models.DateTimeField()
    contest_location = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    introduction = models.TextField()
    rules = models.TextField()
    reward = models.TextField()
    type = models.IntegerField(choices=TYPE, default=0)

    def __str__(self):
        return self.name


class Team(models.Model):
    STATUS = (
        (0, "Accepted"),
        (1, "Rejected"),
        (2, "No Response"),
        (3, "Waiting Judge"),
        (4, "UnRating"),
        (5, "Skipped"),
        (6, "Cancelled"),
        (7, "Deleted"),
    )
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    @property
    def remark(self):
        par_list = Participant.objects.filter(team=self)
        mk = -1
        for par in par_list:
            if par.remark != 0 and par.remark != 4:
                mk = par.remark
            elif mk <= 0 and par.remark == 4:
                mk = 4
            elif mk == -1 and par.remark == 0:
                mk = 0
        if mk == -1:
            mk = 7
        return mk

    @remark.setter
    def remark(self, mk):
        Participant.objects.filter(team=self).update(remark=mk)

    def get_remark_display(self):
        return self.STATUS[self.remark][1]

    def participant(self):
        par_list = list(Participant.objects.filter(team=self).values_list('name', 'get_remark_display'))
        while par_list.__len__() < 3:
            par_list.append(('', ''))
        return par_list

    def __str__(self):
        return self.name


class Participant(models.Model):
    STATUS = (
        (0, "Accepted"),
        (1, "Rejected"),
        (2, "No Response"),
        (3, "Waiting Judge"),
        (4, "UnRating"),
        (5, "Skipped"),
        (6, "Cancelled"),
        (7, "Deleted"),
    )
    name = models.CharField(max_length=10)
    school_id = models.BigIntegerField()
    qq_number = models.BigIntegerField()
    faculty = models.CharField(max_length=20)
    team = models.ForeignKey(Team,  on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    remark = models.IntegerField(choices=STATUS, default=3)

    def __str__(self):
        return self.name

