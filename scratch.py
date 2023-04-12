import itertools
import random

# Generate all combinations of numbers from 2 to 7
num_accts = 4
acct_pct = [0.4, 0.3, 0.2, 0.1]
numbers = [2, 3, 4, 5, 6, 7]
num_portfolios = len(numbers)

combinations = list(itertools.product(numbers, repeat = num_accts))

# Map each number to a list of 5 portfolio weights of random value between 0 and 100
portfolio_weights = {}
for num in numbers:
    rand_list = [random.randint(0, 100) for _ in range(22)]
    weights = [i / sum(rand_list) for i in rand_list]
    portfolio_weights[num] = weights

# Map each asset class to a return of a random number between 1 and 10
asset_returns = {}
for num in numbers:
    rand_list = [random.randint(1, 23) for _ in range(22)]
    returns = [i / 100 for i in rand_list]
    asset_returns[num] = returns

# Calculate the overall weighted return for each combination of numbers
for combination in combinations:
    weighted_return = 0
    for i, num in enumerate(combination):
        weights = portfolio_weights[num]
        returns = asset_returns[num]
        weighted_return += acct_pct[i] * sum([w * r for w, r in zip(weights, returns)])
        #for i, weight in enumerate(weights):
        #    asset_return = asset_returns[i]
        #    weighted_return += weight / 100 * asset_return
    print(f"Combination {combination}: Overall Weighted Return: {weighted_return:.2f}")
