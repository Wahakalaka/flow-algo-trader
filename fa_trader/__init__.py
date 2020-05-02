from datetime import datetime


class FATrade:
    """Represent trades as objects for ease of filtering and calculating"""
    def __init__(self, date, time, ticker, expiry, strike, cp, spot, qty, price, trade_type, volume, oi, premium, sector, unusual):
        self.unusual = False if unusual == 'FALSE' else True
        self.sector = sector
        self.premium = int(premium.replace('$', '').replace(',', ''))
        self.oi = int(oi)
        self.volume = int(volume)
        self.trade_type = trade_type
        self.price = float(price)
        self.qty = int(qty)
        self.spot = float(spot)
        self.cp = cp
        self.strike = float(strike)
        self.expiry = datetime.strptime(expiry, '%Y-%m-%d')
        self.ticker = ticker
        self.date = datetime.strptime(date, '%m/%d/%y')
        time = time if time != 'undefined' else '9:00:00'  # default to 9am if FA shits itself
        self.time = time
        self.placed = datetime.strptime(f'{date} {time}', '%m/%d/%y %H:%M:%S.%f' if '.' in time else '%m/%d/%y %H:%M:%S')
        self.dte = self.expiry - self.placed

        # relative to spot
        self.percent_otm = 1 - (self.spot / self.strike if cp == 'CALLS' else self.strike / self.spot)  # < 1 if ITM
        self.atm = -0.05 <= self.percent_otm <= 0.05
        self.itm = self.spot >= self.strike if cp == 'CALLS' else self.spot <= self.strike
        self.otm = self.percent_otm > 0.05

        # additional data points
        self.market_cap = None
        self.daily_volume = None
        self.iv = None  # todo this is pretty important to interpreting percent_otm

    # --- contract formatting --- #

    def __str__(self):
        """e.g. SPY 180p 4/24"""
        return f'{self.ticker} ${self.strike}{"p" if self.cp == "PUTS" else "c"} {self.expiry.strftime("%m/%d")}'

    @property
    def tos(self):
        """The TOS ticker for this contract, e.g. .AAPL190621C197.5"""
        s = int(self.strike) if int(self.strike) == self.strike else round(self.strike, 1)
        return f'.{self.ticker}{self.expiry.strftime("%y%m%d")}{"C" if self.cp == "CALLS" else "P"}{s}'

    @property
    def ticker_date(self) -> str:
        return f'{self.ticker} {self.expiry.strftime("%m/%d")}{"p" if self.cp == "PUTS" else "c"}'

    # --- date extractions --- #

    @property
    def minute_of_day(self) -> int:
        return int(self.placed.strftime('%H')) * 60 + int(self.placed.strftime('%M'))

    @property
    def day_of_week(self) -> str:
        return self.placed.strftime('%a')

    @property
    def day_of_month(self) -> int:
        return int(self.placed.strftime('%d'))

    @property
    def month_of_year(self) -> int:
        return int(self.placed.strftime('%m'))

    # --- hashing methods --- #

    def __key(self) -> tuple:
        """Return a tuple that uniquely identifies this trade (trade, not contract)"""
        return self.date, self.time, self.ticker, self.price, self.expiry, self.cp, self.spot, self.qty, self.price, self.volume, self.premium

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, FATrade):
            return self.__key() == other.__key()
        return NotImplemented
