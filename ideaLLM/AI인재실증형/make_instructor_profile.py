#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유승범 AI 교육 강사 프로필 PDF (A4 세로, 1장)
"""

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUT = "/Users/jasonmac/Claude/ideaLLM/ideaLLM/AI인재실증형/강사프로필_유승범.pdf"
W, H = 595, 842  # A4

# 색상
C_NAVY     = HexColor("#1a1a2e")
C_ACCENT   = HexColor("#7c83ff")
C_ACCENT2  = HexColor("#a8acff")
C_BG       = HexColor("#f5f5fb")
C_CARD     = HexColor("#eeeeff")
C_GRAY     = HexColor("#666666")
C_LGRAY    = HexColor("#cccccc")
C_WHITE    = white
C_GREEN    = HexColor("#2ecc71")
C_ORANGE   = HexColor("#f39c12")

FONT_PATHS = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleGothic.ttf",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
]

def reg_font():
    for fp in FONT_PATHS:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont("KR", fp, subfontIndex=0))
                pdfmetrics.registerFont(TTFont("KR-B", fp, subfontIndex=1))
                return "KR", "KR-B"
            except:
                try:
                    pdfmetrics.registerFont(TTFont("KR", fp))
                    pdfmetrics.registerFont(TTFont("KR-B", fp))
                    return "KR", "KR-B"
                except:
                    continue
    pdfmetrics.registerFont(TTFont("KR", "/System/Library/Fonts/Helvetica.ttc"))
    return "KR", "KR"

def rect(c, x, y, w, h, fill=None, stroke=None, radius=0):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    else:
        c.setStrokeColor(HexColor("#00000000"))
    if radius > 0:
        c.roundRect(x, y, w, h, radius, fill=1 if fill else 0, stroke=1 if stroke else 0)
    else:
        c.rect(x, y, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)

def txt(c, text, x, y, font, size, color=None, align="left"):
    if color:
        c.setFillColor(color)
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)

def make_profile():
    F, FB = reg_font()
    c = canvas.Canvas(OUT, pagesize=(W, H))

    # ── 배경 ──────────────────────────────────────────────
    rect(c, 0, 0, W, H, fill=C_WHITE)

    # ── 상단 헤더 바 (네이비) ──────────────────────────────
    rect(c, 0, H-130, W, 130, fill=C_NAVY)

    # 헤더 왼쪽 — 이름·직함
    txt(c, "유  승  범", 40, H-58, FB, 28, C_WHITE)
    txt(c, "Seungbeom Yoo", 43, H-76, F, 11, C_ACCENT2)
    txt(c, "AI 자동화 전문 강사  |  주식회사 킷에이아이 대표", 40, H-100, F, 11, HexColor("#bbbbee"))
    txt(c, "kitt.ai.ceo@gmail.com", 40, H-118, F, 10, C_LGRAY)

    # 헤더 오른쪽 — 키워드 태그
    tags = ["AI 에이전트", "업무 자동화", "ChatGPT 활용", "마케팅 AI", "창업·스타트업"]
    tx = W - 40
    for tag in tags:
        tw = len(tag) * 9 + 16
        tx -= tw
        rect(c, tx, H-75, tw, 20, fill=C_ACCENT, radius=10)
        txt(c, tag, tx + tw/2, H-63, F, 9, C_WHITE, align="center")
        tx -= 6

    # ── 좌측 컬럼 (x: 30~235) ──────────────────────────────
    LX = 30
    LW = 205

    # 전문 분야
    rect(c, LX, H-175, LW, 22, fill=C_NAVY, radius=4)
    txt(c, "전문 분야", LX+10, H-162, FB, 11, C_WHITE)

    areas = [
        ("🤖", "AI 에이전트 설계·구현"),
        ("📊", "마케팅 데이터 자동화"),
        ("✍️", "콘텐츠 자동화 파이프라인"),
        ("🏢", "B2B 업무 프로세스 AI 전환"),
        ("🚀", "창업 실전 AI 활용"),
    ]
    ay = H - 190
    for icon, area in areas:
        rect(c, LX, ay-2, LW, 18, fill=C_CARD, radius=3)
        txt(c, f"{icon} {area}", LX+8, ay+4, F, 10, C_NAVY)
        ay -= 22

    # 강의 대상
    rect(c, LX, ay-10, LW, 22, fill=C_NAVY, radius=4)
    txt(c, "강의 대상", LX+10, ay+2, FB, 11, C_WHITE)
    ay -= 28

    targets = ["직장인·소상공인 AI 활용", "시니어 디지털 역량강화", "여성 재취업 디지털 교육",
               "스타트업·예비창업자", "초중고 AI·SW 교육"]
    for t in targets:
        txt(c, f"▸  {t}", LX+8, ay, F, 10, C_NAVY)
        ay -= 18

    # 강의 형태
    rect(c, LX, ay-10, LW, 22, fill=C_NAVY, radius=4)
    txt(c, "강의 형태 & 조건", LX+10, ay+2, FB, 11, C_WHITE)
    ay -= 28

    conditions = [
        "오프라인 출강 / 온라인 가능",
        "1회 특강 ~ 정기 과정 모두 가능",
        "실습 중심 (노트북 지참 권장)",
        "강의료 협의 가능",
    ]
    for cond in conditions:
        txt(c, f"•  {cond}", LX+8, ay, F, 10, C_NAVY)
        ay -= 17

    # 연락처 박스
    ay -= 5
    rect(c, LX, ay-36, LW, 42, fill=C_ACCENT, radius=6)
    txt(c, "강의 문의", LX+10, ay+2, FB, 11, C_WHITE)
    txt(c, "kitt.ai.ceo@gmail.com", LX+10, ay-14, F, 10, C_WHITE)
    txt(c, "주식회사 킷에이아이", LX+10, ay-28, F, 9, HexColor("#ddddff"))

    # ── 우측 컬럼 (x: 255~565) ──────────────────────────────
    RX = 255
    RW = W - RX - 30

    # 강사 소개
    rect(c, RX, H-175, RW, 22, fill=C_NAVY, radius=4)
    txt(c, "강사 소개", RX+10, H-162, FB, 11, C_WHITE)

    intro_lines = [
        "LLM 기반 AI 자동화 솔루션 전문 스타트업 킷에이아이(KittAI) 대표.",
        "Claude, ChatGPT, Gemini 등 최신 AI를 활용한 실무 자동화 시스템을",
        "직접 설계·개발하고, 기업·기관·개인에게 실전형 AI 교육을 제공합니다.",
        "이론보다 '내일부터 바로 쓸 수 있는 AI'를 가르칩니다.",
    ]
    iy = H - 192
    for line in intro_lines:
        txt(c, line, RX+8, iy, F, 10, C_NAVY)
        iy -= 16

    # 주요 강의 이력
    iy -= 8
    rect(c, RX, iy, RW, 22, fill=C_NAVY, radius=4)
    txt(c, "주요 강의 이력", RX+10, iy+13, FB, 11, C_WHITE)
    iy -= 8

    lectures = [
        ("카이앤컴퍼니", "AI 마케팅 자동화 실무 과정 (광고주 대상)", "2024~2025"),
        ("자사 워크숍", "ChatGPT 업무 활용 실전 특강", "2024"),
        ("자사 워크숍", "AI 콘텐츠 자동화 파이프라인 구축", "2025"),
        ("스타트업 컨설팅", "AI 에이전트 기반 업무 자동화 설계", "2025~2026"),
    ]
    for org, title, year in lectures:
        iy -= 20
        rect(c, RX+4, iy-2, RW-8, 18, fill=HexColor("#f0f0ff"), radius=3)
        txt(c, f"[{year}]  {org}", RX+10, iy+5, FB, 9, C_ACCENT)
        txt(c, title, RX+10, iy-7, F, 10, C_NAVY)

    # 주요 개발 솔루션 (기술 역량)
    iy -= 28
    rect(c, RX, iy, RW, 22, fill=C_NAVY, radius=4)
    txt(c, "개발 및 운영 중인 AI 솔루션", RX+10, iy+13, FB, 11, C_WHITE)
    iy -= 8

    solutions = [
        ("셀킷(SellKitt)", "도매·유통 AI 자동화 플랫폼 — 상품 등록·발주·리포트 자동화"),
        ("뉴스레터 에이전트", "7단계 파이프라인 — 뉴스 수집·요약·발행 완전 자동화"),
        ("광고 리포트 자동화", "Meta·네이버 데이터 자동 수집·분석·보고서 생성"),
        ("정책자금 문서 자동화", "LLM 기반 사업계획서·신청서 자동 작성 시스템"),
    ]
    for name, desc in solutions:
        iy -= 20
        rect(c, RX+4, iy-4, RW-8, 20, fill=HexColor("#e8f5e9"), radius=3)
        txt(c, f"◆ {name}", RX+10, iy+5, FB, 9, C_GREEN)
        txt(c, desc, RX+12, iy-7, F, 9, C_NAVY)

    # 보유 역량 요약 바
    iy -= 28
    rect(c, RX, iy, RW, 22, fill=C_NAVY, radius=4)
    txt(c, "보유 역량", RX+10, iy+13, FB, 11, C_WHITE)
    iy -= 8

    skills = [
        ("LLM 프롬프트 엔지니어링", 92),
        ("AI 에이전트 설계 (Claude Code / Cursor)", 90),
        ("마케팅 자동화", 95),
        ("Python / Node.js AI 개발", 80),
    ]
    for skill_name, pct in skills:
        iy -= 22
        txt(c, skill_name, RX+8, iy+4, F, 9, C_NAVY)
        # 바 배경
        rect(c, RX+8, iy-6, RW-16, 8, fill=C_LGRAY, radius=4)
        # 바 채우기
        bar_w = int((RW-16) * pct / 100)
        rect(c, RX+8, iy-6, bar_w, 8, fill=C_ACCENT, radius=4)
        txt(c, f"{pct}%", RX+8+bar_w+4, iy-4, F, 8, C_GRAY)

    # ── 하단 푸터 ──────────────────────────────────────────
    rect(c, 0, 0, W, 28, fill=C_NAVY)
    txt(c, "주식회사 킷에이아이  |  kitt.ai.ceo@gmail.com  |  AI 자동화 · 교육 전문", W/2, 9, F, 9, C_ACCENT2, align="center")

    c.save()
    print(f"✅ 저장 완료: {OUT}")

if __name__ == "__main__":
    make_profile()
