import random

class Alice:
    def __init__(self):
        self.past_play_styles = [1, 1]
        self.results = [1, 0]
        self.opp_play_styles = [1, 1]
        self.points = 1

    def play_move(self):
        if(29*(len(self.results)-self.points)>15*self.points):
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
        return random.choice([0, 1, 2])

    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result


def simulate_round(alice, bob, payoff_matrix):
    alice_move = alice.play_move()
    bob_move = bob.play_move()
    prob = payoff_matrix[alice_move][bob_move]
    outcome = random.random()

    result = 1 if outcome < prob[0] else 0.5 if outcome < prob[0] + prob[1] else 0
    alice.observe_result(alice_move, bob_move, result)
    bob.observe_result(bob_move, alice_move, 1 - result)

    payoff_matrix[0][0] = (bob.points / (alice.points + bob.points), 0, alice.points / (alice.points + bob.points))


def monte_carlo(num_rounds):
    alice = Alice()
    bob = Bob()
    payoff_matrix = [
        [(1/2, 0, 1/2), (7/10, 0, 3/10), (5/11, 0, 6/11)],
        [(3/10, 0, 7/10), (1/3, 1/3, 1/3), (3/10, 1/2, 1/5)],
        [(6/11, 0, 5/11), (1/5, 1/2, 3/10), (1/10, 4/5, 1/10)]
    ]

    for _ in range(num_rounds):
        simulate_round(alice, bob, payoff_matrix)

    print(f"Alice's points: {alice.points}, Bob's points: {bob.points}")


# Run Monte Carlo simulation with 100,000 rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=10**5)
