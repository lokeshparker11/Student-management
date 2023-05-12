from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

@api_view(['GET'])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": 200, "message": "successfully added"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['POST'])
def add_student_mark(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    student.marks_percentage = request.data.get('marks_percentage', student.marks_percentage)
    student.save()

    return Response({"status": 200, "message": "successfully added"})

@api_view(['PUT'])
def update_student_mark(request):
    pk = request.query_params.get('id', None)
    if pk is not None:
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "message": "successfully updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_pass_percentage(request):
    students = Student.objects.all()
    total_students = students.count()
    pass_students = students.filter(marks_percentage__gte=50).count()
    fail_students = total_students - pass_students
    if total_students > 0:
        pass_percentage = (pass_students / total_students) * 100
    else:
        pass_percentage = 0
    return Response({'pass_percentage': pass_percentage})