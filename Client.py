import threading
import datetime
import socket
import time
from dateutil import parser


def startSendingTime(slave_client):
    """Send local time to server periodically"""
    while True:
        try:
            slave_client.send(str(datetime.datetime.now()).encode())
            print("Recent time sent successfully\n")
        except Exception as e:
            print("Connection lost while sending:", e)
            break
        time.sleep(5)


def startReceivingTime(slave_client):
    """Receive synchronized time from server"""
    while True:
        try:
            data = slave_client.recv(1024).decode()
            if not data:
                break
            sync_time = parser.parse(data)
            print(f"Synchronized time at the client is: {sync_time}\n")
        except Exception as e:
            print("Connection lost while receiving:", e)
            break


def initiateSlaveClient(port=8080):
    slave_client = socket.socket()
    slave_client.connect(('127.0.0.1', port))

    print("Connected to clock server.\n")
    print("Starting to send and receive time...\n")

    threading.Thread(target=startSendingTime, args=(slave_client,), daemon=True).start()
    threading.Thread(target=startReceivingTime, args=(slave_client,), daemon=True).start()


if __name__ == '__main__':
    initiateSlaveClient(port=8080)
    while True:
        time.sleep(1)
