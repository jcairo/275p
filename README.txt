Cmput 275 Final Project
Jonathan Cairo
Sean Schneideman


Use Instructions:
Open a terminal and cd into the directory.
type "python main.py" to run the program, please note this program uses python 2.
Navigate with the tab and arrow keys.
Login using any gmail account credentials. Then visit the inbox.
The inbox should display your 10 most recent emails.
If the emails are unread there text is bright white, otherwise grey.
Send yourself an email from your phone computer etc...., 
and you should get an instant push notification that
you have new mail. This will show in the inbox.

You can also mark the email as read by hitting the mark as read button or
delete. All changes should be reflected in your gmail account. To reply
to an email simply hit reply and you will be taken to a compose form.
Here you can write your email and spell check its contents.

Once done hit the send button.

Frameworks:
We rely on a few frameworks:
npyscreen manages the terminal display
gmaillib manages messages and there states. It also manages
a seperate thread which holds a connection to gmail and creates events
when changes take place on the server passing events into a shared queue.
This allows for push style email notifications.


You can mark as read by placing your cursor over a message, hitting 
tab until you reach the mark as read button and then 
