---
name: check-a4-page-fit
description: A4 HTML/CSS 문서의 페이지별 사용률, 남은 높이, 요소 이동 후 적합 여부와 실제 인쇄 페이지 수를 검증한다. 이력서·포트폴리오·인쇄용 HTML이 A4에 들어가는지, 페이지가 늘어나는지, 섹션을 다른 페이지로 옮겨도 되는지 확인할 때 사용한다.
---

# A4 페이지 적합성 검사

## 기준

- 이 프로젝트의 A4 높이는 `297mm`, 위·아래 여백은 각각 `11mm`, 본문 높이는 `275mm`다.
- CSS 픽셀 변환은 `1mm = 96 / 25.4px`이며, `275mm ≈ 1039.37px`다.
- `@page` 세로 여백이 바뀌면 본문 높이를 `297 - 위 여백 - 아래 여백`으로 다시 계산한다.
- 기준 배율은 `100%`다. 사용자 지정 배율은 별도 조건으로만 보고한다.
- 현재 HTML과 로드가 끝난 폰트로만 측정한다.

## 검사 절차

1. `Ctrl+P`에서 용지를 A4, 배율을 100%로 설정한다.
2. 실제 페이지 수, 잘림, 빈 페이지, 카드 강제 이동, 제목·본문 분리를 확인한다.
3. Chrome CDP에서 `Emulation.setEmulatedMedia({ media: "print" })`를 적용하고 `document.fonts.ready`를 기다린 뒤, 각 `.page`의 `getBoundingClientRect().height`를 측정한다.
4. 페이지별 사용률을 계산한다.

   `사용률 = 사용한 콘텐츠 높이 / 275mm × 100`

5. 요소 이동 전에는 다음 값을 모두 포함해 예상 높이를 계산한다.

   `예상 높이 = 현재 사용 높이 + 이동 요소의 margin 포함 높이 + 새 간격 - 제거되는 높이`

6. `scripts/calculate_page_fit.py`로 수치를 판정한다.

   ```powershell
   python .agents/skills/check-a4-page-fit/scripts/calculate_page_fit.py --used 900 --delta 100 --unit px
   ```

7. 변경 후 `Ctrl+P`와 수치 계산을 모두 다시 실행한다.

브라우저 자동 검증은 `Page.printToPDF`에 `preferCSSPageSize: true`, `printBackground: true`, `scale: 1`을 사용한다.

## 판정

- `SAFE`: 사용률 95% 이하
- `TIGHT`: 95% 초과 100% 이하. 폰트·줄바꿈 차이에 취약하므로 인쇄 결과를 반드시 재확인한다.
- `OVERFLOW`: 100% 초과. 이동하거나 압축해야 한다.
- 수치가 100% 이하라도 `page-break-inside: avoid`, `.page-break`, 폰트 로딩 때문에 페이지가 늘 수 있다. 실제 인쇄 결과가 우선이다.
- 두 검사 중 하나라도 실패하면 A4 적합으로 판정하지 않는다.

## 결과 보고 형식

```text
페이지 1: 사용률 00.0% | 남은 높이 00.0mm | SAFE/TIGHT/OVERFLOW
페이지 2: 사용률 00.0% | 남은 높이 00.0mm | SAFE/TIGHT/OVERFLOW
Ctrl+P: A4 100% | 총 0장 | 잘림/강제 이동 여부
결론: 적합/부적합과 필요한 조치
```
