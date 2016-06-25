#!/usr/bin/python

import sys, os, time, atexit
from signal import SIGTERM


class Daemon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self,path,pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null',childlist='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.ListOfChildsPath= childlist
        self.path=path
        self.dictionary={}
        self.debug=False
        # if os.path.exists(self.ListOfChildsPath):
        #     print "Childs Already Executing? Exitting Application"
        #

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        print 'Daemonizing !!'
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                #print 'Exitting First Parent'
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        #print 'Decoupling Child 1'
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def SetDebug(self,bool):
        self.debug=bool

    def stop(self):
        """
        Stop the daemon
        """
        self.KillAllChilds()
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)

        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def RegisterChild(self,pid):
        file(self.ListOfChildsPath, 'a+').write("%s\n" % pid)

    def KillAllChilds(self):
        if os.path.exists(self.ListOfChildsPath):
            childs = file(self.ListOfChildsPath,'r')
            #line = childs.readline()
            #print line
            for key in childs.xreadlines():
                print key
                os.kill(int(key), SIGTERM)
            os.remove(self.ListOfChildsPath)
        else:
            message = "Childs.txt file does not exist. Daemon not running?\n"
            sys.stderr.write(message)
            return

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def refresh(self):
        """
        Restart the daemon
        """
        self.KillAllChilds()
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

        self.start()
        return pid
        #os.kill(pid, SIGTERM)
        #exit(0)



    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
