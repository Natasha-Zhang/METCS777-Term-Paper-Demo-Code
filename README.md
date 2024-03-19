# METCS777-Term-Paper-Demo-Code
## Environment Setup
Installed Python 3.x.

## How to Run the Code
Copy code and save in a single script for each example(example1.py and example2.py).

Run the script.
## Example 1:Basic File and Chunk Storage
This example shows how files can be split into chunks and stored across different servers.
```{example1}
#define MasterServer
class MasterServer:
    def __init__(self):
        #initialize a mapping of file names to their chunk identifiers
        self.file_to_chunks = {}
        #initialize a mapping of chunk identifiers to their corresponding server
        self.chunk_to_server = {}

    def create_file(self, filename, num_chunks, servers):
        #create chunk identifiers for each part of the file and store them
        self.file_to_chunks[filename] = [f'{filename}_chunk_{i}' for i in range(num_chunks)]
        #assign each chunk to a server using round-robin scheduling
        for i, chunk_id in enumerate(self.file_to_chunks[filename]):
            self.chunk_to_server[chunk_id] = servers[i % len(servers)]

    def get_file_chunks(self, filename):
        #return a list of chunks that make up the file
        return self.file_to_chunks.get(filename, [])

#define ChunkServer
class ChunkServer:
    def __init__(self, server_id):
        #initialize the chunk server with a unique ID and empty storage
        self.server_id = server_id
        self.storage = {}

    def store_chunk(self, chunk_id, data):
        #store the given data in the chunk identified by chunk_id
        self.storage[chunk_id] = data
        print(f"Chunk {chunk_id} stored on server {self.server_id}")

    def retrieve_chunk(self, chunk_id):
        #retrieve the data stored in the specified chunk
        return self.storage.get(chunk_id)

if __name__ == "__main__":
    #create a MasterServer instance
    master_server = MasterServer()
    #create three chunk servers
    chunk_servers = [ChunkServer(i) for i in range(3)]  

    #file path
    sample_text_file = '/Users/natashazhang/Desktop/sample_text.txt'

    #read the sample text
    with open(sample_text_file, 'r') as file:
        #each line of the file will be an element in the list
        sample_text = file.read().splitlines()

    #create example.txt with chunks equal to the number of lines in the sample text
    master_server.create_file("example.txt", len(sample_text), chunk_servers)

    #store each line of the sample text in its respective chunk on the assigned server
    for i, chunk_id in enumerate(master_server.get_file_chunks("example.txt")):
        assigned_server = master_server.chunk_to_server[chunk_id]
        assigned_server.store_chunk(chunk_id, sample_text[i])

    #retrieve and print the stored data from each chunk of example.txt
    for chunk_id in master_server.get_file_chunks("example.txt"):
        server = master_server.chunk_to_server[chunk_id]
        print(f"{chunk_id}: {server.retrieve_chunk(chunk_id)}")
```
MasterServer class is used to creating and tracking of files and their chunks, which uses round-robin scgeduling to distribute chunks across the servers.

ChunkServer class simulates the storage and retrieval of chunk data on a server.

In the main part, a simulate distributed storage system create by MasterServer and multiple ChunkServer.
### Results and Dataset
The output indicate where each chunk is stored and the contents of each chunk.

Output:
```{output1}
Chunk example.txt_chunk_0 stored on server 0
Chunk example.txt_chunk_1 stored on server 1
Chunk example.txt_chunk_2 stored on server 2
Chunk example.txt_chunk_3 stored on server 0
Chunk example.txt_chunk_4 stored on server 1
example.txt_chunk_0: text1
example.txt_chunk_1: text2
example.txt_chunk_2: text3
example.txt_chunk_3: text4
example.txt_chunk_4: text5
```

### Pros:
The sample text can be divided into chunks and distributed across multiple servers, which reflecting GFS's ability to manage large datasets efficiently.

The demo code shows the basic principle of horizontal scaling, where adding more servers can increase storage capacity.

## Example 2: File and Chunk Storage with Replication
This example introduces a replication_factor to replicate chunks across multiple servers, enhancing fault tolerance.

In a real GFS setup, this would help ensure data availability even if one of the servers fails.
```{example2}
# define MasterServer
class MasterServer:
    def __init__(self):
        #initialize a mapping of file names to their chunk identifiers
        self.file_to_chunks = {}
        #initialize a mapping of chunk identifiers to their corresponding server
        self.chunk_to_server = {}

    def create_file(self, filename, num_chunks, servers, replication_factor=2):
        #create chunk identifiers for each part of the file and store them
        self.file_to_chunks[filename] = [f'{filename}_chunk_{i}' for i in range(num_chunks)]
        #assign each chunk to the specified number of servers for replication
        for chunk_id in self.file_to_chunks[filename]:
            self.chunk_to_server[chunk_id] = servers[:replication_factor]

    def get_chunk_servers(self, chunk_id):
        #return the list of servers that store the specified chunk
        return self.chunk_to_server.get(chunk_id, [])

    def get_file_chunks(self, filename):
        #return a list of chunks that make up the file
        return self.file_to_chunks.get(filename, [])

#define ChunkServer
class ChunkServer:
    def __init__(self, server_id):
        #initialize the chunk server with a unique ID and empty storage
        self.server_id = server_id
        self.storage = {}

    def store_chunk(self, chunk_id, data):
        #store the given data in the chunk identified by chunk_id
        self.storage[chunk_id] = data
        print(f"Chunk {chunk_id} stored on server {self.server_id}")

    def retrieve_chunk(self, chunk_id):
        #retrieve the data stored in the specified chunk
        return self.storage.get(chunk_id)

if __name__ == "__main__":
    #create a MasterServer instance
    master_server = MasterServer()
    #create three chunk servers
    chunk_servers = [ChunkServer(i) for i in range(3)]

    #file path 
    filename = "example.txt"
    sample_text_file = '/Users/natashazhang/Desktop/sample_text.txt'

    #read the sample text
    with open(sample_text_file, 'r') as file:
        #each line of the file will be an element in the list
        sample_text = file.readlines()  

    #determine the number of chunks based on the number of lines in the sample text
    num_chunks = len(sample_text)

    #create the file in the simulated GFS with the determined number of chunks
    master_server.create_file(filename, num_chunks, chunk_servers, 2)

    #store each line of the sample text in its respective chunk on the assigned servers
    for i, chunk_id in enumerate(master_server.get_file_chunks(filename)):
        #get the corresponding part of the text, and removing any newline characters
        data = sample_text[i].strip() 
        servers = master_server.get_chunk_servers(chunk_id)
        for server in servers:
            server.store_chunk(chunk_id, data)

    #retrieve and print the stored data from each chunk of the file from the servers
    for chunk_id in master_server.get_file_chunks(filename):
        servers = master_server.get_chunk_servers(chunk_id)
        for server in servers:
            print(f"Data from server {server.server_id} for {chunk_id}: {server.retrieve_chunk(chunk_id)}")

```
### Results and Dataset
The output shows where each chunk is stored and replicated, and the contents of each chunk as  retrieved from the first server.   Also, the output shows that each chunk is stored on two different servers.

Output:
```{output2}
Chunk example.txt_chunk_0 stored on server 0
Chunk example.txt_chunk_0 stored on server 1
Chunk example.txt_chunk_1 stored on server 0
Chunk example.txt_chunk_1 stored on server 1
Chunk example.txt_chunk_2 stored on server 0
Chunk example.txt_chunk_2 stored on server 1
Chunk example.txt_chunk_3 stored on server 0
Chunk example.txt_chunk_3 stored on server 1
Chunk example.txt_chunk_4 stored on server 0
Chunk example.txt_chunk_4 stored on server 1
Data from server 0 for example.txt_chunk_0: text1
Data from server 1 for example.txt_chunk_0: text1
Data from server 0 for example.txt_chunk_1: text2
Data from server 1 for example.txt_chunk_1: text2
Data from server 0 for example.txt_chunk_2: text3
Data from server 1 for example.txt_chunk_2: text3
Data from server 0 for example.txt_chunk_3: text4
Data from server 1 for example.txt_chunk_3: text4
Data from server 0 for example.txt_chunk_4: text5
Data from server 1 for example.txt_chunk_4: text5
```
### Pros:
This example add replication for the code, which ensuring that data is copied across multiple server to prevent data loss or server faliures.
## Cons for GFS:
These two examples didn't show cons for Google File System. Here are some cons for GFS list:

GFS is optimized for large files, which leads to inefficiencies when managing a large number of small files.
