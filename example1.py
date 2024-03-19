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
    master_server = MasterServer()
    chunk_servers = [ChunkServer(i) for i in range(3)]  #three chunk servers

    #file path
    sample_text_file = '/Users/natashazhang/Desktop/sample_text.txt'

    #read the sample text
    with open(sample_text_file, 'r') as file:
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
