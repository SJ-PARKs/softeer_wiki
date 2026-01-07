# WordCloud Pipeline  
**Text → Frequency → Visual Layout**

워드클라우드는 **텍스트 데이터를 단어 빈도 기반으로 분석한 뒤, 이를 크기·위치·색상으로 시각화한 이미지**로 변환하는 파이프라인을 가지고 있다. 
Python `wordcloud` 라이브러리의 내부 구조는 크게 다음 세 단계로 구성된다.

1. **텍스트 전처리 (Tokenization & Filtering)**  
2. **단어 중요도(가중치) 계산 (Frequency Normalization)**  
3. **레이아웃 및 색상 배치 (Layout & Coloring)**  

---

## 1. Text Preprocessing: Tokenization & Frequency Generation

워드클라우드는 입력 텍스트를 다음과 같은 호출 흐름으로 처리한다.

`WordCloud.generate(text)`
→ `generate_from_text(text)`
→ `process_text(text)`


### 1.1 Tokenization: 텍스트를 단어로 분리

`process_text` 함수는 정규식을 사용하여 입력 텍스트를 단어 단위로 토큰화한다.

- 기본 패턴은 알파벳, 숫자, 그리고 `'`(apostrophe)를 포함하는 연속된 문자열을 하나의 단어로 인식한다.
- 이 과정에서는 형태소 분석, 품사 태깅, 한국어 분해와 같은 언어학적 처리는 수행하지 않는다.
- 따라서 토큰화 방식은 영어와 숫자를 중심으로 한 단순한 규칙 기반 분리 방법이다.


---

### 1.2 Filtering: 소유격, 숫자, 짧은 단어 제거

토큰화 이후 다음과 같은 필터링이 적용된다. (의미없는 기호와 숫자 제거)

1. **소유격 제거**
 - `"John's"` → `"John"`
2. **숫자 제거**
 - `include_numbers=False`가 기본값
 - `"2024", "123"` 등의 숫자 토큰 제거
3. **최소 길이 필터**
 - `min_word_length` 미만인 단어 제거
 - 의미 없는 짧은 토큰 제거 목적

---

### 1.3 Stopword Removal, Plural Normalization, Collocation

#### 1.3.1 불용어 제거
- 라이브러리 내부에 정의된 `STOPWORDS` 집합을 사용
- `"the", "is", "and", "of"` 등 의미 기여도가 낮은 단어 제거

#### 1.3.2 복수형 정규화 (`normalize_plurals=True`)
- `"dogs"` → `"dog"`
- 복수형과 단수형을 동일한 단어로 취급하여 빈도 통합

#### 1.3.3 Bigram(연어) 처리 (`collocations=True`)
- `"New York"`과 같이 자주 함께 등장하는 단어 쌍을 하나의 토큰으로 처리
- 내부적으로 `unigrams_and_bigrams` 함수 사용

---

### 1.4 전처리 단계 요약

`Text`
→ `Regex Tokenization`
→ `Remove numbers & short tokens`
→ `Stopword removal`
→ `Plural normalization`
→ `(Optional) Bigram detection`
→ `word_counts: {word → frequency}`


즉, **1단계는 “텍스트 → 단어 빈도 딕셔너리”를 생성하는 과정**이다.

---

## 2. Importance Calculation: Frequency Normalization

WordCloud는 기본적으로 **빈도 기반 가중치 모델**을 사용한다.

### 2.1 빈도 정렬 및 상위 단어 선택

`generate_from_frequencies()` 함수에서:

- 단어-빈도 쌍을 빈도 기준 내림차순 정렬
- `max_words`(기본값 200) 개까지만 사용

→ 너무 많은 단어가 출력되는 것을 방지

---

### 2.2 정규화된 가중치 (0 ~ 1)

가장 빈도가 높은 단어의 빈도를 기준으로 정규화:

```
max_frequency = frequencies[0][1]
normalized_freq = freq / max_frequency
```

결과:
- 가장 자주 등장한 단어 → 1.0
- 나머지 단어 → 0~1 사이의 비율값

이 값이 이후 **폰트 크기 스케일링의 기준**이 된다.

---

### 2.3 TF-IDF 등 고급 가중치 확장

WordCloud 내부는 기본적으로 **단순 빈도 기반 가중치**만 계산한다.  
그러나 사용자는 다음과 같이 외부에서 계산한 가중치를 직접 전달할 수 있다.

```
wc.generate_from_frequencies({"good": 0.9, "bad": 0.1})
```

- 0.9, 0.1은 TF-IDF, 감성 점수, 토픽 점수 등 어떤 지표도 가능
- 즉, **2단계는 “빈도 기반 중요도 정규화”이며, 확장은 사용자가 한다.**

---

## 3. Layout & Coloring: Visual Rendering

**워드클라우드가 실제 이미지로 배치되는 핵심 알고리즘**이다.

---

### 3.1 Canvas & Occupancy Map

- 마스크(`mask`)가 있으면 그 형태를 따라 캔버스 생성
- 없으면 `(width × height)` 크기의 직사각형 캔버스 사용
- `IntegralOccupancyMap`:
  - 현재 캔버스에서 “이미 사용된 영역”과 “빈 영역”을 빠르게 탐색하기 위한 누적합(적분 영상) 구조
  - 충돌 감지를 효율적으로 수행

---

### 3.2 Font Size Scaling (Relative Scaling)

단어 빈도에 따라 폰트 크기를 결정:

- `relative_scaling` 기본값: `0.5`
- 폰트 크기 계산:
  - 이전 단어 크기와 현재 단어 빈도 비율을 혼합
- 효과:
  - 빈도 높은 단어는 크게
  - 그러나 극단적인 크기 차이는 완화(smoothing)

→ **시각적 균형을 유지하면서 빈도 차이를 반영**

---

### 3.3 Orientation (회전)

- `prefer_horizontal=0.9` 기본값
- 약 90%는 가로, 10%는 세로 방향
- 가독성과 시각적 다양성의 균형을 위한 설계

---

### 3.4 Positioning & Collision Detection

각 단어에 대해:

1. 폰트 크기·회전에 따른 bounding box 계산
2. `IntegralOccupancyMap`을 사용해 배치 가능한 위치 탐색
3. 배치 불가 시:
   - 방향 변경 → 실패 시 폰트 크기 감소
4. 최소 크기(`min_font_size`)보다 작아지면 종료

→ **“충돌 감지 + 공간 최적화” 기반 배치 알고리즘**

---

### 3.5 Color Assignment

기본 색상 정책:

- 랜덤 색상 또는 `colormap` 기반
- 단어 의미와 색상을 직접 연결하지 않음

사용자 정의 색상 함수(`color_func`)를 제공하면:
- 감성 점수 기반 색상
- 중요도 기반 색상
등 의미 기반 시각화 확장 가능

---

### 3.6 Final Image Rendering

- 내부적으로 계산된 `layout_`(단어, 위치, 크기, 색상)를 바탕으로 실제 이미지 렌더링
- 마스크 외곽선 표시 옵션 포함

---

## 4. Pipeline Summary

워드클라우드 생성 파이프라인은 다음과 같이 요약된다.

`Text`
→ `Tokenization & Filtering`
→ `Word Frequency Dictionary`
→ `Normalized Importance (0~1)`
→ `Font Size Scaling`
→ `Collision-Free Layout`
→ `Color Assignment`
→ `Final Image`