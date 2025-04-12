import boto3

import pandas as pd
import numpy as np

df = pd.read_csv("/Users/mariolaczajkowska/anaconda_projects/python/project_mcz2/downloads/AB_US_2023.csv", low_memory=False)

print(df['name'].unique())
print(df['neighbourhood_group'].unique())
print(df['neighbourhood'].unique())
print(df['room_type'].unique())
print(df['minimum_nights'].unique())
print(df['number_of_reviews'].unique())
print(df['reviews_per_month'].unique())
print(df['calculated_host_listings_count'].unique())
print(df['availability_365'].unique())
print(df['number_of_reviews_ltm'].unique())
print(df['city'].unique())
print(df['price'].max)

df['LAT'] = pd.to_numeric(df['latitude'], errors='coerce')
df['LONG'] = pd.to_numeric(df['longitude'], errors='coerce')


print(df['price'].describe())


high_price = df[df['price'] > 2000]
print(f"Liczba bardzo wysokich cen (>1000): {len(high_price)}")
print(f"Procent: {len(high_price) / len(df) * 100:.2f}%")
#print(df['LAT'])
#print(df['LONG'])

print(df['city'].head())  
print(type(df['city']))   