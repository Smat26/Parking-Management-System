import sys, time, os, atexit
import socket
from thread import *
import signal

from daemon import Daemon
#import PythonSystem.services.restservices as RestService
#from PythonSystem.services.dbservices import DBServices
#from Main import Main


class MyDaemon(Daemon):
    def run(self):
        print "Server Started !!"
	self.StartDjango()
        #self.StartRestService()
        #self.children()
        #start_new_thread(self.socketThread, ())
        while 1:
            time.sleep(10)
        self.stop()

    def StartDjango(self):
	pid = os.fork()
        if pid == 0:  # Child
#      	    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panel.settings")
 #           from django.core.management import execute_from_command_line
#	    testargv=["manage.py","runserver"]
 #           execute_from_command_line(testargv)
	    os.system("python manage.py runserver 0.0.0.0:8000")
        else:
            self.dictionary["DJANGO"] = pid
            self.RegisterChild(pid)
            print 'forked for DJANGO Service with pid: ' + str(self.dictionary["DJANGO"])

    def StartRestService(self):
        pid = os.fork()
        if pid == 0:  # Child
            RestService.run(self.path + '/logs/')
        else:
            self.dictionary["REST"] = pid
            self.RegisterChild(pid)
            print 'forked for REST Service with pid: ' + str(self.dictionary["REST"])

    def children(self):
        db = DBServices(self.path + '/logs/')
        self.cameras = {}
        self.cameras = db.getCameraDict()
        for cam in self.cameras.keys():
            try:
                pid = os.fork()
                if pid == 0:
                    cam = self.cameras[cam]
                    print (cam.CameraName + ', ' + cam.URL + ', ' + str(cam.FPS) + ', ' + '\n')
                    print (cam.ROIs)
                    print '\n'
                    self.Main = Main(cam, self.path, self.cameras, self.debug)
                    exit()
                else:
                    self.dictionary[cam] = pid
                    self.RegisterChild(pid)
                    print 'forked for camera: ' + cam + ', pid: ' + str(self.dictionary[cam])

            except OSError, e:
                sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                sys.exit(1)

    def socketThread(self):

        HOST = ''
        PORT = 12345

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print 'Socket created'
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code: ' + str(msg[0]) + '. Message: ' + msg[1]
            sys.exit()

        print 'Socket bind complete'

        s.listen(10)
        print 'Socket now listening'
        pid = os.getpid()
        while 1:
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            data = conn.recv(1024)

            s.shutdown(socket.SHUT_RDWR)
            s.close()
            pid = self.refresh()

            #reply = '\'' + data + '\' command received. Server Restarting.'
            #conn.sendall(reply)
            break
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                exit(0)
            else:
                print str(err)
                sys.exit(1)


if __name__ == "__main__":
    # target = open("./LogFile.txt", 'w')
    # app = Flask(__name__)
    # db = DBOperations()
    # url = '/parksmart'

    path = os.getcwd()
    print (sys.path)
    daemon = MyDaemon(path, path + '/logs/daemon-example.pid', '/dev/null',
                      path + '/logs/log.txt',
                      path + '/logs/error_log.txt',
                      path + '/logs/childs.txt')

    if len(sys.argv) == 3:
        if 'start' == sys.argv[1]:
            if '--debug' == sys.argv[2]:
                daemon.SetDebug(True)
                daemon.start()
    elif len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            # daemon.KillAllChilds()
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
