import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://github.com/melaniewalsh/Intro-Cultural-Analytics/raw/master/book/data/bellevue_almshouse_modified.csv'

df_bellevue = pd.read_csv(url)
# df_bellevue = pd.read_csv('./data/.../mydata.csv')  # you can also reference locally stored data

# Exercise 1
def fib(n: int) -> int:
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be >= 0")

    if n in (0, 1):
        return n

    return fib(n - 1) + fib(n - 2)


fib(9)

# Exercise 2
def to_binary(n: int) -> str:
    """Return the binary (base-2) representation of a non-negative integer.

    Uses a single recursive function. For example:
        to_binary(2)  -> "10"
        to_binary(12) -> "1100"

    Args:
        n: Integer to convert. Must be >= 0.

    Returns:
        Binary string without the '0b' prefix.

    Raises:
        ValueError: If n is negative or not an integer.
    """
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be >= 0")

    if n in (0, 1):
        return str(n)

    return to_binary(n // 2) + str(n % 2)

to_binary(2)

# Exercise 3
def task_1():
    """Column names sorted by fewest -> most missing values."""
    df = df_bellevue.copy()

    if "gender" in df.columns:
        df["gender"] = (
            df["gender"].astype("string").str.strip().str.lower()
            .replace({"": pd.NA, "na": pd.NA, "n/a": pd.NA, "none": pd.NA})
            .replace({
                "m": "male", "h": "male", "b": "male", "boy": "male", "man": "male",
                "f": "female", "w": "female", "g": "female", "girl": "female", "woman": "female"
            })
        )

    return df.isna().sum().sort_values().index.tolist()


def task_2():
    """DataFrame with 'year' and 'total_admissions'."""
    df = df_bellevue.copy()

    if "year" in df.columns:
        year = pd.to_numeric(df["year"], errors="coerce")
    elif "date_in" in df.columns:
        year = pd.to_datetime(df["date_in"], errors="coerce").dt.year
    else:
        print("Need 'year' or 'date_in'.")
        return pd.DataFrame({"year": [], "total_admissions": []})

    out = (
        year.dropna().astype(int).to_frame("year")
        .groupby("year").size().reset_index(name="total_admissions")
        .sort_values("year").reset_index(drop=True)
    )
    return out


def task_3():
    """Series: average age by gender."""
    df = df_bellevue.copy()

    if "gender" not in df.columns or "age" not in df.columns:
        print("Need 'gender' and 'age'.")
        return pd.Series(dtype="float64", name="age")

    gender = (
        df["gender"].astype("string").str.strip().str.lower()
        .replace({"": pd.NA, "na": pd.NA, "n/a": pd.NA, "none": pd.NA})
        .replace({
            "m": "male", "h": "male", "b": "male", "boy": "male", "man": "male",
            "f": "female", "w": "female", "g": "female", "girl": "female", "woman": "female"
        })
    )
    age = pd.to_numeric(df["age"], errors="coerce")

    avg = (
        pd.DataFrame({"gender": gender, "age": age})
        .dropna().groupby("gender")["age"].mean().round(6)
    )
    return avg


def task_4():
    """Top 5 professions (most common first)."""
    df = df_bellevue.copy()

    col = "profession"
    if col not in df.columns:
        if "occupation" in df.columns:
            col = "occupation"
        else:
            print("No profession/occupation column.")
            return []

    s = df[col].astype("string").str.strip().str.lower().replace({"": pd.NA}).dropna()
    return s.value_counts().head(5).index.tolist()



# call the defined functions 
print("Task 1 (cols by missingness):")
print(task_1())

print("\nTask 2 (year + total_admissions):")
print(task_2().head())  # .head() so it’s short

print("\nTask 3 (avg age by gender):")
print(task_3())

print("\nTask 4 (top 5 professions):")

print(task_4())

# Seaborn visualization: Admissions per year
admissions_per_year = task_2()
plt.figure(figsize=(8, 4))
sns.barplot(data=admissions_per_year, x="year", y="total_admissions", palette="Blues_d")
plt.title("Admissions per Year")
plt.xlabel("Year")
plt.ylabel("Total Admissions")
plt.tight_layout()
plt.savefig("admissions_per_year.png")
print("\n[INFO] Plot saved as admissions_per_year.png")
# plt.show()  # Not used in headless environments

# Seaborn visualization: Admissions per year
admissions_per_year = task_2()
plt.figure(figsize=(8, 4))
sns.barplot(data=admissions_per_year, x="year", y="total_admissions", palette="Blues_d")
plt.title("Admissions per Year")
plt.xlabel("Year")
plt.ylabel("Total Admissions")
plt.tight_layout()
plt.show()