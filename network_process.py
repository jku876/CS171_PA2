import socket
import time
import random


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 3000))
s.listen()
network = {}

while True:
        c, addr = s.accept()
        pid = c.recv(1024)
        pid = pid.decode('utf-8')
        network[pid] = con
        # print(connections)
        threading.Thread(target = thread, args=[con, connections]).start()



# proc = {
#     'p1': 3001,
#     'p2': 3002,
#     'p3': 3003
# }

# while True:
#     cmd, addr = s.recvfrom(1024)
#     cmd = cmd.decode('utf-8')
#     temp = cmd.split(',')
#     time.sleep(random.randint(1,6))
#     #s, name, receiver, clock, pid
#     s.sendto(cmd.encode('utf-8'), ('127.1', proc[temp[2]]))