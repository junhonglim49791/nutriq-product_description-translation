import pandas as pd

df = pd.read_excel("product_description.xlsx", header=0, skiprows=[1,2,3])
print(df)