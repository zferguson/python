import itertools
import random

# Generate all combinations of numbers from 2 to 7
numbers = [2, 3, 4, 5, 6, 7]
combinations = list(itertools.combinations(numbers, 3))

# Map each number to a list of 5 portfolio weights of random value between 0 and 100
portfolio_weights = {}
for num in numbers:
    weights = [random.randint(0, 100) for _ in range(5)]
    portfolio_weights[num] = weights

# Map each asset class to a return of a random number between 1 and 10
asset_returns = {i: random.randint(1, 10) for i in range(5)}

# Calculate the overall weighted return for each combination of numbers
for combination in combinations:
    weighted_return = 0
    for num in combination:
        weights = portfolio_weights[num]
        for i, weight in enumerate(weights):
            asset_return = asset_returns[i]
            weighted_return += weight / 100 * asset_return
    print(f"Combination {combination}: Overall Weighted Return: {weighted_return:.2f}")
