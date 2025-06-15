# 🛠 com.on 기술 구조 문서 (업데이트: 2025.06.15)

---

## 1. 📦 전체 구조 개요

com.on은 **Flask 기반의 웹 애플리케이션**으로,  
사용자의 자연어 입력을 기반으로 **맞춤형 쇼핑 추천**을 제공합니다.  
추천 엔진은 ChatGPT 및 외부 API들과 연동되며, 프론트엔드는 간단한 정적 HTML로 구성되어 있습니다.

### 🧱 주요 구성 요소

- **Frontend**
  - HTML + JavaScript 기반 정적 페이지 (`index.html`, `result.html`)
  - 빠른 검증을 위한 **메카니컬 터크 방식 프로토타입**으로 시작 -> mvp확장 중
  - `result.html`에서 **ChatGPT 결과 HTML 카드**를 렌더링
  - ✅ **Intro 문구 + 제품 카드 병렬 출력**으로 UX 개선
  - ✅ **로딩 애니메이션 + 타이핑 효과** 적용
  - ✅ **SEO 최적화** 완료
  - 🛠 React 기반 UI로 리팩토링 예정

- **Backend (Flask)**
  - Python Flask로 API 제공 및 라우팅 처리
  - 쿠키 기반 **사용자 식별 시스템** 및 **행동 로그 저장**
  - ✅ `search`, `chat`, `click`, `event` 등 주요 기능별 라우트 구성
  - ✅ **공격성 쿼리 방어 로직**, **검색 속도 측정 로깅** 적용

- **추천/연동 시스템**
  - n8n Workflow:
    1. ChatGPT 기반 추천 Agent
    2. 네이버 이미지 검색 API 중계(proxy)
  - ✅ **역질문 기반 인터랙션** 및 클릭 로깅 포함
  - ✅ **네이버 쇼핑 API로 가격/링크 보완**
  - ✅ **Google 검색 API를 통한 실시간 링크 크롤링** 보류

- **배포**
  - **Render.com 무료 플랜** 기반 배포
  - ✅ `keep-alive` 라우트로 초기 접속 대기시간 개선
  - ✅ **Docker 빌드 환경 설정 완료**
  - 🛠 AWS 이전 여부 검토 중

- **모니터링**
  - ✅ [UptimeRobot](https://uptimerobot.com/) 활용하여 웹 서비스 상태 모니터링

---

## 2. 🔁 사용자 흐름 요약

```plaintext
사용자 질문 입력 (index.html)
        ↓
 JS fetch → Flask API 호출 (/chat 또는 /api/products)
        ↓
 Flask → n8n GPT Agent 또는 외부 API 호출
        ↓
 추천 카드 HTML + 가격/링크 반환
        ↓
 result.html에서 병렬 렌더링 (Intro + 제품 카드)

## 3. 🔗 API 연동 구조

| 목적        | API 설명                             | 방식    | 비고                             |
|-----------|------------------------------------|-------|--------------------------------|
| GPT 추천     | n8n Webhook → OpenAI API            | POST  | HTML 카드 형태로 반환               |
| 이미지 검색   | 네이버 검색 API (n8n proxy)           | REST  | API 키 보안 목적 proxy 처리        |
| 가격/링크 검색 | `/api/get_price` (Naver Shopping API) | POST  | 정확한 가격 + 상세 링크 제공        |
| 상세검색     | `/api/google_search` (Google 검색)    | GET   | 쿠팡/네이버 실시간 제품 링크 추출     |
| 대화 기반 추천 | `/chat`                              | POST  | 역질문 인터페이스, 최종 검색 키워드 생성 |
| 이벤트 로깅  | `/log/click`, `/log/event`            | POST  | 상세 클릭/역질문/채팅 등 사용자 행동 기록 |

## 4. ⚙️ 기술 스택

| 영역        | 사용 기술                             |
|-----------|------------------------------------|
| 프론트엔드    | HTML, CSS, JavaScript               |
| 백엔드      | Python (Flask)                      |
| 추천 엔진    | OpenAI GPT API                     |
| 자동화 워크플로우 | n8n                                 |
| 외부 API    | Naver Search, Google Search         |
| 배포       | Render.com + Docker 빌드             |
| 모니터링     | UptimeRobot                         |
| 분석 도구    | Google Analytics 4 (GA4) 적용 중     |
| 향후 계획    | React, AWS                          |


## 5. 🚧 향후 개발 계획

- ✅ Docker 배포 환경 구축 완료
- 🛠 React 기반 UI 리팩토링 (컴포넌트 단위 재구성)
- 🛠 AWS 인프라로 이전 검토 (Lambda, EC2 등 비교 예정)
- ✅ GA4 기반 사용자 행동 분석 고도화
- ✅ 로그 기반 개인화 추천 시스템 준비
- 🛠 AI비중을 줄이고 api이용하여 정확도&속도 개선

## 7. 🧪 Flask API 라우트 요약

| 라우트                  | 설명                                               |
|----------------------|--------------------------------------------------|
| `/`                  | index.html 렌더링 (사용자 쿠키 생성 포함)                |
| `/search`            | result.html 렌더링 (결과 카드 출력)                    |
| `/api/questions`     | 질문카드 리스트 JSON 반환                                 |
| `/api/products`      | 제품 추천 결과 반환 (기본 프롬프트 기반)                    |
| `/api/google_search` | 실시간 구글 검색 → 쿠팡/네이버 제품 링크 5개 반환             |
| `/api/get_price`     | 네이버 쇼핑 API 기반 가격/링크 추출                        |
| `/chat`              | 대화형 추천 API (GPT 프롬프트에 따라 역질문 처리 포함)         |
| `/log/click`         | 제품 카드 클릭 이벤트 로깅                                 |
| `/log/event`         | 검색/역질문/채팅 등 전체 이벤트 로깅                         |
| `/api/keep-alive`    | UptimeRobot ping 응답 라우트                               |
| `/sitemap.xml`       | SEO 사이트맵 제공                                       |
| `/robots.txt`        | 크롤러용 robots 정책 파일                                 |
