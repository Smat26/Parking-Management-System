from camera import Stream
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import json
from django.core import serializers
from models import Roi, Camera


# Create your views here.

Streaming = True
@login_required
def panel(request):
    src = '\"http://' + str(request.META['HTTP_HOST']) + '/video/\"'
    Context = ({

        'src': src
    })

    return render(request, 'main.html', Context)


def gen(stream):
    """Video streaming generator function."""
    while True:
        frame = stream.get_frame()
        yield (b'--frame\r\n' +
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@login_required
def videofeed(request):
    url = 'rtsp://mm2.pcslab.com/mm/7m800.mp4'
    if request.method == 'POST':
        Streaming = False
        print('Streaming is :'+str(Streaming))
        myDict = dict(request.POST.iterlists())
        # print('Dict: '+ myDict['url'][0])
        url = myDict['url'][0]
    else:
        
        url = 'rtsp://media.smart-streaming.com/mytest/mp4:sample_phone_300k.mp4'
        
    # a = gen(Camera())
    # red = camera.get_frame()
    # output = StringIO.StringIO()
    # a.save(output, "JPEG")
    # contents = output.getvalue().encode("base64")
    # output.close()
    # return HttpResponse('<html><body><img src="data:image/JPEG;base64,' + contents + ' " width="720" height="480"/></body></html>')
    # return HttpResponse(gen(Camera()),
    #                 content_type='multipart/x-mixed-replace; boundary=frame')
    # print("URL = "+ url)

    response = StreamingHttpResponse(
        gen(Stream(url)), content_type="multipart/x-mixed-replace; boundary=frame")
    # a.save(response, "JPEG")
    Streaming = True
    print('Streaming is :' + str(Streaming))
    return response

    # response =  HttpResponse(content_type="image/jpeg")
    # Camera.get_frame().save(response, "jpeg")
    # return Camera().get_frame()


def generateJson():
    a = {'ix': 0, 'iy': 0, 'fx': 8, 'fy': 8, 'name': 'F1'}
    b = {'ix': 10, 'iy': 10, 'fx': 15, 'fy': 12, 'name': 'F2'}
    c = [a, b]
    return json.dumps(c)


@login_required
def getRoi(request):
    a = HttpResponse(serializers.serialize("json", Roi.objects.all()))
    return a


@login_required
def getCamera(request):
    b = HttpResponse(Camera.objects.all())
    a = HttpResponse(serializers.serialize("json", Camera.objects.all()))
    return a


@login_required
def AddRoi(request):
    if request.method == 'POST':
        ret = request.POST
        print ret
        myDict = dict(request.POST.iterlists())
        print(myDict['min_x'][0])
        a = Roi(
            name = myDict['name'][0],
            min_x= int(myDict['min_x'][0]),
            min_y= int(myDict['min_y'][0]),
            max_x= int(myDict['max_x'][0]),
            max_y= int(myDict['max_y'][0]),
            camera = Camera.objects.get(pk = myDict['camera'][0]),
            occupied = 0,
            )
        a.save()
        print('saved')
