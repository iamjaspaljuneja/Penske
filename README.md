# Penske Fall 2023 Dynamic Pricing Project

## Project Scope
Penske's onDemand fleet is an additional opportunity for revenue. To optimize the pricing of these onDemand trucks, a dynamic pricing model can be implemented. This project utilizes three statistical models to create a model that can predict utilization: linear regression, gradient boosting, and random forest regression. This predicts the utilzation rates of various trucks on a given date using weather and prior utilization rate information. These model's output can then be used to understand the supply and demand dynamics, which in turn, allows us to understand how trucks can be adequately priced.

## Flow of Script Usage
1. Gather data (utilization, transaction, weather, etc)
2. Run the data aggregation scripts.
3. Input the data file output from part two into the models.
4. Analyze output and utilize the pricing optimization script to determine a price for the trucks that would maximize utilization.

## Technologies Used
* Google Colab: train and execute these models
* Python3, libraries: scikit-learn and pandas were used to write the program
* GitHub and Git: Version control

## How to download repository
1. Move to the directory you want to clone this respository.
```
cd /path
```

2. Clone this respository using the command below. This assumes you already have Git set up properly.

```
git clone https://github.com/mausaye/Penske_F23.git
```

3. Now that you have copied the repository, you can modify it in any way. To make changes you can use the commands below:
```
git add (insert changed files to add to staging area)
git commit -m "message for commit"
git push
``` 

## How to run the data aggregation script (grouped by transaction)
1. Find the file<span style="color:lightblue"> data_agg_script.py</span>.
2. Updates these lines of code to be specific to the city desired. You will need utilization data, transaction data, and weather data.
```
df = pd.read_excel('utilization data.xlsx")

ld_trans = pd.read_excel('path to transaction data.xslx')

weather = pd.read_excel('path to weather.xlsx')
```
Fields used to filter the data documents by a specific city. These fields must match the contents of the dataset provided.
```
district_id = "XXXX"
city = "City_Name"
district =  "XXXX - City_Name    "
```
4. Click **Run** and the results of the script will be saved to <span style="color:lightblue">Data_City.xlsx</span>

## How to run data aggregation script (grouped by date)
1. Find the file <span style="color:lightblue"> Data Aggregation.ipynb</span>
2. Ensure that these file paths are correct and correspond to the specific city.
```
df = pd.read_excel('Utilization.xlsx', sheet_name='All Data')

transactions = pd.read_excel('Transactions.xlsx', sheet_name='All Data')

weather = pd.read_excel('Weather.xlsx', sheet_name='Sheet1')
```
4. Ensure these fields are correct and correspond to the correct city.
```
district_id = "XXXX"
district_str = 'XXXX - City_Name    '
```

5. Click **Run** and the results of the script will be saved to <span style="color:lightblue">Data_City.xlsx</span>

## How to run the statistical models
1. Install dependecies, if needed.

2. Open up Jupyter Notebook. These files have a <span style="color:lightblue">.ipynb</span> extension.

3. Make sure the paths of the data files are in the expected directory.
```
ld_trans = pd.read_excel("path to transaction files.xslx")
util = pd.read_excel("path to utilization data.xslx")
```

4. Click **Run All** and the results of the model will be displayed once finished.

## How to run the price optimization script
