from django.shortcuts import render
from .models import Student

def dashboard_view(request):
    context = {}
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(student_id=student_id)
            roommates = student.room.students.exclude(student_id=student_id)
            context = {
                'student': student,
                'roommates': roommates,
                'room': student.room
            }
        except Student.DoesNotExist:
            context['error'] = "Student ID not found"
    return render(request, 'dashboard/dashboard.html', context)