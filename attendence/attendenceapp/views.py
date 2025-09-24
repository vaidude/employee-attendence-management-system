import base64
from io import BytesIO
import cv2
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from .models import Employee, Attendance
from deepface import DeepFace

def home(request):
    return render(request, 'home.html')

def recognize(request):
    if request.method == 'POST':
        try:
            img_data = request.POST.get('image').split(',')[1]
            img_data = base64.b64decode(img_data)
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                return JsonResponse({'status': 'error', 'message': 'Invalid image'})
            # Save temp image
            temp_path = 'temp.jpg'
            cv2.imwrite(temp_path, img)
            # Compare with employees
            for emp in Employee.objects.all():
                try:
                    result = DeepFace.verify(temp_path, emp.face_image.path, model_name='VGG-Face')
                    if result['verified']:
                        Attendance.objects.create(employee=emp)
                        return JsonResponse({'status': 'success', 'name': emp.name, 'message': 'Attendance recorded, thank you'})
                except:
                    pass
            return JsonResponse({'status': 'failure', 'message': 'No match found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

from django.shortcuts import render
from .models import Attendance
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

from django.utils import timezone
from datetime import datetime
import pytz


def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-timestamp')
    # Convert timestamps to IST
    ist = pytz.timezone('Asia/Kolkata')
    for attendance in attendances:
        attendance.timestamp = attendance.timestamp.astimezone(ist)
    return render(request, 'attendance_list.html', {'attendances': attendances})

def download_attendance_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, "Attendance Records")
    p.drawString(100, 730, "Employee          Timestamp")
    p.drawString(100, 725, "-" * 50)
    y = 700
    ist = pytz.timezone('Asia/Kolkata')
    for attendance in Attendance.objects.all().order_by('-timestamp'):
        ist_timestamp = attendance.timestamp.astimezone(ist)
        p.drawString(100, y, f"{attendance.employee.name}            {ist_timestamp.strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance.pdf"'
    return response