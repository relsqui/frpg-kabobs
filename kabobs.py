import random
import sys

from tabulate import tabulate

# Price calculation parameters
MIN_PRICE = 9500
MAX_PRICE = 10500
LOW_MISS = 9700             # how low a price feels bad to not buy?
HIGH_MISS = 10300           # how high a price feels bad to not sell?
SPIKE_FREQUENCY = 24        # rate of price spikes = 1/SPIKE_FREQUENCY
SPIKE_BOOST = 1000          # spike prices add SPIKE_BOOST to the price

# Simulation parameters
SIMULATION_HOURS = 10000000
PRINT_HOURLY = False                # set this to True to see what every investor does every hour
OUTPUT_FILE = True                  # set to a filename in quotes to output to a file (recommended with PRINT_HOURLY)
DOT_COUNT = SIMULATION_HOURS/100    # print a dot to show progress every DOT_COUNT simulated hours

class Investor(object):
  def __init__(self, buy_policy, sell_policy):
    self.name = f"{buy_policy}/{sell_policy}"
    self.buy_policy = buy_policy
    self.sell_policy = sell_policy
    self.wanna_buy = buy_policies[buy_policy]
    self.wanna_sell = sell_policies[sell_policy]
    self.bought_at = 0
    self.profit = 0
    self.trades = 0
    self.misses = 0

  def maybe_trade_at(self, price):
    if self.bought_at > 0:
      # we're holding kabobs, consider selling
      if self.wanna_sell(price, self.bought_at):
        self.profit += price - self.bought_at
        self.bought_at = 0
        self.trades += 1
        return f"{self.name} sold."
    else:
      # we're not holding kabobs, consider buying
      if self.wanna_buy(price):
        self.bought_at = price
        self.trades += 1
        return f"{self.name} bought."
    if price < self.bought_at or price < LOW_MISS or price > HIGH_MISS:
      # a "miss" is a good price we don't trade at.
      # misses/trades is a measure of how a strategy feels, not how well it works
      self.misses += 1
    return f"{self.name} waited."

buy_policies = dict(
  always = lambda price: True,
  under_10k = lambda price: price < 10000,
  lte_10k = lambda price: price <= 10000,
  under_9800 = lambda price: price < 9800,
  lte_9800 = lambda price: price <= 9800,
)

sell_policies = dict(
  always = lambda price, bought_at: True,
  any_profit = lambda price, bought_at: price > bought_at,
  profit_500 = lambda price, bought_at: price >= bought_at + 500,
  profit_200 = lambda price, bought_at: price >= bought_at + 200,
  over_10k = lambda price, bought_at: price > 10000,
  gte_10k = lambda price, bought_at: price >= 10000,
  over_10k200 = lambda price, bought_at: price > 10200,
  gte_10k200 = lambda price, bought_at: price >= 10200,
)

def get_price():
  price = random.randrange(MIN_PRICE, MAX_PRICE)
  if random.randrange(SPIKE_FREQUENCY) == 0:
    price += SPIKE_BOOST
  return price

def generate_investors():
  investors = []
  for buy_policy in buy_policies.keys():
    for sell_policy in sell_policies.keys():
      investors.append(Investor(buy_policy, sell_policy))
  return investors

def simulate(hours, filehandle):
  investors = generate_investors()
  dot_counter = 0
  for _ in range(hours):
    dot_counter += 1
    price = get_price()
    for investor in investors:
      investor_decision = investor.maybe_trade_at(price)
      if PRINT_HOURLY:
        print(investor_decision)
    if dot_counter == DOT_COUNT:
      print(".", end="", file=sys.stderr)
      dot_counter = 0
  print("", file=sys.stderr)
  investors.sort(key=lambda i: i.profit/hours, reverse=True)
  results = [[i.buy_policy, i.sell_policy, i.misses/i.trades, i.profit/hours] for i in investors]
  print(f"Results over {hours} hours:\n", file=filehandle)
  print(tabulate(results, headers=["Buy @", "Sell @", "Misses/Trades", "Profit/Kabob/Hour"]), file=filehandle)

def main():
  if OUTPUT_FILE is not None:
    with open(OUTPUT_FILE, "w") as f:
      simulate(SIMULATION_HOURS, f)
  else:
    simulate(SIMULATION_HOURS, sys.stdout)

if __name__ == "__main__":
  main()