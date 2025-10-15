# croler

네이버 IT 뉴스를 자동으로 크롤링하여 정리해주는 Python 프로그램입니다.

## 개요

croler는 네이버 뉴스의 특정 분야(IT, 경제, 정치 등) 기사를 자동으로 수집하고 JSON 형식으로 저장하는 크롤링 도구입니다. 시스템 트레이에 상주하며 로컬 웹 서버를 통해 수집된 뉴스 목록을 확인할 수 있습니다.

## 주요 기능

- **자동 크롤링**: 설정된 URL에서 주기적으로 뉴스 수집
- **다중 타겟**: 여러 뉴스 카테고리 동시 크롤링
- **JSON 저장**: 구조화된 데이터로 저장
- **트레이 아이콘**: 백그라운드 실행 및 빠른 접근
- **로컬 웹 서버**: `http://127.0.0.1:2022`에서 파일 목록 확인
- **설정 파일**: JSON으로 크롤링 타겟 관리

## 프로젝트 구조

```
croler/
├── news/
│   ├── IT/
│   │   └── data/           # IT 뉴스 JSON 파일
│   └── unity/
│       ├── data/
│       │   ├── economy/    # 경제 뉴스
│       │   ├── politics/   # 정치 뉴스
│       │   └── it/         # IT 뉴스
│       └── setting/
│           └── crol_setting.json  # 크롤링 설정
├── main.py                 # 메인 크롤러
└── README.md
```

## 설치 및 실행

### 사전 요구사항
- Python 3.x
- pip

### 1. 의존성 설치

```bash
pip install requests beautifulsoup4 pystray pillow
```

### 2. 크롤링 타겟 설정

`data/setting/crol_setting.json` 파일 편집:

```json
{
  "targetList": [
    {
      "name": "IT",
      "url": "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=283"
    },
    {
      "name": "경제",
      "url": "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101"
    }
  ],
  "interval": 3600
}
```

**파라미터**:
- `name`: 카테고리 이름
- `url`: 네이버 뉴스 분야별 URL
- `interval`: 크롤링 주기 (초 단위)

### 3. 실행

```bash
python main.py
```

프로그램이 시스템 트레이에 상주하며 백그라운드에서 실행됩니다.

## 사용 방법

### 1. 트레이 아이콘 접근

- 시스템 트레이에서 croler 아이콘 우클릭
- "파일 목록 보기" 클릭
- 브라우저가 자동으로 `http://127.0.0.1:2022` 열림

### 2. 수집된 뉴스 확인

웹 인터페이스에서 수집된 뉴스 JSON 파일 목록 확인:

```
IT 뉴스 목록:
- 2022-03-18_SKT_인공지능_사업_직접_챙긴다.json
- 2022-03-18_삼성_갤럭시S22_발열_논란.json
...
```

### 3. JSON 파일 구조

```json
{
  "title": "SKT, AI 사업 직접 챙긴다",
  "date": "2022-03-18",
  "url": "https://news.naver.com/...",
  "content": "기사 본문...",
  "category": "IT",
  "keywords": ["SKT", "AI", "인공지능"]
}
```

## 크롤링 타겟 추가

### 1. 네이버 뉴스 URL 찾기

1. 네이버 뉴스 접속
2. 원하는 분야 선택 (예: IT > 모바일)
3. URL 복사

### 2. 설정 파일에 추가

`crol_setting.json`의 `targetList`에 추가:

```json
{
  "targetList": [
    {
      "name": "모바일",
      "url": "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=283"
    }
  ]
}
```

### 3. 프로그램 재시작

변경사항이 자동으로 적용됩니다.

## 네이버 뉴스 URL 형식

```
https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=[대분류]&sid2=[소분류]
```

**대분류 (sid1)**:
- `100`: 정치
- `101`: 경제
- `102`: 사회
- `103`: 생활/문화
- `104`: 세계
- `105`: IT/과학

**소분류 (sid2)** - IT 예시:
- `731`: 모바일
- `226`: 인터넷/SNS
- `227`: 통신/뉴미디어
- `230`: IT일반
- `732`: 보안/해킹
- `283`: 컴퓨터

## 주요 기능 설명

### 자동 크롤링

설정된 `interval`마다 자동으로 뉴스 수집:

```python
while True:
    crawl_news()
    time.sleep(config['interval'])
```

### 중복 제거

이미 수집한 뉴스는 스킵:

```python
if os.path.exists(filename):
    print(f"이미 존재: {filename}")
    continue
```

### 파일명 정제

URL에서 안전한 파일명 생성:

```python
filename = re.sub(r'[\\/:*?"<>|]', '', title) + '.json'
```

## 로컬 웹 서버

### 기능

- 포트: 2022
- 기능: 수집된 JSON 파일 목록 제공
- 접근: `http://127.0.0.1:2022`

### 엔드포인트

| Endpoint | 설명 |
|----------|------|
| `/` | 메인 페이지 (파일 목록) |
| `/files` | JSON 파일 목록 API |
| `/download/<file>` | 파일 다운로드 |

## 트레이 아이콘

### 메뉴

- **파일 목록 보기**: 웹 인터페이스 열기
- **설정**: 크롤링 설정 편집
- **일시 정지/재개**: 크롤링 일시 중지
- **종료**: 프로그램 종료

### 상태 표시

- 🟢 초록색: 정상 작동
- 🟡 노란색: 일시 정지
- 🔴 빨간색: 오류 발생

## newsAI 프로젝트와 연동

수집된 뉴스 데이터는 newsAI 프로젝트에서 사용:

```
croler/news/unity/data/it/*.json
→ newsAI에서 Word2Vec 분석
```

## 주의사항

### 법적 고지

⚠️ **중요**: 이 도구는 교육 목적으로 제작되었습니다.

- 네이버 뉴스 이용약관 준수 필요
- 과도한 크롤링은 IP 차단 가능
- 상업적 이용 금지
- 크롤링 간격 최소 10분 이상 권장

### 윤리적 사용

- `interval`을 충분히 길게 설정 (최소 600초)
- robots.txt 준수
- User-Agent 설정 권장

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (educational purpose crawler)'
}
```

## 문제 해결

### 크롤링 실패

```
Error: HTTP 403 Forbidden
```
- IP가 차단되었을 가능성
- `interval` 값을 더 크게 설정
- User-Agent 헤더 추가

### JSON 저장 오류

```
Error: Permission denied
```
- 쓰기 권한 확인
- 디스크 공간 확인

### 트레이 아이콘 안 보임

- pystray 설치 확인: `pip install pystray`
- 관리자 권한으로 실행

## 데이터 활용

수집된 데이터 활용 예시:

- **newsAI**: Word2Vec 단어 분석
- **트렌드 분석**: 시간대별 키워드 추출
- **감성 분석**: 긍정/부정 뉴스 분류
- **추천 시스템**: 유사 기사 추천

## 성능 최적화

- **비동기 처리**: asyncio로 동시 크롤링
- **캐싱**: 중복 요청 방지
- **압축 저장**: gzip으로 JSON 압축

## 확장 기능 아이디어

- [ ] 다른 뉴스 사이트 지원
- [ ] 이미지 다운로드
- [ ] 댓글 수집
- [ ] 데이터베이스 저장 (MongoDB)
- [ ] Telegram 봇 알림
- [ ] 스케줄링 (cron)

## 참고 자료

- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/)
- [requests 라이브러리](https://docs.python-requests.org/)
- [네이버 robots.txt](https://www.naver.com/robots.txt)

## 라이선스

교육 목적으로 작성된 프로젝트입니다. 사용 시 네이버 이용약관을 준수하세요.
