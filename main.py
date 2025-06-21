import pandas as pd
from bs4 import BeautifulSoup
from googletrans import Translator


df = pd.read_excel("product_description_ubuntu.xlsx", header=0, skiprows=[1,2,3])
# print(df.iloc[0]["Main Description"])

soup = BeautifulSoup(df.loc[0, "Main Description"], 'html.parser')

print(soup.prettify())