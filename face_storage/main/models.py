from django.db import models

# Create your models here.
class StudentData(models.Model):
    student_number = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    image = models.FileField()

    def __str__(self):
        return self.name
