#!/usr/bin/env python3
"""Draw entry.png for news-image-20261124 (vocaine v3):
WORLD ATLAS - ONE DAY, FIVE REGIONS. All shapes drawn with PIL at runtime;
no downloaded images. Output: 1024x1024 PNG, <= 1 MiB.
Only verified 24 Nov 2026 events from the task brief are used.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (11, 30, 51)
NAVY2 = (16, 44, 74)
PANEL = (19, 54, 88)
PANEL_EDGE = (64, 120, 160)
GOLD = (212, 175, 55)
GOLD_LT = (240, 205, 110)
INK = (235, 240, 245)
MUTED = (168, 190, 205)
LAND = (46, 110, 96)
LAND_EDGE = (120, 190, 160)
RED = (226, 84, 66)
TEAL = (94, 200, 190)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


# --- equirectangular lon/lat -> map pixels (map box x 24..1000, y 118..396) ---
MX0, MY0, MX1, MY1 = 24, 118, 1000, 360


def ll(lon, lat):
    x = MX0 + (lon + 180.0) / 360.0 * (MX1 - MX0)
    y = MY0 + (82.0 - lat) / 164.0 * (MY1 - MY0)
    return (x, y)


# Simplified continent silhouettes (lon, lat) - deliberately rough atlas shapes.
N_AMERICA = [(-168, 66), (-150, 70), (-130, 71), (-120, 70), (-105, 68), (-95, 69),
             (-85, 66), (-80, 62), (-76, 58), (-70, 58), (-65, 60), (-60, 55),
             (-55, 47), (-60, 45), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
             (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-91, 19), (-95, 16),
             (-92, 14), (-86, 12), (-83, 9), (-80, 8), (-77, 7), (-79, 9),
             (-83, 15), (-90, 14), (-97, 16), (-105, 20), (-110, 23), (-114, 28),
             (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55), (-140, 60),
             (-155, 58), (-165, 60), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
             (-25, 74), (-32, 76), (-45, 76), (-55, 74), (-58, 70), (-58, 64)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
             (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50), (-68, -55),
             (-65, -55), (-62, -49), (-58, -42), (-52, -33), (-48, -28), (-41, -23),
             (-38, -15), (-35, -8), (-44, -3), (-50, 0), (-55, 4), (-60, 8),
             (-66, 9), (-72, 11), (-77, 8), (-79, 9)]
AFRICA = [(-6, 35), (10, 37), (20, 32), (30, 31), (34, 28), (37, 22), (39, 18),
          (43, 12), (48, 11), (51, 10), (46, 5), (42, -2), (40, -8), (36, -16),
          (33, -26), (28, -33), (20, -35), (17, -29), (14, -22), (12, -15),
          (13, -10), (9, -2), (9, 4), (4, 6), (-8, 4), (-13, 8), (-17, 15),
          (-17, 21), (-16, 28), (-13, 33), (-6, 35)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
           (5, 53), (8, 57), (10, 59), (5, 60), (10, 62), (14, 66), (18, 69),
           (25, 71), (32, 70), (40, 68), (45, 66), (50, 69), (60, 69), (70, 72),
           (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
           (140, 72), (150, 70), (160, 69), (170, 67), (178, 65), (170, 60),
           (162, 56), (156, 51), (150, 59), (142, 59), (142, 50), (135, 43),
           (130, 42), (127, 40), (122, 39), (120, 34), (122, 30), (118, 25),
           (110, 20), (108, 18), (105, 9), (103, 2), (100, 6), (98, 10),
           (95, 16), (92, 21), (89, 22), (86, 20), (80, 16), (77, 8),
           (75, 20), (72, 21), (66, 25), (62, 25), (57, 26), (52, 26),
           (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36),
           (27, 37), (23, 36), (22, 40), (19, 42), (16, 44), (12, 44),
           (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36), (-10, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52), (-5, 50)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
             (132, -32), (136, -35), (140, -38), (146, -39), (150, -37), (153, -32),
             (153, -27), (150, -23), (146, -19), (142, -15), (142, -11), (137, -12),
             (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
             (114, -22)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
         (141, 41), (143, 42), (145, 44), (142, 44), (140, 40), (138, 37),
         (136, 35), (133, 34), (131, 33), (130, 31)]
PINS = {  # number -> (lon, lat): brief list number -> story location
    1: (96, 16), 2: (6, 46), 3: (84, 29), 4: (47, 25), 5: (114, 23),
    6: (-98, 36), 7: (-75, 10), 8: (-17, 14), 9: (-9, 39), 10: (26, 40),
    11: (34, 31), 12: (18, 32), 13: (45, 15), 14: (51, 35), 15: (35, 48),
    16: (-77, 39), 17: (-88, 41), 18: (90, 24), 21: (106, 38),
}


def draw_map(draw):
    draw.rectangle([MX0, MY0, MX1, MY1], fill=(13, 42, 68),
                   outline=PANEL_EDGE, width=2)
    for lon in range(-150, 181, 30):
        x = MX0 + (lon + 180) / 360.0 * (MX1 - MX0)
        draw.line([(x, MY0), (x, MY1)], fill=(28, 70, 100), width=1)
    for lat in range(-60, 81, 30):
        y = MY0 + (82 - lat) / 164.0 * (MY1 - MY0)
        draw.line([(MX0, y), (MX1, y)], fill=(28, 70, 100), width=1)
    for poly in (N_AMERICA, GREENLAND, S_AMERICA, AFRICA, EURASIA, UK,
                 AUSTRALIA, JAPAN):
        pts = [ll(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    draw.text((MX0 + 10, MY1 - 26), "WORLD MAP  •  WHERE THE DAY HAPPENED",
              font=font(BOLD, 15), fill=MUTED)
    for n, (lon, lat) in PINS.items():
        x, y = ll(lon, lat)
        r = 11
        draw.ellipse([x - r, y - r, x + r, y + r], fill=GOLD,
                     outline=(255, 255, 255), width=2)
        t = str(n)
        tw = draw.textlength(t, font=font(BOLD, 13))
        draw.text((x - tw / 2, y - 8), t, font=font(BOLD, 13), fill=(20, 20, 20))


PANELS = [  # item numbers = brief list numbers; pins on the map match them
    ("MIDDLE EAST", GOLD, [
        ("4", "Houthi drone hits Riyadh tower", "PIF tower struck; 11 injured"),
        ("11", "Gaza: Oxfam calls land \u201ctoxic\u201d", "Meningitis warning as siege bites"),
        ("13", "Saudi airstrikes hit Yemen", "Houthis report dozens killed"),
        ("14", "Iran: singer gets 74 lashes", "Parastoo Ahmadi; Tehran sets 7 terms"),
    ]),
    ("EUROPE", GOLD, [
        ("12", "Ukraine hits Russian ship off Libya", "Tripoli demands answers from Kyiv"),
        ("15", "Zaporizhzhia struck again overnight", "NATO jets patrol over Poland"),
        ("10", "COP31 ends with no fossil-fuel call", "Climate talks fail on transition"),
    ]),
    ("ASIA", GOLD, [
        ("3", "Quake M5.6 shakes Nepal", "Koshi province, near China border"),
        ("18", "Hasina to return 16 December", "Ex-PM heads back to Bangladesh"),
        ("21", "Tiangong opens to foreign crew", "Pakistan joins Shenzhou-24 mission"),
        ("5", "Huawei guilty of trade-secret theft", "Cleared of racketeering charges"),
    ]),
    ("AMERICAS", GOLD, [
        ("6", "US recovers $8 billion in fraud sweep", "800+ charged in largest crackdown"),
        ("7", "Gunman holds 25 hostage in Cartagena", "Supermarket siege in Colombia"),
        ("17", "Democrats retake US House", "259 seats flip the chamber"),
        ("16", "Trump honours Giuliani", "Medal of Freedom awarded"),
    ]),
    ("AFRICA  ·  WORLD", GOLD, [
        ("8", "Senegal lift AFCON crown", "Title confirmed after CAS appeal"),
        ("1", "14 nations back ICJ Rohingya ruling", "UK, Spain, Canada, Australia +10"),
        ("2", "UN chief: AI-risk framework in a year", "Guterres sets multilateral deadline"),
        ("9", "Ronaldo reaches 987 goals", "Career milestone keeps climbing"),
    ]),
]


def draw_panel(draw, x, y, w, h, title, items):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_EDGE, width=2)
    draw.rectangle([x, y, x + w, y + 34], fill=(24, 66, 104))
    draw.text((x + 12, y + 7), title, font=font(BOLD, 19), fill=GOLD_LT)
    cy = y + 44
    for num, head, sub in items:
        r = 10
        draw.ellipse([x + 12, cy + 2, x + 12 + 2 * r, cy + 2 + 2 * r],
                     fill=GOLD, outline=(255, 255, 255), width=1)
        tw = draw.textlength(num, font=font(BOLD, 12))
        draw.text((x + 12 + r - tw / 2, cy + 4), num, font=font(BOLD, 12),
                  fill=(20, 20, 20))
        hx = x + 42
        cy = text_block(draw, hx, cy, head, font(BOLD, 18), INK, w - 54, 20)
        cy = text_block(draw, hx, cy + 1, sub, font(REG, 13), MUTED, w - 54, 15)
        cy += 4
    return cy


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 104], fill=NAVY2)
    d.line([(0, 104), (W, 104)], fill=GOLD, width=3)
    d.text((24, 12), "TUESDAY 24 NOVEMBER 2026", font=font(BOLD, 52), fill=INK)
    d.text((24, 72), "WORLD ATLAS  •  ONE DAY, FIVE REGIONS  •  THE WORLD IN ONE PICTURE",
           font=font(BOLD, 19), fill=GOLD_LT)
    d.text((W - 24 - d.textlength("24 NOV 2026", font=font(BOLD, 19)), 72),
           "24 NOV 2026", font=font(BOLD, 19), fill=MUTED)
    # Map
    draw_map(d)
    # Panels: row 1 (3), row 2 (2 + numbers box)
    pw, ph, gap = 325, 285, 10
    x0, y1 = 12, 368
    for i in range(3):
        title, _, items = PANELS[i]
        draw_panel(d, x0 + i * (pw + gap), y1, pw, ph, title, items)
    y2 = y1 + ph + gap
    for i in range(3, 5):
        title, _, items = PANELS[i]
        draw_panel(d, x0 + (i - 3) * (pw + gap), y2, pw, ph, title, items)
    # BY THE NUMBERS box (third slot, row 2)
    nx = x0 + 2 * (pw + gap)
    d.rectangle([nx, y2, nx + pw, y2 + ph], fill=(24, 66, 104),
                outline=PANEL_EDGE, width=2)
    d.rectangle([nx, y2, nx + pw, y2 + 34], fill=GOLD)
    d.text((nx + 12, y2 + 7), "BY THE NUMBERS", font=font(BOLD, 19), fill=(20, 20, 20))
    nums = [("$8bn", "fraud cash recovered"),
            ("800+", "charged in US sweep"),
            ("259", "House seats for Democrats"),
            ("987", "Ronaldo career goals"),
            ("M5.6", "Nepal earthquake"),
            ("11", "injured in Riyadh strike"),
            ("25", "hostages in Cartagena")]
    ny = y2 + 46
    for big, small in nums:
        d.text((nx + 14, ny), big, font=font(BOLD, 22), fill=GOLD_LT)
        d.text((nx + 108, ny + 4), small, font=font(REG, 15), fill=INK)
        ny += 30
    # Footer strip: markets + source note
    fy = y2 + ph + gap
    d.rectangle([12, fy, W - 12, fy + 34], fill=NAVY2, outline=PANEL_EDGE, width=1)
    d.text((22, fy + 8),
           "MARKETS:  S&P +4.7%   •   Nasdaq +6.5%   •   Nikkei +3.9%   •   Brent $86.7   •   Gold $3,620",
           font=font(BOLD, 16), fill=INK)
    d.text((24, fy + 44), "All events happened or were first reported on Tuesday 24 November 2026.",
           font=font(REG, 14), fill=MUTED)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
