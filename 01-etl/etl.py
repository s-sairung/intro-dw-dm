import pandas as pd
import numpy as np

file1 = pd.ExcelFile("ETLDataSource1.xlsx")
order1 = file1.parse("orderSource1")
product1 = file1.parse("productSource1")
join1 = pd.merge(order1, product1, on="OrderID")

state = file1.parse("StateLookup", index_col=1)
state_dict = state.to_dict()["State"] # might be better ways

join1["CustomerState"].replace(state_dict, inplace=True)

split1 = pd.DataFrame(join1.CustomerName.str.split(" ", 1).tolist(), columns=["CustomerFirstName", "CustomerLastName"])
print(split1.head())
# https://stackoverflow.com/questions/14745022/how-to-split-a-dataframe-string-column-into-two-columns


file1.close()