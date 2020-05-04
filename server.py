import threading
import queue
import socket
import sys
import time 

# transfer, sender, receiver, dollar_amount
def receive():
    global replies
    global blockchain
    global balance
    global requests
    global clock
    global pid
    global lock
    global s

    while True:
        length = s.recv(2)
        length = int(length.decode())
        msg = s.recv(length)
        msg = msg.decode().split(', ')
        # request, clock, pid
        if msg[0] == 'request':
            with lock:
                requests.put((int(msg[1]),msg[2]))
                # reply, sender_pid, receiver_pid
                reply = 'reply, ' + pid + ', ' + msg[2]
                reply = str(len(reply)) + reply
                # send reply back to requesting process
                s.sendall(reply.encode())
        # reply, sender_pid, receiver_pid
        elif msg[0] == 'reply':
            # Add reply to the set of replies
            with lock:
                replies.add(msg[1])
        # transfer, sender_pid, receiver_pid, amount
        elif msg[0] == 'transfer':
            with lock:
                temp = requests.get()
                temp_list = []
                while temp[1] != msg[1]:
                    temp_list.append(temp)
                    temp = requests.get()
                if msg[2] == pid:
                    clock = max(clock, temp[0]) + 1
                    balance += int(msg[3])
                blockchain.append((msg[1], msg[2], msg[3]))
                for t in temp_list:
                    requests.put(t)





def process():
    global events
    global blockchain
    global requests
    global balance
    global clock
    global pid
    global replies
    global lock
    global s

    while True:
        while events.not_empty:
            # get top of queue
            e = events.get()
            event = e[0]
            # transfer
            if event == 'transfer':
                amount = e[1]
                receiver = e[2]
                with lock:
                    clock += 1
                    print('Clock: ' + str(clock))
                    # Check if transfer amount is valid
                    if balance < int(amount) or receiver == pid:
                        print('FAILURE')
                        continue
                    requests.put((clock, pid))
                    # Send requests to other processes
                    request = 'request, ' +  str(clock) + ', ' + pid
                    request = str(len(request)) + request
                    s.sendall(request.encode())
                # Wait until request is at the top of the queue
                # and replies have been received from the other processes
                while True:
                    if len(replies) == 2:
                        with lock:
                        # Check if request is at the top
                            top = requests.get() 
                            if top[1] == pid:
                                replies.clear()
                                break
                            requests.put(top)
                with lock:
                    # Change own balance
                    balance -= int(amount)
                    # Update own blockchain
                    blockchain.append((pid, receiver, amount))
                    # Transfer, release, and broadcast message combined together
                    release = 'transfer, ' + pid + ', ' + receiver + ', ' + amount
                    release = str(len(release)) + release
                    s.sendall(release.encode())
            # print blockchain
            elif event == 'blockchain':
                with lock:
                    print('blockchain: ' + str(blockchain))
            # print balance
            elif event == 'balance':
                with lock:
                    print('balance: ' + str(balance))

# python server.py pid
pid = sys.argv[1]

# Establish TCP connection with NW
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 3000))
s.sendall(pid.encode('utf-8'))

events = queue.Queue()
replies = set()
requests = queue.PriorityQueue()
blockchain = []
balance = 10
clock = 0


lock = threading.Lock()

threading.Thread(target = receive).start()
threading.Thread(target = process).start()

while(True):
    time.sleep(0.01)
    # Possible inputs
    # transfer, amount, receive_pid
    # balance
    # blockchain 
    e = input('Enter command: ')
    e = e.split(', ')
    if e[0] != 'transfer' and e[0] != 'balance' and e[0] != 'blockchain':
        print('Invalid commmand')
        continue
    events.put(e)

