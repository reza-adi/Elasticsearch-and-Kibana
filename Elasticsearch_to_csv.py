# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:52:37 2019

@author: reza
"""
    
import urllib.request
import elasticsearch
import csv

es = elasticsearch.Elasticsearch('http://your elasticsearch address:9200', verify_certs=False, timeout=30, max_retries=5, retry_on_timeout=True)
#your Elasticsearch query
query = {
    "query": {
    "bool": {
      "must": [
        {
          "match": {
            "store.url": "client1"
          }
        }
      ]
    }
  },
  "size": 2500
}
res = es.search(index='productsg', doc_type='product', body=query)

with open('client1_urls.csv', 'w') as file:
    header_present  = False
    for doc in res['hits']['hits']:
        my_dict = doc
        my_dict2 = doc['_source']
        my_dict.update(my_dict2)
        if not header_present:
            output = csv.DictWriter(file, my_dict.keys())
            output.writeheader()
            header_present = True

        output.writerow(my_dict)

