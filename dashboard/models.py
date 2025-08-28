from django.db import models

class Room(models.Model):
    block = models.CharField(max_length=10)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.block} {self.number}"

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='students')
    cleaning_status = models.CharField(max_length=20, choices=[('done', '✔️ Completed'), ('pending', '❌ Not done')])
    last_activity = models.CharField(max_length=50)
    badge = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.full_name