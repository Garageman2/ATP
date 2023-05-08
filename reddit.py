from dotenv import dotenv_values
from dotenv import load_dotenv
import praw

def search_reddit(name1:str, name2:str) ->(int,int):
    conf = dotenv_values(".env")

    threads = 0
    comments = 0
    
    reddit = praw.Reddit(client_id = conf["REDDIT_KEY"], client_secret = conf["REDDIT_SECRET"], user_agent = "TennisHype 1.0 by /u/AverageBeef")
    for s in reddit.subreddit("tennis").search("flair:'post-match thread'" + name1 + "d. " + name2, time_filter = "year", sort = "top",syntax = "plain",):
        if name1 in s.title and name2 in s.title:
            threads += 1
            comments += len(s.comments.list())
    return (threads,comments)