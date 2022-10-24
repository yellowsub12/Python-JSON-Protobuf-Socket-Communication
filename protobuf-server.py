# protobuf-server.py
import socket
import sys
import json
import csv
from xmlrpc.client import Server
import numpy as np
import protobuf_pb2 as pb



#CLIENT'S RFW
#1. RFW ID
#2. Benchmark Type (such as DVD store or NDBench)
def BenchmarkType(Benchmark_type, Data_type):
    return f"WorkloadData/{Benchmark_type}-{Data_type}.csv"
#3. Workload Metric (such as CPUUtilization or NetworkIn)
#4. Batch Unit (number of samples contained in each batch, such as 100)
#5. Batch ID (such as 1st, 2nd or 5th Batch)
#6. Batch Size (such as how many batches to return, 5 means 5 batches to return)
#7. Data Type (training data or testing data)
#8. Data analytics (avg, std, max, min)

def ProcessData(typeName, BatchUnit, BatchSize, BatchID, WorkloadMetric, DataAnalytics):
    ProcessedData = []
    with open(typeName, mode = 'r') as file:
        datasetFile = csv.reader(file)
        datasetFileList = list(datasetFile)
        FirstBatch = BatchID * BatchUnit
        SecondBatch = FirstBatch + BatchSize * BatchUnit - 1
        for i in range(FirstBatch, SecondBatch): 
            ProcessedData.append(float(datasetFileList[i][WorkloadMetric - 1]))
    return ProcessedData

#SERVER'S RFD
#1. RFW ID
#2. Last Batch ID
#3. Data samples requested
#4. Data analytics (avg, std, max, min)



HOST = "127.0.0.1" # Standard loopback interface address (localhost), can be hostname, IP address or empty string.
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    try: # Creates socket object that supports context manager type, so you can use it in a with statement without needed s.close()=
    # AF_INET is the Internet address family (IPv4), SOCK_STREAM is TCP
    
        s.bind((HOST, PORT)) # Values passed to bind depend on address family (AF_INET)
        s.listen() # enables server to accept connections
        print("Server is awaiting connection! Make sure to turn on the client connection!")
        conn, addr = s.accept() # blocks execution and waits for incoming connection. when a client connects, it returns a new socket object representing the connection and a tuple (host, port) holding the address of the client
        print(f"Server has connected! Connected to {addr}!")
        with conn:
            print(f"Connected by {addr}")
            while True: #infinite loop used to loop over blocking calls
                data = conn.recv(1024) #reads client data
                if not data:
                    break
                print("RFW Received! Preparing to send RFD!")
                server_request = pb.RequestForWork()
                server_request.ParseFromString(data)
                BenchmarktypeName = BenchmarkType(server_request.typeName, server_request.data_type)
                ProcessedData = ProcessData(BenchmarktypeName, server_request.BatchUnit, server_request.BatchSize, server_request.BatchID, server_request.WorkloadMetric, server_request.DataAnalytics)
                DataAnalytics = server_request.DataAnalytics
                if DataAnalytics == 'avg':
                    DataAnalyticsAnswer = sum(ProcessedData)/len(ProcessedData)
                elif DataAnalytics == 'std':
                    DataAnalyticsAnswer = np.std(ProcessedData)
                elif DataAnalytics == 'max':
                    DataAnalyticsAnswer = max(ProcessedData)
                elif DataAnalytics == 'min':
                    DataAnalyticsAnswer = min(ProcessedData)
                elif DataAnalytics == '10p':
                    DataAnalyticsAnswer = np.percentile(ProcessedData,10)
                elif DataAnalytics == '50p':
                    DataAnalyticsAnswer = np.percentile(ProcessedData,50)
                elif DataAnalytics == '95p':
                    DataAnalyticsAnswer = np.percentile(ProcessedData,90)
                elif DataAnalytics == '99p':
                    DataAnalyticsAnswer = np.percentile(ProcessedData,95)
                else:
                    DataAnalyticsAnswer = 0
                
                FinalBatchID = server_request.BatchID + server_request.BatchSize - 1
                #ResponseForData = {"RFW_ID"= server_request.RFW_ID, "FinalBatchID"= FinalBatchID, "ProcessedData"= ProcessedData, "DataAnalytics"=DataAnalyticsAnswer} 
                ServerResponse = pb.ResponseForData(RFW_ID = server_request.RFW_ID, FinalBatchID= FinalBatchID, ProcessedData= ProcessedData, DataAnalytics=str(DataAnalyticsAnswer))
                ServerDataResponse= ServerResponse.SerializeToString()
                conn.sendall(ServerDataResponse) #sends client data back
                print("The Server's Response Has Been Sent!")
                print(ServerDataResponse)
                print("Awaiting for a new request!")
                #if conn.recv returns an empty bytes object, that means client closed the connection and  the loop is terminated, with statement closes the socket at the end of the block.
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")

# with .send(), it's possible that you don't end up sending all the data
# with .sendall() however, this makes sure everything is sent. 
# .select() method allows to check for I/O completion on more than one socket
# asyncio does multitasking and an event loop to manage tasks
