from django.shortcuts import render
import os
from django.conf import settings
from .models import File
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UploaderSerializer


class FileUploaderAPIView(generics.CreateAPIView):
    serializer_class = UploaderSerializer

    @staticmethod
    def get_storage_location(filename):
        if not os.path.isdir(settings.MEDIA_ROOT):
            os.mkdir(settings.MEDIA_ROOT)
        return os.path.join(settings.MEDIA_ROOT, filename)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        storage_path = request.POST['storage_path']
        is_end = bool(int(request.POST['is_end']))
        if storage_path == 'null':
            storage_path = self.get_storage_location(request.POST['filename'])
            with open(storage_path, 'wb+') as destination:
                destination.write(request.FILES['file'].read())
        else:
            with open(storage_path, 'ab+') as destination:
                destination.write(request.FILES['file'].read())
        if is_end:
            return Response({'data': 'Uploaded Successfully'})
        return Response({'storage_path': storage_path})


def home(request):
    return render(request, 'upload.html')


"""
def index2(request):
    if request.method == 'POST':  
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = Response({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                path = 'media/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                file_obj = File()
                file_obj.existingPath = fileName
                file_obj.eof = end
                file_obj.name = fileName
                file_obj.save()
                if int(end):
                    file_obj.delete()
                    res = Response({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = Response({'existingPath': fileName})
                return res

            else:
                path = 'media/' + existingPath
                file_object = File.objects.get(existingPath=existingPath)
                if file_object.name == fileName:
                    if not file_object.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            file_object.eof = int(end)
                            file_object.save()
                            file_object.delete()
                            res = Response({'data':'Uploaded Successfully','existingPath':file_object.existingPath})
                        else:
                            res = Response({'existingPath':file_object.existingPath})    
                        return res
                    else:
                        res = Response({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = Response({'data':'No such file exists in the existingPath'})
                    return res
    return render(request, 'upload.html')
"""
