import time
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from enum import Enum

class Player_Url(Enum):
    OVERVIEW = "overview"
    BIO = "bio"
    ACTIVITY = "player-activity"
    WIN_LOSS = "fedex-atp-win-loss"
    TITLES_FINALS = "titles-and-finals"
    RANKINGS_HISTORY = "rankings-history"
    RANKINGS_BREAKDOWN = "rankings_breakdown"



class Player:

    #TODO: set config to headless for release
    @staticmethod
    def query_player(name: str):
        base = "https://www.atptour.com/en/players"
        editname = name.strip().lower().replace(" ", "-")
        print(name)
        with Browser() as browser:
            browser.visit(base)
            pSearch = browser.find_by_id("playerInput")
            pSearch.fill(name)
            pSearch.click()
            time.sleep(2.0)
            pDropdown = browser.find_by_id("playerDropdown")
            for link in browser.find_by_tag('a'):
                if link.value == name:
                    print(link.value)
                    link.click()
                    return browser.url, BeautifulSoup(browser.html,features='html.parser')


    def __init__(self, name:str):
        self.name = name
        self.base_url, html = Player.query_player(name)
        info = html.find("div",class_="player-profile-hero-table")
        wraps = [x for x in info.descendants if hasattr(x,"attrs") and "class" in x.attrs and "wrap" in x["class"]]
        for wrap in wraps:
            try:
                print(len(wrap.contents))
                for div in [ x for x in wrap.contents if x != '\n']:
                    if "table-big-value" in div["class"]:
                        pass
                    elif "table-value" in div["class"]:
                        pass
            except AttributeError:
                pass


    def __str__(self):
        return self.name;


