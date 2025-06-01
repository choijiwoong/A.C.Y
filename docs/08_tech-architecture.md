# 🛠 com.on 기술 구조 문서

---

## 1. 📦 전체 구조 개요

com.on은 **Flask 기반의 웹 애플리케이션**으로,
클라이언트에서 사용자 입력을 받아 n8n 및 외부 API와 연동하여 맞춤형 추천 결과를 생성합니다.

### 🧱 주요 구성 요소

* **Frontend**

  * HTML + JavaScript로 구성된 정적 페이지(`index.html`, `result.html`)
  * 초기에는 메카니컬 터크 방식의 **빠른 프리토타이핑**을 위해 간단하게 구축됨
  * `result.html`은 사용자가 입력한 프롬프트를 n8n의 **ChatGPT Agent**를 통해 처리한 뒤, 해당 결과를 **HTML 카드 형태로 출력**함
  * 2025년 6월 1일 기준, 실제 서비스화되는 MVP에 맞춰 **React 등으로 프론트 리팩토링 예정**

* **Backend (Flask)**

  * Python 기반 Flask를 사용하여 라우팅 및 API 제공
  * com.on은 복잡한 기능보다는 추천 카드 렌더링 중심이므로 **가볍고 직관적인 백엔드 프레임워크로 Flask 선택**

* **추천 엔진 및 API 연동**

  * n8n은 두 가지 용도로 사용 중:

    1. ChatGPT 기반 추천 Agent 실행 (OpenAI API 연동 포함)
    2. **네이버 이미지 검색 API**의 **Proxy 역할** (API 키 숨김용)
  * 다만, n8n에 의존적인 구조이므로 **차후 Flask 기반 자체 API 서버로 리팩토링 여부를 검토 중**

* **외부 API 활용**

  * **쿠팡 API**: 이미지, 가격, 리뷰, 상세페이지 링크 등 **검색 정확도 향상**을 위한 실험 중
  * 현재는 임시로 `https://www.coupang.com/np/search?q={query}` 형식의 URL을 활용해 상세 링크를 생성 중이며, **쿠팡 공식 API 도입 시 보완 예정**

* **배포**

  * 현재는 **Render.com 무료 요금제**를 통해 배포 중
  * Docker 기반 무중단 배포를 검토했으나, 현재는 서비스가 가벼워 **중단 배포도 무방**하다고 판단하여 추후 논의 예정
  * 사용자 접속 초기 대기시간 문제는 **Render 유료 플랜 전환 또는 AWS 이전 여부를 비교해 대응 예정**

---

## 2. 🔁 사용자 흐름 요약

```plaintext
사용자 질문 입력 (index.html)
          ↓
 JS fetch → Flask API 요청 (/ask 등)
          ↓
 Flask → n8n ChatGPT Agent 또는 외부 API 호출
          ↓
 추천 카드 HTML 반환
          ↓
 결과 페이지(result.html)에 렌더링
```

---

## 3. 🔗 API 연동 구조

### ✅ n8n Webhook

* **Endpoint**: `https://n8n.1000.school/webhook/{workflow_id}`
* **Method**: `POST`
* **Payload 예시**:

  ```json
  {
    "question": "맥북 추천해줘"
  }
  ```
* **Response**:
  HTML `<div class="product">...</div>` 카드 형태로 반환됨 (ChatGPT 기반 프롬프트 처리 결과)

---

### ✅ 외부 API 목록

| 목적     | API 설명                    | 방식     | 비고                     |
| ------ | ------------------------- | ------ | ---------------------- |
| 이미지 검색 | 네이버 검색 API (n8n proxy 처리) | REST   | API 키 숨김 처리 목적         |
| 쇼핑 링크  | 쿠팡 검색 링크 (`q=${p.name}`)  | URL 생성 | CPS 기반 수익 모델 활용        |
| 상세검색   | Flask 내부 API (구글 검색 이용)   | GET    | 실시간 링크 크롤링 (쿠팡/네이버 한정) |
| GPT 처리 | OpenAI API (n8n 내부 사용)    | POST   | 프롬프트 기반 추천 카드 생성       |

---

## 4. ⚙️ 기술 스택

| 영역     | 사용 기술                     |
| ------ | ------------------------- |
| 프론트엔드  | HTML, CSS, JavaScript     |
| 백엔드    | Python (Flask)            |
| 데이터 처리 | n8n (Workflow Automation) |
| API 연동 | Fetch API, RESTful API    |
| 배포     | Render.com (무료 플랜)        |
| 향후 보완  | Docker, React, AWS 등      |

---

## 5. 🚧 향후 개발 계획

* React 기반 컴포넌트 UI로 프론트 리팩토링
* n8n → Flask 기반 자체 API 서버 전환 여부 검토
* Docker 기반 무중단 배포 및 구조 분리 (선택적)
* 쿠팡 API 정밀 활용 + 사용자 로그 기반 추천 고도화
* Render 유료 요금제 전환 or AWS 등 대안 인프라 비교

---

## 6. 📎 관련 문서

* [서비스 개요 및 배경](./00_overview.md)
* [MVP 진행 현황](./05_mvp-status.md)
* [비즈니스 모델](./06_business-model.md)
* [사용자 흐름 UX](./04_user-flow.md)

---

## 7. 🧪 현재 Flask API 라우트 요약

| 라우트                  | 설명                                          |
| -------------------- | ------------------------------------------- |
| `/`                  | index.html 렌더링 (질문 입력 UI)                   |
| `/result.html`       | result.html 렌더링 (추천 카드 표시 UI)               |
| `/api/questions`     | questions.json에서 질문 리스트 불러오기                |
| `/api/products`      | products.json에서 쿼리에 맞는 제품 목록 반환             |
| `/api/google_search` | Google Custom Search 통해 쿠팡/네이버 링크 5개 크롤링 반환 |

---
