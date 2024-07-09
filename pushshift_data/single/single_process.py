import zstandard
from parser import Parser
from user import Users
from user_data import UserData
import os.path
import os
from sys import argv

MAX_MEM = 2**31
CHUNK_SIZE = 2**27

class SaveSeekHandler:
    def __init__(self, file, bytes_processed = 0):
        self.file = file
        self.bytes_processed = str(bytes_processed)

    def save(self):
        with open(f"{self.file}.save", "w") as f:
            f.write(self.bytes_processed)
        print("Saved file at:", self.bytes_processed, "bytes")
        return True

    def load(self):
        with open(f"{self.file}.save", "r") as f:
            self.bytes_processed = f.read()

        return int(self.bytes_processed)

def get_reader_start_location(reader):
    return reader.tell() - CHUNK_SIZE



def decode_handler(reader, file, previous_chunk=None, bytes_read=0):
    chunk = reader.read(CHUNK_SIZE)
    bytes_read += CHUNK_SIZE

    if previous_chunk != None:
        chunk = previous_chunk + chunk

    try:
        return chunk.decode()

    except KeyboardInterrupt:
        print("Caught keyboard interrupt\nStopping program...\n")
        SaveSeekHandler(file, get_reader_start_location(reader)).save()
        
    except UnicodeDecodeError:
        print("Unicode decode error")
        if bytes_read > MAX_MEM:
            print("Bytes read exceeds allocated memory!")
        SaveSeekHandler(file, get_reader_start_location(reader)).save()
        return decode_handler(reader, file, previous_chunk = chunk, bytes_read = bytes_read)
    except Exception as e:
        print(e)
        SaveSeekHandler(file, get_reader_start_location(reader)).save()


def decomp(file, start = 0):
    dctx = zstandard.ZstdDecompressor(max_window_size=MAX_MEM)
    loaded = False

    with open(file, 'rb') as f:
        reader = dctx.stream_reader(f, read_across_frames=MAX_MEM)
        try:
            if start != 0:
                print(f"Seeking file to {start} bytes...")
                reader.seek(start)
                loaded = True

            partial_json = ''
            while True:
                decoded_chunk = decode_handler(reader, file)

                if not decoded_chunk:
                    break

                lines = (partial_json + decoded_chunk).split('\n')

                if loaded:
                    lines = lines[1:]
                    loaded = False

                partial_json = lines[-1]
                lines = lines[:-1]


                for line in lines:
                    yield line

        except KeyboardInterrupt:
            print("Caught keyboard interrupt\nStopping program...\n")
            SaveSeekHandler(file, get_reader_start_location(reader)).save()

        except Exception as e:
            print(e)
            SaveSeekHandler(file, get_reader_start_location(reader)).save()

        
def get_file_by_ext(ext: str):
    for file in os.listdir():
        if file.endswith(ext):
            yield file


def main():
    files = argv[1:]


    for file in files:
        lines = None
        loaded = False
        if os.path.isfile(f"{file}.save"):
            lines = decomp(file, SaveSeekHandler(file).load())
            loaded = True

        else:
            lines = decomp(file)

        reddit_users = Users()
        if os.path.isfile(f'{file}.users'):
            reddit_users.load_file(f'{file}.users')

        for line in lines:
            parsed = Parser(line)
            if parsed.get_subs()[0] == 'depression' and parsed.get_user()[0] != '[deleted]':
                reddit_users.add(parsed.get_user()[0])

        reddit_users.save_file(f'{file}.users')

    all_user_data = UserData()
    for file in files:
        all_reddit_users = Users()

        for user_file in get_file_by_ext('.users'):
            all_reddit_users.load_file(user_file)

        lines = decomp(file)

        for line in lines:
            parsed = Parser(line)
            user = parsed.get_user()[0]
            body = parsed.get_body()
            if user in all_reddit_users.users:
                all_user_data.add(user, body)

       


        


if __name__ == "__main__":
    main()
