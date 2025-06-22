"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
M = 1000000007

def mod_add(a, b):
    a = (a % M + M) % M
    b = (b % M + M) % M
    return (a + b) % M

def mod_multiply(a, b):
    a = (a % M + M) % M
    b = (b % M + M) % M
    return (a * b) % M

def mod_divide(a, b):
    a = (a % M + M) % M
    b = (b % M + M) % M
    return mod_multiply(a, pow(b, M - 2, M))

def calc_prob(alice_wins, bob_wins):
    """
    Returns:
        The probability of Alice winning alice_wins times and Bob winning bob_wins times will be of the form p/q,
        where p and q are positive integers.
        The result will be p.q^(-1) mod 1000000007.
    """
    dp = [[0] * (bob_wins + 1) for _ in range(alice_wins + 1)]
    dp[1][1] = mod_divide(1, 1)

    for a in range(1, alice_wins + 1):
        for b in range(1, bob_wins + 1):
            if a == 1 and b == 1:
                continue
            total_games = a + b - 1
            
            prob_from_alice_win = mod_multiply(dp[a - 1][b], mod_divide(b, total_games)) if a > 1 else 0
            prob_from_bob_win = mod_multiply(dp[a][b - 1], mod_divide(a, total_games)) if b > 1 else 0
            
            dp[a][b] = mod_add(prob_from_alice_win, prob_from_bob_win)
    
    return dp[alice_wins][bob_wins]

# Problem 1b (Expectation)      
def calc_expectation(t):
    """
    Returns:
        The expected value of sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.
    """

    dp = [[0] * (t + 1) for _ in range(t + 1)]
    dp[1][1] = mod_divide(1, 1)

    for a in range(1, t + 1):
        for b in range(1, t + 1):
            if a == 1 and b == 1:
                continue
            total_games = a + b - 1

            prob_from_alice_win = mod_multiply(dp[a - 1][b], mod_divide(b, total_games)) if a > 1 else 0
            prob_from_bob_win = mod_multiply(dp[a][b - 1], mod_divide(a, total_games)) if b > 1 else 0

            dp[a][b] = mod_add(prob_from_alice_win, prob_from_bob_win)

    exp = 0
    for a in range(1, t + 1):
        for b in range(1, t + 1):
            i = a - b
            if a+b==t:
                exp = mod_add(exp, mod_multiply(i, dp[a][b])) 
    return exp

# Problem 1b (Variance)
def calc_variance(t):
    """
    Returns:
        The variance of sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    dp = [[0] * (t + 1) for _ in range(t + 1)]
    dp[1][1] = mod_divide(1, 1)

    for a in range(1, t + 1):
        for b in range(1, t + 1):
            if a == 1 and b == 1:
                continue
            total_games = a + b - 1

            prob_from_alice_win = mod_multiply(dp[a - 1][b], mod_divide(b, total_games)) if a > 1 else 0
            prob_from_bob_win = mod_multiply(dp[a][b - 1], mod_divide(a, total_games)) if b > 1 else 0

            dp[a][b] = mod_add(prob_from_alice_win, prob_from_bob_win)

    eX2= 0
    for a in range(1, t + 1):
        for b in range(1, t + 1):
            i = a - b
            if a+b==t:
                eX2 = mod_add(eX2, mod_multiply(i**2, dp[a][b])) 
    return eX2- calc_expectation(t)
print(calc_variance(38))
