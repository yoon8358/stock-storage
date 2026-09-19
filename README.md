# stock-storage

주식 분석소의 구조화된 투자정보 저장소입니다.

## 저장 원칙
- 기사/공시 원문을 무작정 복사하지 않고 검색 가능한 **원자적 사실(fact)** 로 가공합니다.
- **출처가 말한 사실**과 **우리의 투자 해석**을 분리합니다.
- 모든 사실은 출처(source_id)와 관측 시점(observed_at)을 가집니다.
- ticker, category, topic, themes, importance, confidence를 사용해 필요한 정보만 조회합니다.
- 시간이 지나며 바뀌는 정보는 가능하면 덮어쓰지 않고 이력을 남깁니다.

## 구조
- `registry/companies.json` — 기업 식별자/티커 레지스트리
- `registry/themes.json` — 투자 테마 레지스트리
- `sources/sources.jsonl` — 출처 레지스트리
- `market/macro.jsonl` — 거시경제 사실/이벤트
- `market/industry.jsonl` — 산업 공통 사실/이벤트
- `stocks/<TICKER>/profile.json` — 기업 기본정보
- `stocks/<TICKER>/thesis.json` — 현재 thesis, 핵심 근거, 반증 조건
- `stocks/<TICKER>/facts.jsonl` — 종목별 원자적 evidence
- `stocks/<TICKER>/events.jsonl` — 실적·계약·제품·규제 등 사건
- `stocks/<TICKER>/financials.jsonl` — 시점별 재무 관측치
- `stocks/<TICKER>/snapshots/` — 특정 시점의 종합 분석
- `schema/` — JSON Schema

## 핵심 조회 키
`ticker`, `event_date`, `observed_at`, `category`, `topic`, `direction`, `importance`, `confidence`, `themes`, `source_id`, `thesis_effect`

JSONL은 한 줄에 JSON 객체 하나를 저장합니다. 따라서 향후 AI나 프로그램이 전체 문서를 다시 읽지 않고 필요한 레코드만 선별할 수 있습니다.
