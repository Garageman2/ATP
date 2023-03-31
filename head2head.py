import math

from player import Player
from bs4 import BeautifulSoup
import requests


class H2HConfig:
    country = 1
    match_threshold = 5
    equal = 1


class Head2Head:
    link: str = None
    p1: Player = None
    p2: Player = None
    p1_name: str = None
    p2_name: str = None
    p1_wins: int = None
    p2_wins: int = None
    matches: int = None
    most_recent = None
    late_round: int = 0
    config: H2HConfig = H2HConfig()

    def __init__(self, p1: Player, p2: Player) -> object:
        self.p1 = p1
        self.p2 = p2
        self.p1_name = p1.name
        self.p2_name = p2.name
        BASE_LINK = "https://www.atptour.com/en/players/atp-head-2-head/"
        link = BASE_LINK + p1.web_name + "-vs-" + p2.web_name + "/" + p1.uuid + "/" + p2.uuid
        html = BeautifulSoup(requests.get(link).text, features='html.parser')
        players = [None, None]
        players[0] = html.find(class_="h2h-player-left")
        players[1] = html.find(class_="h2h-player-right")
        for p in players:
            class_ = p["class"]
            w = int(p.find(class_="players-head-rank").text.strip())
            match class_[0]:
                case "h2h-player-left":
                    self.p1_wins = w
                case "h2h-player-right":
                    self.p2_wins = w
        self.matches = self.p1_wins + self.p2_wins
        if self.matches > 0:
            table = html.find(class_="modal-event-breakdown-table").tbody
            for child in [x for x in table.children if hasattr(x, "children")]:
                iterc = child.children
                next(iterc)  # this advances to the date
                next(iterc)
                next(iterc)  # this one gives places
                next(iterc)
                next(iterc)  # surface
                next(iterc)
                next(iterc)
                if next(iterc).text.strip() in ["QF", "SF", "F"]: self.late_round += 1
            print(self.late_round)

    def __str__(self):
        return self.p1_name + " has a h2h of " + str(self.p1_wins) + " - " + str(self.p2_wins) + " with " + self.p2_name

    def eval(self) -> int:
        score = 0

        # metric to measure equality of head to head
        angle = round(math.atan2(float(self.p1_wins), float(self.p2_wins)),3)
        #TODO: distance from 45 will be max 45. Find distance, do a one minus operation, maybe the distance divided by .45, then the absolute value and mult by score for equality
        print("Angle ", angle)

        if self.matches >= self.config.match_threshold:
            score = self.config.equal * .5
            if (self.p1_wins != 0) and (self.p2_wins != 0):
                score += self.config.equal * .5 * (min(self.p2_wins, self.p1_wins) / max(self.p2_wins, self.p1_wins))

        if self.p1.country == self.p2.country:
            score += self.config.country

        # TODO: score slams, masters, career high, rank, streak, age
