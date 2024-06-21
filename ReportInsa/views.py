from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from base.models import Attachment
from django.http import FileResponse
import os

@login_required
def secure_media(request,path):
    doc = get_object_or_404(Attachment, image=path)
    response = FileResponse(doc.image)
    return response