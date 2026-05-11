import requests

import pandas as pd
from io import StringIO

urls = [
  {
    "name" : "human_result",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/8eb7f207-1ce5-460c-b941-5f1761a79c46"
  },
  {
    "name" : "operation_stats",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/5d3c65fb-c861-4b22-b8aa-1eab58e3d9db"
  },
  {
    "name" : "flotteurs",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/ae0e17e4-7117-45f0-80c4-b11b38f31c5c"
  },
  {
    "name" : "operations",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/fae6bc13-fe4c-4838-b281-b16628b7babe"
  }
]

for item in urls:
  res = requests.get(item['url'])
  data = StringIO(res.content.decode("utf-8"))
  df = pd.read_csv(data,sep=',',low_memory=False)
  df.to_csv(f'./data/{item['name']}.csv')

