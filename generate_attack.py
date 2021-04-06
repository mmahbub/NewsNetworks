import pandas as pd
import numpy as np
import argparse
import random 
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
import re
from copy import deepcopy

def adv_attack(source, rel_df, unrel_df, data, ratio):
    s = unrel_df[unrel_df['source']==source]
    n = int(round(s.shape[0]*(ratio/100),0))
    sample_rel = rel_df.sample(n)
    source_list = sample_rel['source'].values.tolist()
    cols = ['id', 'source', 'author']

    adv_cols = []
    for i in range(len(cols)):
        adv = []
        col_cont = sample_rel[cols[i]].values.tolist()
        for j in range(len(col_cont)):
            y = re.sub(str(source_list[j]), source, str(col_cont[j]))
            adv.append(y)
        adv_cols.append(adv)
                
    df_adv = pd.DataFrame()
    df_adv['id'] = adv_cols[0]
    df_adv['date'] = sample_rel['date'].values.tolist()
    df_adv['source'] = adv_cols[1]
    df_adv['title'] = sample_rel['title'].values.tolist()
    df_adv['content'] = sample_rel['content'].values.tolist()
    df_adv['author'] = adv_cols[2]
    df_adv['url'] = sample_rel['url'].values.tolist()
    df_adv['published'] = sample_rel['published'].values.tolist()
    df_adv['published_utc'] = sample_rel['published_utc'].values.tolist()
    df_adv['collection_utc'] = sample_rel['collection_utc'].values.tolist()
    df_adv['label'] = sample_rel['label'].values.tolist()
    return df_adv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to data folder")
    parser.add_argument("--percentage", type=str, help="Percentage of unreliable source articles to be used for inflation")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    path = args.input
    ratio = args.percentage

    data = pd.read_csv(path+'/data.csv')
    rel_df = data[data['label']==0]
    unrel_df = data[data['label']==1]

    unrl_sources = unrel_df['source'].unique()
    df_ls = []
    for s in unrl_sources:
        df_ls.append(adv_attack(s, rel_df, unrel_df, data, int(ratio)))

    df = pd.DataFrame()
    df_ls.append(data)
    df = pd.concat(df_ls).reset_index(drop=True)
    df['published_utc'] = df['published_utc'].astype('Int64')
    df['collection_utc'] = df['collection_utc'].astype('Int64')
    df['label'] = df['label'].astype('Int64')
    
    df.to_csv(path+'/data_'+str(ratio)+'.csv', index=False)
