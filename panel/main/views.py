from camera import Camera
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
import json
from rects import Rect

# Create your views here.
@login_required
def panel(request):
    a = generateJson();
    print a;

    Context = ({})

    return render(request, 'main.html', Context)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'+
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def videofeed(request):
    # a = gen(Camera())

    # red = camera.get_frame()
    # output = StringIO.StringIO()
    # a.save(output, "JPEG")
    # contents = output.getvalue().encode("base64")
    # output.close()
    # return HttpResponse('<html><body><img src="data:image/JPEG;base64,' + contents + ' " width="720" height="480"/></body></html>')
    # return HttpResponse(gen(Camera()),
    #                 content_type='multipart/x-mixed-replace; boundary=frame')

    response = StreamingHttpResponse(gen(Camera()),content_type="multipart/x-mixed-replace; boundary=frame")
    # a.save(response, "JPEG")
    return response

    # response =  HttpResponse(content_type="image/jpeg")
    # Camera.get_frame().save(response, "jpeg")
    # return Camera().get_frame()

def generateJson():
    a = {'ix':0,'iy':0,'fx':8,'fy':8,'name':'F1'}
    b = {'ix':10,'iy':10,'fx':15,'fy':12,'name':'F2'}
    c = [a,b]
    return json.dumps(c)

