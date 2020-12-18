GSPC_lines = open("^GSPC.csv",'r').readlines()
VIX_lines = open("^VIX.csv",'r').readlines()
sentiments = open("text_sentiment_per_day.txt").readlines()

used_sentiments = []
VIX_price_changes = []
GSPC_price_changes = []

VIX_dates = []
GSPC_dates = []

f = open("sentiment_and_price_change.txt",'w')

#getting available dates for GSPC
for line in GSPC_lines:
    try:
        cur_line = line.split(',')
        cur_date = cur_line[0].split('/')
        temp = cur_date[len(cur_date)-1]
        cur_date[len(cur_date)-1] = cur_date[0]
        cur_date[0] = temp
        formatted_date = cur_date[0] + "-" + cur_date[1] + "-" + cur_date[2]
        GSPC_dates.append(formatted_date)
    except IndexError:
        pass

#get available VIX dates
for line in VIX_lines:
    VIX_dates.append(line.split(",")[0])

#get price changes for VIX and GSPC and get associated sentiments
for i in range(len(GSPC_lines)-1):
    GSPC_price_changes.append(float(GSPC_lines[i+1].split(",")[4]) - float(GSPC_lines[i].split(",")[4]))

for i in range(len(VIX_lines)-1):
    VIX_price_changes.append(float(VIX_lines[i+1].split(",")[4]) - float(VIX_lines[i].split(",")[4]))

for i in range(len(sentiments)-1):
    if sentiments[i].split(" ")[0] in VIX_dates:
        used_sentiments.append(sentiments[i].split(" ")[2])



#write tofile
for i in range(len(used_sentiments)):
    entry = tuple((float(used_sentiments[i]),VIX_price_changes[i],GSPC_price_changes[i]))
    f.write((str(entry).strip("(").strip(")")).replace(" ","") + '\n')



