import random as r
import os
from time import sleep

# Duke 0, Captain 1, Assassin 2, Contessa 3, Ambassador 4

def intinputvalidate(prompt, lower, upper):
    while True:
        try:
            temp = int(input(prompt))
            if lower != -1 and upper != -1:
                if temp < lower or temp > upper:
                    1 / 0
                else:
                    return temp
            else:
                return temp
        except:
            print("Invalid input")


players = intinputvalidate("How many players?\n", 2, 100)

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear') # Wipe terminal

# Setup

# Deck

deck = []
totaldecknum = 15
totaldecknum *= (players // 6) + 1

for i in range(totaldecknum // 5):
    deck.append(0)
    deck.append(1)
    deck.append(2)
    deck.append(3)
    deck.append(4)

r.shuffle(deck)

def deckdraw():
    return deck.pop(0)

def deckreturn(card):
    deck.append(card)


# General

cards = []
coins = []
living = []

for i in range(players):
    cards.append([deckdraw(), deckdraw()])
    coins.append(2)
    living.append(True)


# Variables
reset = "\033[0m"
dim = "\033[38;5;240m"
lessdim = "\033[38;5;245m"
dukecolour = "\033[35m"
captaincolour = "\033[36m"
assassincolour = "\033[1;90m"
red = "\033[31m"
ambassadorcolour = "\033[32m"

duke = f"{dukecolour}Duke{reset}"
captain = f"{captaincolour}Captain{reset}"
assassin = f"{assassincolour}Assassin{reset}"
contessa = f"{red}Contessa{reset}"
ambassador = f"{ambassadorcolour}Ambassador{reset}"

# Subroutines

def displayoptions():
    print("Game actions (will end turn):")
    print(f"1: Income: Take 1 coin {dim}(Cannot be blocked){reset}")
    print(f"2: Foreign Aid: Take 2 coins {dim}(Can be blocked by Duke){reset}")
    print(f"3: {duke}: Take 3 coins {dim}(Cannot be blocked){reset}")
    print(f"4: {captain}: Steal 2 coins from another player {dim}(Can be blocked by Captain or Ambassador){reset}")
    print(f"5: {assassin}: Pay 3 coins, pick a player to lose a card {dim}(Can be blocked by Contessa){reset}")
    print(f"{contessa}: Blocks assassination {dim}(Cannot be blocked){reset}")
    print(f"6: {ambassador}: Exchange cards with the deck {dim}(Cannot be blocked){reset}")
    print(f"7: Coup: Pay 7 coins, pick a player to lose a card {dim}(Cannot be blocked, must coup if 10+ coins){reset}")
    print()
    print("Check actions (will not end turn):")
    print(f"8: {lessdim}Check coin counts of all players{reset}")
    print(f"9: {lessdim}Check card numbers of all players{reset}")
    print(f"10: {lessdim}Check own cards (get all other players to look away for 3 seconds){reset}")
    print()

def findwin():
    temp = 0
    for j in range(len(living)):
        if living[j]:
            temp += 1

    if temp <= 1:
        for i in range(len(living)):
            if living[i]:
                print(f"Player {i + 1} wins!")
                sleep(5)
                quit()

def coincheck():
    for i in range(players):
        print(f"Player {i+1}: {coins[i]} coins")

def cardnumcheck():
    for i in range(players):
        print(f"Player {i+1}: {len(cards[i])} cards")

def selfcardcheck(player):
    print(f"{red}ALL PLAYERS EXCEPT PLAYER {player+1} LOOK AWAY{reset}")
    print("3", end="\r")
    sleep(1)
    print("2", end="\r")
    sleep(1)
    print("1", end="\r")
    sleep(1)
    tempcardlist = ['', '']
    for i in range(len(cards[player])):
        match cards[player][i]:
            case 0:
                tempcardlist[i] = duke
            case 1:
                tempcardlist[i] = captain
            case 2:
                tempcardlist[i] = assassin
            case 3:
                tempcardlist[i] = contessa
            case 4:
                tempcardlist[i] = ambassador
            case _:
                tempcardlist[i] = "?"
    print(f"{tempcardlist[0]}, {tempcardlist[1]}", end="\r")
    sleep(2)
    print("=" * 50)

def die(player):
    print(f"Player {player+1} is losing a card")
    if len(cards[player]) == 2:
        seecards = intinputvalidate("Would you like to see your cards? (1=yes, 0=no)\n", 0, 1)
        if seecards:
            selfcardcheck(player)
        losecard = intinputvalidate("Which card would you like to lose? (1 or 2)\n", 1, 2)
        if losecard == 1:
            cards[player] = [cards[player][1]]
        elif losecard == 2:
            cards[player] = [cards[player][0]]
    else:
        print(f"Player {player+1} lost their final card and is now out.")
        cards[player] = []
        living[player] = False
    findwin()


def challenge(accuser, challenged, card):
    flag1 = False
    for i in range(len(cards[challenged])):
        if cards[challenged][i] == card:
            flag1 = True
    if flag1:
        print("Challenge failed.")
        die(accuser)
        print(f"Player {challenged+1} must now replace their card.")
        flag = False
        for i in range(len(cards[challenged])):
            if cards[challenged][i] == card:
                cards[challenged][i] = deckdraw()
                flag = True
            if flag:
                continue
        return False
    else:
        print("Challenge successful!")
        die(challenged)
        return True

def income(player):
    coins[player] += 1
    print(f"Player {player+1} took 1 coin.")

def foreignaid(player):
    print(f"Player {player + 1} is attempting to take foreign aid.")
    block = intinputvalidate(f"Would anyone like to block with a {duke}? (input blocking player number, 0 if no block)\n", 0, players)
    if block == 0:
        coins[player] += 2
    else:
        print(f"Player {block} is claiming to have a {duke} and is blocking the foreign aid.")
        challengeconfirm = intinputvalidate(f"Player {player+1}, would you like to challenge? (1=yes, 0=no)\n", 0, 1)
        if not challengeconfirm:
            print(f"Player {player + 1} attempted to take foreign aid, but it was blocked by player {block} with a {duke}.")
        else:
            if challenge(player, block-1, 0):
                coins[player] += 2
                print(f"Player {player + 1} took 2 coins.")

def dukeact(player):
    print(f"Player {player + 1} is taking 3 coins with their {duke}.")
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has a {duke}? (input challenging player number, 0 if no challenge)\n", 0, players)
    if challenger == 0:
        coins[player] += 3
        print(f"Player {player + 1} took 3 coins.")
    else:
        if not challenge(challenger-1, player, 0):
            coins[player] += 3
            print(f"Player {player + 1} took 3 coins.")

def stealcoins(theif, victim):
    if coins[victim] == 0:
        print(f"No coins could be stolen from player {victim+1} as they had no coins.")
    elif coins[victim] == 1:
        print(f"Only 1 coin was stolen from player {victim+1} as they only had one coin.")
        coins[victim] -= 1
        coins[theif] += 1
    else:
        print(f"Player {theif + 1} stole 2 coins from player {victim+1}")
        coins[victim] -= 2
        coins[theif] += 2

def captainact(player):
    victim = intinputvalidate(f"Select a player to steal 2 coins from: (1 - {players})\n", 1, players)
    block = intinputvalidate(f"Player {victim}, would you like to block with a {captain} or an {ambassador}? (1=Captain, 2=Ambassador, 0=No block)\n", 0, 2)
    if block == 0:
        victimchallengeconfirm = intinputvalidate(f"Player {victim}, would you like to challenge player {player+1}'s {captain}? (1=yes, 0=no)\n", 0, 1)
        if not victimchallengeconfirm:
            stealcoins(player, victim-1)
        else:
            if not challenge(victim-1, player, 1):
                stealcoins(player, victim-1)
    else:
        if block == 1:
            challengeconfirm = intinputvalidate(f"Player {player + 1}, would you like to challenge player {victim}'s {captain}? (1=yes, 0=no)\n", 0, 1)
            if challengeconfirm:
                if challenge(player, victim-1, 1):
                    stealcoins(player, victim-1)
        elif block == 2:
            challengeconfirm = intinputvalidate(
                f"Player {player + 1}, would you like to challenge player {victim}'s {ambassador}? (1=yes, 0=no)\n", 0, 1)
            if challengeconfirm:
                if challenge(player, victim - 1, 4):
                    stealcoins(player, victim-1)

def assassinact(player):
    victim = intinputvalidate(f"Select a player to assassinate: (1 - {players})\n", 1, players)
    block = intinputvalidate(f"Player {victim}, would you like to block with a {contessa}? (1=yes, 0=no)\n",0, 1)
    if block == 0:
        victimchallengeconfirm = intinputvalidate(f"Player {victim}, would you like to challenge player {player + 1}'s {assassin}? (1=yes, 0=no)\n", 0, 1)
        if not victimchallengeconfirm:
            die(victim-1)
        else:
            if not challenge(victim-1, player, 2):
                die(victim-1)
    else:
        challengeconfirm = intinputvalidate(f"Player {player + 1}, would you like to challenge player {victim}'s {contessa}? (1=yes, 0=no)\n", 0, 1)
        if challengeconfirm:
            if challenge(player, victim - 1, 3):
                die(victim-1)

def exchange(player):
    print(f"{red}ALL PLAYERS EXCEPT PLAYER {player + 1} LOOK AWAY{reset}")
    print("3", end="\r")
    sleep(1)
    print("2", end="\r")
    sleep(1)
    print("1", end="\r")
    sleep(1)
    if len(cards[player]) == 1:
        exchangelist2 = [cards[player][0], deckdraw(), deckdraw()]
        exchangelist = [0, 0, 0]
    elif len(cards[player]) == 2:
        exchangelist2 = [cards[player][0], cards[player][1], deckdraw(), deckdraw()]
        exchangelist = [0, 0, 0, 0]
    for i in range(len(exchangelist)):
        match exchangelist2[i]:
            case 0:
                exchangelist[i] = duke
            case 1:
                exchangelist[i] = captain
            case 2:
                exchangelist[i] = assassin
            case 3:
                exchangelist[i] = contessa
            case 4:
                exchangelist[i] = ambassador
            case _:
                exchangelist[i] = "?"
    if len(exchangelist) == 3:
        print(f"{exchangelist[0]}, {exchangelist[1]}, {exchangelist[2]}", end="\r")
    elif len(exchangelist) == 4:
        print(f"{exchangelist[0]}, {exchangelist[1]}, {exchangelist[2]}, {exchangelist[3]}", end="\r")
    sleep(3)
    print("="*50)

    if len(cards[player]) == 1:
        select1 = intinputvalidate("Pick one card to keep (1 - 3)\n", 1, 3)
        cards[player][0] = exchangelist2.pop(select1-1)
        deckreturn(exchangelist2[0])
        deckreturn(exchangelist2[1])
    elif len(cards[player]) == 2:
        select1 = intinputvalidate("Pick a card to keep (1 - 4)\n", 1, 4)
        select2 = intinputvalidate("Pick a second card to keep (1 - 4)\n", 1, 4)
        cards[player][0] = exchangelist2.pop(select1 - 1)
        cards[player][1] = exchangelist2.pop(select2 - 2)
        deckreturn(exchangelist2[0])
        deckreturn(exchangelist2[1])

def ambassadoract(player):
    print(f"Player {player+1} is claiming to have an {ambassador} and is attempting to exchange their cards.")
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has an {ambassador}? (input challenging player number, 0 if no challenge)\n",0, players)
    if challenger == 0:
        exchange(player)
    else:
        if not challenge(challenger-1, player, 4):
            exchange(player)

def coup(player):
    victim = intinputvalidate(f"Select a player to coup: (1 - {players})\n", 1, players)
    print(f"Player {victim} is being couped.")
    die(victim-1)



# Game Loop

for i in range(players):
    input(f"Player {i+1}, are you ready to see your starting cards?\n")
    selfcardcheck(i)

run = True
while run:
    for i in range(players):
        clearscreen()

        if living[i]:

            print(f"Player {i+1} turn\n")
            sleep(1)

            displayoptions()
            sleep(1)

            while True:
                cmd = intinputvalidate("Choose an action (numbers 1 - 10)\n", 1, 10)
                match cmd:
                    case 1:
                        income(i)
                        break
                    case 2:
                        foreignaid(i)
                        break
                    case 3:
                        dukeact(i)
                        break
                    case 4:
                        captainact(i)
                        break
                    case 5:
                        if coins[i] >= 3:
                            coins[i] -= 3
                            assassinact(i)
                            break
                        else:
                            print("You need at least 3 coins to assassinate")
                    case 6:
                        ambassadoract(i)
                        break
                    case 7:
                        if coins[i] >= 7:
                            coins[i] -= 7
                            coup(i)
                            break
                        else:
                            print("You need at least 7 coins to coup")
                    case 8:
                        coincheck()
                    case 9:
                        cardnumcheck()
                    case 10:
                        selfcardcheck(i)
                    case _:
                        print("how did this happen")

        else:
            print(f"Player {i+1} is dead.")

        sleep(1)

    findwin()