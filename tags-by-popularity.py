import csv
import pandas as pd
import argparse

def process_tag_data(input_csv):
    with open(input_csv, 'r', encoding = 'utf8') as csvfile:
        df = pd.read_csv(csvfile)

    rows = [
        {'Tag': tag, 'Inverse Obscurity': 5 - row['Popularity (5=most obscure)']}
        for _, row in df.dropna(subset=['Tags']).iterrows()
        for tag in row['Tags'].split(' // ')
    ]

    tags_with_popularity = pd.DataFrame(rows)
    tag_popularity_summary = tags_with_popularity.groupby('Tag')['Inverse Obscurity'].sum().reset_index()
    tag_count = tags_with_popularity.groupby('Tag').size().reset_index(name='Count')

    return tag_popularity_summary, tag_count

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process a CSV file for tag popularity.')
    parser.add_argument('inputcsv', type=str, help='Input CSV file path')
    args = parser.parse_args()

    tag_popularity_summary, tag_count = process_tag_data(args.inputcsv)

    # Export the DataFrames to new CSV files
    tag_popularity_summary.to_csv('tag_popularity.csv', index=False)
    tag_count.to_csv('tag_count.csv', index=False)