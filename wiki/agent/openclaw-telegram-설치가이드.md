> [!takeaway] 핵심 테이크어웨이
> 마케팅/광고 대행사 운영 관점에서 OpenClaw는 무료 AI 모델을 텔레그램 봇으로 연동해 팀 커뮤니케이션 채널에 AI를 즉시 투입할 수 있는 도구. 별도 서버 없이 로컬에서 구동되고, 무료 모델 폴백 체인으로 비용 없이 운영 가능.

# OpenClaw — Telegram 연동 설치 가이드

## 개요

OpenClaw는 AI 모델을 다양한 채널(텔레그램 등)에 게이트웨이로 연결해주는 CLI 도구. 무료 LLM 모델을 우선 사용하고 rate limit 초과 시 자동 폴백.

## 설치 순서

### 1단계: 환경 준비

- Node.js 26.x 설치 (`brew install node`)
- OpenClaw 전역 설치: `npm install -g openclaw@latest`

### 2단계: 필요한 API 키

| 키 | 발급처 | 용도 |
|---|---|---|
| Groq API Key | console.groq.com/keys | AI 모델 (무료) |
| OpenRouter API Key | openrouter.ai/keys | AI 모델 (무료) |
| Telegram Bot Token | @BotFather → /newbot | 텔레그램 봇 |

### 3단계: 환경변수 등록

```bash
echo 'export GROQ_API_KEY="키입력"' >> ~/.zshrc
echo 'export OPENROUTER_API_KEY="키입력"' >> ~/.zshrc
source ~/.zshrc
```

### 4단계: 설정 파일

`~/.openclaw/openclaw.json` 생성:

```json
{
  "gateway": { "mode": "local" },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/google/gemma-4-31b-it:free",
        "fallbacks": [
          "groq/llama-3.3-70b-versatile",
          "openrouter/openai/gpt-oss-120b:free"
        ]
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "봇토큰입력",
      "dmPolicy": "pairing"
    }
  }
}
```

### 5단계: 게이트웨이 시작 및 페어링

```bash
# 게이트웨이 시작
openclaw gateway

# 텔레그램 봇에 메시지 전송 → 페어링 코드 수신 후
openclaw pairing approve telegram [페어링코드]
```

## 모델 폴백 전략

Gemma free → Groq → OpenRouter 순서로 자동 폴백. 모두 실패 시 몇 분 대기 후 재시도.

## 관련 페이지

- [[킷에이아이-AI에이전트-사업전략]]
- [[도구-기술]]

## 출처

- 원본: 사용자 제공 설치 가이드 (채팅)
- 처리일: 2026-06-09
