import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('results.csv')

print("First five elements of dataset: ")
print(df.head())

print("Size of dataset: ")
print(df.shape)

print("Number of missing data: ")
print(df.isnull().sum())

df.dropna(inplace=True)

print("Number of missing data: ")
print(df.isnull().sum())

df['year'] = df['date'].str.extract(r'([0-9]{4})', expand=True).astype(int)
df['month'] = df['date'].str.extract(r'-([0-9]{2})-', expand=True).astype(int)
df['day'] = df['date'].str.extract(r'-([0-9]{2})$', expand=True).astype(int)

print(df.head())

print(df.info())

print(df.describe())

sns.barplot(df['year'].value_counts().index, df['year'].value_counts().values)
plt.title('Number of matches in specific year')
plt.show()

sns.barplot(df['month'].value_counts().index,
            df['month'].value_counts().values)
plt.title("Number of matches in specific month")
plt.show()

sns.barplot(df['tournament'].value_counts().index[:10],
            df['tournament'].value_counts().values[:10])
plt.show()

# all goals scored by team

home_countries = df['home_team'].unique()
away_countries = df['away_team'].unique()

no_home_game = list(set(away_countries) - set(home_countries))
no_away_game = list(set(home_countries) - set(away_countries))

countries = set(list(home_countries) + list(away_countries))

print("Countries with no home game:")
print(no_home_game)

print("Countries with no away game:")
print(no_away_game)

