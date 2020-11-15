#!/usr/bin/env python3

import json
import pandas as pd

from clean import clean

src = pd.read_json('articles.json').astype(str)
dst = list()
for id, article in src.iterrows():
  dst.append({"id": id, "query": clean(article['title'])})

with open('articles_clean.json', 'w') as f:
  json.dump(dst, f, ensure_ascii=False)
