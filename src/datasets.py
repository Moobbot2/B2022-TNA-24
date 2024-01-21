import pandas as pd
from config import FEATURES, KQ, OUTPUT_LINK

df = pd.read_excel(OUTPUT_LINK)

X = df[FEATURES]
Y = df[KQ]