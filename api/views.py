import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework import permissions
from base.models import Report
from .serializers import ReportSerializer, UserSerializer
from .decorators import jwt_auth_required
from base.models import User
import jwt
import api.utils as utils
from django.shortcuts import get_object_or_404
from base.models import Attachment
from django.http import FileResponse


@api_view(['GET', 'POST'])
@jwt_auth_required
def report_api_view(request):
    if request.method == 'GET':
        reports = Report.objects.filter(user = request.user).order_by('-date_reported')
        serializer = ReportSerializer(reports, many=True)
        
        # print(serializer.data)
        
        return Response({"reports":serializer.data},content_type='application/json; charset=utf-8')

@api_view(['GET'])
@jwt_auth_required
def report_detail_view(request,pk):
    if request.method == 'GET':
        report = Report.objects.filter(id=pk).first()
        serializer = ReportSerializer(report)
        print(serializer.data)
        
        return Response({"report":serializer.data},content_type='application/json; charset=utf-8')


@api_view(['POST'])
@jwt_auth_required
def report_add_view(request):
    try:
        data = request.data
        attachments = []

        # Create the report first
        report = Report(
            report_type=data.get('report_type', None),
            report_description=data.get('report_description', None),
            location_url=data.get('location_url', None),
            date_of_crime=data.get('date_of_crime', None),
            user=request.user
        )
        report.save()
        
        # Save attachments and associate them with the report
        if request.FILES.getlist('attachment'):
            for attachment_file in request.FILES.getlist('attachment'):
                attachment = Attachment(image=attachment_file, report=report)
                attachment.save()
                attachments.append(attachment)
        
        # Serialize and return the report
        serializer = ReportSerializer(report)
        return Response({"report": serializer.data}, status=201)  # Created
    except Exception as e:
        print(e)
        return Response({"detail": "Please fill the information correctly."}, status=400, content_type='application/json; charset=utf-8')

@api_view(['GET'])
@jwt_auth_required
def report_attachment_media(request,path):
    user = request.user
    doc = get_object_or_404(Attachment, image=path)
    print(doc.report)
    if  user == doc.report.user:
        response = FileResponse(doc.image)
        return response
    
    raise AuthenticationFailed('You are not owner to view this attachment!')




class UserRegisterApiView(APIView):
    
    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.filter(username=serializer.data["username"]).first()
            token = utils.generatetoken(user)
            serializer.data["token"] = token
            response = Response({"user":{
                
                "id": serializer.data["id"],
                "username": serializer.data["username"],
                "uid": serializer.data["uid"],
                "name": serializer.data["name"],
            'token': token,
            }
            }, status=201)
     
            return response
        errorFields = [field for field in serializer.errors.items()];
        usernameDuplication = User.objects.filter(username=serializer.data["username"]).first()
        if usernameDuplication:
            return Response({
                "detail":"The email address is already registered."
            },status=400)
        if len(errorFields) > 1:
            return Response({
                "detail":"Please provide valid information."
            },status=400)
        
        
        return Response(serializer.errors)

class UserLoginApiView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        token = utils.generatetoken(user)

        response = Response({"user":{
                "id": user.id,
                "username": user.username,
                "uid": user.uid,
                "name": user.name,
            'token': token,
        },

        },content_type='application/json; charset=utf-8')
        
        return response