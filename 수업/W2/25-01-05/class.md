# 수업 Review


## 코드 리뷰

1. extract_gdp와 save_extract_json을 분리할 필요 없다.
2. 변수 naming할 때 자기 생각에 제일 맞는 단어들 붙이는데 이러면 오해 불러 일으킬 가능성 높다.

    여기서는 clean이라는 단어 -> transform하고 안어울린다. (garbage같이 없앤다는거 연상됨)

    변수명 지을 때는 코드를 다 읽지 않아도 이해 되어야하는데 여기서는 읽고 오해가 생긴다. 

3. Extract code
  
  - url, config은 다 밖으로 빼야 한다. 
  - wiki에서 데이터 가져오는것은 특정 페이지의 데이터를 가지고 오는 로직이다. 
    코드가 함수화 되는것도 고려?
  - 제일 중요한것은 page가 바뀌면 mapping되는게 바뀔 수 있다. 
  
    validattion같은거를 적용해서 어떤 문자열이 테이블에 있는지 없는지 확인해서 내가 추출했던 시점을 판단할 수 있어야한다. 
    
    그래서 페이지가 바뀌었다면 사용자한테 알려주는 방법이 좋지 않을까. 페이지가 바뀌었으니까 누구한테 연락하세요. 이메일 가게 하는 방법등으로
  -  그 비용이 훨 씬 싸다. 어떻게 바뀔지 모르니까 그거에 대응하는 로직을 짜는 것 자체가 멍청하다. 

4. 화면에 뿌릴 로그는 어디에 이어서 저장한다... 

    뽑는 목록도 마찬가지로 output 폴더를 하나 만들고 거기에다가 계속 이어서 저장하는 방식으로

5. 상대방과 어떤 판단을 했는지 대화하면서 공유하는 것이 필요하다. 
- 판단하고 내 코드에 대해서 대화를 하지 않았다. 평가할 방법이 없다. 

6. country_raw라고 column에 집어넣고 바꾼걸 country로 빼는 방법?
- Gdp 2025라고 가져왔을 때 이거는 million이고 이거는 billion이다. 바로 이해할 수 있을까?
- 주석을 잘못 붙였다. 밑에 있어야할 주석

7. 지금 내 코드는 error 가 난다는 전제가 현재 없다.  

    예외 처리할 수도 있고 unit test같은 거를 할 수 있다. 

    Unit test-> 에러가 날 거를 생각하고 짜기 떄문에..

    몇개월 수련하면 코드를 짜면서 날 수 있는 에러의 가능성들이 눈에 보인다. 

    현재 아무것도 없다. 

    만약 테이블이 바뀌어서 내가 원하는 데이터가 안오면 어떻게 해야할까? 

    또한 Connection이 안되거나 그럴 때 처리하는 예외가 없다. 




## BigData 수업

- Salesforce(데이터의 신뢰성, 함부로 AI에 X)

- DataLake은 쭉 이어져있따. (모든 데이터를 가지고 있겠다)

- Data는 금전적으로 가치 있는 정보로 바꿔야한다!
  
    즉 경제적 가치가 있어야한다. 

  저장만하면 -> Cost sink(하는 일도 없는)
  
  데이터가 활용되어야한다.

- 금전적인 가치가 있는 문제를 해결해야한다. 

  -> data가 꼭 들어가고 technology

5Vs of BiG Data

- Veracity(진리) 이게 맞는 데이터인지 (엔지니어가 해야할까?)

- 의미있는 데이터의 소멸 (쓰레기  데이터로 학습 악순환)


**Parallel processing**

Parallel processing 되는거 안되는거 구분하는게 중요
- 전에거가 영향을 미치면 X

두가지 완전 다른 approach
- Task & Data

Data!

subset을 쪼갰을 때 돌아가야한다
-> disjoint partitions

-> 백엔드는 아니고 우리는 Data processing이 기본적으로 깔려 있다


**IO-bound / CPU-bound**

처리해야하는 10개 일

IO bound된 일일 때
- multi threading이 좋다
- extract(file을 쓰거나 network에서)

CPU-bound
- network 사용할 일 상대적으로 적음
- 그렇다면 local file을 쓰는것이 좋다


**컴퓨터 구성**

컴퓨터를 어떻게 구성하면 IO bound에 적합할까
- CPU가 강력할 필요없다
- lambda(network adapter도 한계라서 어차피 할게 없다)

Spark는 java로 짜서 GIL에 안걸린다

Multiprocessing modules


**Parallel Computing vs Distributed Computing**

Parallel Computing
Data가 parallel하게 쪼개져서 각각 돈다
Data Parallelism이 안되면 할 수 없다

Distributed Computing
메모리가 여러개이다
잘 쪼개놓으면 머신이 여러개면 그냥 처리할 수 있다


**High Availability vs Fault tolerance**

Client에서 request 줬을 때 응답을 주냐 안주느냐

Fault tolerance는 서버 관리자 입장
시스템이 정상적으로 동작해야한다
서버 관리자(Redundancy하게 두는게 제일 좋다)

High availability는 고객 가치
이렇게 만들고 싶은 거다


**Cloud**

Pay-as-you-go pricing

가격 정책
외부로 데이터 나가는 비용 비싸다

OS License는 1억
VM은 10개, Container는 1억
사실상 퍼진 이유는 이러한 비용적인 부분 때문


**Dockerfile**

Dockerfile은 연습장이 아니다
정리를 해야한다
Jupyter notebook처럼

실험 작게 하고 피드백 여러번
한줄씩 확인
실행하면 전체 돌리게 되어있다

Docker container 안에 들어가서 직접 terminal을 쳐본다
그리고 그거를 docker file에 정리하는 느낌
무작정 docker file을 적으면 안된다


**Data Product**

data + technology

Project vs Product

데이터를 가지고 한번 실행되고 되면 끝
-> Project (One time)

어떻게 reusable하게 할것인가, 만약 여러번 한다면
-> Product-driven (Reusable)
-> Evolving해야한다

Product는 계속적인 요구가 추가로 들어온다
여러개 팔면 monetary value 증가한다


**Data driven**

Data driven decision tool(Youtube)
더 사람들이 원한다

Actionable data 수준으로 원한다
