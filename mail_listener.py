# import imaplib2, time
from threading import *
import os

# adapted from
# http://blog.timstoop.nl/2009/03/11/python-imap-idle-with-imaplib2/
 
 # This is the threading object that does all the waiting on 
 # the event
 
# This is the threading object that does all the waiting on 
# the event
class Idler(object):
    """
    The idler object is passed an imap connection,
    and instance of the shared queue between the main program
    thread and itself, and a link to the instance of the parent
    class that created it.
    """
    def __init__(self, conn, queue, parent=None):
        # attach shared process queue
        self.queue = queue
        # create link to creating instance
        self.parent = parent
        # create an instance of the threading.Thread object
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
 
    def start(self):
        self.thread.start()
 
    def stop(self):
        # This is a neat trick to make thread end. Took me a 
        # while to figure that one out!
        self.event.set()
 
    def join(self):
        self.thread.join()
 
    def idle(self):
        # Starting an unending loop here
        while True:
            # This is part of the trick to make the loop stop 
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when a new 
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately, 
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is 
            # set by the callback, when the server 'answers' 
            # the idle call and the callback function gets 
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing 
            # anything if the stop() is called. Kinda neat 
            # solution.
            if self.needsync:
                self.event.clear()
                self.sync()
 
    # The method that gets called when a new email arrives. 
    # Replace it with something better.
    def sync(self):
        # place an element in the shared queue for the application to find.      
        self.queue.put("NewMail")
