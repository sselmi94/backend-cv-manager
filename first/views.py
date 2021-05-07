from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import MyFileSerializer
from .models import Terme
from django.forms.models import model_to_dict
from .utilities import CvManagerUtilties
import os



class Simple(APIView):
    parser_classes = (MultiPartParser, )
    UPLOAD_FOLDER = "./upload"
    fileName = "/sselmi_eng_resume.pdf"
    objCvManagerUtilities = CvManagerUtilties()
    def get(self, request):
        #queryset = Terme.objects.all()
        #dictionaries = [ obj.as_dict() for obj in queryset]
        target = self.UPLOAD_FOLDER + self.fileName
        dictionaries = self.objCvManagerUtilities.parseCV(target)
        return JsonResponse({"data":dictionaries})

    def post(self, request, *args, **kwargs):
        file_serializer = MyFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            self.fileName = file_serializer.data["resume"]
            targetPath = self.UPLOAD_FOLDER + self.fileName
            destination = open( targetPath, 'wb+')
            for chunk in request.FILES["resume"].chunks():
               destination.write(chunk)
            destination.close() 
            os.remove(self.fileName.replace("/",""))
            data = self.objCvManagerUtilities.parseCV(targetPath)
            return JsonResponse({"extracted":data})
        else:
            return Response(file_serializer.errors)
        
  

