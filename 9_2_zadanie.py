import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

sns.set_style("ticks")

df = pd.read_csv(r'D:\KODILLLA\wizualizacje\HRDataset.csv')

df['DOB'] = pd.to_datetime(df['DOB'], format='%m/%d/%y', errors='coerce')
df.loc[df['DOB'] > pd.to_datetime('today'), 'DOB'] -= pd.DateOffset(years=100)
df['DateofHire'] = pd.to_datetime(df['DateofHire'], format='%m/%d/%Y', errors='coerce')
df['DateofTermination'] = pd.to_datetime(df['DateofTermination'], format='%m/%d/%y', errors='coerce')

df['Age'] = (dt.datetime(2019, 9, 27) - df['DOB']).apply(lambda x: x.days) / 365.25
df['Seniority'] = df.apply(
    lambda row: ((dt.datetime(2019, 9, 27) if pd.isnull(row['DateofTermination']) else row['DateofTermination']) - row['DateofHire']).days / 365.25,
    axis=1)
df['HispanicLatino'] = df['HispanicLatino'].str.title()

# 1. Manager vs efetywnosć
plt.figure(figsize=(12, 5))
sns.boxplot(x='ManagerName', y='PerformanceScore', data=df)
plt.title("Manager vs efetywnosć")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 2. Lojalność vs źródło Rekrutacji
plt.figure(figsize=(12, 5))
sns.boxplot(x='RecruitmentSource', y='Seniority', data=df)
plt.title("Lojalność vs źródło Rekrutacji")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 3. Stan Cywilny vs satysfakcja
plt.figure(figsize=(10, 5))
sns.violinplot(x='MaritalDesc', y='EmpSatisfaction', data=df)
plt.title("Satysfakcja z pracy a stan cywilny")
plt.tight_layout()
plt.show()

# 4. Struktura wieku
plt.figure(figsize=(10, 5))
sns.histplot(df['Age'].dropna(), bins=20)
plt.title("Struktura Wieku")
plt.xlabel("Wiek")
plt.ylabel("Liczba pracowników")
plt.tight_layout()
plt.show()

# 5. Specjalne projekty vs. wiek
plot = sns.lmplot(x='Age', y='SpecialProjectsCount', data=df, aspect=1.5)
plot.fig.suptitle("Specjalne projekty vs wiek", y=1.03)
plt.tight_layout()
plt.show()
plt.close()