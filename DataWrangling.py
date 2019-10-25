import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib import pyplot
# URL to import data
filename = "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/auto.csv"
# Name for each column
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
# Define de dataframe by reading data from the url provided and set the name of each column
df = pd.read_csv(filename, names = headers)
# Replace missing data form ? to NaN, detect the missing data and count the missing data of each column
df.replace("?", np.nan, inplace = True)
missing_data = df.isnull()
for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")
# Calculate the average of the columns
avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
print("Average of normalized-losses:", avg_norm_loss)
avg_bore=df['bore'].astype('float').mean(axis=0)
print("Average of bore:", avg_bore)
avg_stroke = df["stroke"].astype("float").mean(axis = 0)
print("Average of stroke:", avg_stroke)
avg_horsepower = df['horsepower'].astype('float').mean(axis=0)
print("Average horsepower:", avg_horsepower)
avg_peakrpm=df['peak-rpm'].astype('float').mean(axis=0)
print("Average peak rpm:", avg_peakrpm)
# Replace NaN by mean value
df["normalized-losses"].replace(np.nan, avg_norm_loss, inplace=True)
df["bore"].replace(np.nan, avg_bore, inplace=True)
df["stroke"].replace(np.nan, avg_stroke, inplace = True)
df['horsepower'].replace(np.nan, avg_horsepower, inplace=True)
df['peak-rpm'].replace(np.nan, avg_peakrpm, inplace=True)
# Check the most common type of number of doors to replace the missing values
print('The most common type of number of doors is: '+df['num-of-doors'].value_counts().idxmax())
df["num-of-doors"].replace(np.nan, "four", inplace=True)
# Drop all rows that do not have a price data and reset index
df.dropna(subset=["price"], axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)
# Convert data type of bore, stroke and price to float; data type of analyzed losses to int
df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")
# Convert city and highway mpg to L/100Km
df['city-L/100km'] = 235/df["city-mpg"]
df['highway-L/100km'] = 235/df["highway-mpg"]
# Normalize length, width and height data by replacing value by originalValue/MaximumValue
df['length'] = df['length']/df['length'].max()
df['width'] = df['width']/df['width'].max()
df['height'] = df['height']/df['height'].max()
# Convert horsepower data to int
df["horsepower"]=df["horsepower"].astype(int, copy=True)
# Plot histogram of horsepower
#plt.pyplot.hist(df["horsepower"])
#plt.pyplot.xlabel("Horsepower")
#plt.pyplot.ylabel("Count")
#plt.pyplot.title("Horsepower")
# Crete four equally spaced values for bins and the names for each group.
bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
group_names = ['Low', 'Medium', 'High']
# Set each value to the group it belongs
df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True )
# Plot the distribution of each bin
pyplot.bar(group_names, df["horsepower-binned"].value_counts())
plt.pyplot.xlabel("Horsepower")
plt.pyplot.ylabel("Count")
plt.pyplot.title("Horsepower Bins")
# Create dummy variables for fuel type and aspiration, merge the data from the dummy variables to the original data frame and drop the fuel-type and aspiration column
dummy_variable_1 = pd.get_dummies(df["fuel-type"])
dummy_variable_2 = pd.get_dummies(df['aspiration'])
dummy_variable_1.rename(columns={'fuel-type-diesel':'gas', 'fuel-type-diesel':'diesel'}, inplace=True)
dummy_variable_2.rename(columns={'std':'aspiration-std', 'turbo': 'aspiration-turbo'}, inplace=True)
df = pd.concat([df, dummy_variable_1], axis=1)
df.drop("fuel-type", axis = 1, inplace=True)
df = pd.concat([df, dummy_variable_2], axis=1)
df.drop('aspiration', axis = 1, inplace=True)
# Save the data frame to a .csv file
df.to_csv('clean_dataframe.csv')
