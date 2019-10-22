"""
Created on Fri Mar 22 11:52:37 2019

@author: reza
"""

import pandas as pd
from selenium import webdriver
import time

driver = webdriver.Chrome(r'C:\Users\yourpath\chromedriver_win32\chromedriver.exe')

driver.get(
    "https://YOUR KIBANA REPORT URL")

time.sleep(10)

driver.execute_script("window.scrollTo(0, 700);")

driver.find_element_by_xpath("//a[@ng-click='aggTable.exportAsCsv(true)']").click()

time.sleep(5)
print("------------------------------------------------")
print('Product import-stat downloaded')



filename = (r'C:\Users\yourpath\output.csv')
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)
df = pd.read_csv(filename)

df['imported'] = df['imported'].str.replace(',', '')
df['imported'] = df['imported'].astype(int)
df['data.country.keyword: Descending'] = df['data.country.keyword: Descending'].str.upper()

df["@timestamp per day"] = df["@timestamp per day"].str.replace(", 00:00:00.000", "")
df  = df[["@timestamp per day", "data.country.keyword: Descending", "imported"]]



test = pd.concat([pd.Series([0]),df['imported']]).reset_index()[0]
df['test'] = test[0:len(test)-1]
df['Drops in %'] = (df['imported'] - df['test']) / df['imported'] * 100
size=int(len(df)/7)
df.loc[0::size,['Drops in %']]= 0


df = df.drop('test', axis=1)
df= df.drop('imported', axis=1)
df['Drops in %'] = df['Drops in %'].apply(lambda x: round(x, 2))
df.columns=["Date", "Country", "Drops in %"]
df.sort_values(by=['Date','Country'], inplace=True, ascending=True)

#print(df)
df.to_csv("Import Drops of all CC.csv", index=False)
#df.plot()
print("------------------------------------------------")
print("Analysis of Percentage Drops for all CC: Passed ")
print("------------------------------------------------")



