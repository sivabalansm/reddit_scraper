

class Users:
    def __init__(self):
        self.users = set()

    def load_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                self.add(line)

    def save_file(self, file):
        with open(file, 'w') as f:
            for user in self.users:
                f.write(user + '\n')


    def add(self, user):
        clean_user = user.strip()
        self.users.add(clean_user)
