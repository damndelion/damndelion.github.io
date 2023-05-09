from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200, help_text="Project name")
    type = models.CharField(max_length=50, help_text="Project type")

class Task(models.Model):
    name = models.CharField(max_length=200, help_text="task name")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, help_text="Task status")