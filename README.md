# Adversarial NewsNetworks

steps:
  1. Export unperturbed data (saved in **data** table) from database to a csv file: 
  
      a) `.header on`
      
      b) `.mode csv`
      
      c) `.output data_folder_path/data.csv`
      
      d) `SELECT * FROM data;`
      
  2. Generate and save perturbed data: 
      a) `python3 generate_attack.py --input data_folder_path --percentage n`
      
      **Example:** Say for n = 5, 
      
      `python3 generate_attack.py --input /home/75y/Documents/CSN/data --percentage 5`
      
  3. After executing step 2 with n = 5, we will have a csv file with perturbed data saved as `data_5.csv`
  4. Next launch the NELA database: `sqlite3 nela-gt-2020.db`
  5. Drop the `data` table: `DROP TABLE data;`
  6. Import the perturbed data `data_5.csv` to the database: 
  
      a) `.mode csv`
      
      b) `.import data_5.csv data_5`
      
  7. Generate network: 
      ```./generate_network.py --input proj_dir/nela-gt-2020.db --output_pair_file out_dir/pair_file_5.csv --output_network_file out_dir/network_5.gml --initial_date 2020-04-09```
  8. repeat steps 2-7 for n = 5, 10, 15, 20, 25, 30, 35, 40, 45, 50
  10. Look out for file names for pair_file and network_file.
