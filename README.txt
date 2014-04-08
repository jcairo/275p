Cmput 275 Final Project
Jonathan Cairo
Sean Schneideman

----

Program overview:
Please see program_diagram for a visual layout of the objects.
An application object manages all other objects. This includes the following
1. Several forms objects which make up the user interface.
2. A mail object which holds the message objects in the inbox.
3. An account object which has 2 sub objects 1 is an interactive
smtp/imap connection used for retrieving messages and sending. The
other is a THread object which contains the event listener on the server.
4. Lastly a queue object that allows the 2 threads to communicate with each other.

----

Use Instructions:
Open a terminal and cd into the directory.
type "python main.py" to run the program, please note this program uses python 2.

Navigate with the tab and arrow keys.
Login using any gmail account credentials. 
Then visit the inbox.
The inbox should display your 10 most recent emails.
Send yourself an email from your phone computer etc...., 
and you should get an instant push notification.

If emails are unread there text is bright white, otherwise grey.
Your new email should appear as bright white.
You can mark as read, and should see this reflected in your account and
in the application.
You can then delete the message.
Lastly try replying to the message, You should be taken to a compose form.
Ctrl + U lets you undo in compose form, and ctrl + y lets you redo.
However you cannot undo spell check changes.
WHen you are done typing your message hit spell check to check your spelling
Then hit send.
When you are done go to the main menu and quit.

----

Notes:
We did have a sporadic issue when trying to use the program on a linux machine,
sometimes we would get an error we could not figure out why. If there are any
issues please try us the client on os x if possible (although it should work fine
on linux)

The application can only be used on gmail accounts.

If you have any complaints about running the program please ensure
your terminal is at least 80 x 25 (standard size)

Added widgets to npyscreen folder: wgemailcomposewidget.py and 
wgspellchecker.py 

----

Libraries Used:
We used several open source libraries in this project
For all user GUI we use npyscreen
https://code.google.com/p/npyscreen/

For email server interaction we use an adapted version of gmaillib
https://github.com/thedjpetersen/gmaillib

Lastly for the Treaded object we use a Thread example from the following link
http://blog.timstoop.nl/2009/03/11/python-imap-idle-with-imaplib2/

For writing the edit_distance algorithm used Recurrence relation referenced
from https://www.stanford.edu/class/cs124/lec/med.pdf (Dan Jurafsky,
Stanford University)

british-english word list retrieved from UNIX usr/share/dict
