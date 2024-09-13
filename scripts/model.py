class Security:
    def __init__(self, name, weighting, funds):
        self.name = name
        self.weighting = weighting
        self.funds = funds

class Fund:
    def __init__(self, name, url, weighting, holdings):
        self.name = name
        self.url = url
        self.weighting = weighting
        self.holdings = holdings  