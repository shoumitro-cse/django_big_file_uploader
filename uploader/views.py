from django.shortcuts import render
from django.http import JsonResponse
import os
from .models import File

def index(request):
    if request.method == 'POST':  
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
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
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
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
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':file_object.existingPath})
                        else:
                            res = JsonResponse({'existingPath':file_object.existingPath})    
                        return res
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return res
    return render(request, 'upload.html')