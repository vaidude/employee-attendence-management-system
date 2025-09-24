from django.db import models
from deepface import DeepFace
from django.core.files.storage import default_storage
import cv2
import numpy as np

class Employee(models.Model):
    name = models.CharField(max_length=100)
    face_image = models.ImageField(upload_to='faces/')
    face_embedding = models.TextField(blank=True)  # Store embedding as JSON string
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.face_image:
            try:
                img_path = default_storage.path(self.face_image.name)
                embedding = DeepFace.represent(img_path, model_name='VGG-Face')[0]['embedding']
                self.face_embedding = str(embedding)  # Convert to string
                super().save(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}")
                pass

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.employee.name
    
    