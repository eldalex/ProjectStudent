import uuid
import pika
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *


# Create your views here.

@api_view(['GET', 'POST'])
def students_list(request):
    if request.method == 'GET':
        data = Student.objects.all()

        serializer = StudentSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        print('post')
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if 'file' in request.FILES:
                save_image_to_media(serializer, request)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def students_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if 'file' in request.FILES:
                save_image_to_media(serializer, request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def send_to_rabbit(data):
    file = data.FILES['file']
    file_name = bytes('separator' + str(uuid.uuid4()) + '.' + file.name[file.name.rfind(".") + 1:], 'utf-8')
    img = file.read() + file_name
    hostname = '192.168.56.101'
    port = 5672
    credentials = pika.PlainCredentials(username='admin', password='admin')
    parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue='to_resize')
    channel.basic_publish(exchange='',
                          routing_key='to_resize',
                          body=img)
    connection.close()
    return file_name.decode('utf-8')

def save_image_to_media(serializer, request):
    print('save_image_to_media')
    file_name = send_to_rabbit(request).split('separator')[1]
    file_path = 'media\\photo\\' + file_name
    serializer.validated_data['photo'] = file_path
    if serializer.is_valid():
        serializer.save()