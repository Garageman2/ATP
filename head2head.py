import math
from typing import Callable
from player import Player
from bs4 import BeautifulSoup
import requests


class H2HConfig:
    country: int = 1
    match_threshold: int = 5
    equal: int = 3
    slam_threshold: int = 1
    have_slam: int = 1
    slam_count_calc: Callable[[int], int] = None
    masters_threshold:int = 3
    have_masters = .5
    masters_count_calc: Callable[[int], int] = None

    def __init__(self):
        self.slam_count_calc = self.default_slam_count

    @classmethod
    def default_slam_count(self,slams:int) -> int:
        return math.log(slams, 2)

    @classmethod
    def default_masters_count(self,slams:int) -> int:
        return math.log(slams, 5)

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
        angle = math.degrees(round(math.atan2(float(self.p1_wins), float(self.p2_wins)),3))
        score += (1 - (abs(45-angle)/45)) * self.config.equal
        #finds proportion of max dist, .45, then subtracts from one to find closeness

        if self.matches >= self.config.match_threshold:
            score = self.config.equal * .5
            if (self.p1_wins != 0) and (self.p2_wins != 0):
                score += self.config.equal * .5 * (min(self.p2_wins, self.p1_wins) / max(self.p2_wins, self.p1_wins))

        if self.p1.country == self.p2.country:
            score += self.config.country

        if self.p1.slams >= self.config.slam_threshold and self.p2.slams >- self.config.slam_threshold:
            score += self.config.have_slam
            slams = self.p1.slams + self.p2.slams
            score += self.config.slam_count_calc()

        if self.p1.masters >= self.config.masters_threshold and self.p2.masters >- self.config.masters_threshold:
            score += self.config.have_masters
            score += self.config.masters_count_calc(((self.p1.masters + self.p2.masters)))

        print(score, " score")
        # TODO: score slams, masters, career high, rank, streak, age
