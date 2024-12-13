from django import forms
from .models import Student, Course, Subject

class StudentForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])  # Updated choices
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False, label="Subject")


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_id', 'name', 'course']



