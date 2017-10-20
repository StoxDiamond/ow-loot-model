import json
import pandas as pd
import numpy as np 

def ImportCollectionJson(fileName):
    with open(fileName, encoding='utf8') as data_file:
        data = json.load(data_file)
    l = []
    for character in data:
        for item_type in data[character]:
            for item in data[character][item_type]:
                if data[character][item_type][item] == True:
                    l.append(item)
    coll = pd.Series(l)
    coll_df = pd.DataFrame(coll)
    coll_df['owned'] = True
    return coll_df.set_index(0)

def ImportDatabaseJson(fileName):
    with open(fileName, encoding='utf8') as data_file:
        data = json.load(data_file)
    l = []
    for character in data:
        for item_type in data[character]['items']:
            for e in data[character]['items'][item_type]:
                rarity = e['quality'] if 'quality' in e else ''
                event = e['event'] if 'event' in e else ''
                group = e['group'] if 'group' in e else ''
                standard = e['standardItem'] if 'standardItem' in e else False
                new = e['isNew'] if 'isNew' in e else False
                t = (e['id'], e['name'], item_type, rarity, event, group, standard, new)
                l.append(t)
    return pd.DataFrame(data=l, index=[x[0] for x in l], columns=['id', 'name', 'type', 'rarity', 'event', 'group', 'standard', 'new'])

# Blizzard Official
# Each loot box contains a rare or better 
# On average, every 5.5 loot boxes contain an item of epic quality
# On average, every 13.5 loot boxes contain an item of legendary quality
# Reddit empirical measurements: https://www.reddit.com/r/Overwatch/comments/4mbpz9/loot_box_drop_rate_1000_boxes_sample_size/
# Return: Tuple of individual probabilities of a rare/epic/legendary per item
def StandardBoxCdf():
    return np.cumsum(1/(np.array([13.5, 5.5, .75])*4))

# Simple simulation of rarity opened in a bunch of loot boxes
def StandardBoxSimulation():
    p_rob = StandardBoxCdf();
    boxes = 100000
    count = [0,0,0,0]
    for _ in range(boxes):
        for i in range(4):
            r = np.random.rand(1)
            if r < p_rob[0]:
               count[0] += 1
            elif r < p_rob[1]:
               count[1] += 1
            elif r < p_rob[2]:
               count[2] += 1
            else:
               if i == 4:
                   count[2] += 1
               else: 
                   count[3] += 1
    return 1.0 * boxes / np.array(count)
    
# 1. Import user's collection in simulation
# 2. Filter out unused items (achievement sprays, drops from other box types)
# 3. Pick a random item after rarity is determined; weighted based on user's collection
# 4. Factor in gold drops when picking a random item (higher weight)
# 5. When a duplicate is dropped, award gold
      
# Returns a collection of structures that make up the model
# Takes database of items, user's collection, loot table config file
def InitializeModel(databaseFile, collectionFile):
    db = ImportDatabaseJson(databaseFile)
    cl = ImportCollectionJson(collectionFile)
    db = db.merge(cl, left_index=True, right_index=True, how='left').fillna(False)
    return db
        



















