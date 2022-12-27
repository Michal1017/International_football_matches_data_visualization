from typing_extensions import Self
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

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
df['date'] = pd.DatetimeIndex(df['date'])

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# Get total goals scored by each team
df['total_goals'] = df['home_score'] + df['away_score']

# function which return name of team which won for each match


def winning_team(x):
    if(x.home_score > x.away_score):
        return x.home_team
    if(x.home_score < x.away_score):
        return x.away_team
    else:
        return None

# function which return name of team which lost for each match


def defeated_team(x):
    if(x.home_score > x.away_score):
        return x.away_team
    if(x.home_score < x.away_score):
        return x.home_team
    else:
        return None


# create new features in dataset with information about winner and looser
df['winner'] = df.apply(winning_team, axis=1)

df['loser'] = df.apply(defeated_team, axis=1)

# Check how dataset looks with new features
print(df.head())

# Print information about dataset
print(df.info())

# Print statistics of dataset
print(df.describe())

# Plot number of played matches through years
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

# create a list with every country contained in dataset
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

# Count how many matches each team played
matches_num = df['home_team'].value_counts() + df['away_team'].value_counts()

# Create new dataset with data about each country
countries_df = pd.DataFrame({'Country': matches_num.index,
                             'Matches': matches_num.values.astype(int)})

# how many each country won matches
won_matches_by_country = df['winner'].value_counts()
lost_matches_by_country = df['loser'].value_counts()

print(won_matches_by_country.sort_values())

# function which return number value based on index of country


def matches_result(x, series):
    if series.index.isin([x]).any():
        return series[x]
    else:
        return 0


# create features with number of won, draw or lost matches by each country
countries_df['Wins'] = countries_df['Country'].apply(
    matches_result, series=won_matches_by_country)

countries_df['Losses'] = countries_df['Country'].apply(
    matches_result, series=lost_matches_by_country)

countries_df['Draws'] = countries_df['Matches'] - \
    countries_df['Wins'] - countries_df['Losses']

# create features with percent of won,draw or lost matches by each country
countries_df['Percent of won games'] = countries_df['Wins'] * \
    100/countries_df['Matches']

countries_df['Percent of lost games'] = countries_df['Losses'] * \
    100/countries_df['Matches']

countries_df['Percent of tied games'] = countries_df['Draws'] * \
    100/countries_df['Matches']

print(countries_df)

# create series with top winning, drawing and loosing coutries
top_winning_countries = countries_df.groupby('Country').sum()[['Matches', 'Percent of won games']].sort_values(
    by=['Percent of won games'], ascending=False).query('Matches >= 100').head(10)

top_drawing_countries = countries_df.groupby('Country').sum()[['Matches', 'Percent of tied games']].sort_values(
    by=['Percent of tied games'], ascending=False).query('Matches >= 100').head(10)

top_loosing_countries = countries_df.groupby('Country').sum()[['Matches', 'Percent of lost games']].sort_values(
    by=['Percent of lost games'], ascending=False).query('Matches >= 100').head(10)

# create barplots with created above series
sns.barplot(x=top_winning_countries.index,
            y=top_winning_countries['Percent of won games'])
plt.title('Countries with highest winning ratio with at least 100 matches')
plt.show()

sns.barplot(x=top_drawing_countries.index,
            y=top_drawing_countries['Percent of tied games'])
plt.title('Countries with highest drawing ratio with at least 100 matches')
plt.show()

sns.barplot(x=top_loosing_countries.index,
            y=top_loosing_countries['Percent of lost games'])
plt.title('Countries with highest loosing ratio with at least 100 matches')
plt.show()

# create dataframe with information only about world cup games
world_cup_df = df.loc[df['tournament'] == 'FIFA World Cup']

best_WC_winners = world_cup_df['winner'].value_counts().head(10)

best_WC_losers = world_cup_df['loser'].value_counts().head(10)

sns.barplot(x=best_WC_winners.index,
            y=best_WC_winners)
plt.title('Countries with the biggest number of wins on World Cup')
plt.show()

sns.barplot(x=best_WC_losers.index,
            y=best_WC_losers)
plt.title('Countries with the biggest number of lost matches on World Cup')
plt.show()
