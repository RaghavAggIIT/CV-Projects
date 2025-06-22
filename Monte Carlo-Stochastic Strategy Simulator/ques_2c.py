import random

class Alice:
    def __init__(self):
        self.past_play_styles = [1, 1]
        self.results = [1, 0]
        self.opp_play_styles = [1, 1]
        self.points = 1
        self.wins = 1

    def play_move(self):
        if self.results[-1] == 0:
            return 1
        elif self.results[-1] == 0.5:
            return 0
        else:
            if (len(self.results) * 5 > self.points * 11):
                return 0
            else:
                return 2
        
    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result

class Bob:
    def __init__(self):
        self.past_play_styles = [1, 1]
        self.results = [0, 1]
        self.opp_play_styles = [1, 1]
        self.points = 1

    def play_move(self):
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:
            return 0
        
    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result

def simulate_round(alice, bob, payoff_matrix):
    alice_move = alice.play_move()
    bob_move = bob.play_move()

    p1 = payoff_matrix[alice_move][bob_move][0]
    p2 = payoff_matrix[alice_move][bob_move][1]

    outcome = random.random()

    if outcome < p1:
        result = 1
        alice.wins += 1
    elif outcome < p1 + p2:
        result = 0.5
    else:
        result = 0

    alice.observe_result(alice_move, bob_move, result)
    bob.observe_result(bob_move, alice_move, 1 - result)
    payoff_matrix[0][0]=(alice.points/len(alice.results),0,bob.points/len(bob.results))

def reset_payoff_matrix():
    return [
        [(1 / 2, 0, 1 / 2), (7 / 10, 0, 3 / 10), (5 / 11, 0, 6 / 11)], 
        [(3 / 10, 0, 7 / 10), (1 / 3, 1 / 3, 1 / 3), (3 / 10, 1 / 2, 1 / 5)], 
        [(6 / 11, 0, 5 / 11), (1 / 5, 1 / 2, 3 / 10), (1 / 10, 4 / 5, 1 / 10)]
    ]

def estimate_tau(T):
    exp = 0
    i=0
    c=0
    while i<10**5:
        alice = Alice()
        bob = Bob()
        payoff_matrix = reset_payoff_matrix()
        rounds = 2

        while alice.wins < T:
            simulate_round(alice, bob, payoff_matrix)
            rounds += 1
        i+=rounds
        exp += rounds
        c+=1

    return float(exp / c)

print(estimate_tau(10))

