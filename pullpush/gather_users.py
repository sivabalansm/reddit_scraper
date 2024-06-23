#! /bin/python
from redditscraper import redditScraper, redditParser
from utils import progressBar


def gatherUsersFromSub(sub: str, userMinQuantity: int, progress = False, subScraperMode = True):
    users = set()
    goBefore = False

    while len(users) < userMinQuantity:
        if subScraperMode:
            scraper = redditScraper('submission')
        else:
            scraper = redditScraper('comment')

        scraper.setSub(sub)

        if goBefore:
            scraper.setBefore(goBefore)

        if progress:
            progressBar(f"Users gathered from {sub}: {len(users)}", len(users), userMinQuantity)

    
        data = scraper.scrape()
    
        parser = redditParser(data)
    
        users.update(parser.getUsers())
    
        goBefore = parser.getOldestTS()

    return users

