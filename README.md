# Advanced-Keylogger
Building an advanced keylogger using Python. The script will log key strokes as well as other system-wide information.


## Pre-requisites
*I recommend using a spare Gmail account for testing the script.*
* Since Google no longer supports the use of third-party apps or devices, the *'less secure app access'* setting is not available anymore.
* You need to generate an *'App Password'* for logging into your account and send email using Python 

*refer:* https://support.google.com/mail/answer/185833?hl=en
 
 
 
## Code Walk-through
1) Every key-strokes log file is inserted with *user & system information* at the beginning using *os*, *socket*, *platform* modules.
2) ***on_press()*** is a callback to call when a button is pressed. It appends the key to the logged data.
3) ***on_release()*** is a callback to call when a button is released. I have used *'ESC'* to terminate the script.
4) ***send_email()*** is used to send email using [SMTP Protocol](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) over [Gmail SMTP server](https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python) (port no. 587)
5) ***random_file_path()*** will help generate the files at random locations. I have used *'Downloads, Documents, Music*.
6) I am using *random* to generate random file names with numbers ranging 1000000000 to 9999999999.
7) ***clipboard()*** will fetch data from clipboard using [win32clipboard](http://timgolden.me.uk/pywin32-docs/win32clipboard.html) module.
8) ***screenshot()*** captures a screenshot of the screen at the time of sending the log. Module used - [ImageGrab](https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html)
9) ***log_file()*** will create a .txt file consisting of the key-strokes.
10) After every specified time interval, ***send_logs()*** will generate the log files and send them via email using the defined functions. Further, it will permanently delete those files from the system.



## Built With

* **Python 3.10.5** - [https://www.python.org/](https://www.python.org/)



#### Disclaimer

> This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for
> illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no
> liability and are not responsible for any misuse or damage caused by this tool and software in general.
