from django.db import models

class Course(models.Model):
    course_id = models.IntegerField(unique=True)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name
    
class Subject(models.Model):
    subject_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    id = models.IntegerField(primary_key= True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(default="")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="No Course Assigned")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.status}"
    


