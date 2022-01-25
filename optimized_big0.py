from time import process_time
from sys import getsizeof
from pympler import muppy
import matplotlib.pyplot as plt
from data_handling import import_data, write_in_csv, filter_and_sort_data
from ram_tools import size_format

# data_csv='data/dataset_20_actions.csv'
data_csv = 'data/dataset1_Python+P7.csv'
# data_csv = 'data/dataset2_Python+P7.csv'
# data_csv = 'data/dataset1_Python+P7.csv'

MAX_INVEST = 500
output = {'nb_stocks': 0, 'bigO': 0, 'processing_time': 0}


def optimized(dispo_stock_list):
    time_start = process_time()
    best_stock_list = []
    best_stock_list_price = 0
    best_stock_list_profit = 0
    bigO = 0
    for stock in dispo_stock_list:
        bigO += 1
        stock_price = stock[1]
        if best_stock_list_price + stock_price <= MAX_INVEST:
            stock_profit_percent = stock[2]
            stock_profit = stock_profit_percent / 100 * stock_price
            best_stock_list_price += stock_price
            best_stock_list_profit += stock_profit
            best_stock_list.append(stock)

    best_stock_list_price = round(best_stock_list_price, 2)
    best_stock_list_profit = round(best_stock_list_profit, 2)
    time_end = process_time()
    processing_time = time_end - time_start
    output = {'bigO': bigO, 'processing_time': processing_time, 'best_stock_list_price': best_stock_list_price,
              'best_stock_list_profit': best_stock_list_profit}
    return output


global_ram_usage = []
global_processing_time = []
portfolio_size = []
complexity = []
dataset_size = len(import_data(data_csv))

for length in range(1, dataset_size):
    dispo_stock_list = import_data(data_csv, length)
    len_dataset = len(dispo_stock_list)
    dispo_stock_list = filter_and_sort_data(dispo_stock_list)
    output = optimized(dispo_stock_list)
    allObjects = muppy.get_objects()
    ram_usage = 0
    for object in allObjects:
        ram_usage += getsizeof(object)

    global_ram_usage.append(ram_usage / 1000000)
    global_processing_time.append(output['processing_time'])
    complexity.append(output['bigO'])
    portfolio_size.append(length)

    print("nb_stocks:", length, "bigO:", output['bigO'], "Processing Time:", output['processing_time'],
          "ram usage", size_format(ram_usage))

    """Telemetric Data Storage"""
    output['nb_stocks'] = length
    output['ram_usage'] = ram_usage
    write_in_csv(output, 'optimized_big0.csv', 'a')

"""Graph Tracing"""
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
