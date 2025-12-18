import random as r
import os
from time import sleep

# Duke 0, Captain 1, Assassin 2, Contessa 3, Ambassador 4, Inquisitor 5, (experimental) Diplomat 6

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
        except Exception:
            print("Invalid input")


players = intinputvalidate("How many players?\n", 2, 100)
inquisitoroption = intinputvalidate("Do you want to play with Inquisitors instead of Ambassadors? (1=yes, 0=no)\n", 0, 1)
if inquisitoroption == 1:
    inquisitoroption = True
else:
    inquisitoroption = False
teamsoption = intinputvalidate("Do you want to play with teams? (1=yes, 0=no)\n", 0, 1)
if teamsoption == 1:
    teamsoption = True
else:
    teamsoption = False
experimentaloption = intinputvalidate("Do you want to play with experimental options? (1=yes, 0=no)\n", 0, 1)
if experimentaloption == 1:
    experimentaloption = True
else:
    experimentaloption = False

optionslist = ["income", "foreign aid", "duke", "captain", "assassin"] # Contessa not in list because not action
if not inquisitoroption:
    optionslist.append("ambassador")
else:
    optionslist.append("inquisitorexchange")
    optionslist.append("inquisitorexamine")
if teamsoption and experimentaloption:
    optionslist.append("diplomat")
optionslist.append("coup")
if teamsoption:
    optionslist.append("switchownteam")
    optionslist.append("switchotherteam")
    if experimentaloption:
        optionslist.append("blockownteam")
    optionslist.append("embezzle")
optionslist.append("checkcoins")
optionslist.append("checkcardnumbers")
optionslist.append("checkowncards")
if teamsoption:
    optionslist.append("checkteams")
    optionslist.append("checktreasury")

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear') # Wipe terminal

# Setup

# Deck

deck = []
if teamsoption and experimentaloption:
    cardtypes = 6
else:
    cardtypes = 5
totaldecknum = cardtypes*3
totaldecknum *= (players-1 // 6) + 1

for i in range(totaldecknum // 5):
    deck.append(0)
    deck.append(1)
    deck.append(2)
    deck.append(3)
    if not inquisitoroption:
        deck.append(4)
    else:
        deck.append(5)
    if teamsoption and experimentaloption:
        deck.append(6)

r.shuffle(deck)

def deckdraw():
    return deck.pop(0)

def deckreturn(card):
    deck.append(card)


# General

cards = []
coins = []
living = []
droppedcards = []
teams = []
teamblock = []
treasury = 0
freeforall = False

for i in range(players):
    cards.append([deckdraw(), deckdraw()])
    coins.append(2)
    living.append(True)
    droppedcards.append([])
    if i % 2 == 0:
        teams.append(True) # Reformist
    else:
        teams.append(False) # Loyalist
    teamblock.append(False)

# Variables
reset = "\033[0m"
dim = "\033[38;5;240m"
lessdim = "\033[38;5;245m"
red = "\033[31m"
dukecolour = "\033[35m"
captaincolour = "\033[36m"
assassincolour = "\033[1;90m"
contessacolour = red
ambassadorcolour = "\033[32m"
inquisitorcolour = "\033[33m"
diplomatcolour = "\033[95m"
reformistcolour = "\033[36m"
loyalistcolour = red

duke = f"{dukecolour}Duke{reset}"
captain = f"{captaincolour}Captain{reset}"
assassin = f"{assassincolour}Assassin{reset}"
contessa = f"{contessacolour}Contessa{reset}"
ambassador = f"{ambassadorcolour}Ambassador{reset}"
inquisitor = f"{inquisitorcolour}Inquisitor{reset}"
diplomat = f"{diplomatcolour}Diplomat{reset}"
reformist = f"{reformistcolour}Reformist{reset}"
loyalist = f"{loyalistcolour}Loyalist{reset}"

# Subroutines

def displayoptions():
    counter = 0
    print("Game actions (will end turn):")

    for i in range(len(optionslist)):
        counter += 1

        if optionslist[i] == "income":
            print(f"{counter}: Income: Take 1 coin {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "foreign aid":
            print(f"{counter}: Foreign Aid: Take 2 coins {dim}(Can be blocked by Duke){reset}")
        elif optionslist[i] == "duke":
            print(f"{counter}: {duke}: Take 3 coins {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "captain":
            if not inquisitoroption:
                print(f"{counter}: {captain}: Steal 2 coins from another player {dim}(Can be blocked by Captain or Ambassador){reset}")
            else:
                if not experimentaloption:
                    print(f"{counter}: {captain}: Steal 2 coins from another player {dim}(Can be blocked by Captain or Inquisitor){reset}")
                else:
                    print(f"{counter}: {captain}: Steal 2 coins from another player {dim}(Can be blocked by Captain){reset}")
        elif optionslist[i] == "assassin":
            print(f"{counter}: {assassin}: Pay 3 coins, pick a player to lose a card {dim}(Can be blocked by Contessa){reset}")
            print(f"{contessa}: Blocks assassination {dim}(Cannot be blocked){reset}") # Contessa not action so not in options list
        elif optionslist[i] == "ambassador":
            print(f"{counter}: {ambassador}: Exchange 2 cards with the deck {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "inquisitorexchange":
            print(f"{counter}: {inquisitor}: Exchange 1 card with the deck {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "inquisitorexamine":
            print(f"{counter}: {inquisitor}: Examine another player's card and can force them to switch it {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "diplomat":
            print(f"{counter}: {diplomat}: Pay 1 coin to switch 2 other players' team {dim}(Can be blocked by Diplomat){reset}")
        elif optionslist[i] == "coup":
            print(f"{counter}: Coup: Pay 7 coins, pick a player to lose a card {dim}(Cannot be blocked, must coup if 10+ coins){reset}")
        elif optionslist[i] == "switchownteam":
            print(f"{counter}: Switch own team: Pay one coin into the treasury to switch your own team {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "switchotherteam":
            if not experimentaloption:
                print(f"{counter}: Switch other player's team: Pay two coins into the treasury to switch another player's team {dim}(Cannot be blocked){reset}")
            else:
                print(f"{counter}: Switch other player's team: Pay two coins into the treasury to switch another player's team {dim}(Can be blocked by Diplomat){reset}")
        elif optionslist[i] == "blockownteam":
            print(f"{counter}: Block own team: Pay one coin into the treasury to prevent your team from being switched until your next turn {dim}(Cannot be blocked){reset}")
        elif optionslist[i] == "embezzle":
            print(f"{counter}: Embezzle the treasury: Take all money currently in the treasury {dim}(Must claim to NOT have a duke){reset}")
        elif optionslist[i] == "checkcoins":
            print("\nCheck actions (will not end turn):")
            print(f"{counter}: {lessdim}Check coin counts of all players{reset}")
        elif optionslist[i] == "checkcardnumbers":
            print(f"{counter}: {lessdim}Check card numbers of all players{reset}")
        elif optionslist[i] == "checkowncards":
            print(f"{counter}: {lessdim}Check own cards (get all other players to look away for 3 seconds){reset}")
        elif optionslist[i] == "checkteams":
            print(f"{counter}: {lessdim}Check the team of each player{reset}")
        elif optionslist[i] == "checktreasury":
            print(f"{counter}: {lessdim}Check how many coins are in the treasury{reset}")
    print()

def visualcard(card):
    match card:
        case 0:
            return duke
        case 1:
            return captain
        case 2:
            return assassin
        case 3:
            return contessa
        case 4:
            return ambassador
        case 5:
            return inquisitor
        case 6:
            return diplomat
        case _:
            return "?"

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
        if living[i]:
            print(f"Player {i+1}: {coins[i]} coins")
        else:
            print(f"{dim}Player {i + 1}: {coins[i]} coins{reset}")

def cardnumcheck():
    for i in range(players):
        if living[i]:
            out = f"Player {i+1}: {len(cards[i])} cards"
        else:
            out = f"{dim}Player {i + 1}: {len(cards[i])} cards"
        if len(droppedcards[i]) != 0:
            out += f", dropped {visualcard(droppedcards[i][0])}"
            if len(droppedcards[i]) == 2:
                out += f"{dim} and {visualcard(droppedcards[i][1])}"
        print(out)

def carddisplaywarning(player):
    print(f"{red}ALL PLAYERS EXCEPT PLAYER {player + 1} LOOK AWAY{reset}")
    print("3", end="\r")
    sleep(1)
    print("2", end="\r")
    sleep(1)
    print("1", end="\r")
    sleep(1)

def selfcardcheck(player):
    carddisplaywarning(player)
    tempcardlist = ['', '']
    for i in range(len(cards[player])):
        tempcardlist[i] = visualcard(cards[player][i])
    print(f"{tempcardlist[0]}, {tempcardlist[1]}", end="\r")
    sleep(2)
    print("=" * 50)

def teamscheck():
    for i in range(players):
        if teams[i]:
            print(f"Player {i + 1}: {reformist}")
        else:
            print(f"Player {i + 1}: {loyalist}")

def treasurycheck():
    print(f"Treasury: {treasury} coins")

def updatefreeforall():
    flag = teams[0]
    for i in range(1, len(teams)):
        if teams[i] != flag:
            return False
    print("As everyone is on the same team, it is now a free for all")
    return True

def die(player):
    print(f"Player {player+1} is losing a card")
    if len(cards[player]) == 2:
        seecards = intinputvalidate("Would you like to see your cards? (1=yes, 0=no)\n", 0, 1)
        if seecards:
            selfcardcheck(player)
        losecard = intinputvalidate("Which card would you like to lose? (1 or 2)\n", 1, 2)
        if losecard == 1:
            droppedcards[player].append(cards[player][0])
            cards[player] = [cards[player][1]]
        elif losecard == 2:
            droppedcards[player].append(cards[player][1])
            cards[player] = [cards[player][0]]
    else:
        print(f"Player {player+1} lost their final card and is now out.")
        droppedcards[player].append(cards[player][0])
        cards[player] = []
        living[player] = False
    findwin()


def challenge(accuser, challenged, card, invert):
    flag1 = False
    flag2 = True
    for i in range(len(cards[challenged])):
        if cards[challenged][i] == card:
            flag1 = True
            flag2 = False
    if flag1 and not invert:
        print("Challenge failed.")
        die(accuser)
        print(f"Player {challenged+1} must now replace their card.")
        flag = False
        for i in range(len(cards[challenged])):
            if cards[challenged][i] == card:
                cards[challenged][i] = deckdraw()
                deckreturn(card)
                flag = True
            if flag:
                continue
        return False
    elif flag2 and invert:
        print("Challenge failed.")
        die(accuser)
        print(f"Player {challenged + 1} must now replace all of their cards.")
        for i in range(len(cards[challenged])):
            deckreturn(cards[challenged][i])
            cards[challenged][i] = deckdraw()
        return False
    else:
        print("Challenge successful!")
        die(challenged)
        return True

def teamsvictimcheck(prompt, player):
    while True:
        victim = intinputvalidate(prompt, 1, players)
        if teams[victim - 1] == teams[player] and not freeforall:
            print(f"You cannot select player {victim} as they are on your team")
        else:
            return victim

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
            if challenge(player, block-1, 0, False):
                coins[player] += 2
                print(f"Player {player + 1} took 2 coins.")

def dukeact(player):
    print(f"Player {player + 1} is taking 3 coins with their {duke}.")
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has a {duke}? (input challenging player number, 0 if no challenge)\n", 0, players)
    if challenger == 0:
        coins[player] += 3
        print(f"Player {player + 1} took 3 coins.")
    else:
        if not challenge(challenger-1, player, 0, False):
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
    if not teamsoption:
        victim = intinputvalidate(f"Select a player to steal 2 coins from: (1 - {players})\n", 1, players)
    else:
        victim = teamsvictimcheck(f"Select a player to steal 2 coins from: (1 - {players})\n", player)
    if not inquisitoroption:
        block = intinputvalidate(f"Player {victim}, would you like to block with a {captain} or an {ambassador}? (1=Captain, 2=Ambassador, 0=No block)\n", 0, 2)
    else:
        if not experimentaloption:
            block = intinputvalidate(f"Player {victim}, would you like to block with a {captain} or an {inquisitor}? (1=Captain, 2=Inquisitor, 0=No block)\n",0, 2)
        else:
            block = intinputvalidate(f"Player {victim}, would you like to block with a {captain}? (1=yes, 0=no)\n",0, 1)
    if block == 0:
        challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has an {captain}? (input challenging player number, 0 if no challenge)\n",0, players)
        if challenger == 0:
            stealcoins(player, victim-1)
        else:
            if not challenge(challenger-1, player, 1, False):
                stealcoins(player, victim-1)
    else:
        if block == 1:
            challenger = intinputvalidate(f"Would anyone like to challenge that player {victim} has an {captain}? (input challenging player number, 0 if no challenge)\n",0, players)
            if challenger != 0:
                if challenge(player, challenger-1, 1, False):
                    stealcoins(player, victim-1)
        elif block == 2:
            if not inquisitoroption:
                challenger = intinputvalidate(f"Would anyone like to challenge that player {victim} has an {ambassador}? (input challenging player number, 0 if no challenge)\n",0, players)
                if challenger != 0:
                    if challenge(player, challenger - 1, 4, False):
                        stealcoins(player, victim - 1)
            else:
                challenger = intinputvalidate(f"Would anyone like to challenge that player {victim} has an {inquisitor}? (input challenging player number, 0 if no challenge)\n",0, players)
                if challenger != 0:
                    if challenge(player, challenger - 1, 5, False):
                        stealcoins(player, victim - 1)

def assassinact(player):
    if not teamsoption:
        victim = intinputvalidate(f"Select a player to assassinate: (1 - {players})\n", 1, players)
    else:
        victim = teamsvictimcheck(f"Select a player to assassinate: (1 - {players})\n", player)
    block = intinputvalidate(f"Player {victim}, would you like to block with a {contessa}? (1=yes, 0=no)\n",0, 1)
    if block == 0:
        challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has an {assassin}? (input challenging player number, 0 if no challenge)\n",0, players)
        if challenger == 0:
            die(victim-1)
        else:
            if not challenge(challenger-1, player, 2, False):
                die(challenger-1)
    else:
        challenger = intinputvalidate(f"Would anyone like to challenge that player {victim} has a {contessa}? (input challenging player number, 0 if no challenge)\n",0, players)
        if challenger != 0:
            if challenge(challenger - 1, victim - 1, 3, False):
                die(victim-1)

def ambassadorexchange(player):
    carddisplaywarning(player)
    if len(cards[player]) == 1:
        exchangelist = [cards[player][0], deckdraw(), deckdraw()]
        exchangelistvisual = [0, 0, 0]
    elif len(cards[player]) == 2:
        exchangelist = [cards[player][0], cards[player][1], deckdraw(), deckdraw()]
        exchangelistvisual = [0, 0, 0, 0]
    for i in range(len(exchangelistvisual)):
        exchangelistvisual[i] = visualcard(exchangelist[i])
    if len(exchangelistvisual) == 3:
        print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}", end="\r")
    elif len(exchangelistvisual) == 4:
        print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}, {exchangelistvisual[3]}", end="\r")
    sleep(3)
    print("="*50)

    if len(cards[player]) == 1:
        while True:
            select1 = intinputvalidate("Pick one card to keep (1 - 3), 0 to replay cards\n", 0, 3)
            if select1 == 0:
                carddisplaywarning(player)
                print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}", end="\r")
                sleep(3)
            else:
                break
        cards[player][0] = exchangelist.pop(select1-1)
        deckreturn(exchangelist[0])
        deckreturn(exchangelist[1])
    elif len(cards[player]) == 2:
        while True:
            select1 = intinputvalidate("Pick a card to keep (1 - 4), 0 to replay cards\n", 0, 4)
            if select1 == 0:
                carddisplaywarning(player)
                print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}, {exchangelistvisual[3]}", end="\r")
                sleep(3)
            else:
                break
        cards[player][0] = exchangelist.pop(select1 - 1)
        while True:
            select2 = intinputvalidate("Pick a second card to keep (1 - 4), 0 to replay cards\n", 0, 4)
            if select2 == 0:
                carddisplaywarning(player)
                print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}, {exchangelistvisual[3]}", end="\r")
                sleep(3)
            else:
                break
        cards[player][1] = exchangelist.pop(select2 - 2)
        deckreturn(exchangelist[0])
        deckreturn(exchangelist[1])

def ambassadoract(player):
    print(f"Player {player+1} is claiming to have an {ambassador} and is attempting to exchange their cards.")
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has an {ambassador}? (input challenging player number, 0 if no challenge)\n",0, players)
    if challenger == 0:
        ambassadorexchange(player, 2)
    else:
        if not challenge(challenger-1, player, 4, False):
            ambassadorexchange(player, 2)

def inquisitorexchange(player):
    carddisplaywarning(player)
    if len(cards[player]) == 1:
        exchangelist = [cards[player][0], deckdraw()]
        exchangelistvisual = [0, 0]
    elif len(cards[player]) == 2:
        exchangelist = [cards[player][0], cards[player][1], deckdraw()]
        exchangelistvisual = [0, 0, 0]
    for i in range(len(exchangelistvisual)):
        exchangelistvisual[i] = visualcard(exchangelist[i])
    if len(exchangelistvisual) == 2:
        print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}", end="\r")
    elif len(exchangelistvisual) == 3:
        print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}",end="\r")
    sleep(3)
    print("=" * 50)

    if len(cards[player]) == 1:
        while True:
            select1 = intinputvalidate("Pick one card to keep (1 - 2), 0 to replay cards\n", 0, 2)
            if select1 == 0:
                carddisplaywarning(player)
                print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}", end="\r")
                sleep(3)
            else:
                break
        cards[player][0] = exchangelist.pop(select1 - 1)
        deckreturn(exchangelist[0])
    elif len(cards[player]) == 2:
        while True:
            select1 = intinputvalidate("Pick a card to keep (1 - 3), 0 to replay cards\n", 0, 3)
            if select1 == 0:
                carddisplaywarning(player)
                print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}",end="\r")
                sleep(3)
            else:
                break
        cards[player][0] = exchangelist.pop(select1 - 1)
        while True:
            select2 = intinputvalidate("Pick a second card to keep (1 - 3), 0 to replay cards\n", 0, 3)
            if select2 == 0:
                carddisplaywarning(player)
                print(f"{exchangelistvisual[0]}, {exchangelistvisual[1]}, {exchangelistvisual[2]}",end="\r")
                sleep(3)
            else:
                break
        cards[player][1] = exchangelist.pop(select2 - 2)
        deckreturn(exchangelist[0])

def inquisitorexchangeact(player):
    print(f"Player {player + 1} is claiming to have an {inquisitor} and is attempting to exchange their cards.")
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has an {inquisitor}? (input challenging player number, 0 if no challenge)\n",0, players)
    if challenger == 0:
        inquisitorexchange(player)
    else:
        if not challenge(challenger - 1, player, 5, False):
            inquisitorexchange(player)

def examine(player, victim):
    print(f"Player {victim+1} must let player {player+1} see a card")
    if len(cards[player]) == 2:
        seecards = intinputvalidate(f"Player {victim+1}, would you like to see your cards? (1=yes, 0=no)\n", 0, 1)
        if seecards:
            selfcardcheck(victim)
        givecardid = intinputvalidate(f"Which card would you like to give to player {player+1}? (1 or 2)\n", 1, 2)
        givecardid -= 1
    else:
        print(f"Player {victim+1} only has one card and must let player {player+1} see it")
        givecardid = 0
    givecard = cards[victim][givecardid]
    print(f"{red}ALL PLAYERS EXCEPT PLAYER {player+1} AND PLAYER {victim+1} LOOK AWAY")
    print("3", end="\r")
    sleep(1)
    print("2", end="\r")
    sleep(1)
    print("1", end="\r")
    sleep(1)
    print(f"{visualcard(givecard)}", end="\r")
    sleep(2)
    print("=" * 50)

    forceswitch = intinputvalidate(f"Player {player+1}, would you like to force player {victim+1} to switch their card? (1=yes, 0=no)\n", 0, 1)
    if forceswitch == 1:
        print(f"Player {victim+1} has to switch their card")
        deckreturn(cards[victim][givecardid])
        cards[victim][givecardid] = deckdraw()
    else:
        print(f"Player {victim + 1} has to keep their card")


def inquisitorexamineact(player):
    print(f"Player {player + 1} is claiming to have an {inquisitor} and is attempting to examine another player's card.")
    if not teamsoption:
        victim = intinputvalidate(f"Select a player to examine: (1 - {players})\n", 1, players)
    else:
        victim = teamsvictimcheck(f"Select a player to examine: (1 - {players})\n", player)
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} has an {inquisitor}? (input challenging player number, 0 if no challenge)\n",0, players)
    if challenger == 0:
        examine(player, victim-1)
    else:
        if not challenge(challenger-1, player, 5, False):
            examine(player, victim - 1)

def diplomatact(player):
    livingplayers = 0
    for i in range(len(living)):
        if living[i]:
            livingplayers += 1
    if livingplayers > 2:
        print("You will be able to select 2 players and switch their teams")
        switchotherteam()
        if living[player]: # Only one switch will happen if player dies to a challenge before the second
            switchotherteam()
    else:
        print(f"As there are only {livingplayers} living players, you can only switch one player's team")
        switchotherteam()

def switchteam(player):
    if not teamblock[player]:
        teams[player] = not teams[player] # Swaps the team of the player
        if teams[player]:
            print(f"Player {player + 1} is now a {reformist}")
        else:
            print(f"Player {player + 1} is now a {loyalist}")
        return True
    else:
        print(f"Player {player + 1}'s team can't be switched until their next turn")
        return False

def switchotherteam():
    flag = True
    blocked = False
    while flag:
        victim = intinputvalidate(f"Select a player to switch their team: (1 - {players})\n", 1, players)
        if experimentaloption:
            block = intinputvalidate(f"Player {victim}, would you like to block with a {diplomat}? (1=yes, 0=no)\n", 0, 1)
            if block:
                challenger = intinputvalidate(f"Would anyone like to challenge that player {victim} has a {diplomat}? (input challenging player number, 0 if no challenge)\n",0, players)
                if challenger != 0:
                    if not challenge(challenger - 1, victim - 1, 6, False):
                        blocked = True
                        flag = False
                else:
                    blocked = True
                    flag = False
        if not blocked:
            flag = not switchteam(victim-1)

def blockteam(player):
    teamblock[player] = True
    print(f"Player {player + 1}'s team can't be switched until their next turn")

def embezzle(player):
    print(f"Player {player + 1} is attempting to embezzle the treasury and is claiming to NOT have a {duke}")
    challenger = intinputvalidate(f"Would anyone like to challenge that player {player + 1} does NOT has a {duke}? (input challenging player number, 0 if no challenge)\n",0, players)
    if challenger == 0:
        print(f"Player {player + 1} has taken all {treasury} coins from the treasury.")
        coins[player] += treasury
        return True
    else:
        if not challenge(challenger-1, player, 0, True):
            print(f"Player {player + 1} has taken all {treasury} coins from the treasury.")
            coins[player] += treasury
            return True
        else:
            return False

def coup(player):
    victim = intinputvalidate(f"Select a player to coup: (1 - {players})\n", 1, players)
    print(f"Player {victim} is being couped.")
    die(victim-1)



# Game Loop

for i in range(players):
    introcmd = input(f"Player {i+1}, are you ready to see your starting cards?\n")
    if introcmd != "skip" and introcmd != "`":
        selfcardcheck(i)

run = True
while run:
    for i in range(players):
        clearscreen()

        if living[i]:

            if not teamsoption:
                print(f"Player {i+1} turn\n")
            else:
                if teams[i]:
                    print(f"{reformistcolour}Player {i + 1} turn{reset}\n")
                else:
                    print(f"{loyalistcolour}Player {i + 1} turn{reset}\n")

                freeforall = updatefreeforall()

            displayoptions()

            if teamblock[i]:
                teamblock[i] = False
                print(f"Player {i + 1}'s team can now be switched again.")
                print()

            while True:
                if coins[i] >= 10:
                    print(f"As you have {coins[i]} coins, you have to coup.")
                    coup(i)
                else:
                    cmd = intinputvalidate(f"Choose an action (numbers 1 - {len(optionslist)})\n", 1, len(optionslist))
                    cmd -= 1
                    if optionslist[cmd] == "income":
                        income(i)
                        break
                    elif optionslist[cmd] == "foreign aid":
                        foreignaid(i)
                        break
                    elif optionslist[cmd] == "duke":
                        dukeact(i)
                        break
                    elif optionslist[cmd] == "captain":
                        captainact(i)
                        break
                    elif optionslist[cmd] == "assassin":
                        if coins[i] >= 3:
                            coins[i] -= 3
                            assassinact(i)
                            break
                        else:
                            print("You need at least 3 coins to assassinate")
                    elif optionslist[cmd] == "ambassador":
                        ambassadoract(i)
                        break
                    elif optionslist[cmd] == "inquisitorexchange":
                        inquisitorexchangeact(i)
                        break
                    elif optionslist[cmd] == "inquisitorexamine":
                        inquisitorexamineact(i)
                        break
                    elif optionslist[cmd] == "diplomat":
                        diplomatact(i)
                        freeforall = updatefreeforall()
                        break
                    elif optionslist[cmd] == "coup":
                        if coins[i] >= 7:
                            coins[i] -= 7
                            coup(i)
                            break
                        else:
                            print("You need at least 7 coins to coup")
                    elif optionslist[cmd] == "switchownteam":
                        if coins[i] >= 1:
                            coins[i] -= 1
                            treasury += 1
                            switchteam(i)
                            freeforall = updatefreeforall()
                            break
                        else:
                            print("You need at least 1 coin to switch your team")
                    elif optionslist[cmd] == "switchotherteam":
                        if coins[i] >= 2:
                            coins[i] -= 2
                            treasury += 2
                            switchotherteam()
                            freeforall = updatefreeforall()
                            break
                        else:
                            print("You need at least 2 coins to switch another player's team")
                    elif optionslist[cmd] == "blockownteam":
                        if coins[i] >= 1:
                            coins[i] -= 1
                            treasury += 1
                            blockteam(i)
                            break
                        else:
                            print("You need at least 1 coin to block your team from being switched")
                    elif optionslist[cmd] == "embezzle":
                        if treasury > 0:
                            if embezzle(i):
                                treasury = 0
                            break
                        else:
                            print("There must be at least 1 coin in the treasury to embezzle")
                    elif optionslist[cmd] == "checkcoins":
                        coincheck()
                    elif optionslist[cmd] == "checkcardnumbers":
                        cardnumcheck()
                    elif optionslist[cmd] == "checkowncards":
                        selfcardcheck(i)
                    elif optionslist[cmd] == "checkteams":
                        teamscheck()
                    elif optionslist[cmd] == "checktreasury":
                        treasurycheck()

        else:
            print(f"Player {i+1} is dead.")

        sleep(2)

    findwin()