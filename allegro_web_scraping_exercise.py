# Provide descriptive statistics pertaining to the data set with information about top recommended products and their
# price in selected categories at www.allegro.pl using only requests and html.parser, and plot median price per category
# on bar chart

from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import os.path
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

# define path where all output files would be saved
savepath = 'C:/Users/DOM/Downloads/'

# check whether the process has already been run
# start
if os.path.isfile(savepath+'details.csv'):
    print('File exists')
else:
    url = "https://allegro.pl/mapa-strony/kategorie"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    a = np.empty((0,2), str)
    for i in soup.findAll('a', {"class" : "_w7z6o"}):
        a = np.append(a, np.array([[i.get('title'),i.get('href')]]), axis=0)

    # control check - print first row of the array
    # print(a[0,0], a[0,1])

    # narrow down the number of categories for better performance and exclude invalid rows
    a = (a[:25,:25])
    a2 = a[a[:,0] != None]
    result = a2[a2[:,1] != 'https://allegro.pl']

    # control check
    # print(result)

    # save list of analyzed categories and hyperlinks to *.csv file
    df = pd.DataFrame(result, columns= ['Category','Link'])
    df.to_csv(savepath+'categories.csv', encoding='utf-8', index=False, sep='|')

    # define arrays and variables for loop
    arr = np.empty((0,2))
    arr2 = np.empty((0,1))
    iter = 0

    # perform tasks for all available categories
    for j in result[:,1]:
        url2 = "https://allegro.pl"+j
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.content, "html.parser")
        for i in soup2.findAll('span', {"class" : "fee8042"}):
            arr = np.append(arr, np.array([[ (re.compile('.*\[(.*)\].*').search(str([result[:,0][result[:,1]==str(j)]][0])).group(1)).replace("'",""),i.get_text()]]), axis=0)
        for i in soup2.findAll('h2', {"class": "ebc9be2"}):
            arr2 = np.append(arr2, np.array([[i.get_text()]]), axis=0)
        iter += 1

        # print completion status % after every 2 iterations
        if iter % 2:
            print('Progress: ',round(iter/len(result)*100,0),'%')
    # end of loop

    # combine arrays into one - please note that they should have exactly the same number of rows
    arr3 = np.concatenate((arr, arr2), axis=1)

    # control check - print results
    # print(arr3)

    # convert results to DataFrame, adjust formats and save to *.csv file
    df2=pd.DataFrame(arr3, columns=['Category','Price (PLN)','Full product name'])
    df2['Price (PLN)'] = df2['Price (PLN)'].str.replace('[^0-9]+', '')
    df2['Price (PLN)'] = pd.to_numeric(df2['Price (PLN)']) / 100
    df2.to_csv(savepath+'details.csv', encoding='utf-8', index=False, sep='|')

# end

#
set = pd.read_csv('C:/Users/DOM/Downloads/details.csv', sep='|', usecols=['Category','Price (PLN)','Full product name'])
set = pd.DataFrame(set)
print(set.head(5))
set['Category'] = set['Category'].astype('category')
# set['Nazwa produktu'] = set['Nazwa produktu'].astype('category')
print(set.dtypes)

print(set.describe(include='all'))
plot_data = set.groupby('Category').agg({'Price (PLN)':['median']})

# drop a multi-level column index - necessary when we want to plot the results
plot_data.columns = plot_data.columns.droplevel(0)
plot_data = plot_data.reset_index()
print(plot_data)

# plot the results
y_pos = np.arange(len(plot_data))
plt.bar(y_pos, plot_data['median'], align='center', alpha=0.5)
plt.xticks(y_pos, plot_data['Category'], rotation='vertical')

# prevent clipping of x-axis ticks
plt.subplots_adjust(bottom=0.4)

# define title and labels
plt.suptitle('Allegro.pl - shopping website')
plt.title('Median price of top recommended products per category')
plt.ylabel('Median price (PLN)')
plt.xlabel('Category')

# display results
# plt.show()

# save plot to a file - alternatively to plt.show()
plt.savefig(savepath+'chart.png')