from django.db import models

# 🔹 Block model: inawakilisha block ya hostel (A, B, C...)
class Block(models.Model):
    name = models.CharField(max_length=10)  # e.g. "A", "B", "C"

    def __str__(self):
        return f"Block {self.name}"

# 🔹 Floor model: kila block ina floor 1 na 2
class Floor(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    number = models.IntegerField()  # 1 or 2

    def __str__(self):
        return f"{self.block.name} Floor {self.number}"

# 🔹 Room model: kila floor ina vyumba viwili (mfano: 101, 102)
class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)  # e.g. "101", "102"

    def __str__(self):
        return f"{self.floor.block.name} {self.number}"

# 🔹 Student model: kila mwanafunzi ana room, status, na badge
class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=[("male", "Male"), ("female", "Female")])
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='students')
    cleaning_status = models.CharField(max_length=20, choices=[('done', '✔️ Completed'), ('pending', '❌ Not done')])
    last_activity = models.CharField(max_length=50)
    badge = models.CharField(max_length=50, blank=True)
    rotation_order = models.IntegerField()

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

# ✅ Feedback model: iko nje ya Student class
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"