GSPC_lines = open("^GSPC.csv",'r').readlines()
VIX_lines = open("^VIX.csv",'r').readlines()


available_dates_GSPC = []
available_dates_VIX = []

GSPC_prices = []
VIX_prices = []

sentiments = open("text_sentiment_per_day.txt",'r').readlines()

for line in VIX_lines:
    cur_line = line.split(",")
    VIX_prices.append(cur_line[4])
    available_dates_VIX.append(cur_line[0])

f_VIX = open("sentiment_day_and_price_VIX.txt.txt",'w')

for sentiment in sentiments:
    cur_sentiment = sentiment.split(" ")
    for i in range(len(available_dates_VIX)):
        if available_dates_VIX[i] == cur_sentiment[0]:
            used_sentiment = cur_sentiment[len(cur_sentiment)-1]
            used_price = VIX_prices[i]
            res_list = [cur_sentiment[0],str(used_sentiment),str(used_price)]
            joined_res_list = ",".join(res_list)
            f_VIX.write(joined_res_list + "\n\n")

for line in GSPC_lines:
    try:
        cur_line = line.split(',')
        cur_date = cur_line[0].split('/')
        temp = cur_date[len(cur_date)-1]
        cur_date[len(cur_date)-1] = cur_date[0]
        cur_date[0] = temp
        formatted_date = cur_date[0] + "-" + cur_date[1] + "-" + cur_date[2]
        GSPC_prices.append(cur_line[4])
        available_dates_GSPC.append(formatted_date)
    except IndexError:
        pass

f_GSPC = open("sentiment_day_and_price_GSPC.txt.txt",'w')

for sentiment in sentiments:
    cur_sentiment = sentiment.split(" ")
    cur_date_splitted = cur_sentiment[0].split("-")
    formatted_month = ""
    formatted_day = ""
    if int(cur_date_splitted[1][0]) == 0:
        formatted_month = cur_date_splitted[1][1]
    else:
        formatted_month = cur_date_splitted[1]

    if int(cur_date_splitted[2][0]) == 0:
        formatted_day = cur_date_splitted[2][1]
    else:
        formatted_day = cur_date_splitted[2]

    formatted_date = str(2020) + "-" + formatted_month + "-" + formatted_day
    for i in range(len(available_dates_GSPC)):
        if available_dates_GSPC[i] == formatted_date:
            used_sentiment = cur_sentiment[len(cur_sentiment)-1]
            price = GSPC_prices[i]
            res_list = [str(formatted_date),str(used_sentiment),str(price)]
            joined_res_list = ",".join(res_list)
            f_GSPC.write(joined_res_list+'\n\n')

