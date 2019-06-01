#-*-coding: utf-8-*-
import sys
import time


class Card(object):
    def __init__(self, card, value, color):
        self.card = card
        self.value = value
        self.color = color
        self.ace_value = value


def permutation(src):
    """Permutations of an list.
    """
    if len(src) == 1:
        return [src]
    else:
        header = src[0]
        res = permutation(src[1:])
        order = []
        for part in res:
            for idx in range(len(part) + 1):
                tmp = part[:]
                tmp.insert(idx, header)
                order.append(tmp)
        return order


def factorial(num):
    """Compute N!.
    """
    factor = 1
    if num == 0:
        return factor
    for i in range(1, num + 1):
        factor = factor*i
    return factor


def check(order, n, m):
    """Return the value of this order.
    Params:
        order: one permutation of cards
        n, m: start, stop
    Rets:
        the value based on given rules.
    """
    # rule 1: N-of-a-kind
    for card in order[n:m+1]:
        # if not the same or exit A
        if card.value != order[n].value or card.value == 20:
            break
    else:
        return order[n].value * factorial(m-n+1)
    # rule 2: a valid run
    run_flag = 1
    if m-n+1 < 3:
        run_flag = 0
    elif order[n].value == 20 or order[m].value == 20:
        run_flag = 0
    else:
        ret = 0
        for idx in range(n, m):
            curr_card = order[idx]
            next_card = order[idx+1]
            ret += curr_card.ace_value
            # replace Ace
            if next_card.value == 20:
                next_card.ace_value = curr_card.ace_value + 1
            if curr_card.ace_value+1 != next_card.ace_value or \
                curr_card.color == next_card.color:
                run_flag = 0
                break
    if run_flag:
        ret += next_card.ace_value
        return ret
    # rule 3: single
    ret = 0
    for card in order[n:m+1]:
        ret -= card.value
    return ret


def backtrack(order, back, n, m, res):
    """Recover the divided result.
    """
    split = back[n][m]
    if split == -1:
        tmp = []
        for idx in range(n, m+1):
            tmp.append(order[idx].card)
        res.append(tmp)
        return
    backtrack(order, back, n, split, res)
    backtrack(order, back, split+1, m, res)


def is_exit(result, test_list):
    """Judge if one result has exited.
    """
    name = []
    for item in result:
        item.sort()
        name.append("".join(item))
    name.sort()
    test = "_".join(name)
    if test in test_list:
        return True
    else:
        test_list.append(test)
        return False


def div_conq(order, n, m, dp, back):
    """Recursion divide and conquer process.
    """
    # if (n, m) has been splited or the boarder.
    if dp[n][m] != -10000:
        return dp[n][m]
    # if make a split.
    for i in range(n, m):
        tmp = div_conq(order, n, i, dp, back) + div_conq(order, i+1, m, dp, back)
        if tmp > dp[n][m]:
            dp[n][m] = tmp
            back[n][m] = i
    # if not split
    ret = check(order, n, m)
    if ret > dp[n][m]:
        dp[n][m] = ret
        back[n][m] = -1
    # TODO: bug here
    elif ret == dp[n][m]:
        pass
    return dp[n][m]


if __name__ == '__main__':
    color_map = {'H': 'R', 'D': 'R', 'S': 'B', 'C': 'B'}
    value_map = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5,
                 '6': 6, '7': 7, '8': 8, '9': 9, '0': 10,
                 'J': 11, 'Q': 12, 'K': 13}
    # test examples:
    input_list = ['9D', '2S', '4D', '4H', '6D', 'AH', '2C', 'JH', '3C', '9H']
    # input_list = ['0H', '8S', '6H', 'AC', '0S', 'JS', '8C', '7C', '6D', 'QS']
    # input_list = ['3C', '5H', '9S', 'JS', '4C', '2C', 'AS', 'KC', '6H', 'QC']
    # input_list = ['0D', 'AS', '5C', '8H', 'KS', 'AH', 'QH', 'AC']
    # my examples:
    # input_list = ['2C', '2S', '3C', '4D', '4H', '6D', '9D', '9H', 'AH', 'JH']
    # input_list = ['0D', 'AS', '5C', '8H', 'KS', 'AH']
    # input_list = ['2D', '3S', '4D', '5S', '6D', '7S']     # NOTE: bug here
    # input_list = ['AH', '2S', 'AD', '4S']
    # input_list = ['2C', '2S', '3C', '4D', '4H']
    # input_list = ['2C', '2S', '3C', '4D']
    # input_list = ['2C', 'AH', '4C']
    # input_list = ['2S', '2C', '3H']
    stime = time.time()
    cards_list = []
    for card in input_list:
        value = value_map[card[0]]
        color = color_map[card[1]]
        cards_list.append(Card(card, value, color))

    # permutation
    perm_list = permutation(cards_list)
    print("permutation cost: %.2f" % (time.time() - stime))
    print("length of permutation list: %d" % len(perm_list))

    results_list = []
    test_list = []
    max_value = -10000
    for order in perm_list:
        num = len(order)
        dp = [[-10000]*num for _ in range(num)]
        for i in range(num):
            dp[i][i] = -order[i].value
        back = [[-1]*num for _ in range(num)]
        div_conq(order, 0, num-1, dp, back)
        if max_value < dp[0][num-1]:
            results_list = []
            result = []
            max_value = dp[0][num-1]
            backtrack(order, back, 0, num-1, result)
            if not is_exit(result, test_list):
                results_list.append(result)
        elif max_value == dp[0][num-1]:
            result = []
            backtrack(order, back, 0, num-1, result)
            if not is_exit(result, test_list):
                results_list.append(result)
    print("max value is: %d" % max_value)
    print("split result: %s" % results_list)
    print("all time cost: %.2f" % (time.time() - stime))
    #================ test ===================#
    # order = cards_list
    # num = len(order)
    # dp = [[-10000]*num for _ in range(num)]
    # for i in range(num):
    #     dp[i][i] = -order[i].value
    # back = [[-1]*num for _ in range(num)]
    # div_conq(order, 0, num-1, dp, back)
    # max_value = dp[0][num-1]
    # result = []
    # backtrack(order, back, 0, num-1, result)
    # print("max value is: %d" % max_value)
    # print("split result: %s" % result)
