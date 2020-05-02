import threading
import queue
import socket
import sys
import time 

# transfer, sender, receiver, dollar_amount
def transferMoney():

def receive():
    global replies
    global blockchain
    global balance
    global requests
    global clock
    global s

    while True:
        msg = s.recv(1024)
        msg = msg.split(', ')
        # request, clock, pid
        if msg[0] == 'request':
            with lock:
                requests.put((msg[1],msg[2]))
                # reply, sender_pid, receiver_pid
                reply = 'reply, ' + pid + ', ' + msg[2]
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
                if msg[2] == pid
                    clock = max(clock, temp[0]) + 1
                    balance += int(msg[3])
                blockchain.append((msg[1], msg[2], msg[3]))





def process():
    global events
    global blockchain
    global balance
    global clock
    global pid
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
                    # Check if transfer amount is valid
                    if balance < int(amount):
                        print('FAILURE')
                        continue
                    requests.put((clock,pid))
                    # Send requests to other processes
                    request = 'request, ' +  str(clock) + ', ' + pid
                    s.sendall(request.encode())
                # Wait until request is at the top of the queue
                # and replies have been received from the other processes
                while True:
                    with lock:
                        # Check if request is at the top
                        top = requests.get()
                        if top[1] == pid and len(replies) == 2:
                            # Clear the replies received from other processes
                            replies.clear()
                            break
                        # Top request is from another process, place request back on the queue
                        requests.put(top)
                with lock:
                    # Change own balance
                    balance -= amount
                    # Update own blockchain
                    blockchain.append((pid, receiver, amount)
                    # Transfer, release, and broadcast message combined together
                    release = 'transfer, ' + pid + ', ' + receiver + ', ' + amount
                    s.sendall(release.encode())

            # print blockchain
            elif event == 'blockchain':
                with lock:
                    clock += 1
                    print('blockchain: ' + blockchain)
            # print balance
            elif event == 'balance'
                with lock:
                    clock += 1
                    print('balance: ' + str(balance))



# python server.py port pid
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
    e = input('Enter command:')
    e = e.split(', ')
    if e[0] != 'transfer' or e[0] != 'balance' or e[0] != 'blockchain':
        print('Invalid commmand')
        pass
    events.put(e)


        




# def comm():
#     global events
#     while True:
#         cmd, addr = s.recvfrom(1024)
#         cmd = cmd.decode('utf-8')
#         temp = "r" + cmd[1:]
#         events.put(temp)
        
# def process():
#     global events
#     global clocks
#     while True:
#         # while queue has elements
#         while events.not_empty:
#             # get top of queue
#             event = events.get()
#             temp = event.split(',')
#             if temp[0] == 'l':
#                 clocks.append((event, clocks[-1][1]+1))
#             elif temp[0] == 's':
#                 # Send to network process
#                 addr = ('127.1', 3000)
#                 # Update clock
#                 clocks.append((event, clocks[-1][1]+1))
#                 # Format event in the form s,[message],receiver pid, clock time, sender pid
#                 event = event + "," + str(clocks[-1][1]) + "," + pid
#                 s.sendto(event.encode('utf-8'), addr)
#             elif temp[0] == 'r':
#                 # Update lamport clock when receiving event
#                 clocks.append((temp[0] + "," + temp[1], max(clocks[-1][1], int(temp[-2])) + 1))
#             else:
#                 print(sys.argv[1] + " Print Clock:")
#                 for i in range(1,len(clocks)):
#                     temp_split = clocks[i][0].split(',')
#                     if temp_split[0] == 'l':
#                         print(temp_split[1] + ', ' + str(clocks[i][1]))
#                     elif temp_split[0] == 's':
#                         print("Send '" + temp_split[1] + "' to " + temp_split[2] + ", " + str(clocks[i][1]))
#                     else:
#                         print("Receive '" + temp_split[1] + "', " + str(clocks[i][1]))

# pid = sys.argv[1]
# port = int(sys.argv[2])
# # UDP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # Bind socket to address (default = '127.1, port')
# s.bind(('127.1', port))
# # Create queue for events
# events = queue.Queue()
# # List of clock events
# clocks = [('',0)]
# threading.Thread(target = process).start()
# threading.Thread(target = comm).start()
# while True:
#     time.sleep(0.01)
#     e = input("Enter message: ")
#     temp = e.split(',')
#     events.put(e)
    

# #l, wakeup
# #s, foo, 3
# #r, foo, 3, clock, pid