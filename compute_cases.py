import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
import sys
import collections
import time

def plot_fig(interested_countries, fn, last_update):
    fig = plt.figure(figsize=(12, 8))
    plt.rcParams['font.size'] = 14
    legends = []
    for country, cnts in interested_countries.items():
        plt.semilogy(cnts)
        legends.append(country + ' ({})'.format(int(cnts[-1])))

    plt.grid(axis='y')
    plt.legend(legends, loc='lower right')
    plt.ylabel('Number of confirmed cases')
    plt.xlabel('Number of days since passing 100 cases')
    plt.title('Confirmed cases since passing 100 cases.\n(Last update: {})'.format(last_update))
    fig.savefig(fn)

def union_dict(dict1, dict2):
    out = {k:v for k, v in dict1.items()}
    for k, v in dict2.items():
        if k not in dict1:
            out[k] = v
    return out

def main():
    # download new data
    input_fn = 'confirmed.csv'
    data_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    cmd = "curl -o {} {}".format(input_fn, data_path)
    os.system(cmd)

    # load data
    confirmed_cases = pd.read_csv(input_fn)
    confirmed_cases = confirmed_cases.drop(['Province/State', 'Lat', 'Long'], axis=1)
    country_sum = confirmed_cases.groupby('Country/Region').sum()
    last_update = country_sum.columns[-1]

    country_names = country_sum.index.tolist()
    country_counts = country_sum.values
    country_counts_100 = collections.defaultdict(list)
    cnts_to_sort = collections.defaultdict(int)
    for r in range(len(country_counts)):
        for c in range(len(country_counts[r])):
            current_cnt = country_counts[r][c]
            if current_cnt >= 100:
                country_counts_100[country_names[r]].append(current_cnt)
        cnts_to_sort[country_names[r]] = current_cnt

    # print(sorted(country_names))
    sorted_countries = sorted(cnts_to_sort.items(), key=lambda kv: kv[1], reverse=True)

    interested_countries = set([c for c, _ in  sorted_countries[:5]] + ['US', 'Korea, South', 'Canada'])
    referenced_countries = {'China', 'Italy'}
    interested_countries = interested_countries.difference(referenced_countries)

    interested_countries = {c:cnts for c, cnts in country_counts_100.items() if c in interested_countries}
    referenced_countries = {c:cnts for c, cnts in country_counts_100.items() if c in referenced_countries}

    print('\ninterested_countries: ', interested_countries)
    print('\nreferenced_countries: ', referenced_countries)

    img_fol = 'images'
    os.system('rm {}/*'.format(img_fol))
    plot_fig(union_dict(interested_countries, referenced_countries), img_fol + '/1.png', last_update)
    cnt = 2
    for country, cnts in interested_countries.items():
        plot_fig(union_dict(referenced_countries, {country:cnts}), '{}/{}.png'.format(img_fol, cnt), last_update)
        cnt += 1

if __name__ == '__main__':
    main()
