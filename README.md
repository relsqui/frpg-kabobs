# FarmRPG Kabob Price Simulator

This python script simulates ten million (by default) hours of steak kabob prices and a set of investors with policies about when they buy and sell, then prints a table showing how much silver each investor made.

## No math please, just advice

Buy under 10,000. Sell over 10,050. Check prices as often as convenient. Don't overthink it. :)

## Installation

You don't need to download this if you just want to read about how it works and what the results are, but if you want to play with it, you can install [git](https://git-scm.com/downloads) and [python 3](https://www.python.org/downloads/) and do this (Windows users, use Powershell or the WSL, not cmd):

```
git clone https://github.com/relsqui/frpg-kabobs.git
cd frpg-kabobs
pip install -r requirements.txt
python ./kabobs.py
```

If it's working it will slowly print dots for a couple minutes (depending on computer speed) and then a table of numbers. You can tinker with settings by changing the all-caps variables near the top of the [kabobs.py](kabobs.py). See [Trade Policies](#trade-policies) for how to add trade policies.

## Assumptions

Because I don't know the real algorithm for kabob prices, I've implemented some guesses based on limited history data. They are:

* Prices are distributed uniformly between 9500-10500. (Minimum/maximum prices are configurable in the settings.)
* About one time in 24 (configurable), the price spikes.
* A spike price adds a flat 2000 silver (configurable).

## Limitations

Right now every investor buys or sells their entire inventory at once. (For arithmetic convenience, the size of that inventory is 1.) A couple of people have suggested testing policies of buying/selling half an inventory, which I'm also curious about, but it would require a few changes I haven't gotten around to making.

Investors also do not have limited silver (they can always buy kabobs if they have room), and don't have any time constraints -- they don't care when reset happens, for example, which might affect real-life decisionmaking.

## Example Output

This is an example with enough variety to explain how it works. The most recent output I thought was interesting enough to share is in [kabobs.log](kabobs.log).

```
Results over 10000000 hours:

Buy @       Sell @         Misses/Trades    Profit/Kabob/Hour
----------  -----------  ---------------  -------------------
under_10k   over_10k            0.509348          139.837
under_10k   profit_200          0.525999          134.91
under_10k   over_10k200         0.665771          133.071
under_10k   any_profit          0.423291          123.038
under_9800  over_10k            0.603559          122.342
under_9800  over_10k200         0.720472          120.036
under_9800  profit_500          0.70271           119.992
under_9800  profit_200          0.565063          115.377
under_10k   profit_500          1.38037           102.038
under_9800  any_profit          0.493718          101.092
always      over_10k200         0.70743            96.7132
under_10k   always              0.242639           94.5383
always      over_10k            0.368167           92.0295
under_9800  always              0.404132           87.54
always      any_profit        781.901               0.213334
always      always              0                   0.0485756
always      profit_200     270269                   0.0011535
always      profit_500     370369                   0.0010892
```

Each row represents one investor who considered trading every hour. The first two columns are the policies they use to decide whether to trade (see below).

The misses/trades column measures how many "good" prices were "missed" -- that is, the investor didn't get to buy for a very low price (because they already had kabobs) or sell for a very high price (because they didn't have any or their sell policy didn't permit it) -- compared to how many trades were actually made. Consider it a measure of how annoying an investment strategy might feel to a real-life human following it: a higher number is more frustrating ("argh, I wish I could buy/sell right now"), and a lower number is less. It's included in the table to show how little this correlates with actually making money.

The last column is the good stuff: how much average profit did the investor make on each kabob?

## Trade Policies

* `always`: buys or sells if possible, regardless of the price.
* `under_####`/`over_####`: buys or sells above or below that price threshold.
* `lte_####`/`gte_####`: as above, but also buys or sells at the exact threshold (less/greater-than-or-equal).
* `any_profit`: sells when the price is more than the price the investor bought kabobs at.
* `profit_###`: sells when the profit per kabob would be at least that amount.

You can add trade policies to test by adding to the `buy_policies` and `sell_policies` sections. The structure is this:

 * Buy policies: `<NAME> = lambda price: <EXPRESSION>`
 * Sell policies: `<NAME> = lambda price, bought_at: <EXPRESSION>`

Where `<NAME>` is the description that will show up in the table and `<EXPRESSION>` is a python expression that evaluates to `True` if the policy says to trade and `False` otherwise. The expressions can include the variable `price` to mean the current kabob price, and sell policies can include `bought_at` to mean the price at which the currently-held kabobs were bought. See the existing policies for examples.

## So how much silver can I make?

If the simulation were exactly accurate (which I have no reason to believe is the case), you could estimate your daily average profit like this: find the row for the strategy you use, and multiply the profit number by your inventory capacity and the number of hours in a day when you will check the price. (Hours you don't even consider trading effectively don't exist for this purpose.)

For example: I plan to buy under 10k and sell over 10k, so the estimated profit per kabob per hour is about 140. If my inventory size is 500 and I have time to check the price four times a day, 140 * 500 * 4 = 280,000 estimated average profit.

It's very important that this is an *average*. The real number has a 50/50 chance to be lower or higher on any given day. The longer you trade and the more often you check prices, the better your results will be. Nevertheless, don't use this estimate to plan your spending, use it to compare the value of kabob trading to other ways you could use your silver.
