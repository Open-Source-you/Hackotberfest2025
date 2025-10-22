"""
Problem - Best Time to Buy and Sell Stock
You are given an array prices where prices[i] is the price of a given stock on the i-th day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example
Input: prices = [7, 1, 5, 3, 6, 4]
Output: 5

Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

0 ≤ prices[i] ≤ 10^4
"""



def maxProfit(prices: list[int]) -> int:
    # Initialize variables for tracking the lowest buy price, current sell price, and maximum profit
    buy = prices[0]
    sell = prices[0]
    max_profit = 0

    # Loop through all prices
    for i in range(len(prices)):

        # Update buy and sell when a lower price is found
        if prices[i] < buy:
            buy = prices[i]
            sell = prices[i]

        # Update sell and calculate profit when a higher price is found
        if prices[i] > sell:
            sell = prices[i]
            profit = sell - buy
            max_profit = profit if profit > max_profit else max_profit

    # Return the maximum profit found
    return max_profit

def main():
    prices = [7, 1, 5, 3, 6, 4]
    print(maxProfit(prices))  # Output: 5

if __name__ == "__main__":
    main()
