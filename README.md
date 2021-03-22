# NewsNetworks

## Data Setup
The data we are working on is `NELA-GT-2020` which can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/CHMUYZ). The database file we will use is `nela-gt-2020`. To prep the data
we have to do a series of steps. These steps assume that you are in the directory of the database
file, you have `sqlite3` installed, and `labels.csv` is present in the same directory. Note some of the steps below will take a while to run.

1. Launch the database: `sqlite3 nela-gt-2020.db` (1779127 rows)
2. Load in the labels csv into a table.
3. Set csv mode: `.mode csv`
4. Load in the csv file: `.import labels.csv labels`
5. **NOT NEEDED: Since we want to only use sources that are either reliable (label=0) or unreliable (label=2), we are going to create another table with only those labels: `create table labels as select * from all_labels where label=0 or label=2;`**
6. Sanity check: `select label, count(*) from labels group by label;`. This should return 0,194 1,128 2,222
7. We want to ignore the missing data from March and April. So for convenience, we are going to work with data that was collected from 4/9/2020. This corresponds to the UTC time of 1586404800. We create another table to hold this filtered data: `create table data_sub as select * from newsdata where published_utc >= 1586404800;`.
8. Sanity check: `select count(*) from data_sub;`. This should return 1384420.
9. Finally, we want the data with the correct sources (labels 0,1,2) and published at the correct times ( > 4/9). We can accomplish using an `inner join` to create our final data table: `create table data as select d.*, l.label from data_sub d inner join labels l on d.source=l.source;`
10. Sanity check: `select count(*), count(distinct source) from data;` (This should give `1833873,324`. This is because there was some data missing from the labeled sources due us removing a fourth of the data (we don't consider the 1st 3 months).)
  
## Network Generation
To generate a news outlet network using a NELA-GT database, simply run generate_network.py with command line arguments for: path to the nela database, path to write pair CSV file to, and path to save GML file to (GML file is the network file). Optionally, you can add the argument --initial_date in the form of YYYY-mm-dd string to start the network building on a specific date. Here is a more detailed look at the arguments:

```
parser.add_argument("input", type=str, help="Path to nela database")
parser.add_argument("output_pair_file", type=str, help="Path to write pair CSV file to")
parser.add_argument("output_network_file", type=str, help="Path to save GML file to")
parser.add_arguement("--heuristics_off", type="store_true", help="Turn off heuristic functions (We strongly recommend not doing this)")
parser.add_argument("--language", type=str, help="Language of the database")
parser.add_argument("--initial_date", type=str, help="YYYY-mm-dd string for initial date of articles")
parser.add_argument("--verbose", action="store_true", help="Verbose mode")
```

By default the network will normalize the edge weights by the number of total articles a source has published. 

## Command line code to generate network
```
./generate_network.py --input proj_dir/nela-gt-2020.db --output_pair_file out_dir/pair_file.csv --output_network_file out_dir/network.gml --initial_date 2020-04-09
```


## Citation when using code
Please cite the following work when using this code:

Horne, B. D., Nørregaard, J., & Adalı, S. (2019, July). Different spirals of sameness: A study of content sharing in mainstream and alternative media. In Proceedings of the International AAAI Conference on Web and Social Media (Vol. 13, pp. 257-266).

Bibtex:

```
@inproceedings{horne2019different,
  title={Different spirals of sameness: A study of content sharing in mainstream and alternative media},
  author={Horne, Benjamin D and N{\o}rregaard, Jeppe and Adal{\i}, Sibel},
  booktitle={Proceedings of the International AAAI Conference on Web and Social Media},
  volume={13},
  pages={257--266},
  year={2019}
}
```
