import zstandard
import multiprocessing
import os
from time import sleep
import sys

MAX_MEM = 2**31
CHUNK_SIZE = 2**27

def decompProc(path, proc_id, start = 0, total_bytes = 0):
    proc_id = f"[{proc_id}]"
    chunks_len = 0
    dctx = zstandard.ZstdDecompressor(max_window_size=MAX_MEM)
    with open(path, 'rb') as f:
        reader = dctx.stream_reader(f, read_across_frames=True)
        print(proc_id, "Using maximum memory of:", MAX_MEM/1024/1024, "MB")
        sleep(1)

        reader.seek(start)
        print(proc_id, "Starting at:", start)
        print(proc_id, "Chunks to read:", total_bytes//CHUNK_SIZE)
        print(proc_id, "Leftover bytes from chunk division:", total_bytes % CHUNK_SIZE)

        for _ in range(total_bytes//CHUNK_SIZE):
            chunk = reader.read(CHUNK_SIZE)
            chunks_len += len(chunk.decode())
        chunk = reader.read(total_bytes % CHUNK_SIZE)
        chunks_len += len(chunk.decode())
        print(proc_id, "Decompressed data size:", chunks_len/1024/1024, "MB")
        print(proc_id, "Done")


def main():
    path = sys.argv[1]
    cpu_count = multiprocessing.cpu_count() - 1
    file_size = os.stat(path).st_size
    print("File size:", file_size/1024/1024, "MB")
    print("Compressed file size:", file_size)

    bytes_per_core = file_size // cpu_count
    leftover_bytes = file_size % cpu_count



    procs = []
    bytes_start = 0

    for proc_id in range(cpu_count-1):
        p = multiprocessing.Process(target = decompProc, args = (path, proc_id, bytes_start, bytes_per_core))
        procs.append(p)
        bytes_start += bytes_per_core

    p = multiprocessing.Process(target = decompProc, args = (path, proc_id + 1, bytes_start, bytes_per_core + leftover_bytes))
    procs.append(p)

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()



if __name__ == "__main__":
    main()




