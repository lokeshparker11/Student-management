from django.urls import path
from student_api.views import StudentList, StudentCreate, StudentDetail, StudentAddMark, StudentResults

urlpatterns = [
    path('api/students/', StudentList.as_view())],
