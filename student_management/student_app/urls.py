from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Home or Login page
    path('students/', views.student_list, name='student_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('get_subjects_by_course/<int:course_id>/', views.get_subjects_by_course, name='get_subjects_by_course'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    
     
    path('courses/', views.course_list, name='course_list'),
    path('add_course/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/edit/<str:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<str:subject_id>/', views.delete_subject, name='delete_subject'),

    path('attendance_form/', views.attendance_form, name='attendance_form'),
    path('get_students_by_subject/<int:subject_id>/', views.get_students_by_subject, name='get_students_by_subject'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('attendance-records/', views.attendance_records, name='attendance_records'),
    
]


