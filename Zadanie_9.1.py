import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych o filmach i gatunkach
movies = pd.read_csv(r'D:\KODILLLA\wizualizacje\tmdb_movies.csv')
genres = pd.read_csv(r'D:\KODILLLA\wizualizacje\tmdb_genres.csv', header=None)
genres.columns = ['genre_id', 'name']

# Dodanie kolumny z rokiem premiery filmu
movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
movies['release_year'] = movies['release_date'].dt.year

# 1. Top 10 filmów z największą oceną i wysoką liczbą głosów (powyżej 3. kwartyla)
kw3_vote_count = movies['vote_count'].quantile(0.75)
top_10_movies = movies[movies['vote_count'] > kw3_vote_count].sort_values('vote_average', ascending=False).head(10)
print("TOP 10 ocenianych filmów (w grupie powyżej 3. kwartyl)")
print(top_10_movies[['title', 'vote_average', 'vote_count']])

# 2. Średni przychód i budżet filmów w latach 2010–2016
filtered = movies[(movies['release_year'] >= 2010) & (movies['release_year'] <= 2016)]
grouped = filtered.groupby('release_year')[['revenue', 'budget']].mean()

fig, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(grouped.index, grouped['revenue'], color='grey', label='Średni przychód')
ax1.set_xlabel('Rok')
ax1.set_ylabel('Przychód (USD)')
ax1.set_title('Średni przychód i budżet filmów (2010–2016)')

ax2 = ax1.twinx()
ax2.plot(grouped.index, grouped['budget'], color='black', marker='o', label='Średni budżet')
ax2.set_ylabel('Budżet (USD)')

# Dodanie legendy
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(1.05, 1))

plt.tight_layout()
plt.show()

# 3. Połączenie tabeli filmów z tabelą gatunków po 'genre_id'
movies = movies.merge(genres, on='genre_id', how='left')

# 4. Najczęstszy gatunek filmowy
top_genre = movies['name'].value_counts().idxmax()
top_genre_count = movies['name'].value_counts().max()
print(f"\nNajpopularniejszy gatunek: {top_genre} ({top_genre_count} filmów)")

# 5. Gatunek z najdłuższym średnim czasem trwania
avg_runtime = movies.groupby('name')['runtime'].mean()
longest_genre = avg_runtime.idxmax()
longest_time = avg_runtime.max()
print(f"Gatunek z najdłuższym średnim czasem trwania: {longest_genre} ({longest_time:.2f} min)")

# 6. Histogram czasu trwania filmów w gatunku z najdłuższym czasem trwania
longest_genre_movies = movies[movies['name'] == longest_genre]
plt.figure(figsize=(10,5))
plt.hist(longest_genre_movies['runtime'].dropna(), bins=30, color='grey', edgecolor='black')
plt.title(f'Histogram czasu trwania filmów: {longest_genre}')
plt.xlabel('Czas trwania (minuty)')
plt.ylabel('Liczba filmów')
plt.grid(True)
plt.tight_layout()
plt.show()