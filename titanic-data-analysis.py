import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def connect_to_sql_server():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=titanic;'
            'Trusted_Connection=yes;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"connection failed : {e}")
        return None
def read_data_from_sql(conn, query):
    if conn:
        try:
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print(f"error reading data: {e}")
            return None
    return None
def close_connection(conn):
    if conn:
        conn.close()
        print("connection closed ")
if __name__ == "__main__":
    conn = connect_to_sql_server()
    query_all = "SELECT * FROM dbo.titanic;"
    df_all = read_data_from_sql(conn, query_all)
    if df_all is not None:
        print("Head:\n", df_all.head())
        print("\nTail:\n", df_all.tail())
        print("\nDescription:\n", df_all.describe(include="all"))
    query1 = """
        SELECT
            CASE WHEN Survived = 1 THEN 'Survived' ELSE 'Did not survive' END AS Outcome,
            COUNT(*) AS PassengerCount
        FROM dbo.titanic
        GROUP BY Survived;
    """
    df1 = read_data_from_sql(conn, query1)
    if df1 is not None:
        plt.figure(figsize=(6, 6))
        colors = ["#3E5C76" if o == "Did not survive" else "#C9A227" for o in df1["Outcome"]]
        plt.pie(df1["PassengerCount"], labels=df1["Outcome"], autopct="%1.1f%%",
                colors=colors, startangle=90)
        plt.title("Who Made It Off the Ship?")
        plt.tight_layout()
        plt.show()
        print(df1)
    query2 = """
        SELECT
            Sex,
            COUNT(*) AS TotalPassengers,
            SUM(Survived) AS Survivors,
            AVG(CAST(Survived AS FLOAT)) * 100 AS SurvivalRatePct
        FROM dbo.titanic
        GROUP BY Sex
        ORDER BY SurvivalRatePct DESC;
    """
    df2 = read_data_from_sql(conn, query2)
    if df2 is not None:
        plt.figure(figsize=(6, 4))
        sns.barplot(x="Sex", y="SurvivalRatePct", data=df2, palette="viridis")
        plt.title("Survival Rate by Gender")
        plt.xlabel("Gender")
        plt.ylabel("Survival Rate (%)")
        plt.ylim(0, 100)
        plt.show()
        print(df2)
    query3 = """
        SELECT
            Pclass,
            COUNT(*) AS TotalPassengers,
            AVG(CAST(Survived AS FLOAT)) * 100 AS SurvivalRatePct,
            AVG(Fare) AS AvgFare
        FROM dbo.titanic
        GROUP BY Pclass
        ORDER BY Pclass;
    """
    df3 = read_data_from_sql(conn, query3)
    if df3 is not None:
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        sns.barplot(x="Pclass", y="SurvivalRatePct", data=df3, palette="Set2", ax=axes[0])
        axes[0].set_title("Survival Rate by Class")
        axes[0].set_xlabel("Passenger Class")
        axes[0].set_ylabel("Survival Rate (%)")
        sns.barplot(x="Pclass", y="AvgFare", data=df3, palette="Set2", ax=axes[1])
        axes[1].set_title("Average Fare by Class")
        axes[1].set_xlabel("Passenger Class")
        axes[1].set_ylabel("Average Fare ($)")
        plt.tight_layout()
        plt.show()
        print(df3)
    query4 = """
        SELECT
            Pclass,
            Sex,
            COUNT(*) AS TotalPassengers,
            AVG(CAST(Survived AS FLOAT)) * 100 AS SurvivalRatePct
        FROM dbo.titanic
        GROUP BY Pclass, Sex
        ORDER BY Pclass, Sex;
    """
    df4 = read_data_from_sql(conn, query4)
    if df4 is not None:
        plt.figure(figsize=(8, 5))
        sns.barplot(x="Pclass", y="SurvivalRatePct", hue="Sex", data=df4, palette="coolwarm")
        plt.title("Survival Rate by Class and Gender")
        plt.xlabel("Passenger Class")
        plt.ylabel("Survival Rate (%)")
        plt.ylim(0, 100)
        plt.show()
        print(df4)
    query5 = """
        SELECT
            CASE
                WHEN Age <= 12 THEN 'Child (0-12)'
                WHEN Age <= 18 THEN 'Teen (13-18)'
                WHEN Age <= 35 THEN 'Adult (19-35)'
                WHEN Age <= 60 THEN 'Mid-age (36-60)'
                ELSE 'Senior (60+)'
            END AS AgeGroup,
            COUNT(*) AS TotalPassengers,
            AVG(CAST(Survived AS FLOAT)) * 100 AS SurvivalRatePct,
            MIN(Age) AS SortHelper
        FROM dbo.titanic
        WHERE Age IS NOT NULL
        GROUP BY
            CASE
                WHEN Age <= 12 THEN 'Child (0-12)'
                WHEN Age <= 18 THEN 'Teen (13-18)'
                WHEN Age <= 35 THEN 'Adult (19-35)'
                WHEN Age <= 60 THEN 'Mid-age (36-60)'
                ELSE 'Senior (60+)'
            END
        ORDER BY SortHelper;
    """
    df5 = read_data_from_sql(conn, query5)
    if df5 is not None:
        plt.figure(figsize=(8, 4))
        sns.barplot(x="AgeGroup", y="SurvivalRatePct", data=df5, palette="mako")
        plt.title("Survival Rate by Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Survival Rate (%)")
        plt.ylim(0, 70)
        plt.show()
        print(df5)
    query6 = """
        SELECT
            CASE WHEN (SibSp + Parch) = 0 THEN 'Alone' ELSE 'With Family' END AS FamilyStatus,
            COUNT(*) AS TotalPassengers,
            AVG(CAST(Survived AS FLOAT)) * 100 AS SurvivalRatePct
        FROM dbo.titanic
        GROUP BY CASE WHEN (SibSp + Parch) = 0 THEN 'Alone' ELSE 'With Family' END;
    """
    df6 = read_data_from_sql(conn, query6)
    if df6 is not None:
        plt.figure(figsize=(6, 4))
        sns.barplot(x="FamilyStatus", y="SurvivalRatePct", data=df6, palette="crest")
        plt.title("Survival Rate: Alone vs. With Family")
        plt.xlabel("Travel Status")
        plt.ylabel("Survival Rate (%)")
        plt.ylim(0, 60)
        plt.show()
        print(df6)
    close_connection(conn)