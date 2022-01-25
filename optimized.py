from time import process_time
from data_handling import filter_and_sort_data, write_in_csv, import_data


# data_csv='data/dataset_20_actions.csv'
data_csv = 'data/dataset2_Python+P7.csv'
# data_csv = 'data/dataset2_Python+P7.csv'
# data_csv = 'data/dataset1_Python+P7.csv'

MAX_INVEST = 500


def optimized(dispo_stock_list):
    time_start = process_time()
    best_stock_list = []
    best_stock_list_price = 0
    best_stock_list_profit = 0
    bigO = 0
    len_dispo_stock_list = len(dispo_stock_list)
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
    output = {'len_dispo_stock_list ': len_dispo_stock_list, 'bigO': bigO, 'best_stock_list': best_stock_list,
              'best_stock_list_price': best_stock_list_price, 'best_stock_list_profit': best_stock_list_profit,
              'len_best_stock_list': len(best_stock_list), 'processing_time': processing_time}
    return output


dispo_stock_list = import_data(data_csv)
stocks_in_dataset = len(dispo_stock_list)
dispo_stock_list = filter_and_sort_data(dispo_stock_list)
data_output = optimized(dispo_stock_list)
write_in_csv(data_output, 'optimized_output.csv', 'w')
print('stocks_in_dataset', stocks_in_dataset, 'bigO', data_output['bigO'])
print("best_portfolio:", data_output['best_stock_list'])
print("processing_time", data_output['processing_time'], "s")


