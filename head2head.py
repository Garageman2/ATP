import math
from typing import Callable
from player import Player
from bs4 import BeautifulSoup
import requests


class H2HConfig:
    country: int = .5
    match_threshold: int = 5
    equal: int = 3
    slam_threshold: int = 1
    have_slam: int = 1
    slam_count_calc: Callable[[int], int] = None
    masters_threshold: int = 3
    have_masters = .5
    masters_count_calc: Callable[[int], int] = None
    career_high: float = .5
    career_high_range: int = 5
    rank: float = .5
    rank_range: int = 5
    generations: int = 2
    gen_min_diff: int = 3
    top_ten: float = .25

    def __init__(self):
        self.slam_count_calc = self.default_slam_count
        self.masters_count_calc = self.default_masters_count

    @classmethod
    def default_slam_count(cls, slams: int) -> int:
        return round(math.log(slams, 2))

    @classmethod
    def default_masters_count(cls, slams: int) -> int:
        return round(math.log(slams, 5))


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
    score: float = 0
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

    def eval(self):
        self.score = 0

        # metric to measure equality of head to head
        angle = math.degrees(round(math.atan2(float(self.p1_wins), float(self.p2_wins)), 3))
        self.score += (1 - (abs(45 - angle) / 45)) * self.config.equal
        # finds proportion of max dist, .45, then subtracts from one to find closeness

        if self.matches >= self.config.match_threshold:
            self.score = self.config.equal * .5
            if (self.p1_wins != 0) and (self.p2_wins != 0):
                self.score += self.config.equal * .5 * (
                            min(self.p2_wins, self.p1_wins) / max(self.p2_wins, self.p1_wins))

        if self.p1.country == self.p2.country:
            self.score += self.config.country

        if self.p1.slams >= self.config.slam_threshold and self.p2.slams > - self.config.slam_threshold:
            self.score += self.config.have_slam
            slams = self.p1.slams + self.p2.slams
            self.score += self.config.slam_count_calc(slams)

        if self.p1.masters >= self.config.masters_threshold and self.p2.masters > - self.config.masters_threshold:
            self.score += self.config.have_masters
            masters = self.p1.masters + self.p2.masters
            self.score += self.config.masters_count_calc(masters)

        if self.p1.career_high in range(max(self.p2.career_high - self.config.career_high_range, 1),
                                        self.p2.career_high +
                                        self.config.career_high_range):
            self.score += self.config.career_high * abs(self.p2.career_high - self.p1.career_high) / \
                                        self.config.career_high_range

        if self.p1.rank in range(max(self.p2.rank - self.config.rank_range, 1), self.p2.rank + self.config.rank_range):
            self.score += self.config.rank * abs(self.p2.rank - self.p1.rank) / self.config.rank_range

        generations = round((abs(self.p1.age - self.p2.age))/5)
        self.score += self.config.generations * ((generations-2)**2)

        if self.p1.rank <= 10:
            self.score += self.config.top_ten

        if self.p2.rank <= 10:
            self.score += self.config.top_ten

        self.score = round(self.score, 3)
        print(self.score, "score")
        # TODO: score streak, reddit hype, similar titles
