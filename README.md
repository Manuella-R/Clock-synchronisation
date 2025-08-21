# 🕒 Clock Synchronization System (Python)

This project implements a Berkeley-style clock synchronization algorithm in Python.
Multiple clients send their local time to a server, which calculates the average difference and broadcasts synchronized time back to all clients.

It mimics distributed system time synchronization, often used in fault-tolerant systems.

## ⚙️ How It Works

### Server (server.py)

Accepts client connections.

Collects client clock values and computes the average difference.

Sends synchronized time back to each client every 5 seconds.

### Client (client.py)

Connects to the server.

Periodically sends its local time.

Receives the synchronized time from the server and prints it.

## ▶️ How to Run

Open 4 terminals (1 server + 3 clients).

Start the server:
```
python server.py
```

Start the clients:
```
python client.py
```

(Run in 3 separate terminals to simulate multiple clients.)

Output will show:
```
Server: connected clients + synchronization cycles.

Clients: synchronized timestamps received from the server.
```

## 🔧 Improvements Made

Compared to the original version, this implementation introduces several key improvements:

### 1. Thread Safety

Added a threading.Lock() to protect shared data (client_data).

Prevents race conditions when multiple client threads update their clock values simultaneously.

### 2. Graceful Client Disconnects

Server now removes clients that disconnect unexpectedly.

Prevents stale or broken connections from affecting synchronization.

### 3. Logging and Output Formatting

Improved output readability (e.g., showing client addresses like 127.0.0.1:53491).

Clear synchronization cycle logs for debugging and demonstration.

Can easily be extended with Python’s logging module for file-based logs.

### 4. Cleaner Multithreading

Both client and server use daemon threads → ensures background tasks don’t block shutdown.

Removed redundant time.sleep() calls inside receive loops (reducing latency).

### 5. Robust Communication

Added error handling in both sending and receiving threads.

Clients print error messages when server disconnects instead of silently crashing.

### 6. Better Synchronization Flow

Server calculates an average clock offset across clients.

Synchronization messages are sent in clean 5-second cycles.

Clients now explicitly state when times are sent and received.

# 📊 Example Output

https://github.com/user-attachments/assets/f318d5cc-600e-4916-a739-c5f16e52294f

Server
```
127.0.0.1:53491 got connected successfully
Client Data updated with: 127.0.0.1:53491

New synchronization cycle started.
Number of clients to be synchronized: 1
```

Client
```
Recent time sent successfully

Synchronized time at the client is: 2025-08-21 16:30:12.123456
```
