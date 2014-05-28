import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Open a file
contents = open('result', 'r').read()

db2 = 0
dataapi2 = 0
server2 = 0
client2 = 0


def retrieveNumber(input):
    line_parts = line.split(input)
    line_parts = line_parts[1].split(' ')
    return float(line_parts[0])

# Parse file contents
for line in contents.split('\n'):

    if '.DB' in line:
        db2 += retrieveNumber('DB: ')

    if '.V' in line:
        dataapi2 += retrieveNumber('V: ')

    if '.W' in line:
        dataapi2 += retrieveNumber('W: ')

    if 'response' in line:
        server2 += retrieveNumber('response: ')

    if '.E' in line:
        client2 += retrieveNumber('E: ')

total = client2
client = client2-server2
server = server2-dataapi2
dataapi = dataapi2-db2
db = db2

print db, dataapi, server, client

N = 1
ind = np.arange(N)
width = 0.35

gs = gridspec.GridSpec(2, 2, height_ratios=[4, 1])
plt.clf()

# Draw stacked bar plot
first = plt.subplot(gs[0, 0])

b1 = plt.bar(ind, db, width, color='b')
b2 = plt.bar(ind, dataapi, width, color='r', bottom=db2)
b3 = plt.bar(ind, server, width, color='y', bottom=dataapi2)
b4 = plt.bar(ind, client, width, color='g', bottom=server2)

plt.title('Execution time on each layer')
plt.ylabel('execution time [ms]')
plt.xticks(ind+width/2., (""))
plt.legend((b1, b2, b3, b4), ('DB', 'Data API', 'Server', 'Client'))

# Draw pie chart
second = plt.subplot(gs[0, 1])

plt.title('Execution time on each layer in %')
x = (db/total, dataapi/total, server/total, client/total)
explode = (0.05, 0.05, 0.05, 0.05)
labels = 'DB', 'Data API', 'Server', 'Client'
colors = ('b', 'r', 'y', 'g')

plt.pie(
    x,
    labels=labels,
    explode=explode,
    shadow=True,
    autopct='%1.1f%%',
    colors=colors
)

# Draw data table
third = plt.subplot(gs[1, :])
third.xaxis.set_visible(False)
third.yaxis.set_visible(False)
third.patch.set_facecolor('#bfbfbf')
third.spines['top'].set_color('#bfbfbf')
third.spines['left'].set_color('#bfbfbf')
third.spines['right'].set_color('#bfbfbf')

values = [db, dataapi, server, client, total]
data = [['%1.1f' % x for x in values]]
columns = ('DB', 'Data API', 'Server', 'Client', 'Total')
rows = ['time [ms]']

plt.title('Data table')
plt.table(
    cellText=data,
    rowLabels=rows,
    colLabels=columns,
    loc='bottom'
)

plt.show()
