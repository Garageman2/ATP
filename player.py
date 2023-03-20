import time
import requests
from selenium.webdriver import Chrome
from splinter import Browser
from bs4 import BeautifulSoup
from enum import Enum
from datetime import date
from dateutil import relativedelta


class Player_Url(Enum):
    OVERVIEW = "overview"
    BIO = "bio"
    ACTIVITY = "player-activity"
    WIN_LOSS = "fedex-atp-win-loss"
    TITLES_FINALS = "titles-and-finals"
    RANKINGS_HISTORY = "rankings-history"
    RANKINGS_BREAKDOWN = "rankings_breakdown"



class Player:

    country = None
    hand = None
    backhand = None

    #TODO: set config to headless for release
    @staticmethod
    def query_player(name: str):
        base = "https://www.atptour.com/en/players"
        editname = name.strip().lower().replace(" ", "-")
        print(name)
        with Browser('chrome') as browser:
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

    def swap_link(self,variant:Player_Url):
        return self.base_url + "/" + variant.value

    def __init__(self, name:str):
        self.name = name
        self.base_url, html = Player.query_player(name)
        hero_table = html.find("div",class_="player-profile-hero-table")
        wraps = [x for x in hero_table.descendants if hasattr(x,"attrs") and "class" in x.attrs and ("wrap" in x["class"])]
        for wrap in wraps:
            edit_var = None
            for div in [ x for x in wrap.contents if x != '\n']:
                match div["class"]:
                    case ["table-big-value"]:
                        if div.span != None:
                            data = div.span.text.strip()
                            match data[-1]:
                                case '\"': self.height = data;
                                case ')': birthdate = data[1:-1].split("."); self.age = relativedelta.relativedelta(date.today(),date(int(birthdate[0]),int(birthdate[1]),int(birthdate[2]))).years;
                                case 's': self.weight = int(data[:-3]);
                    case ["table-value"]:
                        match edit_var:
                            case self.country:
                                print(div.contents[0].strip())
                                self.country = div.contents[0].split(", ")[1]
                            case self.hand:
                                print(div.contents[0].strip())
                                self.hand = div.contents[0].strip().split("-")[0]
                                self.backhand = div.contents[0].strip().split(" ")[1].strip()

                    case ["table-label"]:
                        print("label")
                        match div.contents[0].strip():
                            case "Birthplace": edit_var = self.country
                            case "Plays": edit_var = self.hand
        self.rank = int(html.find(class_="data-number").contents[0].strip())
        #TODO: get recent win-loss information
        self.base_url = self.base_url[:-9]
        self.uuid = self.base_url[-4:]
        print(self.swap_link(Player_Url.TITLES_FINALS))
        #TODO: Curl and parse


    def __str__(self):
        return self.name;