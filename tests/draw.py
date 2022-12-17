import sys
import pandas as pd

path = sys.argv[1]
data = pd.read_csv(path)
print(data)