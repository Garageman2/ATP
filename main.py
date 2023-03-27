import time
import sys

from player import Player
from threading import Thread
from head2head import Head2Head
from time import sleep

loading = False

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
    build_h2h()

def build_h2h():
    name1 = input("Enter Player 1's name as spelled in English: ")
    name2 = input("Enter Player 2's name as spelled in English: ")
    global loading
    loading = True
    thread = Thread(target=lambda: print_prog())
    thread.start();
    p1 = Player(name1);
    p2 = Player(name2);
    loading = False;
    thread.join();
    print(p1,"\n", p2)
    print(Head2Head(p1,p2))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

