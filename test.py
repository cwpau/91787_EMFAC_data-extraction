import pandas as pd


lista = list(range(8,51,1))
print(lista)
index = list(range(1,25,1))
index = [str(x) for x in index]

df = pd.DataFrame(lista*24, columns = index)
print(df)