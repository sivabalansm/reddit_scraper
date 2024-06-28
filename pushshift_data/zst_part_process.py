# this is an example of loading and iterating over a single file
import zstandard
import os
import json
import sys
from datetime import datetime
import logging.handlers


log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
    chunk = reader.read(chunk_size)
    bytes_read += chunk_size
    if previous_chunk is not None:
        chunk = previous_chunk + chunk
    try:
        return chunk.decode()
    except UnicodeDecodeError:
        if bytes_read > max_window_size:
            raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
        log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
        return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
    with open(file_name, 'rb') as file_handle:
        buffer = ''
        reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)

            print(len(chunk))
            break
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")


            
            for line in lines[:-1]:
                yield line

            buffer = lines[-1]

        reader.close()


if __name__ == "__main__":
    file_path = sys.argv[1]
    file_size = os.stat(file_path).st_size
    
    for line in read_lines_zst(file_path):
        obj = json.dumps(line)




