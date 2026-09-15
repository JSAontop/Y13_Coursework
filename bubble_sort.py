# cards = [4, 8, 2, 10, 1, 7, 5, 9, 3, 6]

def count_order(cards):
    end = len(cards)-1
    for j in range (end):
        for i in range (end):
            # print("check")
            ordered = True
            if cards[i] > cards[i + 1]:
                temp = cards[i + 1]
                cards[i + 1] = cards[i]
                cards[i] = temp
                if ordered == True:
                    ordered = False
                # print("swap")
            print(cards)
        end -= 1
        print("Pass", j+1)


    return cards

print(count_order(sorted([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])))