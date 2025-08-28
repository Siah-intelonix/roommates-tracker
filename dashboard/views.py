from django.shortcuts import render, redirect
from datetime import date
from django.utils import timezone
from .models import Student, Feedback, Room  # ✅ Room added

def get_today_turn(roommates):
    total = roommates.count()
    start_date = date(2025, 8, 1)  # tarehe ya kuanza rotation
    days_passed = (date.today() - start_date).days
    turn_index = (days_passed % total) + 1
    return roommates.get(rotation_order=turn_index)

def dashboard_view(request):
    context = {}
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(student_id=student_id)
            room = student.room
            floor = room.floor
            block = floor.block
            roommates = room.students.all()
            today_turn = get_today_turn(roommates)

            context = {
                'student': student,
                'room': room,
                'floor': floor,
                'block': block,
                'roommates': roommates.exclude(student_id=student_id),
                'today_turn': today_turn,
                'is_my_turn': student == today_turn
            }
        except Student.DoesNotExist:
            context['error'] = "Student ID not found"
    return render(request, 'dashboard/dashboard.html', context)

def mark_cleaning_done(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        try:
            student = Student.objects.get(student_id=student_id)
            roommates = Student.objects.filter(room=student.room)
            today_turn = get_today_turn(roommates)

            if student == today_turn:
                student.cleaning_status = "done"
                student.last_activity = timezone.now().strftime("%Y-%m-%d %H:%M")
                student.save()
        except Student.DoesNotExist:
            pass
    return redirect("dashboard_view")

def submit_feedback(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        message = request.POST.get("message")
        try:
            student = Student.objects.get(student_id=student_id)
            if message:
                Feedback.objects.create(student=student, message=message)
        except Student.DoesNotExist:
            pass
    return redirect("dashboard_view")

# ✅ Step 9: Warden Dashboard View
def warden_dashboard(request):
    rooms = Room.objects.select_related('floor__block').prefetch_related('students')
    feedbacks = Feedback.objects.select_related('student__room__floor__block').order_by('-submitted_at')

    room_data = []
    for room in rooms:
        students = room.students.all()
        status = [s.cleaning_status for s in students]
        harmony_score = "High" if status.count("done") == len(students) else "Mixed"
        room_data.append({
            "block": room.floor.block.name,
            "floor": room.floor.number,
            "room": room.number,
            "students": students,
            "status": status,
            "harmony": harmony_score
        })

    context = {
        "room_data": room_data,
        "feedbacks": feedbacks
    }
    return render(request, "dashboard/warden_dashboard.html", context)