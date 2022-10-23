# app-client.py
import socket
import sys
import json
import pandas as pd
import os
df = pd.read_json (r'C:\Users\Jed\Desktop\COEN424_ASSIGNMENT1\WorkloadData\New-DVD-testing.json')


HOST = "127.0.0.1" # The server's hostname or IP address
PORT = 65432 # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    addr = (HOST,PORT)
    print(f"Accepted connection from {addr}")
    s.connect((HOST,PORT))
    has_reqs = True
        while has_reqs:
            rfw_id, benchmark_type, workload_metric, batch_unit, batch_size, batch_id, data_type = make_request() 
            RFW_ID, typeName, BatchUnit, BatchSize, BatchID, WorkloadMetric, DataAnalytics =

            # Create Folder to Store Request and Response
            os.mkdir(f"../output/{rfw_id}")

            # Serialize Request
            rfw = {"rfw_id": rfw_id,  "benchmark_type": benchmark_type, "workload_metric": workload_metric, "batch_unit": batch_unit, "batch_id": batch_id, "batch_size": batch_size, "data_type": data_type}
            req = json.dumps(rfw)

            # Write Request to File
            write_file_output(rfw_id, "rfw", rfw)

            # Send Request to Server
            s.sendall(req.encode("utf-8"))
            
            # Notify User Request Sent
            print("\nRequest Sent!")
            print(req)
            print("\nWaiting for Response ...\n")

            # Receive Response from Server
            # 1024 Represents Buffer Size in Bytes
            data = s.recv(1024)
            
            # Deserialize Response
            res = json.loads(data.decode('utf-8'))

            # Print Response
            print("Response Received!")
            print(res)

            # Write Response to File
            write_file_output(rfw_id, "rfd", res)

            # Continue Loop If More Requests Are to Be Done
            has_reqs = keep_connection()

    except KeyboardInterrupt:
        # Close Socket on Keyboard Interrupt Before Ending Program
        write_warning_message("Closing Socket due to Keyboard Interrupt! (Ctrl C)")
    except Exception:
        # Could Not Connect to Server Socket 
        write_warning_message("Failed to Connect to Server Socket! Must Run Server Before Running Client!")

    print("\nClient Socket Closed!\n")
    

print(f"Client Received back {data!r}")

#this creates a socket object
#uses .connect() to connect to the server
#uses .sendall() to send its messages
#uses .recv() to read the server's reply and then prints it.