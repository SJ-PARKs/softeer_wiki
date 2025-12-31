from log_file import log_message
import pandas as pd

# Transform 함수
def transform_gdp_from_raw(df_raw):
    log_message("Transform start")

    df = df_raw.copy()

    # 1. 국가명 정제 (각주 제거)
    df["Country"] = (
        df["Country"]
        .str.replace(r"\[.*?\]", "", regex=True)
        .str.strip()
    )

    # 2. GDP_2025 → GDP_USD_billion 변환
    df["GDP_2025"] = (
        df["GDP_2025"]
        .str.replace(r"\(.*?\)", "", regex=True) # (2024) 같은 괄호 제거
        .str.strip()
        .replace(
            to_replace=r"^(-|—|N/?A|—N/?A)$",
            value=pd.NA,
            regex=True # -, —, N/A, N\A → "not"
        )
    )

    df["GDP_USD_billion"] = (
        pd.to_numeric(
            df["GDP_2025"].str.replace(",", "", regex=False),
            errors="coerce"  # ← "not", "-", "N/A" 전부 NaN 처리
        )
        .div(1000)
        .round(2)
    )

    log_message("Transform end")
    # 3. 필요한 컬럼만 반환
    return df[["Country", "GDP_USD_billion"]]
