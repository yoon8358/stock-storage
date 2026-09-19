# STOCK-STORAGE DATA CONSTITUTION

Version: 1.0.0
Effective: 2026-09-20 (KST)
Status: MANDATORY

이 문서는 stock-storage의 최상위 데이터 규칙이다. 이후 수집·가공·조회·분석은 이 규칙을 우선 적용한다.

## 제1조 — 저장소의 지위
stock-storage는 '현재 사실의 정답 DB'가 아니라 **시간축을 가진 투자 지식 원장(temporal knowledge ledger)** 이다.
저장되어 있다는 이유만으로 현재에도 유효하다고 간주해서는 안 된다.

## 제2조 — 사실과 해석의 분리
1. source가 직접 뒷받침하는 내용은 fact/evidence로 저장한다.
2. 방향성, 중요도, thesis 영향 등 AI 판단은 assessment 계층으로 분리한다.
3. 추정·소문·전망을 확정 사실처럼 기록하지 않는다.

## 제3조 — 출처 의무
모든 투자 판단용 fact/event에는 source_id가 있어야 한다.
source에는 URL, 발행 주체, source_type, published_at(알 수 있는 경우), retrieved_at, primary_source 여부를 기록한다.
가능하면 SEC/규제기관/기업 IR·공시·실적자료 같은 1차 출처를 우선한다.

## 제4조 — 시간 정보 의무
시간에 따라 변할 수 있는 레코드는 다음을 구분한다.
- event_date: 실제 사건/정보가 발생한 날짜
- observed_at: 시스템이 확인한 시각
- valid_as_of: 해당 정보가 유효하다고 확인된 기준시점
- expires_at: 자동 재검증이 필요한 시점(적용 가능한 경우)
- superseded_by: 더 최신 레코드가 대체했을 때 그 ID
미래 시점 정보는 scheduled/forecast/estimate임을 명시한다.

## 제5조 — 최신성 원칙
저장소의 과거 정보만으로 '현재'를 단정하지 않는다.
현재성이 결론에 영향을 주는 질문은:
1) 저장소에서 과거 기록 검색
2) 최신성 필요한 필드 식별
3) 웹/1차 출처에서 재검증
4) 과거와 현재 비교
5) 새 레코드 append
6) 그 후 판단
순서를 따른다.

## 제6조 — 데이터 종류별 재검증
freshness_class를 사용한다.
- REALTIME: 가격, 시장반응 등 — 분석 시점에 재확인
- FAST: 뉴스, 가이던스, 애널리스트 전망, 주요 계약/규제 — 현재 판단 전 재확인
- PERIODIC: 재무실적, 백로그, 점유율 등 — 최신 보고기간 확인
- SLOW: 사업구조, 경영진, 제품군 등 — 중요한 판단 전 변경 여부 확인
- STATIC: CIK 등 사실상 고정 식별자 — 오류 징후가 있을 때 재확인
TTL은 편의를 위한 재검증 신호일 뿐, TTL 안이라는 이유로 현재 사실임을 보장하지 않는다.

## 제7조 — 불변 이력
과거 사실은 새 정보가 나왔다고 삭제/덮어쓰지 않는 것을 원칙으로 한다.
정정은 status=corrected/retracted/superseded 및 superseded_by로 연결한다.
명백한 저장 오류 수정은 변경 이력이 Git commit에 남아야 한다.

## 제8조 — 식별자
회사 정보는 ticker만으로 동일성을 판단하지 않는다.
가능하면 ticker + exchange + CIK/LEI 등 안정적 식별자를 registry에 기록한다.
티커 변경, 합병, 분할, 상장폐지는 별도 event로 남긴다.

## 제9조 — 원자성
facts.jsonl 한 레코드에는 가능한 한 하나의 검증 가능한 주장만 저장한다.
한 기사 전체 요약을 하나의 fact로 저장하지 않는다.
같은 출처에서 여러 독립 사실이 나오면 여러 fact로 분리한다.

## 제10조 — 중복과 충돌
동일 사실의 반복 수집은 source 추가 또는 evidence 연결로 처리하고 무의미한 중복 fact 생성을 피한다.
서로 충돌하는 출처가 있으면 하나를 임의 삭제하지 말고 conflict 상태와 양쪽 source를 보존한다.

## 제11조 — 신뢰도
confidence는 출처의 존재만으로 high가 되지 않는다.
1차 출처 여부, 직접성, 최신성, 상호검증 여부를 고려한다.
AI의 confidence는 사실의 진실도를 보증하는 값이 아니다.

## 제12조 — 조회 규칙
현재 투자판단에 사용되는 레코드는 최소한 ticker/entity, category/topic, source, 시간정보, freshness 상태를 확인한다.
superseded/retracted/expired 레코드는 현재 근거로 단독 사용하지 않는다.

## 제13조 — 저장 단위
기계 검색용 데이터는 JSON/JSONL을 우선한다.
사람이 읽는 종합 분석은 Markdown을 사용할 수 있으나, 핵심 evidence는 구조화 데이터에도 존재해야 한다.
Markdown만 존재하는 판단은 장기 데이터 근거로 간주하지 않는다.

## 제14조 — 스키마 검증
schema/의 JSON Schema를 저장 규격으로 사용한다.
필수 필드가 없는 레코드는 정식 evidence로 승격하지 않는다.
스키마 변경 시 schema_version을 올리고 하위 호환성 또는 migration 방법을 기록한다.

## 제15조 — 분석 실패 안전장치
최신 검증에 실패하면 오래된 데이터를 최신인 것처럼 대신 사용하지 않는다.
그 경우 stale/unverified임을 표시하고 판단의 불확실성으로 반영한다.

## 제16조 — 핵심 원칙
**GitHub는 기억이고, 최신 출처 확인은 현재 상태 검증이다. 둘을 결합한 뒤에만 현재 투자 판단을 만든다.**
