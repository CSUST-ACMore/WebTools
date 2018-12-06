from django.db import models

# Create your models here.


class Participant(models.Model):
    name = models.CharField(max_length=10)
    school_id = models.BigIntegerField()
    qq_number = models.BigIntegerField()
    faculty = models.CharField(max_length=20)
    remark = models.CharField(max_length=10, default='等待审核')

    def __str__(self):
        return self.name

