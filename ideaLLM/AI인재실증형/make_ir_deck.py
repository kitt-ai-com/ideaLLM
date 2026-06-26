#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
킷에이아이 IR Deck PDF 생성 (reportlab 직접 드로잉)
슬라이드 크기: 1280 x 720 pt (16:9)
"""

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os, sys

OUT = "/Users/jasonmac/Claude/ideaLLM/ideaLLM/AI인재실증형/IR_Deck_킷에이아이_v2.pdf"
W, H = 1280, 720

# ── 색상 ──────────────────────────────────────────────
C_BG_DARK  = HexColor("#1a1a2e")
C_BG_GRAD1 = HexColor("#0f0c29")
C_BG_GRAD2 = HexColor("#302b63")
C_ACCENT   = HexColor("#7c83ff")
C_ACCENT2  = HexColor("#a8acff")
C_WHITE    = white
C_GRAY     = HexColor("#888888")
C_LIGHT    = HexColor("#f8f8fc")
C_TEXT     = HexColor("#1a1a2e")
C_RED      = HexColor("#ff6b6b")
C_ORANGE   = HexColor("#ffa94d")
C_GREEN    = HexColor("#51cf66")
C_CARD1    = HexColor("#f0f0ff")
C_CARD2    = HexColor("#e8f5e9")
C_CARD3    = HexColor("#fff3e0")

# ── 폰트 등록 ──────────────────────────────────────────
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
    # 폴백: Helvetica
    return "Helvetica", "Helvetica-Bold"

F, FB = reg_font()

# ── 유틸 ──────────────────────────────────────────────
def rect(c, x, y, w, h, fill=None, stroke=None, r=0):
    """y는 슬라이드 상단 기준 (내부에서 reportlab 좌표로 변환)"""
    ry = H - y - h
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    else:
        c.setStrokeColor(HexColor("#00000000"))
    if r > 0:
        c.roundRect(x, ry, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)
    else:
        c.rect(x, ry, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)

def text(c, x, y, s, size=14, color=white, font=None, align="left"):
    f = font or F
    c.setFont(f, size)
    c.setFillColor(color)
    ry = H - y
    if align == "center":
        c.drawCentredString(x, ry, str(s))
    elif align == "right":
        c.drawRightString(x, ry, str(s))
    else:
        c.drawString(x, ry, str(s))

def badge(c, x, y, w, h, label, bg=None, fg=white, size=11, r=6):
    bg = bg or C_ACCENT
    rect(c, x, y, w, h, fill=bg, r=r)
    text(c, x + w/2, y + h/2 + size*0.35, label, size=size, color=fg, font=FB, align="center")

def tag_box(c, x, y, w, h, label, border_color=None, bg=C_LIGHT, size=13, r=10):
    bc = border_color or C_ACCENT
    rect(c, x, y, w, h, fill=bg, r=r)
    rect(c, x, y, w, 4, fill=bc, r=0)
    # top border only - redraw top strip
    c.setFillColor(bc)
    ry_top = H - y - 4
    c.rect(x, ry_top, w, 4, fill=1, stroke=0)

def divider(c, y, color=None, alpha=0.15):
    c.setStrokeColor(color or C_GRAY)
    c.setLineWidth(0.5)
    c.line(56, H - y, W - 56, H - y)

def chip(c, x, y, w, h, t, bg, fg=white, size=10, r=5):
    rect(c, x, y, w, h, fill=bg, r=r)
    text(c, x + w/2, y + h/2 + size*0.38, t, size=size, color=fg, font=FB, align="center")

def slide_header(c, num, total=10, dark=False):
    tc = C_GRAY if not dark else HexColor("#666699")
    text(c, 56, 30, "kitt AI", size=14, color=C_ACCENT if dark else C_TEXT, font=FB)
    text(c, W - 56, 30, f"{num:02d} / {total}", size=12, color=tc, align="right")

def metric_box(c, x, y, w, h, val, unit, label, bg=C_LIGHT):
    rect(c, x, y, w, h, fill=bg, r=12)
    text(c, x + w/2, y + 22, val, size=36, color=C_ACCENT, font=FB, align="center")
    if unit:
        # unit is drawn inline after val — approximate
        pass
    text(c, x + w/2, y + 60, unit, size=14, color=C_ACCENT, font=FB, align="center")
    for i, line in enumerate(label.split("\n")):
        text(c, x + w/2, y + 82 + i*16, line, size=12, color=C_GRAY, align="center")

def comp_row(c, y, cols, h=36, dark=True, highlight=False):
    x_starts = [56, 356, 620, 860, 1080]
    widths    = [290, 254, 230, 210, 144]
    bg = HexColor("#2a2a4e") if highlight else (HexColor("#1e1e38") if dark else C_LIGHT)
    rect(c, 56, y, W - 112, h, fill=bg, r=0)
    for i, (col, xs, cw) in enumerate(zip(cols, x_starts, widths)):
        fc = C_ACCENT if highlight else (C_WHITE if dark else C_TEXT)
        if col in ("✓", "O"):
            fc = C_GREEN
        elif col in ("✗", "X"):
            fc = C_RED
        elif col in ("△",):
            fc = C_ORANGE
        align = "left" if i == 0 else "center"
        cx = xs + 10 if align == "left" else xs + cw/2
        text(c, cx, y + h/2 + 5, col, size=12, color=fc,
             font=FB if (highlight or col in ("✓","✗","△","O","X")) else F,
             align=align)


# ══════════════════════════════════════════════════════
#  슬라이드 함수들
# ══════════════════════════════════════════════════════

def slide1(c):
    """표지"""
    # 배경 그라디언트 흉내 (직사각형 여러 개)
    steps = 20
    for i in range(steps):
        t = i / steps
        r1,g1,b1 = 0x0f,0x0c,0x29
        r2,g2,b2 = 0x30,0x2b,0x63
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        color = HexColor(f"#{r:02x}{g:02x}{b:02x}")
        bw = W // steps + 2
        rect(c, i*bw, 0, bw+2, H, fill=color)

    # 악센트 사각형
    rect(c, 0, 0, 8, H, fill=C_ACCENT)

    # 태그
    chip(c, 100, 160, 260, 28, "AI Agent Platform · B2B SaaS", HexColor("#ffffff22"), size=12)

    # 메인 타이틀
    text(c, 100, 210, "중소기업의 AI 전환을", size=58, color=C_WHITE, font=FB)
    text(c, 100, 278, "에이전트로 완성한다", size=58, color=C_ACCENT, font=FB)

    # 서브타이틀
    text(c, 100, 340, "LLM 기반 업종 특화 AI 에이전트로 반복 업무를 자동화하는 kitt AX Agent", size=18, color=HexColor("#aaaacc"))

    # 구분선
    divider(c, 400, color=HexColor("#444466"))

    # 메타
    text(c, 100, 430, "주식회사 킷에이아이  ·  대표 유승범", size=14, color=HexColor("#9999bb"))
    text(c, 100, 458, "서울특별시 서초구  ·  설립 2026.04  ·  AI 에이전트 B2B SaaS", size=13, color=HexColor("#7777aa"))
    text(c, 100, 484, "kitt.ai.ceo@gmail.com", size=13, color=C_ACCENT)


def slide2(c):
    """문제"""
    rect(c, 0, 0, W, H, fill=white)
    slide_header(c, 2, dark=False)

    text(c, 56, 68, "PROBLEM", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "중소기업은 AI를 쓰고 싶어도 쓸 수 없다", size=30, color=C_TEXT, font=FB)

    # 카드 3개
    cw, cy, ch = 368, 130, 200
    gaps = [56, 56+368+16, 56+368+16+368+16]
    borders = [C_RED, C_ORANGE, C_ACCENT]
    titles = ["시간 낭비", "전문인력 부재", "범용 솔루션 한계"]
    nums   = ["01", "02", "03"]
    descs  = [
        "담당자 1명이 주문·문서·정산\n반복 업무에 하루 2~4시간 소모.\n경영 집중 불가.",
        "AI 도입하려면 전문 인력이\n필요하지만 채용 여력과\n검증 능력 모두 부족.",
        "시중 챗봇·RPA는 업종\n특화가 안 돼 현장 적용율이\n낮고 유지비만 발생.",
    ]
    for i, gx in enumerate(gaps):
        rect(c, gx, cy, cw, ch, fill=C_LIGHT, r=12)
        rect(c, gx, cy, cw, 4, fill=borders[i], r=0)
        c.setFillColor(borders[i])
        c.rect(gx, H - cy - 4, cw, 4, fill=1, stroke=0)
        text(c, gx+20, cy+24, nums[i], size=32, color=borders[i], font=FB)
        text(c, gx+20, cy+68, titles[i], size=17, color=C_TEXT, font=FB)
        for j, line in enumerate(descs[i].split("\n")):
            text(c, gx+20, cy+92+j*18, line, size=12, color=HexColor("#555555"))

    # 통계 바
    rect(c, 56, 350, W-112, 76, fill=C_BG_DARK, r=12)
    stats = [("770만", "국내 중소기업 수"), ("<5%", "AI 도입률"),
             ("4,200억", "AI 자동화 시장(2025)"), ("2~4시간", "반복업무 일일 소모")]
    sw = (W-112) // 4
    for i, (val, lbl) in enumerate(stats):
        sx = 56 + i*sw + sw//2
        text(c, sx, 375, val, size=24, color=C_ACCENT, font=FB, align="center")
        text(c, sx, 402, lbl, size=11, color=HexColor("#aaaacc"), align="center")

    # 출처
    text(c, 56, 458, "※ 중소기업벤처부 2025 AI 활용 실태조사 기준", size=10, color=C_GRAY)


def slide3(c):
    """솔루션"""
    rect(c, 0, 0, W, H, fill=C_BG_DARK)
    slide_header(c, 3, dark=True)

    text(c, 56, 68, "SOLUTION", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "kitt AX Agent — 업종 특화 AI 에이전트 플랫폼", size=28, color=C_WHITE, font=FB)

    # 플로우 화살표
    flow_items = [("📥", "데이터 입력", "주문·문서·키워드"),
                  ("🤖", "LLM 처리", "Claude / Gemini"),
                  ("⚡", "AI 에이전트", "업종별 자동화"),
                  ("📊", "정형 산출물", "보고서·발주·CS")]
    fw = 240; fgap = 20; fx0 = 56
    total_flow = len(flow_items)*fw + (len(flow_items)-1)*(fgap+30)
    fx0 = (W - total_flow) // 2

    for i, (icon, title, sub) in enumerate(flow_items):
        bx = fx0 + i*(fw+fgap+30)
        rect(c, bx, 128, fw, 80, fill=HexColor("#2a2a50"), r=10)
        c.setFillColor(HexColor("#7c83ff44"))
        c.setStrokeColor(C_ACCENT)
        c.setLineWidth(1)
        ry = H - 128 - 80
        c.roundRect(bx, ry, fw, 80, 10, fill=1, stroke=1)
        text(c, bx+fw//2, 148, icon, size=22, align="center")
        text(c, bx+fw//2, 174, title, size=14, color=C_WHITE, font=FB, align="center")
        text(c, bx+fw//2, 192, sub, size=11, color=HexColor("#aaaacc"), align="center")
        if i < len(flow_items)-1:
            ax = bx + fw + 6
            text(c, ax+9, 166, "→", size=20, color=C_ACCENT, font=FB, align="center")

    # 에이전트 카드 3개
    aw = 374; ay = 232; ah = 190
    agent_data = [
        ("LIVE", "ai-agent", "메타 광고 리포트 자동화.\nRSS→LLM→리포트 자동 생성·발송.", "월 60시간 절감 · 6개사 운영 중"),
        ("LIVE", "newsletter-agent", "7단계 자동 파이프라인.\n주제설정→크롤링→LLM요약→발송.", "주 2회 자동 발행 · 무인 운영"),
        ("LIVE", "Sellkitt B2B 유통", "주문 처리 자동화.\nAI 엑셀 매핑·발주 자동화 납품 완료.", "주문처리 90% 단축 · 계약 완료"),
    ]
    for i, (badge_t, title, desc, result) in enumerate(agent_data):
        ax2 = 56 + i*(aw+16)
        rect(c, ax2, ay, aw, ah, fill=HexColor("#ffffff0d"), r=10)
        c.setStrokeColor(HexColor("#ffffff1a"))
        c.setLineWidth(1)
        ry = H - ay - ah
        c.roundRect(ax2, ry, aw, ah, 10, fill=0, stroke=1)
        chip(c, ax2+16, ay+16, 48, 20, badge_t, C_ACCENT, size=10)
        text(c, ax2+16, ay+52, title, size=16, color=C_WHITE, font=FB)
        for j, line in enumerate(desc.split("\n")):
            text(c, ax2+16, ay+76+j*18, line, size=12, color=HexColor("#aaaacc"))
        text(c, ax2+16, ay+152, result, size=12, color=C_ACCENT, font=FB)

    text(c, 56, 448, "→ AI 인재 채용 시 이 검증된 파이프라인을 업종별로 빠르게 확장", size=13, color=HexColor("#aaaaee"))


def slide4(c):
    """실증 성과"""
    rect(c, 0, 0, W, H, fill=white)
    slide_header(c, 4, dark=False)

    text(c, 56, 68, "TRACTION", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "이미 납품·운영 중 — 가설이 아닌 실증", size=30, color=C_TEXT, font=FB)

    # 메트릭 4개
    mw = 278; my = 120; mh = 130
    metrics = [("6개사", "광고 에이전트\n실운영 고객사"),
               ("60h+", "고객사당\n월 절감 시간"),
               ("3건", "B2B 납품\n전주기 완료"),
               ("2년+", "LLM 실운영\n경험")]
    for i, (val, lbl) in enumerate(metrics):
        mx2 = 56 + i*(mw+16)
        rect(c, mx2, my, mw, mh, fill=C_LIGHT, r=12)
        text(c, mx2+mw//2, my+48, val, size=34, color=C_ACCENT, font=FB, align="center")
        for j, line in enumerate(lbl.split("\n")):
            text(c, mx2+mw//2, my+88+j*18, line, size=12, color=C_GRAY, align="center")

    # 타임라인
    text(c, 56, 278, "실증 이력", size=14, color=C_TEXT, font=FB)
    divider(c, 296)

    tl_data = [
        ("2024", "ai-agent 구축", "메타광고 자동화 파이프라인 구축.\n6개사 계약·운영 시작."),
        ("2025", "Sellkitt 납품", "B2B 유통 자동화 납품 완료.\n주문처리 90% 단축 실증."),
        ("2025", "newsletter-agent", "7단계 자동 파이프라인 구축.\n주 2회 무인 발행 운영 중."),
        ("2026.04", "킷에이아이 법인 설립", "AI 에이전트 전문 법인화.\n정부 AI 인재 사업 신청."),
    ]
    tw = 278
    for i, (date, title, desc) in enumerate(tl_data):
        tx = 56 + i*(tw+16)
        rect(c, tx, 308, 4, 100, fill=C_ACCENT, r=2)
        text(c, tx+14, 316, date, size=11, color=C_ACCENT, font=FB)
        text(c, tx+14, 336, title, size=14, color=C_TEXT, font=FB)
        for j, line in enumerate(desc.split("\n")):
            text(c, tx+14, 358+j*18, line, size=12, color=C_GRAY)

    # 하단 요약
    rect(c, 56, 432, W-112, 50, fill=C_BG_DARK, r=10)
    text(c, W//2, 451, "→  CEO 10년+ 운영 경험 + CTO LLM 2년+ 실운영 = 즉시 실행 가능한 팀", size=14, color=C_WHITE, align="center")
    text(c, W//2, 471, "아이디어 단계가 아닌 이미 고객사에 납품·운영 중인 검증된 솔루션", size=12, color=HexColor("#aaaacc"), align="center")


def slide5(c):
    """시장"""
    rect(c, 0, 0, W, H, fill=C_LIGHT)
    slide_header(c, 5, dark=False)

    text(c, 56, 68, "MARKET", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "TAM 4.2조 · 초기 타깃 중소 광고주·유통업체", size=30, color=C_TEXT, font=FB)

    # TAM 박스
    rect(c, 56, 120, 580, 310, fill=white, r=12)
    text(c, 76, 144, "MARKET SIZE (2025 기준)", size=11, color=C_GRAY, font=FB)

    bars = [("TAM", "4조 2,000억  국내 AI 자동화 전체", C_BG_DARK, 480),
            ("SAM", "8,000억  중소기업 AI 도입", C_ACCENT, 300),
            ("SOM", "200억  3년 목표", C_ACCENT2, 130)]
    for i, (lbl, desc, color, bw) in enumerate(bars):
        by = 162 + i*72
        text(c, 76, by+16, lbl, size=12, color=C_TEXT, font=FB)
        rect(c, 140, by, bw, 36, fill=color, r=8)
        text(c, 152, by+22, desc, size=12, color=white, font=FB)

    # 타깃 박스
    rect(c, 660, 120, 564, 310, fill=white, r=12)
    text(c, 680, 144, "초기 타깃 세그먼트", size=11, color=C_GRAY, font=FB)

    targets = [
        ("광고주 (SMB)", "월 마케팅비 500만원+ · Meta 광고 운영", "~30만개"),
        ("B2B 유통·도매업체", "주문·발주 반복 업무 과중", "~15만개"),
        ("병원·학원 (서비스업)", "CS·문서 자동화 수요", "~20만개"),
    ]
    for i, (name, desc, size2) in enumerate(targets):
        ty = 164 + i*74
        divider(c, ty, color=HexColor("#eeeeee"))
        text(c, 680, ty+22, name, size=14, color=C_TEXT, font=FB)
        text(c, 680, ty+42, desc, size=12, color=C_GRAY)
        text(c, W-76, ty+22, size2, size=14, color=C_ACCENT, font=FB, align="right")

    # 하단 메시지
    rect(c, 56, 452, W-112, 50, fill=C_BG_DARK, r=10)
    text(c, W//2, 470, "300만 중소기업 중 AI 도입률 5% 미만 → 선점 기회", size=14, color=C_WHITE, font=FB, align="center")
    text(c, W//2, 490, "초기 6개 광고주 고객사 기반으로 확장 시작", size=12, color=HexColor("#aaaacc"), align="center")


def slide6(c):
    """경쟁우위"""
    rect(c, 0, 0, W, H, fill=C_BG_DARK)
    slide_header(c, 6, dark=True)

    text(c, 56, 68, "COMPETITIVE ADVANTAGE", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "경쟁사 대비 핵심 차별점", size=28, color=C_WHITE, font=FB)

    # 헤더 행
    rect(c, 56, 120, W-112, 36, fill=HexColor("#2a2a5a"), r=0)
    headers = ["구분", "kitt AX Agent", "발주모아(위드소프트)", "사방넷(다우기술)", "범용 챗봇"]
    x_starts = [66, 366, 626, 866, 1086]
    for i, (h, xs) in enumerate(zip(headers, x_starts)):
        text(c, xs, 142, h, size=12, color=C_ACCENT, font=FB)

    rows = [
        (True,  ["LLM 기반 자율 에이전트",  "✓ Claude·Gemini", "✗ 규칙기반 ML",  "✗ FAQ 챗봇",  "△ 범용"]),
        (False, ["업종 특화 커스터마이징",  "✓ 물류·광고·학원", "△ 유통 한정",   "△ 커머스 한정","✗"]),
        (True,  ["실운영 납품 실적",        "✓ 3건 완료",      "✓ 463개사",     "✓ 7,000개사", "✗"]),
        (False, ["초기 도입 비용",          "✓ 낮음(SaaS)",    "△ 중간",        "✗ 높음",       "✓ 낮음"]),
        (True,  ["자율처리(사람 개입 최소)","✓ 풀 자동화",     "✗",             "✗",            "✗"]),
    ]
    for i, (alt, cols) in enumerate(rows):
        ry2 = 156 + i*46
        bg = HexColor("#1e1e3a") if alt else HexColor("#232340")
        rect(c, 56, ry2, W-112, 44, fill=bg)
        for j, (col, xs) in enumerate(zip(cols, x_starts)):
            fc = C_WHITE
            if "✓" in col: fc = C_GREEN
            elif "✗" in col: fc = C_RED
            elif "△" in col: fc = C_ORANGE
            text(c, xs, ry2+26, col, size=12, color=fc,
                 font=FB if j==0 else F)

    # kitt 행 강조선
    text(c, 56, 396, "※  발주모아: 위드소프트(463개사, 규칙기반 ML)  /  사방넷: 다우기술(7,000개사, FAQ챗봇)", size=10, color=C_GRAY)


def slide7(c):
    """비즈니스 모델"""
    rect(c, 0, 0, W, H, fill=white)
    slide_header(c, 7, dark=False)

    text(c, 56, 68, "BUSINESS MODEL", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "컨설팅 → SaaS 구독 → AI바우처 연계 3단계 수익화", size=28, color=C_TEXT, font=FB)

    # 3단계 카드
    pw = 374; py = 122; ph = 180
    phases = [
        ("PHASE 1 · NOW", "AX 컨설팅·구축", "1,000만원+", "건당 프로젝트",
         "업종별 AI 에이전트 설계·구축·납품.\n즉각 매출 발생.", C_CARD1),
        ("PHASE 2 · '26 Q4", "SaaS 구독", "30~100만원", "월 구독 / 사",
         "멀티테넌트 플랫폼.\n운영 대시보드 포함. MRR 축적.", C_CARD2),
        ("PHASE 3 · '27", "AI바우처 연계", "2억원", "건당 정부 과제",
         "NIPA 공급기업 POOL 등록.\n대형 B2B 계약 연결.", C_CARD3),
    ]
    for i, (phase_lbl, title, price, price_sub, desc, bg) in enumerate(phases):
        px2 = 56 + i*(pw+16)
        rect(c, px2, py, pw, ph, fill=bg, r=12)
        text(c, px2+pw//2, py+22, phase_lbl, size=10, color=C_GRAY, font=FB, align="center")
        text(c, px2+pw//2, py+46, title, size=16, color=C_TEXT, font=FB, align="center")
        text(c, px2+pw//2, py+80, price, size=26, color=C_ACCENT, font=FB, align="center")
        text(c, px2+pw//2, py+100, price_sub, size=11, color=C_GRAY, align="center")
        for j, line in enumerate(desc.split("\n")):
            text(c, px2+pw//2, py+124+j*18, line, size=12, color=HexColor("#555555"), align="center")

    # 로드맵
    text(c, 56, 326, "실행 로드맵", size=14, color=C_TEXT, font=FB)
    rw = 278
    roadmap = [
        ("'26 Q3", "AI 인재 채용", "정규직 2명 온보딩.\n에이전트 고도화 착수."),
        ("'26 Q4", "SaaS 베타 출시", "업종별 에이전트 2종.\n수요기업 실증 1건."),
        ("'27 Q1", "AI바우처 공급 등록", "NIPA POOL 등록.\n파트너십 확대."),
        ("'27 Q2+", "MRR 1억 목표", "구독 고객 100사+.\n시리즈A 준비."),
    ]
    for i, (q, title, desc) in enumerate(roadmap):
        rx2 = 56 + i*(rw+16)
        rect(c, rx2, 344, rw, 106, fill=C_LIGHT, r=10)
        text(c, rx2+16, 362, q, size=11, color=C_ACCENT, font=FB)
        text(c, rx2+16, 380, title, size=14, color=C_TEXT, font=FB)
        for j, line in enumerate(desc.split("\n")):
            text(c, rx2+16, 402+j*18, line, size=12, color=C_GRAY)


def slide8(c):
    """팀"""
    rect(c, 0, 0, W, H, fill=C_LIGHT)
    slide_header(c, 8, dark=False)

    text(c, 56, 68, "TEAM", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "납품 완료한 2인 팀 — 경험·기술 동시 보유", size=30, color=C_TEXT, font=FB)

    # 팀 카드 2개
    tw2 = 574
    team = [
        ("CEO · 대표이사", "유승범", "세종대 대학원 컴퓨터공학 석사",
         ["카이앤컴퍼니 대표 10년+ · Meta 광고 100개사+ 운영",
          "Sellkitt B2B 유통 플랫폼 직접 설계·납품·운영",
          "ai-agent 구축 · 광고 클라이언트 6개사 월 60h 절감",
          "AI 전략 컨설팅·소프트웨어 구축·리터러시 교육 총괄"]),
        ("CTO · 기술이사", "김상훈", "경민대 컴퓨터소프트웨어과 겸임교수 · 현장실습 강사",
         ["Claude·Gemini LLM 실운영 2년+",
          "newsletter-agent 7단계 파이프라인 설계",
          "셀킷 AI 아키텍처 설계",
          "기존 고객사(유통·병원·학원) 실증 완료"]),
    ]
    for i, (role, name, edu, bullets) in enumerate(team):
        tx2 = 56 + i*(tw2+16)
        rect(c, tx2, 118, tw2, 240, fill=white, r=12)
        chip(c, tx2+16, 132, 120, 22, role, C_ACCENT, size=10)
        text(c, tx2+16, 172, name, size=22, color=C_TEXT, font=FB)
        text(c, tx2+16, 194, edu, size=12, color=C_GRAY)
        for j, b in enumerate(bullets):
            text(c, tx2+28, 218+j*22, f"· {b}", size=12, color=HexColor("#444444"))

    # 채용 박스
    rect(c, 56, 374, W-112, 60, fill=C_BG_DARK, r=12)
    text(c, 96, 394, "👥", size=22)
    text(c, 136, 394, "AI 인재 2명 정규직 채용 예정 ('26.10월)", size=14, color=C_ACCENT, font=FB)
    text(c, 136, 416, "AI 양성과정 수료생 채용 → LLM 커스터마이징·AX 솔루션 개발 역량 강화. 채용 후 60일 내 4대보험·근로계약 증빙 완료.", size=12, color=HexColor("#aaaacc"))


def slide9(c):
    """AI 활용"""
    rect(c, 0, 0, W, H, fill=C_BG_DARK)
    slide_header(c, 9, dark=True)

    text(c, 56, 68, "AI AS A TEAMMATE", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "AI를 도구가 아닌 팀원으로 운영한다", size=28, color=C_WHITE, font=FB)

    # AI 카드 3개
    aw = 374; ay = 122; ah = 160
    ai_cards = [
        ("CLAUDE (ANTHROPIC)", "콘텐츠·문서 생성",
         "뉴스레터 자동생성, 사업계획서 초안,\n보고서 작성. 주 2회 무인 발행 중."),
        ("GEMINI (GOOGLE)", "데이터 분석·처리",
         "광고 성과 데이터 자동 분석,\n인사이트 추출, 대시보드 수치 생성."),
        ("MULTI-AGENT", "파이프라인 자동화",
         "7단계 워크플로우를 AI가 순차 실행.\n사람 개입 없이 전 과정 처리."),
    ]
    for i, (model, title, desc) in enumerate(ai_cards):
        ax2 = 56 + i*(aw+16)
        c.setFillColor(HexColor("#ffffff0d"))
        c.setStrokeColor(HexColor("#7c83ff55"))
        c.setLineWidth(1)
        ry = H - ay - ah
        c.roundRect(ax2, ry, aw, ah, 10, fill=1, stroke=1)
        text(c, ax2+16, ay+20, model, size=10, color=C_ACCENT, font=FB)
        text(c, ax2+16, ay+44, title, size=15, color=C_WHITE, font=FB)
        for j, line in enumerate(desc.split("\n")):
            text(c, ax2+16, ay+68+j*20, line, size=12, color=HexColor("#aaaacc"))

    # 인용구
    rect(c, 56, 304, W-112, 90, fill=HexColor("#7c83ff1a"), r=0)
    c.setFillColor(C_ACCENT)
    c.rect(56, H-304-90, 4, 90, fill=1, stroke=0)
    text(c, 76, 326, '"우리는 2인 팀이지만 AI 에이전트 덕분에 10인 팀처럼 일한다.', size=14, color=HexColor("#ddddee"), font=F)
    text(c, 76, 348, '사람은 전략과 판단만 하고, 반복 실행은 모두 AI가 담당한다.', size=14, color=HexColor("#ddddee"), font=F)
    text(c, 76, 370, '이 운영 방식 자체가 우리 제품의 프로토타입이다."', size=14, color=HexColor("#ddddee"), font=F)
    text(c, W-76, 382, "— 유승범, 킷에이아이 대표", size=12, color=C_ACCENT, align="right")

    # 수치 요약
    rect(c, 56, 416, W-112, 60, fill=HexColor("#2a2a50"), r=10)
    summary = [("3종", "실운영 AI 에이전트"), ("7단계", "자동 파이프라인"), ("2년+", "LLM 운영 경험"), ("0명", "추가 인력 필요")]
    sw = (W-112)//4
    for i, (val, lbl) in enumerate(summary):
        sx = 56 + i*sw + sw//2
        text(c, sx, 436, val, size=20, color=C_ACCENT, font=FB, align="center")
        text(c, sx, 458, lbl, size=11, color=HexColor("#aaaacc"), align="center")


def slide10(c):
    """투자 요청"""
    steps = 20
    for i in range(steps):
        t = i / steps
        r1,g1,b1 = 0x0f,0x0c,0x29
        r2,g2,b2 = 0x30,0x2b,0x63
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        color = HexColor(f"#{r:02x}{g:02x}{b:02x}")
        bw = W // steps + 2
        rect(c, i*bw, 0, bw+2, H, fill=color)
    rect(c, 0, 0, 8, H, fill=C_ACCENT)

    slide_header(c, 10, dark=True)

    text(c, 56, 68, "THE ASK", size=11, color=C_ACCENT, font=FB)
    text(c, 56, 92, "SparkClaw와 함께 중소기업 AX 시장을 선점한다", size=26, color=C_WHITE, font=FB)

    # 왼쪽 — 투자 요청
    rect(c, 56, 122, 564, 300, fill=HexColor("#ffffff0d"), r=12)
    c.setStrokeColor(HexColor("#7c83ff55"))
    c.setLineWidth(1)
    ry = H - 122 - 300
    c.roundRect(56, ry, 564, 300, 12, fill=0, stroke=1)
    text(c, 76, 144, "FUNDING REQUEST", size=11, color=C_ACCENT, font=FB)
    text(c, 76, 178, "5,000만원", size=42, color=C_WHITE, font=FB)
    text(c, 76, 204, "~ 2억원 투자 유치 목표", size=13, color=HexColor("#aaaacc"))

    use_items = [
        ("AI 인재 인건비 (2명 · 7개월)", "6,000만원"),
        ("에이전트 고도화 · 외주",        "3,500만원"),
        ("클라우드 · LLM API",           "2,500만원"),
        ("지재권 · 마케팅",              "2,000만원"),
    ]
    divider(c, 220, color=HexColor("#444466"))
    for i, (name, val) in enumerate(use_items):
        uy = 234 + i*38
        text(c, 76, uy, name, size=12, color=HexColor("#bbbbdd"))
        text(c, 604, uy, val, size=12, color=C_ACCENT, font=FB, align="right")
        if i < len(use_items)-1:
            c.setStrokeColor(HexColor("#333355"))
            c.setLineWidth(0.5)
            c.line(76, H-uy-16, 604, H-uy-16)

    # 오른쪽 — KPI
    rect(c, 644, 122, 580, 300, fill=HexColor("#ffffff0d"), r=12)
    c.setStrokeColor(HexColor("#7c83ff55"))
    c.setLineWidth(1)
    ry2 = H - 122 - 300
    c.roundRect(644, ry2, 580, 300, 12, fill=0, stroke=1)
    text(c, 664, 144, "12개월 목표 KPI", size=11, color=C_ACCENT, font=FB)

    kpis = [("20개사", "SaaS 구독 고객"), ("MRR 2,000만", "월 반복 매출"),
            ("2종", "업종별 에이전트"), ("AI바우처", "NIPA 공급기업 등록")]
    kw = 258
    for i, (val, lbl) in enumerate(kpis):
        kx = 664 + (i%2)*(kw+16)
        ky = 164 + (i//2)*110
        rect(c, kx, ky, kw, 96, fill=HexColor("#7c83ff18"), r=10)
        text(c, kx+kw//2, ky+38, val, size=20, color=C_ACCENT, font=FB, align="center")
        text(c, kx+kw//2, ky+62, lbl, size=11, color=HexColor("#aaaacc"), align="center")

    # 연락처
    rect(c, 56, 444, W-112, 48, fill=HexColor("#ffffff0d"), r=10)
    text(c, W//2, 462, "유승범  ·  주식회사 킷에이아이  ·  kitt.ai.ceo@gmail.com", size=14, color=C_WHITE, font=FB, align="center")
    text(c, W//2, 482, "sparkclaw.co.kr 지원 중  ·  마감 2026.06.28", size=12, color=C_ACCENT, align="center")


# ══════════════════════════════════════════════════════
#  메인
# ══════════════════════════════════════════════════════
def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))

    slides = [slide1, slide2, slide3, slide4, slide5,
              slide6, slide7, slide8, slide9, slide10]

    for fn in slides:
        fn(c)
        c.showPage()

    c.save()
    print(f"✅ 저장 완료: {OUT}")

if __name__ == "__main__":
    main()
