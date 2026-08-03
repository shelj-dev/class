from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    profile_pic = models.ImageField(upload_to="profile/", null=True, blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name.name