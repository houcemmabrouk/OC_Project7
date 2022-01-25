from itertools import combinations
from time import process_time
from data_handling import import_data, write_in_csv

data_csv = 'data/dataset_20_actions.csv'
# data_csv = 'data/dataset1_Python+P7.csv'

MAX_INVEST = 500


def brute_force(dispo_stock_list):
    time_start = process_time()
    can_buy_stock_list = []
    bigO = 0
    best_portfolio = ["", 0, 0]
    for len_combi in range(0, len(dispo_stock_list) + 1):
        for combination in combinations(dispo_stock_list, len_combi):
            stock_combi_price = 0
            stock_combi_profit = 0
            bigO += 1
            for stock in combination:
                stock_price = stock[1]
                stock_profit_percent = stock[2]
                """supprimer les calculs non necessaires et les integrer dans les csv"""
                """utiliser la fonction sum plus performante"""
                stock_profit = stock_profit_percent / 100 * stock_price
                stock_combi_price += stock_price
                stock_combi_profit += stock_profit
            if stock_combi_price <= MAX_INVEST:
                new_portfolio = [combination, stock_combi_price, stock_combi_profit]
                can_buy_stock_list.append(new_portfolio)
                if new_portfolio[2] > best_portfolio[2]:
                    best_portfolio = new_portfolio
                    write_in_csv({'current best solution found': best_portfolio[0]}, "bruteforce_solution.csv", 'w')

    # sort by stock_combi_profit
    """nettoyer cette partie"""
    print('can_buy_stock_list', can_buy_stock_list[2])
    can_buy_stock_list = sorted(can_buy_stock_list, key=lambda stock: stock[2], reverse=True)
    len_can_buy_stock_list = len(can_buy_stock_list)
    can_buy_stock_list_best_element = can_buy_stock_list[0]
    best_stock_list = can_buy_stock_list_best_element[0]
    best_stock_list_price = round(can_buy_stock_list_best_element[1], 2)
    best_stock_list_profit = round(can_buy_stock_list_best_element[2], 2)
    len_best_stock_list = len(best_stock_list)
    time_end = process_time()
    processing_time = time_end - time_start
    output = {'bigO': bigO, 'processing_time': processing_time, 'best_stock_list_price': best_stock_list_price,
              'best_stock_list_profit': best_stock_list_profit, 'len_dispo_stock_list': len(dispo_stock_list),
              'len_can_buy_stock_list': len_can_buy_stock_list, 'len_best_stock_list': len_best_stock_list,
              'best_stock_list': best_stock_list}
    print("best_portfolio", best_portfolio)
    return output


dataset = import_data(data_csv)
output = brute_force(dataset)
write_in_csv(output, "bruteforce_output.csv", 'a')
print("bigO:", output['bigO'])
print("best_portfolio:", output['best_stock_list'])
print("processing_time", output['processing_time'], "s")
