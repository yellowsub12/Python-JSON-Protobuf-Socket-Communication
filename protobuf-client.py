# protobuf-client.py
import socket
import uuid
import protobuf_pb2 as pb


HOST = "127.0.0.1" # The server's hostname or IP address
PORT = 65432 # The port used by the server

def RequestGenerator():
    RFW_ID = str(uuid.uuid4())[:5]
    typeName =  input("Welcome! Start off by choosing your desired benchmark! Type DVD or NDBench: ")
    WorkloadMetricA = input("Choose your desired Workload Metric! Choose 1 for CPU Utilization, 2 for Network In Average, 3 for Network Out Average Or 4 for Memory Utilization Average: ")
    WorkloadMetric = int(WorkloadMetricA)
    BatchUnit = input("Choose Batch Unit: ")
    BatchUnit = int(BatchUnit)
    BatchSizeA = input("Choose Batch Size: ")
    BatchSize = int(BatchSizeA)
    BatchIDA = input("Choose Batch ID: ")
    BatchID = int(BatchIDA)
    data_type = input("Choose desired Data Type! Type either training or testing: ")
    DataAnalytics = input("Enter your desired Data Analytics! Write avg for Average, std for Standard Deviation, max for Maximum, min for Minimum,\n and 10p, 50p, 95p and 99p for 10th, 50th, 99th percentile respectively! ")


    return RFW_ID, typeName, WorkloadMetric, BatchUnit, BatchSize, BatchID, data_type, DataAnalytics




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    addr = (HOST,PORT)
    print(f"Accepted connection from {addr}")
    s.connect((HOST,PORT))
    connection = True
    while connection:
        RFW_ID, typeName, WorkloadMetric, BatchUnit, BatchSize, BatchID, data_type,DataAnalytics = RequestGenerator() 

        # Serializes
        RequestWork = pb.RequestForWork(RFW_ID=RFW_ID, typeName=typeName,WorkloadMetric=WorkloadMetric,BatchUnit=BatchUnit,BatchID=BatchID, BatchSize=BatchSize, data_type=data_type, DataAnalytics=DataAnalytics)
        receivedRequest = RequestWork.SerializeToString()
        s.sendall(receivedRequest)
        
        print("\nRequest Sent!")
        print(receivedRequest)
        print("\nWaiting for Response ...\n")
        data = s.recv(1024)
        
        # Deserialize Response
        Response = pb.ResponseForData()
        Response.ParseFromString(data)

        # Print Response
        print("Response Received!")
        print(Response)
        user_input = input('Would you like to continue or end the program? Press 9 to exit! Else press 1 to continue : ')
        if user_input == '9':
            connection = False
        else:
            continue



   


    print("\nClient Socket Closed!\n")
    

print(f"Client Received back {data!r}")

#this creates a socket object
#uses .connect() to connect to the server
#uses .sendall() to send its messages
#uses .recv() to read the server's reply and then prints it.