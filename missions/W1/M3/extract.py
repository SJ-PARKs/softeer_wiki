import requests
from bs4 import BeautifulSoup
import pandas as pd
from log_file import log_message

# Extract 함수
def extract_gdp():
    log_message("Extract start")

    # 1. 웹 페이지 요청
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    headers = { "User-Agent": "Mozilla/5.0" }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 2. Wikipedia 페이지에서 GDP 데이터가 포함된 테이블 선택
    table = soup.select_one("table.wikitable.sortable")
    rows = table.select("tbody tr") # 테이블의 본문(tbody)에서 모든 행(tr) 추출

    # 3. 데이터 추출
    raw_data = []
    for row in rows[2:]:
        cols = row.select("td")
        if len(cols) >= 4:
            country_raw = cols[0].get_text(strip=True)
            gdp_2026 = cols[1].get_text(strip=True)      # IMF 2026
            gdp_2025 = cols[2].get_text(strip=True)      # IMF 2025
            gdp_2024 = cols[3].get_text(strip=True)      # WB 2024

            raw_data.append({
                "Country": country_raw,
                "GDP_2026": gdp_2026,
                "GDP_2025": gdp_2025,
                "GDP_2024": gdp_2024
            })

    log_message("Extract end")
    return pd.DataFrame(raw_data)

# Extract 결과를 JSON으로 저장
def save_extract_json(df):
    df.to_json(
        "Countries_by_GDP.json",
        orient="records",
        indent=4,
        force_ascii=False
    )

