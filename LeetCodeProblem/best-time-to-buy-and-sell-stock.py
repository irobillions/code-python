def maxProfit(prices: list[int]) -> int:
    less_price = prices[0]
    max_profit = 0
    for current_price in prices:
        if current_price < less_price:
            less_price = current_price
        else:
            max_profit = max(current_price - less_price, max_profit)
    return max_profit


if __name__ == '__main__':
    print(maxProfit([6, 4, 7, 5, 9]))
