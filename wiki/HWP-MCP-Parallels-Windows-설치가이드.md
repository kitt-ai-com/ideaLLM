---
tags:
  - 도구
  - HWP
  - MCP
  - 정부지원
date: 2026-06-02
---

> [!takeaway] 핵심 테이크어웨이
> 맥에는 한글을 직접 제어하는 MCP가 **없다**(구조적 한계). 하지만 **Parallels Windows + 한글 설치** 환경이 있으면 `hwp-mcp`로 *양식에 내용 채워 제출용 HWP 생성*이 가능하다. 단 MCP·Claude·한글이 **모두 Windows 안**에 있어야 깔끔하다. 이 가이드는 청년창업 바우처(6/8) 같은 제출용 HWP 양식 작성에 직접 쓰인다. 맥쪽 변환(읽기 전용)은 [[사업과제-스케줄-마스터]]에서 설치한 @ohah/hwpjs로 따로 처리.

# HWP-MCP 설치 가이드 (Parallels Windows)

> ⚠️ **이 가이드의 모든 명령은 맥이 아니라 Parallels 안의 Windows에서 실행한다.**

## 왜 Windows에서 하나 (구조 이해)

| 도구 | 한글 설치 | OS | 할 수 있는 일 |
|---|---|---|---|
| `@ohah/hwpjs` (맥에 설치됨) | 불필요 | 맥/Linux | 읽기·변환·이미지추출 (편집 ❌) |
| **`hwp-mcp`** (이 가이드) | **필요** | **Windows 전용** | 문서 생성·텍스트 삽입·**표 채우기**·저장 |

`hwp-mcp`는 한글 프로그램을 **COM 자동화(pywin32)**로 조종한다. 그래서 한글이 깔린 Windows에서만 동작한다. Parallels로 Windows + 한글이 준비됐으니 의도된 환경이 갖춰진 것.

---

## 사전 준비 (Windows 안)

> ⚠️ **모든 작업은 맥이 아니라 Parallels Windows 안에서 한다.**
> PowerShell 열기: 시작 버튼 → `PowerShell` 입력 → 실행

- [x] Windows (Parallels) — 확인됨
- [x] 한글(HWP) 프로그램 설치 — 확인됨
- [ ] **0-A. Python 3.7+** → [python.org/downloads/windows](https://www.python.org/downloads/windows/) (설치 첫 화면에서 **"Add Python to PATH" 반드시 체크**)
- [ ] **0-B. Claude Desktop** → [claude.ai/download](https://claude.ai/download) Windows판 (← 이게 없으면 hwp-mcp를 써도 부를 방법이 없음)
- [ ] **0-C. Git** (선택) → [git-scm.com/download/win](https://git-scm.com/download/win) — 없으면 ZIP 다운로드로 대체

**설치 확인** (PowerShell에서):
```powershell
python --version
pip --version
```
버전이 나오면 OK. `python`이 안 먹으면 `py --version` 시도.

---

## 1단계: hwp-mcp 내려받기 (PowerShell)

```powershell
cd $env:USERPROFILE
git clone https://github.com/jkf87/hwp-mcp.git
cd hwp-mcp
```

→ 받아지는 위치: `C:\Users\<사용자명>\hwp-mcp`

> [!note] Git이 없을 때 (ZIP 방식)
> 1. 브라우저로 https://github.com/jkf87/hwp-mcp 접속
> 2. 초록색 **Code → Download ZIP**
> 3. `C:\Users\<사용자명>\hwp-mcp` 에 압축 해제 (폴더 안에 `hwp_mcp_stdio_server.py`가 바로 보이게)
> 4. PowerShell에서 `cd $env:USERPROFILE\hwp-mcp`

## 2단계: Python 패키지 설치

```powershell
pip install -r requirements.txt
pip install mcp
```

설치되는 핵심 패키지: `pywin32`(한글 COM 제어), `comtypes`, `fastmcp`, `mcp`

## 3단계: 연결 테스트 (한글 먼저 실행해두기)

```powershell
python hwp_mcp_stdio_server.py
```

- 에러 없이 멈춰 있으면(입력 대기) 정상 → **Ctrl+C로 종료**
- "한글을 찾을 수 없음" 류 에러 → 한글 프로그램 먼저 실행 후 재시도, COM 보안경고는 허용
- `python`이 안 되면 `py hwp_mcp_stdio_server.py`

## 4단계: Claude Desktop에 MCP 등록

**4-1. config 파일 열기** — PowerShell에서:
```powershell
notepad $env:APPDATA\Claude\claude_desktop_config.json
```
> "파일을 만들까요?" 물으면 **예**. (Claude Desktop을 한 번도 안 켰으면 폴더가 없을 수 있음 → 먼저 Claude Desktop 1회 실행 후 종료)

**4-2. 아래 내용 붙여넣기** (이미 다른 mcpServers가 있으면 `"hwp"` 항목만 추가):
```json
{
  "mcpServers": {
    "hwp": {
      "command": "python",
      "args": ["C:\\Users\\<사용자명>\\hwp-mcp\\hwp_mcp_stdio_server.py"]
    }
  }
}
```

> - `<사용자명>`을 실제 Windows 계정명으로 교체. 모르면 PowerShell에 `echo $env:USERNAME`.
> - 경로 역슬래시는 반드시 `\\` 두 개.
> - `python`이 PATH에 없던 경우 `"command"`를 `py` 또는 python 전체경로로.

**4-3. 저장 후 Claude Desktop 완전 종료 → 재시작.**
→ 채팅창 입력란의 🔨(도구) 아이콘에 `hwp` 도구들이 보이면 성공.

---

## 주요 도구 (Claude에게 시키는 작업)

| 도구 | 기능 |
|---|---|
| `hwp_create()` | 새 한글 문서 생성 |
| `hwp_open(path)` | 기존 HWP(양식) 열기 |
| `hwp_insert_text(text)` | 커서 위치에 텍스트 삽입 |
| `hwp_insert_table(rows, cols)` | 표 생성 |
| `hwp_fill_table(...)` | 표 셀 채우기 (hwp_table_tools 모듈) |
| `hwp_save(path)` | 저장 |
| batch operations | 여러 편집 명령 묶음 실행 |

---

## 청년창업 바우처 제출 실전 흐름 (6/8)

1. Parallels Windows에서 Claude Desktop + hwp-mcp 실행
2. 공유폴더로 `nxt/AI 청년창업기업 동반성장 바우처/` 양식 HWP를 Windows에서 접근
3. 우리가 이미 작성한 MD 내용([[과제/AI청년창업기업-동반성장바우처]] 체크리스트의 9종)을 Claude에게 주고 양식 HWP에 채우게 함
4. 인감 날인란 등 수기 항목 표시 → 출력 후 날인
5. nxt.nipa.kr 온라인 제출

> [!tip] 맥 ↔ Windows 파일 공유
> Parallels는 기본적으로 맥 홈폴더를 Windows에서 네트워크 드라이브로 마운트한다.
> `\\Mac\Home\Claude\ideaLLM\ideaLLM\nxt\...` 경로로 맥의 양식 파일에 바로 접근 가능.

---

## 한계 / 주의

- **맥쪽 Claude에서는 직접 못 부른다** — MCP·한글·Claude가 모두 Windows 안에 있어야 함 (원격 브리지는 복잡)
- `.hwpx`는 hwp-mcp/hwpjs 모두 제약 → 한글에서 직접 열어 `.hwp`로 저장 후 처리
- COM 자동화는 한글이 떠 있어야 안정적 (백그라운드 모드 불안정 시 한글 먼저 실행)
- 표 채우기는 양식의 셀 구조에 민감 → 결과 반드시 육안 검증

## 관련 페이지
- [[사업과제-스케줄-마스터]] — 6/8 청년창업 바우처 마감, 맥쪽 hwpjs 변환 도구
- [[과제/AI청년창업기업-동반성장바우처]] — 채워 넣을 서류 9종 체크리스트

## 출처
- [hwp-mcp (jkf87)](https://github.com/jkf87/hwp-mcp) — requirements.txt, README
- hwp 스킬 라우팅 정책 (Windows direct-control path)
- 처리일: 2026-06-02
