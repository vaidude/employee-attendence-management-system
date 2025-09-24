Face Recognition Attendance System
Overview
A Django-based web application for tracking employee attendance using face recognition. Captures images via webcam, processes them for recognition, and logs attendance.
Features

Webcam Capture: Real-time video feed for capturing employee images.
Face Recognition: Submits captured images to a /recognize/ endpoint for processing.
Admin Interface: Manage employees and view attendance records.
Responsive UI: Built with Tailwind CSS, featuring a centered status pop-up and small navigation buttons.

Requirements

Python 3.x
Django
Pillow (for image handling)
A face recognition library (e.g., face_recognition)
Webcam access

Setup

Clone the Repository:
git clone <repository-url>
cd <repository-folder>


Install Dependencies:
pip install -r requirements.txt


Apply Migrations:
python manage.py makemigrations
python manage.py migrate


Run the Server:
python manage.py runserver


Access the app at http://localhost:8000.


Models

Employee:

name: CharField (max 100 characters)
face_image: ImageField (stored in faces/)
face_embedding: TextField (stores face encoding)
__str__: Returns employee's name


Attendance:

employee: ForeignKey to Employee
timestamp: DateTimeField (auto-set on creation)
__str__: Returns employee's name



Templates

index.html:
Displays webcam feed and captured image side-by-side.
Includes "Capture Image" and "Submit for Recognition" buttons.
Shows a centered status pop-up for feedback.
Navigation links to /admin/ and /attendance/ with small buttons.
Logo size: h-20.



Usage

Open the app and allow webcam access.
Click "Capture Image" to take a photo.
Click "Submit for Recognition" to process the image.
View attendance records at /attendance/.
Manage employees at /admin/.

Notes

Ensure the /recognize/ endpoint is implemented for face recognition.
The <span></span> between navigation buttons is unnecessary and can be removed.
Update the logo URL if needed, as the current one may expire.
