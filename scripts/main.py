import yaml

from parse import analyze_portfolio
from visualise import visualise_holdings, visualise_graph


def main():
    with open('data/portfolio.yaml', 'r') as file:
        portfolio_data = yaml.safe_load(file)

    holdings = analyze_portfolio(portfolio_data)
    visualise_holdings(holdings, include_other=False, top_n=20)
    visualise_graph(holdings, include_other=False, top_n=15)


if __name__ == "__main__":
    main()