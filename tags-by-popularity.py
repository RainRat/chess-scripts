import csv
import pandas as pd
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process a CSV file for tag popularity.')
parser.add_argument('inputcsv', type=str, help='Input CSV file path')
args = parser.parse_args()

# Load the CSV file
df = pd.read_csv(args.inputcsv)

# Prepare the data by splitting tags and associating them with their popularity
rows = []
for _, row in df.dropna(subset=['Tags']).iterrows():
    for tag in row['Tags'].split(' // '):
        inverse_popularity = 5 - row['Popularity (5=most obscure)']
        rows.append({'Tag': tag, 'Inverse Popularity': inverse_popularity})

# Create a DataFrame from the processed rows
tags_with_popularity = pd.DataFrame(rows)

# Group by tag and sum the adjusted popularity
tag_popularity_summary = tags_with_popularity.groupby('Tag')['Inverse Popularity'].sum().reset_index()

# Export the DataFrame to a new CSV file
tag_popularity_summary.to_csv('tag_popularity.csv', index=False)

# Additionally, count the number of times each tag appears
tag_count = tags_with_popularity.groupby('Tag').size().reset_index(name='Count')

# Export the tag counts to a new CSV file
tag_count.to_csv('tag_count.csv', index=False)