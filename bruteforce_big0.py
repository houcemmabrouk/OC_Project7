from itertools import combinations
from time import process_time
from sys import getsizeof
from pympler import muppy
import matplotlib.pyplot as plt
from ram_tools import size_format
from data_handling import import_data, filter_and_sort_data, write_in_csv

data_csv = 'data/dataset1_Python+P7.csv'

MAX_INVEST = 500
output = {'nb_stocks': 0, 'bigO': 0, 'processing_time': 0, 'best_stock_list_price': 0, 'best_stock_list_profit': 0}


def brute_force(dispo_stock_list):
    time_start = process_time()
    bigO = 0
    len_dispo_stock_list = len(dispo_stock_list)
    best_portfolio = ["", 0, 0]
    for len_combi in range(0, len_dispo_stock_list + 1):
        for combi in combinations(dispo_stock_list, len_combi):
            stock_combi_price = 0
            stock_combi_profit = 0
            bigO += 1
            for stock in combi:
                stock_price = stock[1]
                stock_profit_percent = stock[2]
                stock_profit = stock_profit_percent / 100 * stock_price
                stock_combi_price += stock_price
                stock_combi_profit += stock_profit
            if stock_combi_price <= MAX_INVEST:
                stock_tuple = (combi, stock_combi_price, stock_combi_profit)
                new_portfolio = [combi, stock_combi_price, stock_combi_profit]
                if new_portfolio[2] > best_portfolio[2]:
                    best_portfolio = new_portfolio

    time_end = process_time()
    processing_time = time_end - time_start
    output = {'bigO': bigO, 'processing_time': processing_time, 'best_stock_list_price': stock_combi_price,
              'best_stock_list_profit': stock_combi_profit}

    return output


global_ram_usage = []
global_processing_time = []
complexity = []
portfolio_size = []
ram_usage = 0
for length in range(1, 20):
    dispo_stock_list = import_data(data_csv, length)
    output = brute_force(dispo_stock_list)
    allObjects = muppy.get_objects()
    for object in allObjects:
        ram_usage += getsizeof(object)

    global_ram_usage.append(ram_usage / 1000000)
    global_processing_time.append(output['processing_time'])
    complexity.append(output['bigO'])
    portfolio_size.append(length)

    print("nb_stocks:", length, "bigO:", output['bigO'], "duration in s:", output['processing_time'], "ram usage",
          size_format(ram_usage), 'global processing time', process_time())

    write_in_csv(output, "bruteforce_big0.csv", 'a')

plt.figure()
plt.subplot(2, 2, 1)
plt.plot(portfolio_size, complexity, label='Time Complexity', c='red')
plt.xlabel('number of stocks available')
plt.ylabel('iterations')
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(portfolio_size, global_processing_time, label='Processing Time', c='orange')
plt.xlabel('number of stocks available')
plt.ylabel('processing time in sec')
plt.legend()
plt.subplot(2, 2, 3)
plt.plot(portfolio_size, global_ram_usage, label='Spatial Complexity', c='grey')
plt.xlabel('number of stocks available')
plt.ylabel('memory usage in MB')
plt.legend()
plt.show()
