import time
import sys
import os
import json
import itertools

from player import Player
from threading import Thread
from head2head import Head2Head
from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas

loading = False

players = {}

#!Seems to require the request coming from the US

def print_prog():
    prog_ind = int(1)
    global loading
    while loading:
        match prog_ind%3:
            case 0: sys.stdout.write("\rWorking.");sys.stdout.flush(); time.sleep(.4);
            case 1: sys.stdout.write("\rWorking..");sys.stdout.flush(); time.sleep(.4);
            case 2: sys.stdout.write("\rWorking...");sys.stdout.flush(); time.sleep(.4);
            case other: print("ERR")
        prog_ind += 1;
    print("\n")


def main():
    
    players = top_100()
    mat = {}

#TODO: can speed up massively by creating a map of players

    for comb in itertools.combinations(players,2):
        if comb[0] not in mat.keys():
            mat[comb[0]] = {}
        if comb[1] not in mat.keys():
            mat[comb[1]] = {}
        score = 0
        score = build_h2h(comb[0],comb[1])
        score = '%.3f'%(score)
        mat[comb[0]][comb[1]] = score
        mat[comb[1]][comb[0]] = score

    frame = pandas.DataFrame(data=mat)
    print(frame)
    print(mat)
    frame.to_csv("Output.csv")
    frame.to_excel("Output.xlsx")



#TODO: Scrape the rankings and create a 100x100 table of the top 100
rec_count:int = 0

def build_h2h(name1:str, name2:str):
    global players
    global rec_count

    if name1 in players.keys():
        p1 = players[name1]
    else:
        p1 = Player(name1)
        players[name1] = p1

    if name2 in players.keys():
        p2 = players[name2]
    else:
        p2 = Player(name2)
        players[name2] = p2

    try:
        stats = Head2Head(p1, p2)
        print(stats.eval(), " final score")
        rec_count = 0
        return stats.eval()
    except TypeError:
        rec_count += 1
        if rec_count < 5:
            time.sleep(7.0)
            return build_h2h(name1,name2)
        else:
            rec_count = 0
            return -1.0
    
def top_100():
    top = []
    soup = BeautifulSoup(requests.get(url="https://www.atptour.com/en/rankings/singles").content,'html.parser')
    table = soup.find("table",{"id":"player-rank-detail-ajax"}).tbody
    for c in table.find_all(recursive=False):
        ref = c.find("td", {"class":"player-cell border-left-dash-1 border-right-dash-1"})
        top.append(ref.span.a.text.strip())
        if len(top) >= 30:
            return top
        
    return top


if __name__ == '__main__':
    main()

