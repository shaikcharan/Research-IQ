"""
generate_ct_logo.py
===================
Generates a crisp, high-resolution official academic emblem for CT University:
- Circular crest in Royal Navy (#1E3A8A) and Gold (#D97706).
- Outer circle banner: 'CT UNIVERSITY • LUDHIANA, PUNJAB •'.
- Inner heraldic shield featuring:
  * Open Book of Knowledge
  * Engineering Cogwheel
  * Neural AI / Data Network nodes
  * Torch of Enlightenment & Stars
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(BASE_DIR, "ResearchIQ_Internship_Report", "figures", "ct_university_logo.png")

def create_university_logo():
    size = (800, 800)
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = 400, 400
    r_outer = 380
    r_mid = 350
    r_inner = 280

    # Colors
    c_navy = (30, 58, 138, 255)       # #1E3A8A
    c_gold = (217, 119, 6, 255)       # #D97706
    c_light_gold = (251, 191, 36, 255)# #FBBF24
    c_white = (255, 255, 255, 255)
    c_slate = (241, 245, 249, 255)

    # 1. Outer decorative ring
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=c_gold, width=8)
    draw.ellipse([cx - (r_outer - 10), cy - (r_outer - 10), cx + (r_outer - 10), cy + (r_outer - 10)], outline=c_navy, width=4)

    # 2. Main Navy Banner Ring
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], fill=c_navy, outline=c_gold, width=6)

    # 3. Inner White Field
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=c_white, outline=c_gold, width=6)

    # 4. Text around the ring
    # Top text: CT UNIVERSITY
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 46)
        font_med = ImageFont.truetype("arialbd.ttf", 30)
        font_small = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_large = font_med = font_small = ImageFont.load_default()

    # Draw "CT UNIVERSITY" curved or centered on top arc
    text_top = "CT UNIVERSITY"
    # Draw letters along top arc
    radius_text = 315
    angle_step = 6.5
    start_angle = -90 - ((len(text_top) - 1) * angle_step) / 2
    for i, ch in enumerate(text_top):
        ang_deg = start_angle + i * angle_step
        ang_rad = math.radians(ang_deg)
        x = cx + radius_text * math.cos(ang_rad)
        y = cy + radius_text * math.sin(ang_rad)
        # Draw character
        draw.text((x, y), ch, fill=c_white, font=font_large, anchor="mm")

    # Bottom text: LUDHIANA, PUNJAB • ESTD. 2016
    text_bot = "• LUDHIANA • PUNJAB •"
    start_angle_bot = 90 - ((len(text_bot) - 1) * 5.5) / 2
    for i, ch in enumerate(text_bot):
        ang_deg = start_angle_bot + i * 5.5
        ang_rad = math.radians(ang_deg)
        x = cx + radius_text * math.cos(ang_rad)
        y = cy + radius_text * math.sin(ang_rad)
        draw.text((x, y), ch, fill=c_light_gold, font=font_med, anchor="mm")

    # 5. Heraldic Shield inside the inner field
    shield_pts = [
        (cx - 150, cy - 170),
        (cx + 150, cy - 170),
        (cx + 150, cy + 20),
        (cx, cy + 180),
        (cx - 150, cy + 20)
    ]
    draw.polygon(shield_pts, fill=c_slate, outline=c_navy, width=6)

    # Shield divider line
    draw.line([(cx, cy - 170), (cx, cy + 180)], fill=c_gold, width=4)
    draw.line([(cx - 150, cy), (cx + 150, cy)], fill=c_gold, width=4)

    # 6. Icons inside Shield quadrants
    # Top-Left: Open Book (Knowledge)
    bx, by = cx - 75, cy - 85
    # Left page
    draw.polygon([(bx - 45, by - 25), (bx - 5, by - 35), (bx - 5, by + 25), (bx - 45, by + 15)], fill=c_navy, outline=c_gold, width=2)
    # Right page
    draw.polygon([(bx + 5, by - 35), (bx + 45, by - 25), (bx + 45, by + 15), (bx + 5, by + 25)], fill=c_navy, outline=c_gold, width=2)
    draw.line([(bx - 5, by + 25), (bx + 5, by + 25)], fill=c_gold, width=3)

    # Top-Right: Engineering Cogwheel / Gear
    gx, gy = cx + 75, cy - 85
    draw.ellipse([gx - 32, gy - 32, gx + 32, gy + 32], fill=c_navy, outline=c_gold, width=3)
    draw.ellipse([gx - 14, gy - 14, gx + 14, gy + 14], fill=c_slate, outline=c_gold, width=2)
    for teeth in range(8):
        t_ang = math.radians(teeth * 45)
        tx1 = gx + 28 * math.cos(t_ang)
        ty1 = gy + 28 * math.sin(t_ang)
        tx2 = gx + 40 * math.cos(t_ang)
        ty2 = gy + 40 * math.sin(t_ang)
        draw.line([(tx1, ty1), (tx2, ty2)], fill=c_navy, width=8)

    # Bottom-Left: AI / Neural Network Nodes
    nx, ny = cx - 75, cy + 80
    n_pts = [
        (nx - 30, ny - 25), (nx + 30, ny - 25),
        (nx - 40, ny + 20), (nx, ny + 35), (nx + 40, ny + 20)
    ]
    # Edges
    for p1 in n_pts[:2]:
        for p2 in n_pts[2:]:
            draw.line([p1, p2], fill=c_gold, width=2)
    # Nodes
    for p in n_pts:
        draw.ellipse([p[0]-8, p[1]-8, p[0]+8, p[1]+8], fill=c_navy, outline=c_gold, width=2)

    # Bottom-Right: Torch of Enlightenment / Flame
    fx, fy = cx + 75, cy + 85
    # Handle
    draw.polygon([(fx - 8, fy + 45), (fx + 8, fy + 45), (fx + 12, fy + 10), (fx - 12, fy + 10)], fill=c_navy, outline=c_gold, width=2)
    # Flame
    flame_pts = [
        (fx, fy - 35), (fx + 20, fy - 5), (fx + 10, fy + 10),
        (fx - 10, fy + 10), (fx - 20, fy - 5)
    ]
    draw.polygon(flame_pts, fill=c_gold, outline=c_light_gold, width=2)
    draw.ellipse([fx - 8, fy - 15, fx + 8, fy + 5], fill=c_light_gold)

    # 7. Motto Ribbon underneath shield
    rx, ry = cx, cy + 225
    draw.rectangle([rx - 160, ry - 18, rx + 160, ry + 18], fill=c_navy, outline=c_gold, width=3)
    draw.text((rx, ry), "INDUSTRIA ET SAPIENTIA", fill=c_white, font=font_small, anchor="mm")

    # Save
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, "PNG")
    print(f"CT University emblem generated successfully at: {OUT_PATH}")

if __name__ == "__main__":
    create_university_logo()
