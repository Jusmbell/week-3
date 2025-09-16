
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://github.com/melaniewalsh/Intro-Cultural-Analytics/raw/master/book/data/bellevue_almshouse_modified.csv')


# =============================================
# Exercise 1
# =============================================
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib(9))
# =============================================
# Exercise 2
# =============================================
def to_binary(n):
    return bin(n)[2:]

to_binary(2)
# =============================================
# Exercise 3
# =============================================
def task_1():
    return df.isna().sum().sort_values().index.tolist()


def task_2():
    if 'year' in df.columns:
        year = pd.to_numeric(df['year'], errors='coerce')
    else:
        year = pd.to_datetime(df['date_in'], errors='coerce').dt.year
    return year.dropna().astype(int).value_counts().sort_index().reset_index().rename(columns={'index':'year', 0:'total_admissions'})


def task_3():
    g = df['gender'].astype(str).str.strip().str.lower().replace({'': pd.NA, 'na': pd.NA, 'n/a': pd.NA, 'none': pd.NA, 'm': 'male', 'h': 'male', 'b': 'male', 'boy': 'male', 'man': 'male', 'f': 'female', 'w': 'female', 'g': 'female', 'girl': 'female', 'woman': 'female'})
    a = pd.to_numeric(df['age'], errors='coerce')
    return pd.DataFrame({'gender': g, 'age': a}).dropna().groupby('gender')['age'].mean().round(2)


def task_4():
    col = 'profession' if 'profession' in df.columns else 'occupation'
    return df[col].astype(str).str.strip().str.lower().replace({'': pd.NA}).dropna().value_counts().head(5).index.tolist()



# Calls the defined functions and print their results
print("Exercise 1 (fib(9)):", fib(9))
print("Exercise 2 (to_binary(12)):", to_binary(12))

print("Task 1 (cols by missingness):")
print(task_1())

print("\nTask 2 (year + total_admissions):")
print(task_2().head())  # .head() so it’s short

print("\nTask 3 (avg age by gender):")
print(task_3())

print("\nTask 4 (top 5 professions):")
print(task_4())

# Seaborn barplot for profession counts in Bellevue dataset
if 'profession' in df.columns:
    plt.figure(figsize=(8, 4))
    prof_counts = df['profession'].astype(str).str.strip().str.lower().value_counts().head(10).reset_index()
    prof_counts.columns = ['profession', 'count']
    sns.barplot(data=prof_counts, x='profession', y='count', color='skyblue')
    plt.title('Top 10 Admissions by Profession')
    plt.xlabel('Profession')
    plt.ylabel('Admissions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('professions.png')
    print('[INFO] Profession bar chart saved as professions.png')
else:
    print('No profession column in the dataset.')
