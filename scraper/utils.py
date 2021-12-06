import csv
import json
from pathlib import Path

import pandas as pd

import scraper.santiment
from scraper._config import SANTIMENT_API_KEY



class classproperty(object):  # noqa
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def traverse_dict(original_dict):
    traversed = {}
    for name, accounts in original_dict.items():
        for account in accounts:
            traversed[account] = name

    return traversed


def save_csv(my_dict, file='results.csv'):
    with open(file, 'w') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.DictWriter(f, my_dict.keys())
        w.writeheader()
        w.writerow(my_dict)


def save_json(data, file='results.json'):
    with open(file, "w") as f:
        json.dump(data, f)
