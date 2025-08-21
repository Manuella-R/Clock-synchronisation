import threading
import datetime
import socket
import time
from dateutil import parser

client_data = {}
lock = threading.Lock()


def startReceivingClockTime(connector, address):
    """Thread function to receive clock time from a client"""
    try:
        while True:
            clock_time_string = connector.recv(1024).decode()
            if not clock_time_string:
                break  # client disconnected

            clock_time = parser.parse(clock_time_string)
            clock_time_diff = datetime.datetime.now() - clock_time

            with lock:
                client_data[address] = {
                    "clock_time": clock_time,
                    "time_difference": clock_time_diff,
                    "connector": connector
                }

            print(f"Client Data updated with: {address}\n")

    except Exception as e:
        print(f"Error with client {address}: {e}")
    finally:
        with lock:
            if address in client_data:
                del client_data[address]
        connector.close()


def startConnecting(master_server):
    """Accept incoming client connections"""
    while True:
        connector, addr = master_server.accept()
        slave_address = f"{addr[0]}:{addr[1]}"
        print(f"{slave_address} got connected successfully")

        current_thread = threading.Thread(
            target=startReceivingClockTime,
            args=(connector, slave_address),
            daemon=True
        )
        current_thread.start()


def getAverageClockDiff():
    """Compute the average clock difference"""
    with lock:
        if not client_data:
            return datetime.timedelta(0)
        time_diffs = [client['time_difference'] for client in client_data.values()]
    return sum(time_diffs, datetime.timedelta(0)) / len(time_diffs)


def synchronizeAllClocks():
    """Broadcast synchronized time to all clients"""
    while True:
        with lock:
            num_clients = len(client_data)

        print("\nNew synchronization cycle started.")
        print(f"Number of clients to be synchronized: {num_clients}")

        if num_clients > 0:
            avg_diff = getAverageClockDiff()
            sync_time = datetime.datetime.now() + avg_diff

            with lock:
                for addr, client in list(client_data.items()):
                    try:
                        client['connector'].send(str(sync_time).encode())
                    except:
                        print(f"Error sending to {addr}, removing client")
                        del client_data[addr]
        else:
            print("No client data. Synchronization not applicable.")

        time.sleep(5)


def initiateClockServer(port=8080):
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    master_server.bind(('', port))
    master_server.listen(10)

    print("Clock server started...\n")
    print("Waiting for client connections...\n")

    threading.Thread(target=startConnecting, args=(master_server,), daemon=True).start()
    threading.Thread(target=synchronizeAllClocks, daemon=True).start()


if __name__ == '__main__':
    initiateClockServer(port=8080)
    while True:
        time.sleep(1)
