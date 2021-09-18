import random
import sys

from tabulate import tabulate

# Price calculation parameters
MIN_PRICE = 9500
MAX_PRICE = 10500
SPIKE_FREQUENCY = 30        # rate of price spikes = 1/SPIKE_FREQUENCY
SPIKE_BOOST = 2000          # spike prices add SPIKE_BOOST to the price

# Simulation parameters
SIMULATION_HOURS = 10000000
PRINT_HOURLY = False        # set this to True to see what every investor does every hour
OUTPUT_FILE = None          # set to a filename in quotes to output to a file

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
    if price < 9800 or price > 10200:
      self.misses += 1
    return f"{self.name} waited."

buy_policies = dict(
  always = lambda price: True,
  under10k = lambda price: price < 10000,
  under9800 = lambda price: price < 9800,
)

sell_policies = dict(
  always = lambda price, bought_at: True,
  profitable = lambda price, bought_at: price > bought_at,
  over10k = lambda price, bought_at: price > 10000,
  over10k200 = lambda price, bought_at: price > 10200,
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
  for _ in range(hours):
    price = get_price()
    for investor in investors:
      investor_decision = investor.maybe_trade_at(price)
      if PRINT_HOURLY:
        print(investor_decision)
  investors.sort(key=lambda i: i.profit/hours, reverse=True)
  results = [[i.buy_policy, i.sell_policy, i.misses/i.trades, i.profit/hours] for i in investors]
  print(f"Results over {hours} hours:\n", file=filehandle)
  print(tabulate(results, headers=["Buy @", "Sell @", "Misses/Trades", "Profit/Hour"]), file=filehandle)

def main():
  if OUTPUT_FILE is not None:
    with open(OUTPUT_FILE, "w") as f:
      simulate(SIMULATION_HOURS, f)
  else:
    simulate(SIMULATION_HOURS, sys.stdout)

if __name__ == "__main__":
  main()