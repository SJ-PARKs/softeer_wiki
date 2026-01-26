# 수업 Review

## RDD가 왜 나왔을까?

### Hadoop / MapReduce

- Hadoop → **Data Redundancy(데이터 중복 저장)** 를 위해 Replication 사용  
- MapReduce는 기본적으로 **디스크 기반 처리 모델**  
- Job 간에 **data reuse라는 개념이 없다**

---

### RDD

- RDD → **Resilience(장애 복구 가능성)**  
  → replication이 아니라 **lineage(계보)** 로 장애 복구  
- 중간 데이터를 **메모리에 유지**해서 재사용 가능



## MapReduce의 문제점

### 1) No data reuse across jobs  
> you must recompute or reload from HDFS every time

- MapReduce는 Job 1, Job 2, Job 3을  
  **따로따로 실행**한다.  
- 1 → 2 → 3 이렇게 연결해서 도는 게 아니라  
  **1, 2, 3이 전부 개별 Job**이다.

### 2) Job을 따로 돌릴 때 생기는 문제

- 만약에 1, 2, 3을 따로따로 돌리면  
  중간에 만들어진 데이터가 있는데  
  다음 Job에서 그 데이터를 바로 쓸 수 없다.  
- 그러면 그 데이터는 결국 **다시 만들어야 한다**.

*input에 대해 +1 *3 /4 연산을 수행할 때, 하나의 MapReduce 로 한번에 실행하는 것과 각 연산 별로 MapReduce를 여러개로 나눠서 하는 것 중 어떤 것이 좋을까?**

### 3) 반복 작업에 최악

- 똑같은 데이터를 가지고  
  **10번, 100번 반복해서 돌리는 작업**이 있다.  
  (예: 머신러닝, 그래프 처리)

- MapReduce에서는  
  이 반복 한 번 한 번이 **전부 새 Job**이다.

- 즉,1, 2, 3 이 3개가  
    하나로 묶여서 도는 게 아니라  
    **완전히 개별적으로 계산**된다.

### 4) 그럼 한 군데서 몰아서 돌리면?

- 한 군데서 돌리면 **뭔가 속도가 빨라질 방법이 있지 않을까?** 라는 생각이 들지만
  매번 **디스크에 쓰고 다시 읽어야 한다.**

    I/O가 **대단히 크다**.


## Data Reuse가 안 되는 구조

### 전처리 예제

- low data → clean up → 그 다음 Job 2개를 따로따로

- 예를 들어:
  1. 데이터를 tokenizer 시킨다  
  2. clean text를 만든다  
  3. 그 데이터를 가지고 filter, 분석을 한다  

- 이 clean data를  
  **계속 쓰고 싶다.**

---

### MapReduce에서는?

- MapReduce는 기본적으로  
  **data reuse라는 개념이 없다.**

- Task 2개를 동시에 돌리면:
  - 전처리 Job을 2번 따로 만들어서  
  - 각각 돌리고  
  - 각각 저장해야 한다.

→ “이걸 **한 번만** 해서  
여러 Job에서 같이 쓸 수 없을까?”  
라는 고민이 생긴다.

### 결국 문제의 핵심

- MapReduce에서는  
  preprocessing을 **매번 해야 한다.**  
  (저장해두는 것과 상관없이)

- 중간 결과를  
  메모리에 유지하거나  
  Job 간에 재사용할 방법이 없다.



## 그래서 RDD가 나왔다

- RDD는:
  - 중간 결과를 **메모리에 유지**할 수 있고  
  - 여러 Action에서 **같은 데이터를 재사용**할 수 있다.
  - lineage 기반으로 **Resilience(장애 복구)** 가능

- 그래서:
  - 반복 작업 빠름  
  - 전처리 결과 재사용 가능  
  - 디스크 I/O 최소화  
  - DAG 기반으로 계산 순서 최적화


### Overcoming Redundancy and Lack of In-Memory Reuse

- RDD → **redundancy랑 in-memory reuse가 없는 걸 해결해보자**가 핵심  
- 기술의 발전은  
  비즈니스 문제를 풀기 위해서 발전한 경우가 많다,  
  아카데믹하게 파고들어서 만들어지는 게 아니다.

- 결국 핵심은  
  **memory 상에서 reuse 하는 것**이다.

- MapReduce는:
  - 다른 Job에 쓸 때 데이터를 **다시 읽어야 한다**.
  - input이 사실상 **하나밖에 없다.**



## In-Memory Reusable Dataset

- RDD는  
  **in-memory에서 reusable한 dataset**이다.

- MapReduce에서 data redundancy는  
  **replication**으로 해결했는데,

- RDD는  
  **lineage라는 개념**을 쓴다.


## RDD의 장점

- RDD의 장점은:
  - **I/O overhead가 줄어든다.**
  - MapReduce의 **weakness(약점)** 를 해결하려고 만든 것

- Spark는:
  - 데이터를 partition으로 나누고  
  - parallel operation을 적용한다.
  - RDD가 기본적으로 **data parallelism**의 단위다.

---

## RDD의 성질

- Spark RDD는 그 자체로 **immutable** 하다.

- 왜 immutable이어야 할까?

  - 값이 있는데  
    +1을 했다.  
    ×3을 했다.

  - 그 결과값을  
    하나의 RDD로 덮어버리는 것과  
    따로따로 RDD로 분리해서 갖고 있는 건  
    큰 차이가 있다.

- **값을 바꿔버리면 안 된다.**  
  → 값을 유지해야 한다.

---

## In-Memory Data Reuse의 본질

- transformation을 하면:
  - 그 결과를 바로 저장하는 게 아니라  
  - **기록(lineage)** 을 갖고 있는 것이다.

- 즉:

  - transformation 결과(값)를  
    메모리에 다 들고 있는 게 아니라  
  - **"이렇게 계산하면 된다"** 라는  
    lineage 기록을 가지고 있는 것이다.

---

## Immutable → Reuse를 위해서

- immutable이 아니면  
  값이 바뀌는 순간 reuse 하기가 힘들어진다.

- immutable이라서:
  - RDD1  
  - RDD2  
  - RDD3  
  이렇게 계속 생긴다.

- 근데:
  - "그럼 메모리 엄청 잡아먹는 거 아니야?"

→ 그래서 Spark는  
**값이 아니라 lineage(그래프)** 를 들고 있는다.

---

## RDD 생성 방법

- RDD는 여러 방식으로 만든다:

  1. parallelize collection  
  2. external dataset  
  3. existing RDD

- 예를 들어:

  - 1번: 작은 데이터를 parallelize해서 RDD 만들고  
  - 2번: Hadoop HDFS 파일을 읽어서 RDD 만들고  
  - 그걸 transform해서  
    또 RDD를 만들고  
  - 그게 3번이다.

---

## RDD vs Transformation vs Action

- RDD에 대해서 뭔가 processing 하는 걸  
  **transformation**이라고 한다.

- RDD에 대해서  
  실제로 값을 뽑아내는 걸  
  **action**이라고 한다.

---

### Transformation

- transformation은:
  - RDD를 또 하나 만든다.
  - 실제 계산을 안 한다.
  - **lineage 기록만 쌓는다.**

- 예:
  - +1 하는 transformation  
  - map, filter 같은 것들

- 이때:
  - 메모리에 값 저장 ❌  
  - 계산 ❌  
  - 기록만 한다.

---

### Action

- sum, count 같은 건 **action**이다.

- action은:
  - 새로운 RDD를 만들지 않는다.
  - lineage 보관할 것도 없다.
  - 결과값만 떨어진다.

- 예:

  - `count()` 하면  
    RDD3이 생기는 게 아니라  
    그냥 숫자 하나 떨어진다.


## Lazy Evaluation

- Spark는:
  - transformation을  
    실시간으로 실행하지 않는다.

- action이 불릴 때까지:
  - 계산 ❌  
  - 실행 ❌  
  - 아무것도 안 한다.

- 대신:
  - lineage(그래프)만 계속 쌓아둔다.

---

## Action이 불리는 순간

- action이 불리는 순간:

  - 위로 쭉 올라가서  
    전부 계산을 시작한다.

→ 이게 **Lazy Evaluation**이다.

---

## Spark가 빠른 이유 (본질)

- Spark가 빠른 이유는:

  - In-memory를 써서 빠른 것도 맞다. (하드웨어적으로)

  - 근데 본질적으로는:
    - lineage를 Graph로 그려서  
    - "어떻게 계산하는 게 빠르겠네?"  
      라고 판단한다. (optimize)

- 그리고 이걸  
  **실시간으로 한다.**

---

## 정리

- RDD:
  - immutable
  - lineage 기반
  - in-memory reuse 가능

- Transformation:
  - RDD를 만든다
  - 계산 안 한다
  - 기록만 쌓는다

- Action:
  - 계산을 시작한다
  - 새로운 RDD 안 만든다
  - 결과만 준다



## Narrow vs Wide Transformation

- MapReduce에서 shuffle이 나왔다.

- shuffle은:
  - 기본적으로 **모든 데이터를 다 봐야 한다.**
  - 네트워크, 디스크 I/O 발생
  - 정리하는 작업이 필요하다.


### Narrow Transformation

- shuffle 안 하는 transformation

- 예:
  - map
  - filter
  - flatMap



### Wide Transformation

- shuffle 하는 transformation

- 예:
  - groupByKey
  - reduceByKey
  - join

- 이건:
  - 전체 데이터에서 key를 다 골라야 하고  
  - 다 확인해야 하고  
  - 셔플이 일어난다.

→ 데이터 처리 속도가  
**엄청 많이 떨어진다.**



## 튜닝의 사명

- 튜닝의 사명은:
  - 이 **shuffle을 최대한 없애는 것**이다.

- wide transformation은:
  - 조합하고 난리 난다.
  - 네트워크 I/O 폭발
  - 디스크 I/O 폭발

→ 그래서:
  - stage 줄이기  
  - shuffle 줄이기  
  - narrow transformation 최대한 쓰기  
  이게 성능 튜닝의 핵심이다.


## Partition이라는 개념

- Partition은  
  **small logical division of data** 이다.

- 기본적으로  
  **data cloud(분산 데이터)** 개념이다.

- RDD라는 dataset의 부분집합이 partition인데  
  **바라보는 레벨이 다르다.**

  - RDD → **logical level**  
  - Partition → **physical execution level**

---

## Cluster 구조랑 연결해서 보면

- container → Resource Manager(RM)가 관리  
- container 안에서 **executor**가 돈다.

- executor → application layer (AM) 개념

- 결국:

  - RDD는  
    완전 추상의 개념 layer는 아니지만  
    **로직 관점의 개념**이고,

  - partition은  
    **executor 안에서 실제로 돌아가는 데이터 단위**다.

---

## Partition = Task (암기)

> **Partition 하나당 Task 하나**

- Partition 하나를  
  **Task 하나**가 처리한다. → 암기

- Spark에서는:

  - Partition = 데이터 단위  
  - Task = 그걸 처리하는 실행 단위

---

## Task에 대한 관점 정리

- "Task를 하는데 데이터가 필요한 게 아니다" ❌  
- 정확히는:

  > **데이터가 있으니까 일을 한다** ⭕

- 즉:

  - Task는  
    어떤 로직을 실행하는 코드 단위이고  
  - Partition은  
    그 Task가 처리할 데이터다.

---

## Single Task vs Single Executor

- Single Task = Single Executor ❌  
  → 이건 개념적으로 틀림

- 정확히는:

  - Executor 하나는  
    **여러 Task를 순차적/병렬로 실행**할 수 있다.  
    (코어 수만큼 동시에)


## Spark가 Partition을 자동으로 정한다

- Spark는:

  - 데이터를 몇 개로 쪼갤지  
  - 즉, partition 개수를  
    **자동으로 정한다.**

- 이 말은:

  > 데이터를 몇 조각으로 나눌지  
  > Spark가 스스로 판단한다는 뜻이다.

- 판단 기준:

  - 데이터 사이즈  
  - 현재 가용 자원(CPU, 메모리)

- 그래서:

  - Spark는  
    데이터 양을 알고  
    가용 자원을 알고  
    그걸 기준으로  
    **partition 개수를 정한다.**



## Optimize를 잘한다는 말의 의미

- Optimize를 잘한다는 건:

  1. Spark가  
     partition을 결정할 수 있게 해주는  
     **정보를 다 알고 있고**

  2. 그 정보에 의해서  
     **합리적인 판단을 한다**는 뜻이다.



## Data Skewing

- Data skewing:

  - 어떤 partition은 데이터 3개  
  - 어떤 partition은 데이터 5개

- 사실은:

  - even하게  
    4개, 4개 있으면 제일 좋다.

- skewing이 문제인 이유:

  - 데이터가 네트워크 타고 간다.  
  - 셔플 시에 한쪽 노드만 오래 걸린다.



## Skewing 해결 아이디어

- 어떻게 해야 하느냐?

  > **데이터를 더 쪼개야 한다.**

- 예:

  - 서울 → 서울1, 서울2, 서울3  
  - key를 더 잘게 쪼개서  
    partition 분산



## 메모리 부족 & Shuffle

- 어떤 노드에 메모리가 없어서:

  - 한 번에 데이터를 다 불러와  
    메모리에 올려놓고  
    작업 처리가 안 되는 경우가 있다.

- Shuffle이라는 것은:

  > **physical data가 네트워크를 타고 이동하는 것**이다.

- 그래서:

  - 네트워크 I/O  
  - 디스크 I/O  
  - 성능 급락



## 예시 코드 흐름

- Driver Program을 짰다.

- `sc.textFile()`로  
  RDD를 읽었다.

- `filter()` → narrow transformation

- `count()` → action



## Action이 불리는 순간

- Driver Program이 돌다가:

  - action이 보이면  
  - SparkContext가  
    application을 submit 한다.

- 그러면:

  - Job이 만들어진다.
  - DAG가 만들어진다.  
    (어떻게 계산할지 그리는 그림)

- 그 다음:

  - partition을 몇 개로 쪼갤지 정한다.
  - partition 수만큼 Task를 만든다.
  - Task를 scheduling 해서  
    executor에서 실행한다.



## 하나의 Application = 여러 Action

- 하나의 application에는  
  **여러 개의 action**이 포함될 수 있다.



## Lineage

- Spark는:

  - transformation을  
    열심히 기록해준다.

- action이 되면:

  - 그 lineage를  
    DAG로 그려서 실행해준다.

- action이 실행되기 전까지는:

  - transformation은  
    SparkContext 안에만 쌓여 있다.



## Job / Task 관계 다시 정리

- Action이 불리면:

  - Job이 만들어진다.

- Job이란:

  - 하나의 RDD에 대해  
    뭔가 일을 하는  
    **Task들의 조합**이다.

- 반대로 보면:

  - Job을 만들면서  
    해야 할 transformation들을  
    Task 단위로 쪼개서 실행한다.

- 결국:

  - Task는  
    Cluster Manager의 컨트롤 하에  
    어떤 노드에서  
    어떻게 실행할지를 정해서 던지는 것이다.

---

## Task에 대한 두 가지 관점

1. 데이터 관점

   > Partition data를 주고  
   > "이 데이터에 맞는 일을 해" 라는 관점  
   > → 이게 Task다.

2. Resource Manager 관점

   > RM / AM 입장에서는  
   > 이 실행 단위를 Task라고 본다.

→ 이 두 가지 관점을  
**같이 이해할 필요가 있다.**


## DAG Scheduler 역할

- RDD lineage를  
  Task로 변환하는 건  
  **DAG Scheduler의 역할**이다.



## Worker Node 실행

- Worker Node가 실행할 때:

  - configuration이 넘어온다.
  - worker node가  
    독자적으로 executor를 띄워서 실행한다.



## Action → Job → DAG

- Action에 의해서:

  - Job이 만들어진다.
  - Spark Shell에서  
    DAG를 볼 수 있다.



## Stage and Task

### Stage란?

- Stage는:

  - 나눠서 관리하는 게  
    효과적일 때가 있다.

- 기본적으로:

  - 안 쪼개고  
    그냥 쭉 이어도 되는데

- 왜 쪼개느냐?

  > 여기서 나온 output이  
  > 다음 계산에 영향을 주기 때문이다.

---

### Stage 경계

- Often stages are delineated on the operator's computation boundaries

- 즉:

  > Stage의 핵심은  
  > **computation boundary(계산 경계)** 다.

- 계산상으로:

  - 여기서 한 번 끊는 게 좋겠네  
    싶은 지점에서 Stage를 나눈다.

### Stage = 여러 Task

- Stage는:

  - 여러 개의 Task로 구성된다.

- Task는:

  - RDD 일부(partition)를 가져다가  
  - computation 하고  
  - 결과를 만들어내는 구조다.

### Stage 분리 기준

- Stage에서  
  **Wide Transformation**이 일어나면 쪼개진다.
  - Stage 1  
  - Stage 2  
    이렇게 나눈다.

- Narrow Transformation만 있으면:

  - 같은 Stage 안에서  
    계속 이어서 실행된다.
