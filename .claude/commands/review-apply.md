# Command: /review-apply

## 목적

GitHub PR 리뷰 코멘트를 가져와서
리뷰 내용을 분석하고 코드에 자동 적용한다.

---

## 사용 방법

```
/review-apply <PR 번호>
```

예시

```
/review-apply 3
```

---

## 동작 규칙

### 1. PR 리뷰 조회

다음 명령으로 PR 리뷰를 가져온다.

```bash
GH_TOKEN=<token> gh pr view <PR번호> \
  --repo EDDI-RobotAcademy/alpha-desk-ai-server \
  --json reviews,comments
```

GH_TOKEN이 없으면 사용자에게 요청한다.

### 2. 리뷰 내용 분석

조회된 리뷰에서 다음을 추출한다.

- 리뷰어 (author.login)
- 리뷰 상태 (state: APPROVED / COMMENTED / CHANGES_REQUESTED)
- 리뷰 본문 (body)
- 제출 시각 (submittedAt)

### 3. 코드 변경 필요 여부 판단

리뷰 본문을 분석하여 코드 수정이 필요한 항목을 식별한다.

- ❌ 표시 → 규칙 위반, 반드시 수정
- ⚠️ 표시 → 경고, 수정 권장
- 💡 표시 → 제안, 선택적 수정

### 4. 코드 자동 적용

각 수정 항목에 대해

1. 관련 파일을 탐색한다
2. 리뷰에서 제시한 수정 방향을 코드에 반영한다
3. CLAUDE.md 아키텍처 규칙을 위반하지 않는지 확인한다

### 5. 적용 결과 보고

수정 완료 후 다음 형식으로 보고한다.

```
## 리뷰 적용 결과

리뷰어: <author>
PR: #<번호>

### 적용 완료
- [파일경로] <수정 내용>

### 미적용 (이유)
- <항목> → <미적용 사유>
```

---

## 주의 사항

- CLAUDE.md 아키텍처 규칙이 리뷰보다 우선한다
- 리뷰 내용이 CLAUDE.md와 충돌하면 사용자에게 확인 후 적용한다
- 코드 적용 전 관련 파일을 반드시 Read로 읽고 확인한다
- 삭제 요청 파일은 사용자 확인 후 삭제한다

ARGUMENTS: $ARGUMENTS
