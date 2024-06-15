#! /bin/python3
from redditscraper import redditScraper, redditParser


def digUser(directory: str, user: str, progress = False):
    parser = 1
    goBefore = False

    userMsgs = set()

    if progress: print()

    while bool(parser):
        scraper = redditScraper(directory)
        scraper.setAuthor(user)

        if goBefore:
            scraper.setBefore(goBefore)

        data = scraper.scrape()

        parser = redditParser(data)

        if len(parser) > 0:
            goBefore = parser.getOldestTS()

            subs = parser.getSubs()
            text = parser.getText()

            if progress:
                print('\r' + f"{user} has so far {len(userMsgs)}", end = "")
            
            userMsgs.update(list(zip(subs, text)))

    if progress:
        print()

    return userMsgs

