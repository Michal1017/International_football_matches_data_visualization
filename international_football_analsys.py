from typing_extensions import Self
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import null, values

# read data from csv file
df = pd.read_csv('results.csv')

# print fisrt 5 elements of dataset
print("First five elements of dataset: ")
print(df.head())

# print shape of dataset
print("Size of dataset: ")
print(df.shape)

# print missing values
print("Number of missing data: ")
print(df.isnull().sum())

# Delete elements with missing data
df.dropna(inplace=True)

# Check if there is not missing data
print("Number of missing data: ")
print(df.isnull().sum())

# Extract year, month and day of specific data
#df['year'] = df['date'].str.extract(r'([0-9]{4})', expand=True).astype(int)
df['date'] = pd.DatetimeIndex(df['date'])

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

df['total_goals'] = df['home_score'] + df['away_score']


def winning_team(x):
    if(x.home_score > x.away_score):
        return x.home_team
    if(x.home_score < x.away_score):
        return x.away_team
    else:
        return None


def defeated_team(x):
    if(x.home_score > x.away_score):
        return x.away_team
    if(x.home_score < x.away_score):
        return x.home_team
    else:
        return None


df['winner'] = df.apply(winning_team, axis=1)

df['loser'] = df.apply(defeated_team, axis=1)
# Check how dataset looks with new features
print(df.head())

# Print information about dataset
print(df.info())

# Print statistics of dataset
print(df.describe())

sns.lineplot(x=df['year'].value_counts().index, y=df['year'].value_counts())
plt.title('Number of played matches through years')
plt.xlabel('year')
plt.ylabel('Number of matches')
plt.show()

# Plot how many games was played in each month
sns.histplot(df['month'])
plt.title("Number of matches in each month")
plt.ylabel('Number of matches')
plt.show()

# Plot how many games was played in each tourmament
sns.barplot(df['tournament'].value_counts().index[:10],
            df['tournament'].value_counts().values[:10])
plt.title('Number of matches in each tourmament')
plt.ylabel('Number of matches')
plt.show()


home_countries = df['home_team'].unique()
away_countries = df['away_team'].unique()

no_home_game = list(set(away_countries) - set(home_countries))
no_away_game = list(set(home_countries) - set(away_countries))

countries = set(list(home_countries) + list(away_countries))

print("Countries with no home game:")
print(no_home_game)

print("Countries with no away game:")
print(no_away_game)

# All goals
print("All goals scored in international football matches: ",
      df['total_goals'].values.sum())


print(df.iloc[0]['home_team'])

ser = df['home_team'].value_counts() + df['away_team'].value_counts()

print(ser.index)

countries_df = pd.DataFrame({'Country': ser.index,
                             'Matches': ser.values.astype(int)})

won_matches_by_country = df['winner'].value_counts()
lost_matches_by_country = df['loser'].value_counts()

print(won_matches_by_country.sort_values())


def matches_result(x, series):
    if series.index.isin([x]).any():
        return series[x]
    else:
        return 0


countries_df['Wins'] = countries_df['Country'].apply(
    matches_result, series=won_matches_by_country)

countries_df['Losses'] = countries_df['Country'].apply(
    matches_result, series=lost_matches_by_country)

countries_df['Draws'] = countries_df['Matches'] - \
    countries_df['Wins'] - countries_df['Losses']

countries_df['Percent of won games'] = countries_df['Wins'] * \
    100/countries_df['Matches']


print(countries_df)

print(df[df['home_team'] == 'England']['home_score'].sum())
