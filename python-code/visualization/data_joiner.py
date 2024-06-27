import pandas as pd
data_path = "./data/df_mc.csv"
df_00 = pd.read_csv(data_path)
data_path = "./data/df_mc_2024-04-17_11:15.csv"
df = pd.read_csv(data_path)

df_mc = pd.concat([df_00, df_01])
df_mc.to_csv("./data/df_mc__.csv", index=False)
df_mc.to_csv("./data/df_mc_2024-04-17_17:50.csv", index=False)
