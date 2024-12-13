from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course, Subject, Attendance
from .forms import StudentForm, CourseForm, SubjectForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login


##########################################
############### Login ####################
##########################################
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is valid, log them in and redirect to another page
            login(request, user)
            return redirect('student_list')  # Replace 'student_list' with your desired view name
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password')

    # Render the login page
    return render(request, 'home.html')

##########################################
############### Course ###################
##########################################
def course_list(request):
    courses = Course.objects.all()  # Fetch all courses
    return render(request, 'course.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to the course list page after saving
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)  # Fetch by course_id
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)  # Fetch by course_id
    course.delete()
    return redirect('course_list')


##########################################
############### Subject ##################
##########################################
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

# View to add a new subject
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')  # Redirect to the subject list page
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'form': form})

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)  # Use subject_id instead of pk
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')  # Redirect to the subject list after saving
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'edit_subject.html', {'form': form})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)  # Use subject_id instead of pk
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')  # Redirect back to subject list after deletion
    return render(request, 'delete_subject.html', {'subject': subject})


##########################################
############### Student ##################
##########################################
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            course = form.cleaned_data['course']
            subject = form.cleaned_data.get('subject')  # Handle None

            # Create and save the student instance
            student = Student(
                
                first_name=first_name,
                last_name=last_name,
                address=address,
                gender=gender,
                course=course,
                subject=subject
            )
            student.save()

            # Redirect to the student list page
            return redirect('student_list')
        else:
            print("Form errors:", form.errors)  # Debugging form errors
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})


def get_subjects_by_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        subjects = Subject.objects.filter(course=course)
        subject_list = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        return JsonResponse(subject_list, safe=False)
    except Course.DoesNotExist:
        return JsonResponse([], safe=False, status=404)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Update the student object manually
            student.first_name = form.cleaned_data['first_name']
            student.last_name = form.cleaned_data['last_name']
            student.address = form.cleaned_data['address']
            student.gender = form.cleaned_data['gender']
            student.course = form.cleaned_data['course']
            student.subject = form.cleaned_data.get('subject')  # Handle optional field
            student.save()
            return redirect('student_list') 
    else:
        # Pre-populate the form with student data
        form = StudentForm(initial={
            'first_name': student.first_name,
            'last_name': student.last_name,
            'address': student.address,
            'gender': student.gender,
            'course': student.course,
            'subject': student.subject,
        })
    return render(request, 'edit_student.html', {'form': form})
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')  


##########################################
############### Attendence ###############
##########################################
def attendance_form(request):
    subjects = Subject.objects.all()
    students = Student.objects.all()
    return render(request, 'attendance_form.html', {
        'subjects': subjects,
        'students': students,
    })

def get_students_by_subject(request, subject_id):
    # Filter students based on the subject
    students = Student.objects.filter(subject__id=subject_id).values(
        'id', 'first_name', 'last_name', 'course'
    )
    return JsonResponse(list(students), safe=False)

def submit_attendance(request):
    if request.method == 'POST':
        selected_subject_id = request.POST.get('selected_subject')
        subject = Subject.objects.get(id=selected_subject_id)

        for key, value in request.POST.items():
            if key.startswith('attendance_'):
                id_str = key.split('_')[1]
                try:
                    id = int(id_str)  # Convert to integer
                    student = Student.objects.get(id=id)
                    if value:  # Ensure there's a value for attendance
                        Attendance.objects.create(
                            student=student,
                            subject=subject,
                            status=value
                        )
                except (ValueError, Student.DoesNotExist):
                    # Handle invalid student ID or empty field gracefully
                    continue

        return redirect("attendance_form")
        
    
    return HttpResponse("Invalid request.")


def attendance_records(request):
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject', None)
    if selected_subject:
        records = Attendance.objects.filter(subject_id=selected_subject)
    else:
        records = Attendance.objects.all()  

    return render(request, 'attendance_records.html', {
        'subjects': subjects,
        'records': records,
    })
