import pandas as pd

# Wczytaj dane ze strony
url = 'https://www.officialcharts.com/chart-news/the-best-selling-albums-of-all-time-on-the-official-uk-chart__15551/'
tables = pd.read_html(url, header=0)
df = tables[0]

# Wstępne czyszczenie
df = df.drop(columns=['POS'])
df.columns = ['TYTUŁ', 'ARTYSTA', 'ROK', 'MAX POZ']

# Unikalni artyści bez duetów (feat., &, and)
individual_artists = df['ARTYSTA'].dropna().unique()
individual_artists = [
    artist for artist in individual_artists
    if all(x not in artist.lower() for x in ['feat.', '&', ' and '])
]
print("Liczba unikalnych artystów bez duetów:", len(individual_artists))

# Najczęściej występujący artyści
most_artists = df['ARTYSTA'].value_counts()
print("\nNajczęściej występujący artyści:")
print(most_artists.head())

# Poprawa nagłówków (tylko pierwsza litera wielka)
df.columns = [col.capitalize() for col in df.columns]

# Usuń kolumnę „Max poz”
if 'Max poz' in df.columns:
    df = df.drop(columns=['Max poz'])

# Rok z największą liczbą albumów
most_year = df['Rok'].value_counts().idxmax()
print("\nNajwięcej albumów wydano w roku:", most_year)

# Albumy z lat 1960–1990
album_6090s = df[(df['Rok'] >= 1960) & (df['Rok'] <= 1990)]
print("Liczba albumów z lat 1960–1990:", len(album_6090s))

# Najnowszy album + pierwszy album każdego artysty
new_album_year = df['Rok'].max()
print("Najmłodszy album został wydany w roku:", new_album_year)

first_albums = df.sort_values(by='Rok').drop_duplicates(subset='Artysta', keep='first')

# Najwcześniejsze wydanie dla każdego artysty
first_albums = (
    df
    .sort_values(by='Rok', ascending=True)
    .drop_duplicates(subset='Artysta', keep='first')
    .reset_index(drop=True)
)

print("Najwcześniejsze albumy każdego artysty (pierwsze z listy):")
print(first_albums[['Artysta', 'Tytuł', 'Rok']])

# Zapis do pliku CSV
first_albums.to_csv('albumy.csv', index=False)