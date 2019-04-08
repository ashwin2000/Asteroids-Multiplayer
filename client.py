from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sample_server as sample
import sys


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("") 
    client_socket.send(bytes(msg))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()



def select_room(room_details):
    global PORT
    PORT=int(room_details['port'])
    
def create_new_room():
    file1=open("rooms_available.txt",'r+')
    for i in rooms_list:
        port=i['port']
        name=i['name']
        num=i['num']
        file1.write(port+','+name+','+num+'\n')
    name1=raw_input("Enter Your Chatroom name")
    num=0
    port=int(port)
    port+=1
    file1.write(str(port)+','+name1+','+str(num))
    file1.close()
    im=sample.IM(port)
    exit(0)
    

PORT=2
rooms_list=list()
file = open("rooms_available.txt","r")
line=file.readline()
while(line):
    if(line.count(',')==2):
        port,name,num=line.split(',')
        ele={'port':port,'name':name,'num':num}
        rooms_list.append(ele)
    line=file.readline()
file.close()

rooms=tkinter.Tk()
rooms.title("Select Room")
for i in rooms_list:
    room=tkinter.Button(rooms,text=i['name'],command=select_room(i))
    room.pack()

create=tkinter.Button(rooms,text="Create New Room",command=create_new_room)
create.pack()
rooms.quit()
rooms.mainloop()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = ''
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()