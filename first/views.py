from rest_framework.views import APIView
# from django.http import Response,JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import MyFileSerializer

# Create your views here.


class Simple(APIView):
    parser_classes = (MultiPartParser, )
    UPLOAD_FOLDER = "./upload"
    fileName = ""
    def get(self, request):
        return Response({"content": "hi"})

    def post(self, request, *args, **kwargs):
        print(request.data)
        file_serializer = MyFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            self.fileName = file_serializer.data["resume"]
            destination = open( self.UPLOAD_FOLDER + self.fileName , 'wb+')
            for chunk in request.FILES["resume"].chunks():
               destination.write(chunk)
            destination.close() 
            return Response(file_serializer.data)
        else:
            return Response(file_serializer.errors)
	
# def sayHello(request):
 #   return JsonResponse({"content":"hi"})
