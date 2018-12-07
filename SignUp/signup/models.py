from django.db import models

# Create your models here.


class Participant(models.Model):
    STATUS = (
        (0, "Accepted"),
        (1, "Rejected"),
        (2, "No Response"),
        (3, "Waiting Judge"),
        (4, "Cancelled"),
        (5, "Deleted"),
    )
    name = models.CharField(max_length=10)
    school_id = models.BigIntegerField()
    qq_number = models.BigIntegerField()
    faculty = models.CharField(max_length=20)
    remark = models.IntegerField(choices=STATUS, default=3)

    def __str__(self):
        return self.name

