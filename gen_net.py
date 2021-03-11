#!/usr/bin/env python

import argparse, sqlite3, re, logging
from pathlib import Path
from threading import Thread
from datetime import datetime, timedelta

import numpy as np
import networkx as nx
from itertools import combinations
from operator import itemgetter

from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from networkx.algorithms.components.connected import connected_components
from nltk.corpus import stopwords

logging.basicConfig(
  format="[%(name)s] %(levelname)s -> %(message)s")
logger = logging.getLogger('gen_net')
logger.setLevel(logging.INFO)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-db', '--database', type=str, help='Path to NELA database', required=True)
  parser.add_argument('-pf', '--pair_file', type=str, help='Path to save CSV file', required=True)
  parser.add_argument('-nf', '--network_file', type=str, help='Path to save GML file', required=True)
  parser.add_argument('-ho', '--heuristics_off', action='store_true', help='Turn off heuristic functions (Not recommended)')
  parser.add_argument('-d', '--date', type=str, help='YYYY-mm-dd format for initial date of articles', default='2020-04-09')
  parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
  args = parser.parse_args()
  
  dbfile = Path(args.database)
  pair_file_path = Path(args.pair_file)
  init_date = args.date
  start_date = datetime.strptime(args.date, '%Y-%m-%d') 
  dtime = timedelta(days=4)
  logger.info(f"Database File: {dbfile}")
  logger.info(f"Pair File: {pair_file_path}")
  logger.info(f"Start Date: {start_date}")
  logger.info(f"Time Delta: {dtime}")  

  