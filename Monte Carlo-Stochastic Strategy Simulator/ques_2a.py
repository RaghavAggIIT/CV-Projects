import random

class Alice:
    def __init__(self):
        self.past_play_styles = [1, 1]
        self.results = [1, 0]
        self.opp_play_styles = [1, 1]
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round.
         
        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        """
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
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
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
        """
        Decide Bob's play style for the current round.

        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        """
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:  
            return 0
        
    def observe_result(self, own_style, opp_style, result):
        """
        Update Bob's knowledge after each round based on the observed results.
        
        Returns:
            None
        """ 
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result

def simulate_round(alice, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    alice_move = alice.play_move()
    bob_move = bob.play_move()
    
    # Get the probabilities from the payoff matrix for the respective moves
    p1 = payoff_matrix[alice_move][bob_move][0]  # Probability of Alice winning
    p2 = payoff_matrix[alice_move][bob_move][1]  # Probability of a draw


    # Randomize a number between 0 and 1 to determine the outcome
    outcome = random.random()

    # Determine the result based on the outcome value
    if outcome < p1:
        result = 1  # Alice wins
    elif outcome < p1 + p2:
        result = 0.5  # Draw
    else:
        result = 0  # Bob wins
    

    # Update both players with the result of the round
    alice.observe_result(alice_move, bob_move, result)
    bob.observe_result(bob_move, alice_move, 1 - result)
    payoff_matrix[0][0]=(alice.points/len(alice.results),0,bob.points/len(bob.results))
def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    # Payoff matrix with probabilities from the image
    payoff_matrix = [
        # Alice: Attack
        [(1 / 2, 0, 1 / 2), (7 / 10, 0, 3 / 10), (5 / 11, 0, 6 / 11)], 
        # Alice: Balanced
        [(3 / 10, 0, 7 / 10), (1 / 3, 1 / 3, 1 / 3), (3 / 10, 1 / 2, 1 / 5)], 
        # Alice: Defence
        [(6 / 11, 0, 5 / 11), (1 / 5, 1 / 2, 3 / 10), (1 / 10, 4 / 5, 1 / 10)]
    ]
    
    alice = Alice()
    bob = Bob()
    
    for _ in range(num_rounds):
        simulate_round(alice, bob, payoff_matrix)
    
    print(f"Alice's points: {alice.points}")
    print(f"Bob's points: {bob.points}")

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=10**5)

