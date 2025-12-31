from extract import extract_gdp, save_extract_json
from transform import transform_gdp_from_raw
from load import load_to_db
from log_file import log_message
import sqlite3
import pandas as pd

DB_NAME = "World_Economies.db"
TABLE_NAME = "Countries_by_GDP"

def query_gdp_over_100(db_name):
    conn = sqlite3.connect(db_name)

    query = """
    SELECT Country, GDP_USD_billion
    FROM Countries_by_GDP
    WHERE GDP_USD_billion >= 100
    ORDER BY GDP_USD_billion DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    print("\n=== GDP >= 100B USD ===")
    print(df)

def query_region_top5_avg_gdp(db_name):
    conn = sqlite3.connect(db_name)

    query = """
    WITH ranked AS (
        SELECT
            g.Country,
            c.Continent,
            g.GDP_USD_billion,
            ROW_NUMBER() OVER (
                PARTITION BY c.Continent
                ORDER BY g.GDP_USD_billion DESC
            ) AS rn
        FROM Countries_by_GDP g
        JOIN Country_Continent c
        ON g.Country = c.Country
        WHERE g.GDP_USD_billion IS NOT NULL
    )
    SELECT
        Continent,
        ROUND(AVG(GDP_USD_billion), 2) AS avg_top5_gdp
    FROM ranked
    WHERE rn <= 5
    GROUP BY Continent
    ORDER BY avg_top5_gdp DESC;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    print("\n=== Region별 TOP 5 국가 평균 GDP (USD Billion) ===")
    print(df)

def query_country_region(db_name):
    conn = sqlite3.connect(db_name)
    query = """
    CREATE TABLE IF NOT EXISTS Country__Region (
        Country TEXT PRIMARY KEY,
        Region TEXT NOT NULL
    );
    """

def main():
    log_message("ETL process started")

    # Extract
    df_raw = extract_gdp()
    save_extract_json(df_raw)

    # Transform
    df_clean = transform_gdp_from_raw(df_raw)

    # Load
    load_to_db(df_clean, DB_NAME, TABLE_NAME)

    # SQL Output
    query_gdp_over_100(DB_NAME)
    query_region_top5_avg_gdp(DB_NAME)

    log_message("ETL process finished")


if __name__ == "__main__":
    main()