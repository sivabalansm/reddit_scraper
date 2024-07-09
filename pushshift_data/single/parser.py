import json
from collections.abc import Iterable

class Parser:
    USER = 'author'
    SUB = 'subreddit'
    COMMENT = 'body'
    POST_TITLE = 'title'
    POST_BODY = 'selftext'

    def __init__(self, data):
        try:
            self.data = json.loads(data)

        except json.decoder.JSONDecodeError:
            print("Can't decode the json, malformed")
            print(f"{data[:50]} ... {data[-50:]}")

        self.is_iter = isinstance(self.data, Iterable)
        self.is_dict = type(self.data) == dict


    def get_user(self) -> list[str]:
        users = []
        if self.is_dict:
            users.append(self.data[self.USER])

        elif self.is_iter:
            for entry in self.data:
                users.append(entry[self.USER])

        return users

    def get_subs(self) -> list[str]:
        subs = []

        if self.is_dict:
           try:
               subs.append(self.data[self.SUB])

           except KeyError:
               return subs

        elif self.is_iter:
            for entry in self.data:
                try:
                    subs.append(entry[self.SUB])
                except KeyError:
                    return subs

        return subs

    def get_body(self) -> list[tuple]:
        body = []

        if self.is_dict:
            try:
              if self.COMMENT in self.data:
                  body.append( ('C', (self.data[self.COMMENT],) ))
              else:
                  # it is a sub post
                  body.append( ('S', (self.data[self.POST_TITLE], self.data[self.POST_BODY])) )

            except KeyError:
                    return body

        elif self.is_iter:
            for entry in self.data:
                try:
                    if self.COMMENT in entry:
                        body.append( ( 'C', tuple(entry[self.COMMENT]) ) )
                    else:
                        # it is a sub post
                        body.append( ('S', (entry[self.POST_TITLE], entry[self.POST_BODY]) ) )

                except KeyError:
                    return body

        return body







        

                

