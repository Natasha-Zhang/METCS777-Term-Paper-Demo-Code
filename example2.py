# Extending the MasterServer from Example 1
class MasterServer:
    def __init__(self):
        self.file_to_chunks = {}
        self.chunk_to_servers = {}

    def create_file(self, filename, num_chunks, servers, replication_factor=2):
        self.file_to_chunks[filename] = [f'{filename}_chunk_{i}' for i in range(num_chunks)]
        for chunk_id in self.file_to_chunks[filename]:
            # Assign the first 'replication_factor' servers to this chunk
            self.chunk_to_servers[chunk_id] = servers[:replication_factor]

    def get_chunk_servers(self, chunk_id):
        return self.chunk_to_servers.get(chunk_id, [])

    def get_file_chunks(self, filename):
        return self.file_to_chunks.get(filename, [])


# ChunkServer remains the same as in Example 1
class ChunkServer:
    def __init__(self, server_id):
        self.server_id = server_id
        self.storage = {}

    def store_chunk(self, chunk_id, data):
        self.storage[chunk_id] = data
        print(f"Chunk {chunk_id} stored on server {self.server_id}")

    def retrieve_chunk(self, chunk_id):
        return self.storage.get(chunk_id)
    
if __name__ == "__main__":
    master_server = MasterServer()
    chunk_servers = [ChunkServer(i) for i in range(3)]  # three chunk servers

    filename = "example.txt"
    sample_text_file = '/Users/natashazhang/Desktop/sample_text.txt'

    # Read sample text from the file
    with open(sample_text_file, 'r') as file:
        sample_text = file.readlines()  # Each line of the file will be an element in the list

    num_chunks = len(sample_text)

    master_server.create_file(filename, num_chunks, chunk_servers, 2)

    for i, chunk_id in enumerate(master_server.get_file_chunks(filename)):
        data = sample_text[i].strip()  # Get the corresponding part of the text, removing any newline characters
        servers = master_server.get_chunk_servers(chunk_id)
        for server in servers:
            server.store_chunk(chunk_id, data)

    # Retrieve and print data from the servers
    for chunk_id in master_server.get_file_chunks(filename):
        servers = master_server.get_chunk_servers(chunk_id)
        for server in servers:
            print(f"Data from server {server.server_id} for {chunk_id}: {server.retrieve_chunk(chunk_id)}")
