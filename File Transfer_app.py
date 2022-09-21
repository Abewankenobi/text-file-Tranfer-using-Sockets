# Importing Pickle to send dictionary objects
import pickle
# Importing python-docx and PyPDF
import PyPDF2
from PyPDF2 import PdfFileWriter
import docx
# Importing sockets in order to get IP_Address
import socket
# Importing reportlab to create new PDF from Scratch
from fpdf import FPDF

class FileTransfer_app:
    # Initializing the class features
    def __init__(self,account_details=""):
        self.hostname = socket.gethostname()
        #self.ip_add = socket.gethostbyname(self.hostname)
        self.ip_add = input("Enter your IPV4 Address: ")
        # Initializing database management system
        #self.conn = sqlite3.connect("FT.sqlite")
        #self.cur = self.conn.cursor()
        # Creating Tables
        #self.cur.execute("DROP TABLE IF EXISTS backend") This line deletes all existing data from the table when the an instance is created
        #self.cur.execute("CREATE TABLE IF NOT EXISTS backend (Hostname TEXT, Ip_Address TEXT)")
        # Insert IP Address into Database: self.cur.execute()
    def server_connection(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating the socket server
        server_socket.bind((self.ip_add,9497)) # Getting reading to bind with clients
        server_socket.listen(5) # Max number of connection devices is 5
        # Reading the file to be copied
        file_dict = dict()
        path = input(r"Enter full file_Path: ")
        filepath = (path)
        filepath = filepath.split("\\")
        index = len(filepath) - 1 # Getting the Last index in the List
        filename = filepath[index]
        file_dict["Filename"] = filename
        # ******Flow statements for type of document to be sent******
        TOD = filename.split(".") # TOD ==> Type of Document e.g .txt,.MP4,.MP4,.Docx 
        # Condition for Documents such as texts, Ms word, Excel, PDF formats
        if TOD[1].lower() == "txt":
            file = open(path)
            file_content = ""
            for line in file:
                file_content += line
            file_dict["Filecontents"] = file_content
        elif TOD[1].lower() == "pdf": # If type of document is .MP3, i.e Music:
            file_content = ""
            reader = PyPDF2.PdfFileReader(path)
            num_page = reader.numPages # Getting number of pages to loop over
            for i in range(num_page):
                page = reader.getPage(i)
                content = page.extract_text()
                file_content += content
            file_dict["Filecontents"] = file_content  # Contents of the PDF
            print(file_dict["Filecontents"])
            file_dict["Num_Pages"] = num_page
        while True:
            client,addr = server_socket.accept() # Accepting connections
            print("Connected with",addr)
            message = client.recv(1024).decode()
            print(f"Message from client is {message}")
            file = pickle.dumps(file_dict) # Sending the document using Pickle module
            client.send(file) # Sending content of file
            client.close() # Closing connections
            print(f"Connection with {addr} ended!")
    def receiver_connection(self):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating the socket
        client.connect((self.ip_add,9497))
        client.send(bytes("Ready to Receive","utf-8"))
        # To store incoming dictionary object
        data = b""
        full_content = "" # To store the contents of the file
        while True:
            received_content = (client.recv(5120))
            if len(received_content) < 1:
                break
            data += received_content
        file = pickle.loads(data)
        TOD = file["Filename"].split(".")[0] # Selectin the File name except type
        TOD1 = file["Filename"].split(".")[1] # Selectin the File extention, e.g pdf,txt,docx
        full_content += file["Filecontents"]
        # Duplicating filename, content of file
        filename = open(TOD+".txt", "a")
        filename.write(full_content)
        filename.close() # Closing the file
        # Converting to required document format e.g. pdf,Docx
        if TOD1 == "pdf":
            pass
        if TOD1 == "docx":
            pass
        client.close() # Closing the socket connection
# Gradual Testing
ft = FileTransfer_app()
print(ft.server_connection())
