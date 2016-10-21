from rest_framework import viewsets, response, status
from rest_framework.decorators import detail_route
from pyfirmata import Arduino
from .models import Activity
from .serializer import ActivitySerializer

PORT = '/dev/cu.usbmodem1421'

board = Arduino(PORT)

class ActivityViewset(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class DeviceViewset(viewsets.ViewSet):
    @detail_route()
    def interact(self, request, pk=None):
        pin = int(pk)
        if board.digital[pin].read() != 1:
            board.digital[pin].write(1)
            log = "User %s turns ON pin %s" % (request.user, pk)
        else:
            board.digital[pin].write(0)
            log = "User %s turns OFF pin %s" % (request.user, pk)
        activity = Activity.objects.create(log=log, user=request.user)
        serializer = ActivitySerializer(activity)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
