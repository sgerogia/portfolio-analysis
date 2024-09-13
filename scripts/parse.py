from model import Security, Fund
from typing import List, Any

funds = []

def parse_fund(fund_data, portfolio_data) -> Fund:
    holdings = []
    for holding in fund_data.get('portfolioHoldings', []):
        if holding.get('fund', False):
            # Recursive call if the holding is a fund itself
            sub_fund = find_fund_by_name(holding['securityName'], portfolio_data)
            sub_fund['weighting'] = holding['weighting'] * fund_data['weighting'] / 100
            holdings.append(parse_fund(sub_fund, portfolio_data))
        else:
            holdings.append(Security(holding['securityName'], holding['weighting'], []))
    return Fund(fund_data['name'], fund_data['url'], fund_data['weighting'], holdings)

def find_fund_by_name(name, portfolio_data) -> Any:
    for item in portfolio_data:
        if item.get('name', '') == name:
            return item
    return None

def calculate_absolute_weightings(fund, parent_weight=100):
    total_declared = sum(h.weighting for h in fund.holdings)
    if total_declared < 100:
        fund.holdings.append(Security("Other", 100 - total_declared, [fund.name]))
    for holding in fund.holdings:
        absolute_weight = holding.weighting * parent_weight / 100
        if isinstance(holding, Fund):
            calculate_absolute_weightings(holding, absolute_weight)
        else:
            holding.weighting = absolute_weight
            holding.funds.append(fund.name)

def aggregate_securities(funds) -> List[Security]:
    security_map = {}
    for fund in funds:
        for security in fund.holdings:
            if isinstance(security, Fund):
                continue
            if security.name not in security_map:
                security_map[security.name] = Security(security.name, 0, [])
            security_map[security.name].weighting += security.weighting
            security_map[security.name].funds.extend(security.funds)
    return list(security_map.values())

def process_etf_data(funds) -> List[Security]:
    for fund in funds:
        calculate_absolute_weightings(fund=fund, parent_weight=fund.weighting)
    
    securities = aggregate_securities(funds)
    securities.sort(key=lambda x: x.weighting, reverse=True)  # Sort by weighting, descending
    return securities

def analyze_portfolio(portfolio_data) -> List[Security]:
    total_holdings = {}
    global funds  # This will hold all top-level funds
    funds = [parse_fund(etf_item, portfolio_data) for etf_item in portfolio_data]

    securities = process_etf_data(funds)
    return securities