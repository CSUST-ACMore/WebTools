from django.db import models

# Create your models here.


class Contest(models.Model):
    TYPE = (
        (0, "个人赛"),
        (1, "组队赛"),
    )
    name = models.CharField(max_length=30, verbose_name=u'比赛名称')
    contest_time = models.DateTimeField(verbose_name=u'比赛时间')
    contest_location = models.CharField(max_length=30, verbose_name=u'比赛地点')
    start_time = models.DateTimeField(verbose_name=u'报名开始时间')
    end_time = models.DateTimeField(verbose_name=u'报名结束时间')
    introduction = models.TextField(verbose_name=u'比赛介绍')
    rules = models.TextField(verbose_name=u'比赛规则')
    reward = models.TextField(verbose_name=u'比赛奖励')
    problem_num = models.IntegerField(default=13, verbose_name=u'题目数量')
    gold_num = models.IntegerField(default=8, verbose_name=u'金奖数量')
    silver_num = models.IntegerField(default=16, verbose_name=u'银奖数量')
    bronze_num = models.IntegerField(default=24, verbose_name=u'铜奖数量')
    type = models.IntegerField(choices=TYPE, default=0, verbose_name=u'比赛类型')

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
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name=u'所属比赛')
    name = models.CharField(max_length=30, verbose_name=u'队伍名称')

    @property
    def remark(self):
        par_list = Participant.objects.filter(team=self)
        mk = -1
        for par in par_list:
            if par.remark == 3:
                mk = 3
            elif par.remark != 0 and par.remark != 4 and par.remark > mk:
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
        pass
        # Participant.objects.filter(team=self).update(remark=mk)

    def get_remark_display(self):
        return self.STATUS[self.remark][1]

    def participant(self):
        par_list = list(Participant.objects.filter(team=self))
        tmp = []
        for s in par_list:
            st = s.name
            if s.remark != 0 and s.remark != 3 and s.remark != 4:
                st = st + '(' + s.get_remark_display() + ')'
            tmp.append(st)
        while tmp.__len__() < 3:
            tmp.append('')
        return tmp

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
    name = models.CharField(max_length=10, verbose_name=u'姓名')
    school_id = models.BigIntegerField(verbose_name=u'学号')
    qq_number = models.BigIntegerField(verbose_name=u'QQ号')
    faculty = models.CharField(max_length=20, verbose_name=u'学院')
    team = models.ForeignKey(Team,  on_delete=models.CASCADE, verbose_name=u'所属队伍')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name=u'所属比赛')
    remark = models.IntegerField(choices=STATUS, default=3, verbose_name=u'审核状态')

    def __str__(self):
        return self.name

