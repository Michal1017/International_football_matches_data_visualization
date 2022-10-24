import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
df['year'] = df['date'].str.extract(r'([0-9]{4})', expand=True).astype(int)
df['month'] = df['date'].str.extract(r'-([0-9]{2})-', expand=True).astype(int)
df['day'] = df['date'].str.extract(r'-([0-9]{2})$', expand=True).astype(int)

# Check how dataset looks with new features
print(df.head())

# Print information about dataset
print(df.info())

# Print statistics of dataset
print(df.describe())

# Function which help visualize better number of matches through time


def get_range_years(x):
    if(x < 1875):
        return '1850-1874'
    if(1875 <= x < 1900):
        return '1875-1899'
    if(1900 <= x < 1925):
        return '1900-1924'
    if(1925 <= x < 1950):
        return '1925-1949'
    if(1950 <= x < 1975):
        return '1950-1974'
    if(1975 <= x < 2000):
        return '1975-1999'
    if(2000 <= x < 2025):
        return '2000-2024'


df['ranged_years'] = df['year'].apply(get_range_years)


# Plot how many matches was played in every year
sns.barplot(df['ranged_years'].value_counts().index,
            df['ranged_years'].value_counts().values)
plt.title('Number of matches in specific year')
plt.show()

# Plot how many games was played in each month
sns.barplot(df['month'].value_counts().index,
            df['month'].value_counts().values)
plt.title("Number of matches in each month")
plt.show()

# Plot how many games was played in each tourmament
sns.barplot(df['tournament'].value_counts().index[:10],
            df['tournament'].value_counts().values[:10])
plt.title('Number of matches in each tourmament')
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
      df['home_score'].values.sum()+df['home_score'].values.sum())


countries_and_goals = []

print(df.iloc[0]['home_team'])



    