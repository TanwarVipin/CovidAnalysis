import pandas as pd
import numpy as np


def country(df):
    x = df.Country.unique().tolist()
    # y=df1.Country.unique().tolist()
    x.sort()
    x.insert(0,'Overall')
    return x


def get(df, country):
    if country == 'Overall':
        return df
    else:
        df = df[df['Country'] == country].set_index('Country')
        return df


def get1(df, country):
    if country == 'Overall':
        df1 = df.set_index('Country')
        df1 = df1.apply(lambda x: x.str.replace(',', '').replace('Missing Values', 0).astype(int))
        return df1
    else:
        df2 = df.set_index('Country')
        df2 = df2.apply(lambda x: x.str.replace(',', '').replace('Missing Values', 0).astype(int))
        df2 = df2.loc[country].reset_index().rename(columns={'index': 'Stats', country: 'Count'})
        return df2


def get2(df, country):
    x = df[df['Country'] == country][['Date_reported', 'New_deaths', 'Cumulative_deaths']].set_index('Date_reported')
    y = df[df['Country'] == country][['Date_reported', 'New_cases', 'Cumulative_cases']].set_index('Date_reported')
    return x, y


def get3(df, country, year):
    if country == 'Overall':
        x = df[df['Year'] == year].groupby('Country', as_index=False)['New_cases'].sum().sort_values(by='New_cases',
                                                                                                     ascending=False).head(
            10)
        y = df[df['Year'] == year].groupby('Country', as_index=False)['New_deaths'].sum().sort_values(by='New_deaths',
                                                                                                      ascending=False).head(
            10)
        return x, y
    else:
        month = df.Month.unique().tolist()
        x = df[(df['Year'] == year) & (df['Country'] == country)].groupby('Month', as_index=False)[
            ['New_cases', 'Cumulative_cases']].sum().sort_values(by='Month',
                                                                 key=lambda x: pd.Categorical(x, month, ordered=True))
        y = df[(df['Year'] == year) & (df['Country'] == country)].groupby('Month', as_index=False)[
            ['New_deaths', 'Cumulative_deaths']].sum().sort_values(by='Month',
                                                                   key=lambda x: pd.Categorical(x, month, ordered=True))
        return x, y
