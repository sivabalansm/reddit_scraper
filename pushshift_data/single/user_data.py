import json

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj

class UserData:
    def __init__(self):
        self.user_data = dict()

    def add(self, user, data):
        if user not in self.user_data:
            self.user_data[user] = set()
        
        self.user_data[user].add(data)

    def save_file(self, file):
        with open(file, 'w') as f:
            f.write(json.dumps(self.user_data, default=serialize_sets))

    def load_file(self, file):
        with open(file, 'r') as f:
            self.user_data = json.loads(f.read())




