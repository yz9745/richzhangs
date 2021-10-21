# ledger, blotter = []
# holding_list, order_list = []
# start, end, cash = 0


# def init():
#     blotter = pd.DataFrame(None, columns=['ID', 'Date', 'Time', 'Ticker', 'Action', 'Price', 'Type', 'Status'])
#     ledger = pd.DataFrame(None, columns=['ID', 'Date', 'Time', 'Active Holdings', 'Cash', 'PnL'])
#     holding_list = pd.DataFrame(None,
#                                 columns=['ID', 'Ticker', 'Holding Status', 'Current Price', 'Holding price', 'Position',
#                                          'Target', 'Stop', 'PnL'])
#     order_list = pd.DataFrame(None, columns=['ID', 'Ticker', 'Action', 'Limit Price'])
#     start = 0
#     end = 365
#     cash = 10000
#     record()
#
#
# def back_test():
#     # record the beginning status
#     while start < end:
#         close_positions()  # close the position which meets the condition
#         if len(active_list) >= 15:
#             pass
#         else:
#             open_positions()  # get the limited orders done
#         updateOrderList()  # update next day trading targets
#         record()
#         start += 1
#     return

