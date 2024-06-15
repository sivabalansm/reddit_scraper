#! /bin/python3
from gather_users import gatherUsersFromSub
from user_stalker import digUser
from utils import progressBar
import json


def userSubStalker(sub = "AskReddit", userMinQuantity = 100, freshBatch = False, progress = False):
    users = set()
    all_users = dict()

    if freshBatch:
        users = gatherUsersFromSub(sub, userMinQuantity, progress = progress)
        with open('users.txt', 'a') as f:
            for user in users:
                f.write(user + '\n')
    else:
        with open('users.txt', 'r') as f:
            for line in f.readlines():
                users.add(line[:-1]) # [:-1] removes the new line (\n) byte at the end of the string

    total_users = len(users)

    for idx in range(total_users):
        user = list(users)[idx]
        userMsgs = digUser("submission", user)
        userMsgs.update(digUser("comment", user))

        userMsgs = list(userMsgs)

        if progress:
            progressBar(f"Gathering {user}. Currently {idx+1} users gathered out of {total_users} ", idx+1, total_users)

        all_users[user] = userMsgs


    return all_users


all_users = userSubStalker(sub = 'depression', userMinQuantity = 1000, freshBatch = True, progress = True)
with open('all_user_data.json', 'w') as f:
    f.write(json.dumps(all_users))




