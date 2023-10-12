import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Given returns and standard deviations for each asset class.
ASSET_CLASSES = {
    'Asset 1': {'return': 0.05, 'sd': 0.1},
    # ... similarly for Asset 2 through Asset 10
}

# Sample correlation matrix for 10 assets. Replace with your correlation matrix.
CORRELATION_MATRIX = np.array([
    # Sample 10x10 matrix filled with ones (perfect correlation)
    [1] * 10 for _ in range(10)
])

CHOLESKY_FACTOR = np.linalg.cholesky(CORRELATION_MATRIX)

def run_simulation(initial_investment, years, runs, weights, rebalance=False):
    """Run the Monte Carlo simulation for the given portfolio with an optional rebalancing."""
    portfolio_returns = []
    for _ in range(runs):
        annual_returns = []
        end_of_year_portfolio_value = initial_investment
        for year in range(years):
            z_scores = np.random.normal(0, 1, len(ASSET_CLASSES))
            correlated_z_scores = CHOLESKY_FACTOR @ z_scores
            weighted_return = sum([weights[asset] * (ASSET_CLASSES[asset]['return'] + ASSET_CLASSES[asset]['sd'] * correlated_z_scores[idx]) for idx, asset in enumerate(ASSET_CLASSES)])
            
            end_of_year_portfolio_value *= (1 + weighted_return)
            annual_returns.append(end_of_year_portfolio_value)
            
            # Rebalancing
            if rebalance:
                individual_asset_values = {asset: end_of_year_portfolio_value * weights[asset] for asset in weights}
                end_of_year_portfolio_value = sum(individual_asset_values.values())
        portfolio_returns.append(annual_returns)
    return portfolio_returns


def show():
    st.header("Portfolio Monte Carlo Simulation")

    # Collecting inputs
    initial_investment = st.number_input("Initial Investment Amount ($)", min_value=0.0, value=10000.0)
    years = st.number_input("Number of Years", min_value=1, value=10)
    runs = st.number_input("Number of Runs", min_value=1, value=1000)
    st.write("Provide Asset Class Weights (%):")

    weights = {}
    for asset in ASSET_CLASSES:
        weights[asset] = st.slider(asset, 0, 100, 10)

    # Ensuring weights sum to 100%
    if sum(weights.values()) != 100:
        st.error("Asset class weights must sum to 100%")
        return

    # Normalizing the weights
    for asset in weights:
        weights[asset] /= 100

    # Running the simulation
    if st.button("Run Simulation"):
        results = run_simulation(initial_investment, years, runs, weights)

        # Visualizing results
        for idx, annual_returns in enumerate(results, 1):
            plt.plot(range(years), annual_returns, label=f'Run {idx}', alpha=0.5)

        plt.title('Monte Carlo Portfolio Simulation Results')
        plt.xlabel('Years')
        plt.ylabel('Portfolio Value ($)')

        st.pyplot(plt)
