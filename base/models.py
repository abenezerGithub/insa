import uuid
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone

class User(AbstractUser):
    uid = models.CharField(max_length=255,default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255,)
    password = models.CharField(max_length=255)

    REQUIRED_FIELDS = ["name","password"]
    # def __str__(self):
    #     return f'User(username={self.username},uid={self.uid})'
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,db_column="user")
    report_type = models.TextField()
    report_description = models.TextField()
    location_url = models.TextField(blank=True)
    date_of_crime = models.DateTimeField(default=None,null=True,blank=True)
    date_reported = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    
    # attachment = models.ManyToManyField('Attachment',related_name='reports',default=None)
    def __str__(self):
        return f"{self.report_type} reported by {self.user.username} on {self.date_reported}"
    
class Attachment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='attachments')

    image = models.ImageField(upload_to='attachments/')
    def __str__(self):
        return f"Attachment"


