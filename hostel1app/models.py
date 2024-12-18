# models.py
from django.db import models

class Complaint(models.Model):
    COMPLAINT_CHOICES = [
        ('Food', 'Food'),
        ('Infrastructure', 'Infrastructure'),
        ('Roommate', 'Roommate'),
    ]
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_CHOICES)
    complaint_description = models.TextField()
    facing_from_date = models.DateField()

    def __str__(self):
        return f"{self.complaint_type} Complaint - {self.id}"
    

class FeeReceipt(models.Model):
    full_name = models.CharField(max_length=255)
    utr_number = models.CharField(max_length=50)
    date = models.DateField()
    hostel_name = models.CharField(max_length=255)
    owner_signature = models.CharField(max_length=255, blank=True, null=True)  # For owner's signature
    
    def __str__(self):
        return f"Fee Receipt for {self.full_name} - {self.date}"    
