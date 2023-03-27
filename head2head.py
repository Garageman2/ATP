from player import Player
from bs4 import BeautifulSoup
import requests


class Head2Head:

    link:str = None
    p1_name:str = None
    p2_name:str = None
    p1_wins:str = None
    p2_wins:str = None
    Matches:int = None
    most_recent = None

    def __init__(self, p1:Player,p2:Player) -> object:
        self.p1_name = p1.name
        self.p2_name = p2.name
        BASE_LINK = "https://www.atptour.com/en/players/atp-head-2-head/"
        link = BASE_LINK + p1.web_name + "-vs-" + p2.web_name + "/" + p1.uuid + "/" + p2.uuid
        html = BeautifulSoup(requests.get(link).text, features='html.parser')
        players = [None,None]
        players[0] = html.find(class_="h2h-player-left")
        players[1] = html.find(class_="h2h-player-right")
        for p in players:
            class_ = p["class"]
            w = int(p.find(class_ = "players-head-rank").text.strip())
            match class_[0]:
                case "h2h-player-left": self.p1_wins = w
                case "h2h-player-right": self.p2_wins = w

    def __str__(self):
        return self.p1_name + " has a h2h of " + str(self.p1_wins) + " - " + str(self.p2_wins) + " with " + self.p2_name

