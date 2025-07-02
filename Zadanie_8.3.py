import pandas as pd
import matplotlib.pyplot as plt

url_incidents = r"D:\KODILLLA\wizualizacje\fatal-police-shootings-data.csv"
df = pd.read_csv(url_incidents)

# Liczba ofiar według rasy i oznak choroby psychicznej
grouped = df.groupby(['race', 'signs_of_mental_illness']).size().unstack(fill_value=0)
true_vals = grouped.get(True, pd.Series(0, index=grouped.index))
false_vals = grouped.get(False, pd.Series(0, index=grouped.index))
grouped['% z chorobą psychiczną'] = grouped[True] / (grouped[True] + grouped[False]) * 100
print("\nOfiary wg rasy i chorób psychicznych:\n", grouped)

highest_rate = grouped['% z chorobą psychiczną'].idxmax()
print("\nRasa z najwyższym odsetkiem chorób psychicznych:", highest_rate)

# Dni tygodnia i ilosć wystapień
df['date'] = pd.to_datetime(df['date'])
df['weekday'] = df['date'].dt.day_name()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_counts = df['weekday'].value_counts().reindex(weekday_order)

# Wykres kolumnowy
plt.figure(figsize=(10, 6))
weekday_counts.plot(kind='bar', color='green')
plt.title('Interwencje policji per day')
plt.ylabel('Liczba interwencji')
plt.xlabel('Day')
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# Dane o populacji i skrótach stanów
url_population = 'https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population'
df_pop = pd.read_html(url_population, header=0)[0]
population = df_pop[['State', 'Census population, April 1, 2020 [1][2]']].copy()
population.columns = ['State', 'Population']

url_abbr = 'https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations'
df_abbr = pd.read_html(url_abbr, header=0)[2]
abbr = df_abbr[['State', 'USPS Code']].copy()
abbr.columns = ['State', 'Abbreviation']

pop_combined = population.merge(abbr, on='State', how='inner')
incidents_by_state = df['state'].value_counts().reset_index()
incidents_by_state.columns = ['Abbreviation', 'Incidents']

# Połączenie wszystkich danych, sortowanie
df_final = pop_combined.merge(incidents_by_state, on='Abbreviation', how='left')
df_final['Incidents'].fillna(0, inplace=True)
df_final['Incidents'] = df_final['Incidents'].astype(int)
df_final['Per_1000'] = df_final['Incidents'] / df_final['Population'] * 1000
df_final_sorted = df_final.sort_values(by='Per_1000', ascending=False)
print("\nIncydenty na 1000 mieszkańców:\n", df_final_sorted[['State', 'Abbreviation', 'Per_1000']])