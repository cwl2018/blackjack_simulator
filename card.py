import random
import math

standardbet = 10
globalcount = 0

def stand(hand,total):
    hand.clear()
    hand.append(total)

def hit(hand, deck):
    hand.append(getcard(deck))

def getcard(deck):
    global globalcount
    card = deck[0]
    del deck[0]

    if card>=2 and card<=6:
        globalcount+=1
    elif card==7 or card==8 or card==9:
        pass
    else:
        globalcount-=1

    return card

def split(deck,hands,hand,index,bets,bet):
    hand2 = []
    hand2.append(hand[0])
    hands[index][1] = getcard(deck)
    hand2.append(getcard(deck))
    hands.insert(index+1,hand2)
    bets.insert(index+1,[standardbet])
    #print("performing split!")
    #print(hands)
    #print(bets)

def action(hand, dealerupcard, deck,bet,index,hands,bets,splitted):
    #print()
    #print("processing hand",index,hand)
    if hand[0] == hand[1] and splitted==0:
        if hand[0]==1 or hand[0]==8:
            split(deck,hands,hand,index,bets,bet)
            action(hands[index],dealerupcard,deck,bet,index,hands,bets,1)
        elif hand[0]==10 or hand[0] == 5:
            hardaction(hand, dealerupcard, deck,bet)
        elif hand[0]==9:
            if dealerupcard == 10 or dealerupcard == 7 or dealerupcard == 1:
                hardaction(hand,dealerupcard,deck,bet)
            else:
                split(deck,hands,hand,index,bets,bet)
                action(hands[index],dealerupcard,deck,bet,index,hands,bets,1)
        elif hand[0]==6:
            if dealerupcard >=2 and dealerupcard < 7:
                split(deck,hands,hand,index,bets,bet)
                action(hands[index],dealerupcard,deck,bet,index,hands,bets,1)
            else:
                hardaction(hand,dealerupcard,deck,bet)
        elif hand[0]==4:
            if dealerupcard ==5 or dealerupcard ==6:
                split(deck,hands,hand,index,bets,bet)
                action(hands[index],dealerupcard,deck,bet,index,hands,bets,1)
            else:
                hardaction(hand,dealerupcard,deck,bet)
        else:
            if dealerupcard >=2 and dealerupcard < 8:
                split(deck,hands,hand,index,bets,bet)
                action(hands[index],dealerupcard,deck,bet,index,hands,bets,1)
            else:
                hardaction(hand,dealerupcard,deck,bet)
    else:
        if 1 in hand:
            softaction(hand, dealerupcard, deck,bet)
        else:
            hardaction(hand, dealerupcard, deck,bet)
    #print("after",hand,hands)
    #print("after",hand,bets)

def softdouble(hand,deck):
    hand.append(getcard(deck))

def softaction(hand, dealerupcard, deck,bet):
    softdoubled = 0
    total = sum(hand)
    while True:
        if total > 11:
            break
        elif total == 11:
            softdoubled = 1
            break
        elif total == 10:                              #A9
            break
        elif total == 9:                               #A8
            if dealerupcard == 6 and len(hand)==2:
                bet[0] *= 2
                softdouble(hand,deck)
                softdoubled = 1
            break
        elif total == 8:                               #A7
            if dealerupcard < 7 and dealerupcard >=2:
                if len(hand)==2:
                    bet[0] *= 2
                    softdouble(hand,deck)
                    softdoubled = 1
                break
            elif dealerupcard == 7 or dealerupcard == 8:
                break
            else:
                hit(hand,deck)
        elif total == 7:                               #A6
            if dealerupcard < 7 and dealerupcard >=3 and len(hand)==2:
                bet[0] *= 2
                softdouble(hand,deck)
                softdoubled = 1
                break
            else:
                hit(hand,deck)
        elif total == 6 or total == 5:                 #A5,A4
            if dealerupcard < 7 and dealerupcard >=4 and len(hand)==2:
                bet[0] *= 2
                softdouble(hand,deck)
                softdoubled = 1
                break
            else:
                hit(hand,deck)
        else:                                         #A3,A2
            if dealerupcard < 7 and dealerupcard >=5 and len(hand)==2:
                bet[0] *= 2
                softdouble(hand,deck)
                softdoubled = 1
                break
            else:
                hit(hand,deck)
        total = sum(hand)
    if softdoubled == 0 and sum(hand) > 11:
        #print(hand,"going to hardaction")
        hardaction(hand,dealerupcard,deck,bet)

def hardaction(hand, dealerupcard, deck,bet):
    total = sum(hand)
    while True:
        if total >= 22:
            break
        elif total < 22 and total >= 17:
            break
        elif total < 17 and total >= 13:
            if dealerupcard < 7 and dealerupcard >= 2:
                break
            else:
                hit(hand, deck)
        elif total == 12:
            if dealerupcard < 7 and dealerupcard >= 4:
                break
            else:
                hit(hand,deck)
        elif total == 11:
            hit(hand, deck)
            if len(hand)==3:
                bet[0] *= 2
                break
        elif total == 10:
            hit(hand, deck)
            if dealerupcard < 10 and dealerupcard >=2 and len(hand)==3:
                bet[0] *= 2
                break
        elif total == 9:
            hit(hand, deck)
            if dealerupcard < 7 and dealerupcard >=3 and len(hand)==3:
                bet[0] *= 2
                break
        else:
            if 1 in hand:
                #print(hand,'going to softaction')
                softaction(hand,dealerupcard,deck,bet)
                break
            else:
                hit(hand, deck)
        total = sum(hand)


def play(no_of_hands,deck):
    roundprofit = 0
    dealer = []
    hands = []
    bets = []
    #print(deck)
    #print()
    # set up cards
    dealer.append(getcard(deck))
    dealer.append(getcard(deck))
    for i in range(no_of_hands):
        hand = []
        hand.append(getcard(deck))
        hand.append(getcard(deck))
        hands.append(hand)
        bets.append([standardbet])
    #print(dealer)
    #print(hands)

    #playeraction
    ind = 0
    while ind < len(hands):
        action(hands[ind], dealer[0], deck, bets[ind],ind,hands,bets,0)
        ind += 1

    #dealeraction
    dealersum = sum(dealer)
    if 1 in dealer:
        dealersum += 10
    while dealersum < 17:
        dealer.append(getcard(deck))
        dealersum = sum(dealer)
        if 1 in dealer and dealersum + 10 <= 21:
            dealersum += 10

    #showdown
    #print()
    #print("dealer's hand",dealer, dealersum)
    #print("player's hand",hands)
    #print("bets",bets)
    dealertotal = dealersum
    if dealertotal > 21:
        for i in range(len(hands)):
            handtotal = sum(hands[i])
            if 1 in hands[i] and handtotal + 10 <= 21:
                handtotal += 10
            if handtotal <= 21:
                if handtotal == 21 and len(hands[i])==2:
                    bets[i][0] *= 1.5
                roundprofit += bets[i][0]
            else:
                roundprofit -= bets[i][0]
        return roundprofit

    if dealertotal == 21 and len(dealer)==2:
        dealertotal = 99

    for i in range(len(hands)):
        handtotal = sum(hands[i])
        if 1 in hands[i] and handtotal + 10 <= 21:
            handtotal += 10
        if handtotal <= 21:
            if handtotal==21 and len(hands[i])==2:
                handtotal=99
                bets[i][0] *= 1.5
            if handtotal > dealertotal:
                roundprofit += bets[i][0]
                #print("hand",i,"profit :",bets[i][0])
            elif (handtotal == dealertotal):
                #print("hand",i,"profit : 0")
                pass
            else:
                roundprofit -= bets[i][0]
                #print("hand",i,"profit :",-bets[i][0])
        else:
            #print("hand",i,"profit :",-bets[i][0])
            roundprofit -= bets[i][0]
    return roundprofit

def newdeck():
    global globalcount
    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]*6
    random.shuffle(deck)
    globalcount = 0
    #print(deck)
    #print()
    return deck

def adjustbet(deck):
    global standardbet
    truecount = math.floor(globalcount*52/len(deck))
    if truecount >= 3:
        standardbet = 200
    elif truecount >= 1 and truecount <3:
        standardbet = 20
    elif truecount <0:
        standardbet = 5
    else:
        standardbet = 10

    #print('truecount',truecount)

def main():
    global standardbet
    rounds = 500000
    totalbet = 0
    profit = 0
    no_of_hands = 1
    max = 0
    min = 0
    deck = newdeck()
    for i in range(rounds):
        if i%50000 == 0:
            print(i,'rounds played, profit:', profit)
        if len(deck) < 160:
            deck = newdeck()
        adjustbet(deck)
        totalbet += (no_of_hands*standardbet)
        #print('round',i,'current card count is',globalcount,'bet is',standardbet)
        roundprofit = play(no_of_hands,deck)
        #print('round',i,'profit:',roundprofit)
        profit += roundprofit
        if max < profit:
            max = profit
        if min > profit:
            min = profit
    print("final profit is ", profit)
    print("max profit is ", max)
    print("min profit is ", min)
    print("percentage is",profit*100/totalbet,'%')


main()
