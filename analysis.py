import sqlite3
import re
import pandas as pd

conn = sqlite3.connect('cars.db')
df = pd.read_sql_query("SELECT * FROM cars_tb", conn)
brands = ["acura", "alfa romeo", "audi", "bmw", "brilliance", "byd", "cadillac",
          "changan", "chery", "chevrolet", "chrysler", "citroen", "daewoo", "Daihatsu",
          "dodge", "donfeng", "ferrari", "fiat", "ford", "foton", "freightliner", "gmc",
          "geely", "gonow", "great wall", "haima", "higer", "hino", "honda", "hummer",
          "hyundai", "infiniti", "international", "isuzu",
          "iveco", "jac", "jmc", "jaguar", "jeep", "kia", "land rover", "lexus", "lifan",
          "mg", "mahindra", "maserati", "mazda", "mercedes benz", "mini", "mitsubishi",
          "nissan", "peterbilt", "peugeot", "porsche", "renault", "sang yong", "seat",
          "smart", "soueast", "ssang yong", "subaru", "suzuki", "tianma", "toyota",
          "volkswagen", "volvo", "/ram"]

pattern_template = "{}"
pattern = "(" + "|".join([pattern_template.format(brand) for brand in brands]) + ")"
df['brand'] = df['marca'].str.extract(pattern, flags=re.IGNORECASE, expand=False).str.strip()
df['model'] = df['modelo'].str.replace(pattern, '', flags=re.IGNORECASE).str.strip().replace('\s+', ' ', regex=True)

df_split_model = df['model'].str.split(' ', expand=True).add_prefix('model_split').fillna('N/A')
df = df.join(df_split_model)
df.to_sql("cars_clean_tb", conn)
# pd.set_option('display.max_column', 3)
# pd.set_option('display.max_row', 100)
# # null_df = df.loc[df['brand'].isnull()].unique()  # Unmatched values
# cars = df[['brand', 'model']]
# print(cars)

