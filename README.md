# FarmRPG Kabob Price Simulator

This python script simulates ten million (by default) hours of steak kabob prices and a set of investors with policies about when they buy and sell, then prints a table showing how much silver each investor made. You can tinker with its behavior by changing a few all-caps variables near the top of the script.

If you have git and python 3 installed, you can get it and try it like this:

```
git clone https://github.com/relsqui/frpg-kabobs.git
cd frpg-kabobs
pip install -r requirements.txt
python ./kabobs.py
```

(Windows users, use Powershell or the WSL instead of cmd.)

## Assumptions

Because I don't know the real algorithm for kabob prices, I've implemented some guesses based on limited history data. They are:

* Prices are distributed uniformly between 9500-10500. (Minimum/maximum prices are configurable in the settings.)
* About one time in thirty (configurable), the price spikes.
* A spike price adds a flat 2000 silver (configurable).

## Limitations

Right now every investor buys or sells their entire inventory at once. (For arithmetic convenience, the size of that inventory is 1.) A couple of people have suggested testing policies of buying/selling half an inventory, which I'm also curious about, but it would require a few changes I haven't gotten around to making.

Investors also do not have limited silver (they can always buy kabobs if they have room), and don't have any time constraints -- they don't care when reset happens, for example, which might affect real-life decisionmaking.

## Example Output

```
Results over 10000000 hours:

Buy @      Sell @        Misses/Trades    Profit/Kabob/Hour
---------  ----------  ---------------  -------------------
under10k   over10k            0.614027          153.075
under10k   over10k200         0.782913          149.106
under10k   profitable         0.483306          133.94
under9800  over10k200         1.00562           132.884
under9800  over10k            0.836396          132.398
always     over10k200         0.449399          110.728
under9800  profitable         0.647066          108.215
under10k   always             0.333497          103.21
always     over10k            0.28051           101.008
under9800  always             0.556048           93.6886
always     profitable       676.392               0.202856
always     always             0                  -0.0990158
```

Each row represents one investor. The first two columns are their trade policies. An investor with the `under10k`/`over10k` policies, for example, will buy kabobs at *any* price below 10,000 (assuming their inventory is empty) and sell at *any* price above 10,000 (assuming their inventory is full). The `always` policy accepts any price (buy every hour that you don't have bobs, sell every hour that you do), and the `profitable` sell policy sells kabobs for any price greater than the price they were bought at.

The misses/trades column measures how many "good" prices were "missed" -- that is, the investor didn't get to buy for a very low price (because they already had kabobs) or sell for a very high price (because they didn't have any or their sell policy didn't permit it). It's included as a measure of how good an investment strategy might feel to an actual human executing it. A higher number is more frustrating ("argh, I wish I could buy/sell right now"), and a lower number is less.

The last column is the good stuff: how much actual profit did the investor make on each kabob bought, divided by the number of hours simulated.

## So how much silver can I make?

If the simulation were exactly accurate (which I have no reason to believe is the case), you could estimate your daily average profit like this: find the row for the strategy you use, and multiply the profit number by your inventory capacity and the number of hours in a day when you will check the price. (Hours you don't even consider trading effectively don't exist for this purpose.)

For example: I plan to buy under 10k and sell over 10k, so the estimated profit per kabob per hour is 153. If my inventory size is 500 and I have time to check the price four times a day, 153 * 500 * 4 = 306,000 estimated average profit.

It's very important that this is an *average*. The real number has a 50/50 chance to be lower or higher on any given day. This math is for estimating long-term profits; the longer you trade and the more often you check the price, the better the overall outcome will be.

## No math please, just advice

Buy under 10,000. Sell over 10,000. Check prices as often as convenient. Don't overthink it. :)
