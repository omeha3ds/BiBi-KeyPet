#!/usr/bin/env python3
"""Generate pre-baked Flash sprites (ui/liquid_sprites.h / .c) for Pip's Liquid eyes.

Every sprite is stored as `const` in Flash (.rodata, 0 bytes internal RAM) using
LVGL 9 native formats (LV_COLOR_FORMAT_RGB565A8 and LV_COLOR_FORMAT_A8) with 4x4
Bayer ordered dithering to eliminate RGB565 banding on the 1.75" AMOLED panel.

Run from the repository root:
    python tools/liquid_sprites.py
Optional preview PNGs (for visual check):
    python tools/liquid_sprites.py --preview <dir>
"""
from __future__ import annotations
import argparse
import math
import os
import struct
import zlib

# 4x4 Bayer matrix in [0, 1) for banding-free RGB565 quantization
BAYER4 = (
    (0.5 / 16, 8.5 / 16, 2.5 / 16, 10.5 / 16),
    (12.5 / 16, 4.5 / 16, 14.5 / 16, 6.5 / 16),
    (3.5 / 16, 11.5 / 16, 1.5 / 16, 9.5 / 16),
    (15.5 / 16, 7.5 / 16, 13.5 / 16, 5.5 / 16),
)

# Exact Pixel palette liquid stops matching docs/index.html (in theme order TH_PEONY..TH_PORCELAIN)
PALETTES = [
    dict(
        id="peony",
        eye_hi=0xFFE4ED, eye_mid=0xF5B0C6, eye_deep=0xAD5270, eye_caustic=0xFFD9E6,
        pupil_hi=0x4AE3E6, pupil_mid=0x00979C, pupil_deep=0x004A52,
        obsidian=False, rim=0,
    ),
    dict(
        id="obsidian",
        eye_hi=0x1A4963, eye_mid=0x050F16, eye_deep=0x000000, eye_caustic=0x4DD0FF,
        pupil_hi=0xE8FDFF, pupil_mid=0x6BE2FF, pupil_deep=0x0B86BD,
        obsidian=True, rim=0x4DD0FF,
    ),
    dict(
        id="bay",
        eye_hi=0xE0EFFF, eye_mid=0x95C5FF, eye_deep=0x447ED0, eye_caustic=0xCCE4FF,
        pupil_hi=0x5D94FF, pupil_mid=0x154EC4, pupil_deep=0x082266,
        obsidian=False, rim=0,
    ),
    dict(
        id="hazel",
        eye_hi=0xE8FAE9, eye_mid=0xB4E2B8, eye_deep=0x569460, eye_caustic=0xDCF7DE,
        pupil_hi=0x4AC47C, pupil_mid=0x167A42, pupil_deep=0x073B1D,
        obsidian=False, rim=0,
    ),
    dict(
        id="coral",
        eye_hi=0xFFE5DC, eye_mid=0xFFAA8E, eye_deep=0xBF593B, eye_caustic=0xFFD8CA,
        pupil_hi=0xFF7A54, pupil_mid=0xD93C16, pupil_deep=0x731704,
        obsidian=False, rim=0,
    ),
    dict(
        id="porcelain",
        eye_hi=0xFFF9E8, eye_mid=0xF0DFA9, eye_deep=0xB09455, eye_caustic=0xFFF2CF,
        pupil_hi=0xEF854C, pupil_mid=0xBD4C16, pupil_deep=0x632105,
        obsidian=False, rim=0,
    ),
]

# Geometry constants shared with ui/pip.c
SCLERA_W, SCLERA_H = 148, 172
SCLERA_RX, SCLERA_RY = 64.0, 76.0  # 10 px margin around ellipse for Obsidian glow & clean AA

PUPIL_W, PUPIL_H = 76, 100
PUPIL_RX, PUPIL_RY = 26.0, 38.0    # 12 px margin around ellipse for Obsidian pupil halo

SPEC_W, SPEC_H = 76, 64
HEART_W, HEART_H = 88, 84
BLUSH_W, BLUSH_H = 104, 42
LID_W, LID_H, LID_EDGE_Y = 240, 216, 182
SMILE_W, SMILE_H, SMILE_EDGE_Y = 240, 152, 28


def hex_rgb(c: int) -> tuple[float, float, float]:
    return ((c >> 16) & 255) / 255.0, ((c >> 8) & 255) / 255.0, (c & 255) / 255.0


def clamp01(v: float) -> float:
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


def smoothstep(e0: float, e1: float, x: float) -> float:
    t = clamp01((x - e0) / (e1 - e0))
    return t * t * (3.0 - 2.0 * t)


def mix3(a: tuple[float, float, float], b: tuple[float, float, float], t: float) -> tuple[float, float, float]:
    t = clamp01(t)
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t


def grad3(c0, c1, c2, mid: float, t: float) -> tuple[float, float, float]:
    t = clamp01(t)
    if t <= mid:
        return mix3(c0, c1, t / mid)
    return mix3(c1, c2, (t - mid) / (1.0 - mid))


def pack_rgb565(r: float, g: float, b: float, x: int, y: int) -> int:
    d = BAYER4[y & 3][x & 3]
    ri = min(31, max(0, int(clamp01(r) * 31.0 + d)))
    gi = min(63, max(0, int(clamp01(g) * 63.0 + d)))
    bi = min(31, max(0, int(clamp01(b) * 31.0 + d)))
    return (ri << 11) | (gi << 5) | bi


def encode_rgb565a8(w: int, h: int, pixels: list[tuple[float, float, float, float]]) -> bytes:
    """LVGL 9 RGB565A8: W*H little-endian uint16 RGB565 plane followed by W*H uint8 alpha plane."""
    rgb = bytearray(w * h * 2)
    alpha = bytearray(w * h)
    for y in range(h):
        row = y * w
        for x in range(w):
            r, g, b, a = pixels[row + x]
            c = pack_rgb565(r, g, b, x, y)
            off = (row + x) * 2
            rgb[off] = c & 0xFF
            rgb[off + 1] = (c >> 8) & 0xFF
            alpha[row + x] = min(255, max(0, int(clamp01(a) * 255.0 + 0.5)))
    return bytes(rgb) + bytes(alpha)


def encode_a8(w: int, h: int, alphas: list[float]) -> bytes:
    out = bytearray(w * h)
    for i, a in enumerate(alphas):
        out[i] = min(255, max(0, int(clamp01(a) * 255.0 + 0.5)))
    return bytes(out)


def render_sclera(pal: dict) -> list[tuple[float, float, float, float]]:
    w, h = SCLERA_W, SCLERA_H
    cx, cy = w * 0.5, h * 0.5
    rx, ry = SCLERA_RX, SCLERA_RY
    c_hi = hex_rgb(pal["eye_hi"])
    c_mid = hex_rgb(pal["eye_mid"])
    c_deep = hex_rgb(pal["eye_deep"])
    c_caus = hex_rgb(pal["eye_caustic"])
    c_rim = hex_rgb(pal["rim"]) if pal["obsidian"] else (1.0, 1.0, 1.0)
    obs = pal["obsidian"]

    px: list[tuple[float, float, float, float]] = []
    for y in range(h):
        dy = (y + 0.5) - cy
        ny = dy / ry
        for x in range(w):
            dx = (x + 0.5) - cx
            nx = dx / rx
            r = math.hypot(nx, ny)
            grad = math.hypot(nx / rx, ny / ry) if r > 1e-6 else (1.0 / min(rx, ry))
            d_px = (1.0 - r) / grad  # >0 inside ellipse, <0 outside

            # Volumetric radial shading focused upper-left (matching docs/index.html gradSclera)
            fx, fy = -0.30, -0.40
            rt = math.hypot((nx - fx) * 0.72, (ny - fy) * 0.72) / 1.15
            col = grad3(c_hi, c_mid, c_deep, 0.54, rt)

            # Lower internal caustic refraction glow
            cx_c, cy_c = (0.04, 0.62) if obs else (0.10, 0.56)
            rc = math.hypot((nx - cx_c) / 0.74, (ny - cy_c) / 0.36)
            if rc < 1.0:
                ca = (1.0 - rc * rc) ** 1.6 * (0.28 if obs else 0.56)
                col = mix3(col, c_caus, ca)

            cov = clamp01(d_px + 0.5)

            if obs:
                # Signature Obsidian liquid cyan glass rim + soft outer & inner glow
                # Core stroke spans d_px in [-0.6, +4.4] (~5.0 px wide)
                rim_core = clamp01(d_px + 1.1) * clamp01(4.7 - d_px)
                # Subtle brighter top-left rim highlight
                rim_col = mix3(c_rim, (0.78, 0.97, 1.0), clamp01((-nx * 0.5 - ny * 0.6) * 0.35 + 0.15))
                if d_px >= 0.0:
                    # Inner soft cyan glass glow fading inward
                    in_glow = math.exp(-((max(0.0, d_px - 3.8) / 5.2) ** 2)) * 0.30
                    col = mix3(col, c_rim, in_glow)
                    col = mix3(col, rim_col, rim_core)
                    # Subtle top-left glass reflection arc inside dark dome
                    sheen = math.exp(-(((d_px - 6.0) / 3.2) ** 2)) * clamp01(-nx * 0.6 - ny * 0.8) * 0.22
                    col = mix3(col, (0.72, 0.94, 1.0), sheen)
                    px.append((col[0], col[1], col[2], 1.0))
                else:
                    # Soft Gaussian cyan outer glow halo (straight RGB for LVGL RGB565A8!)
                    out_dist = -d_px
                    # Fade smoothly to exactly 0 at margin edge (9.5 px) so no box seam ever appears
                    edge_win = clamp01((9.5 - out_dist) / 3.0)
                    out_glow = math.exp(-((out_dist / 4.2) ** 2)) * 0.72 * edge_win
                    a = max(cov, out_glow)
                    if a <= 1e-4:
                        px.append((0.0, 0.0, 0.0, 0.0))
                    else:
                        # Blend rim/body near the anti-aliased edge, pure straight rim_col in halo
                        edge_t = clamp01(cov / a)
                        bcol = mix3(col, rim_col, clamp01(rim_core + 0.75))
                        final = mix3(rim_col, bcol, edge_t * 0.3)
                        px.append((final[0], final[1], final[2], a))
            else:
                if cov <= 1e-4:
                    px.append((0.0, 0.0, 0.0, 0.0))
                else:
                    # Subtle inner depth rim on lower-right + delicate white glass sheen on top-left
                    dir_tl = -nx * 0.58 - ny * 0.81  # +1 top-left, -1 bottom-right
                    edge_band = math.exp(-(((d_px - 2.0) / 2.0) ** 2))
                    if dir_tl > 0.0:
                        col = mix3(col, (1.0, 1.0, 1.0), edge_band * (dir_tl ** 1.2) * 0.58)
                    else:
                        # Subtle darker deep rim on bottom-right for lush droplet thickness
                        col = mix3(col, c_deep, edge_band * ((-dir_tl) ** 1.1) * 0.34)
                    px.append((col[0], col[1], col[2], cov))
    return px


def render_pupil(pal: dict) -> list[tuple[float, float, float, float]]:
    w, h = PUPIL_W, PUPIL_H
    cx, cy = w * 0.5, h * 0.5
    rx, ry = PUPIL_RX, PUPIL_RY
    c_hi = hex_rgb(pal["pupil_hi"])
    c_mid = hex_rgb(pal["pupil_mid"])
    c_deep = hex_rgb(pal["pupil_deep"])
    c_glow = hex_rgb(pal["rim"]) if pal["obsidian"] else c_mid
    obs = pal["obsidian"]

    px: list[tuple[float, float, float, float]] = []
    for y in range(h):
        dy = (y + 0.5) - cy
        ny = dy / ry
        for x in range(w):
            dx = (x + 0.5) - cx
            nx = dx / rx
            r = math.hypot(nx, ny)
            grad = math.hypot(nx / rx, ny / ry) if r > 1e-6 else (1.0 / min(rx, ry))
            d_px = (1.0 - r) / grad

            fx, fy = -0.28, -0.38
            rt = math.hypot((nx - fx) * 0.72, (ny - fy) * 0.72) / 1.12
            col = grad3(c_hi, c_mid, c_deep, 0.52, rt)
            cov = clamp01(d_px + 0.5)

            if obs:
                out_dist = max(0.0, -d_px)
                edge_win = clamp01((11.5 - out_dist) / 3.5)
                halo = math.exp(-((out_dist / 5.4) ** 2)) * 0.78 * edge_win
                # Smoothly blend droplet edge into luminous cyan halo without any step
                core_t = smoothstep(-1.0, 1.4, d_px)
                a = max(cov, halo)
                if a <= 1e-4:
                    px.append((0.0, 0.0, 0.0, 0.0))
                else:
                    final = mix3(c_glow, col, core_t)
                    px.append((final[0], final[1], final[2], a))
            else:
                if cov <= 1e-4:
                    px.append((0.0, 0.0, 0.0, 0.0))
                else:
                    px.append((col[0], col[1], col[2], cov))
    return px


def render_specular() -> list[float]:
    """Soft liquid glass top-left specular pill + tiny crisp pinpoint dot (A8 white mask)."""
    w, h = SPEC_W, SPEC_H
    out: list[float] = []
    # Main tilted pill (matching .eye-spec in docs/index.html)
    c1x, c1y, rx1, ry1, ang1 = 44.0, 23.0, 25.0, 12.5, math.radians(-28.0)
    ca1, sa1 = math.cos(-ang1), math.sin(-ang1)
    # Secondary pinpoint oval (matching .eye-dot in docs/index.html)
    c2x, c2y, rx2, ry2, ang2 = 20.0, 47.0, 5.5, 3.6, math.radians(-22.0)
    ca2, sa2 = math.cos(-ang2), math.sin(-ang2)

    for y in range(h):
        for x in range(w):
            px, py = x + 0.5, y + 0.5
            # Pill 1 with top-to-bottom glossy fade (matching #gradSpec)
            dx1, dy1 = px - c1x, py - c1y
            u1 = (dx1 * ca1 - dy1 * sa1) / rx1
            v1 = (dx1 * sa1 + dy1 * ca1) / ry1
            r1 = math.hypot(u1, v1)
            a1 = 0.0
            if r1 < 1.18:
                edge1 = smoothstep(1.15, 0.65, r1)
                # Linear fade from top-left (-1) to bottom-right (+1)
                fade1 = smoothstep(0.95, -0.85, v1 * 0.85 + u1 * 0.25)
                a1 = edge1 * fade1 * 0.86

            # Dot 2
            dx2, dy2 = px - c2x, py - c2y
            u2 = (dx2 * ca2 - dy2 * sa2) / rx2
            v2 = (dx2 * sa2 + dy2 * ca2) / ry2
            r2 = math.hypot(u2, v2)
            a2 = smoothstep(1.15, 0.55, r2) * 0.78 if r2 < 1.18 else 0.0

            out.append(clamp01(1.0 - (1.0 - a1) * (1.0 - a2)))
    return out


def heart_sdf(x: float, y: float) -> float:
    """Inigo Quilez heart SDF, y up, tip at (0, 0), height ~1.0 (negative inside)."""
    x = abs(x)
    if y + x > 1.0:
        return math.hypot(x - 0.25, y - 0.75) - 0.35355339
    ax, ay = x, y - 1.0
    m = 0.5 * max(x + y, 0.0)
    bx, by = x - m, y - m
    d = min(ax * ax + ay * ay, bx * bx + by * by)
    return math.sqrt(d) * (1.0 if x > y else -1.0)


def render_heart() -> list[tuple[float, float, float, float]]:
    """Glossy volumetric liquid rose-pink heart for PIP_LOVE."""
    w, h = HEART_W, HEART_H
    cx, cy = w * 0.5, h * 0.5
    scale = 68.0
    c_hi = hex_rgb(0xFFB3CA)
    c_mid = hex_rgb(0xFF3E75)
    c_deep = hex_rgb(0x9E103D)

    px: list[tuple[float, float, float, float]] = []
    for y in range(h):
        for x in range(w):
            # Map pixel into heart SDF space (centered vertically around y_sdf = 0.52)
            hx = ((x + 0.5) - cx) / scale
            hy = -((y + 0.5) - cy) / scale + 0.52
            d = heart_sdf(hx, hy) * scale  # negative inside, in pixels
            cov = clamp01(0.5 - d)
            if cov <= 1e-4:
                px.append((0.0, 0.0, 0.0, 0.0))
                continue
            rt = math.hypot((hx + 0.18) * 1.1, (hy - 0.78) * 1.1) / 1.05
            col = grad3(c_hi, c_mid, c_deep, 0.50, rt)
            # Soft liquid gloss highlight on left lobe
            lx, ly = (hx + 0.22) / 0.19, (hy - 0.80) / 0.11
            gl = smoothstep(1.1, 0.3, math.hypot(lx, ly)) * 0.55
            col = mix3(col, (1.0, 1.0, 1.0), gl)
            px.append((col[0], col[1], col[2], cov))
    return px


def render_blush() -> list[float]:
    w, h = BLUSH_W, BLUSH_H
    cx, cy = w * 0.5, h * 0.5
    rx, ry = w * 0.48, h * 0.46
    out: list[float] = []
    for y in range(h):
        ny = ((y + 0.5) - cy) / ry
        for x in range(w):
            nx = ((x + 0.5) - cx) / rx
            r = math.hypot(nx, ny)
            a = clamp01(1.0 - r) ** 1.7 * 0.88 if r < 1.0 else 0.0
            out.append(a)
    return out


def render_lid() -> list[float]:
    """Curved upper eyelid A8 mask (black): follows eye dome curvature + soft feathered rim & 3D contact shadow."""
    w, h = LID_W, LID_H
    cx = w * 0.5
    out: list[float] = []
    for y in range(h):
        py = y + 0.5
        for x in range(w):
            # Normalized horizontal offset across the eye dome (-1..+1)
            u = ((x + 0.5) - cx) / (w * 0.36)
            # Graceful convex dome arch: center higher, outer/inner sides wrap gently down around the eye
            y_curve = LID_EDGE_Y - 14.0 + 14.0 * min(u * u, 1.85)
            d = py - y_curve  # <0 above lid (solid black), >0 below lid (soft contact shadow fading to 0)
            if d <= 0.0:
                a = 1.0
            else:
                # Smooth anti-aliased eyelid lip (0..4.5 px) + soft 3D shadow falloff (up to ~22 px)
                lip = smoothstep(4.5, 0.0, d)
                shadow = 0.44 * math.exp(-((d / 9.5) ** 1.55))
                # Fade shadow cleanly to 0 before the bottom edge of the sprite
                win = smoothstep(h - 1.5, h - 10.0, py)
                a = max(lip, shadow) * win
            out.append(clamp01(a))
    return out


def render_smile() -> list[float]:
    """Curved lower cheek-smile A8 mask (black): smooth happy arc + delicate soft upper rim shadow."""
    w, h = SMILE_W, SMILE_H
    cx = w * 0.5
    out: list[float] = []
    for y in range(h):
        py = y + 0.5
        for x in range(w):
            u = ((x + 0.5) - cx) / (w * 0.34)
            # Cheerful upward-arching smile crescent (^ ^): center highest, slopes smoothly down at sides
            y_curve = SMILE_EDGE_Y + 22.0 * min(u * u, 2.2)
            d = y_curve - py  # <0 below arc (solid black cheek), >0 above arc (soft rim shadow fading to 0)
            if d <= 0.0:
                a = 1.0
            else:
                lip = smoothstep(4.2, 0.0, d)
                shadow = 0.34 * math.exp(-((d / 7.8) ** 1.5))
                win = smoothstep(1.5, 9.0, py)
                a = max(lip, shadow) * win
            out.append(clamp01(a))
    return out


def write_png(path: str, w: int, h: int, rgba_bytes: bytes) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw.extend(rgba_bytes[y * stride : (y + 1) * stride])
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def format_c_array(name: str, data: bytes) -> str:
    lines = [f"static const uint8_t {name}[{len(data)}] = {{"]
    for i in range(0, len(data), 16):
        row = ",".join(f"0x{b:02X}" for b in data[i : i + 16])
        lines.append(f"    {row},")
    lines.append("};")
    return "\n".join(lines)


def format_img_dsc(name: str, arr: str, w: int, h: int, cf: str, stride: int, size: int) -> str:
    return (
        f"const lv_image_dsc_t {name} = {{\n"
        f"    .header = {{.magic = LV_IMAGE_HEADER_MAGIC, .cf = {cf}, .w = {w}, .h = {h}, .stride = {stride}}},\n"
        f"    .data_size = {size},\n"
        f"    .data = {arr},\n"
        f"}};\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="Optional directory to write preview PNGs of baked sprites")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    h_path = os.path.join(root, "ui", "liquid_sprites.h")
    c_path = os.path.join(root, "ui", "liquid_sprites.c")

    total_bytes = 0
    c_parts = [
        "/* Auto-generated by tools/liquid_sprites.py — do not edit by hand. */\n"
        "#include \"liquid_sprites.h\"\n\n"
    ]

    if args.preview:
        os.makedirs(args.preview, exist_ok=True)

    sclera_refs = []
    pupil_refs = []

    for pal in PALETTES:
        pid = pal["id"]
        s_px = render_sclera(pal)
        s_data = encode_rgb565a8(SCLERA_W, SCLERA_H, s_px)
        total_bytes += len(s_data)
        c_parts.append(format_c_array(f"liq_sclera_{pid}_map", s_data) + "\n")
        c_parts.append(format_img_dsc(f"liq_sclera_{pid}", f"liq_sclera_{pid}_map", SCLERA_W, SCLERA_H,
                                      "LV_COLOR_FORMAT_RGB565A8", SCLERA_W * 2, len(s_data)) + "\n")
        sclera_refs.append(f"&liq_sclera_{pid}")

        p_px = render_pupil(pal)
        p_data = encode_rgb565a8(PUPIL_W, PUPIL_H, p_px)
        total_bytes += len(p_data)
        c_parts.append(format_c_array(f"liq_pupil_{pid}_map", p_data) + "\n")
        c_parts.append(format_img_dsc(f"liq_pupil_{pid}", f"liq_pupil_{pid}_map", PUPIL_W, PUPIL_H,
                                      "LV_COLOR_FORMAT_RGB565A8", PUPIL_W * 2, len(p_data)) + "\n")
        pupil_refs.append(f"&liq_pupil_{pid}")

        if args.preview and pid in ("peony", "obsidian"):
            # Composite preview PNG on black
            rgba = bytearray(SCLERA_W * SCLERA_H * 4)
            for idx, (r, g, b, a) in enumerate(s_px):
                rgba[idx * 4 : idx * 4 + 4] = bytes((int(r * a * 255), int(g * a * 255), int(b * a * 255), 255))
            write_png(os.path.join(args.preview, f"sprite_sclera_{pid}.png"), SCLERA_W, SCLERA_H, bytes(rgba))
            rgba_p = bytearray(PUPIL_W * PUPIL_H * 4)
            for idx, (r, g, b, a) in enumerate(p_px):
                rgba_p[idx * 4 : idx * 4 + 4] = bytes((int(r * a * 255), int(g * a * 255), int(b * a * 255), 255))
            write_png(os.path.join(args.preview, f"sprite_pupil_{pid}.png"), PUPIL_W, PUPIL_H, bytes(rgba_p))

    spec_a = render_specular()
    spec_data = encode_a8(SPEC_W, SPEC_H, spec_a)
    total_bytes += len(spec_data)
    c_parts.append(format_c_array("liq_specular_map", spec_data) + "\n")
    c_parts.append(format_img_dsc("liq_specular", "liq_specular_map", SPEC_W, SPEC_H,
                                  "LV_COLOR_FORMAT_A8", SPEC_W, len(spec_data)) + "\n")

    heart_px = render_heart()
    heart_data = encode_rgb565a8(HEART_W, HEART_H, heart_px)
    total_bytes += len(heart_data)
    c_parts.append(format_c_array("liq_heart_map", heart_data) + "\n")
    c_parts.append(format_img_dsc("liq_heart", "liq_heart_map", HEART_W, HEART_H,
                                  "LV_COLOR_FORMAT_RGB565A8", HEART_W * 2, len(heart_data)) + "\n")

    blush_a = render_blush()
    blush_data = encode_a8(BLUSH_W, BLUSH_H, blush_a)
    total_bytes += len(blush_data)
    c_parts.append(format_c_array("liq_blush_map", blush_data) + "\n")
    c_parts.append(format_img_dsc("liq_blush", "liq_blush_map", BLUSH_W, BLUSH_H,
                                  "LV_COLOR_FORMAT_A8", BLUSH_W, len(blush_data)) + "\n")

    lid_a = render_lid()
    lid_data = encode_a8(LID_W, LID_H, lid_a)
    total_bytes += len(lid_data)
    c_parts.append(format_c_array("liq_lid_map", lid_data) + "\n")
    c_parts.append(format_img_dsc("liq_lid", "liq_lid_map", LID_W, LID_H,
                                  "LV_COLOR_FORMAT_A8", LID_W, len(lid_data)) + "\n")

    smile_a = render_smile()
    smile_data = encode_a8(SMILE_W, SMILE_H, smile_a)
    total_bytes += len(smile_data)
    c_parts.append(format_c_array("liq_smile_map", smile_data) + "\n")
    c_parts.append(format_img_dsc("liq_smile", "liq_smile_map", SMILE_W, SMILE_H,
                                  "LV_COLOR_FORMAT_A8", SMILE_W, len(smile_data)) + "\n")

    c_parts.append(f"const lv_image_dsc_t *const liquid_sclera[{len(PALETTES)}] = {{{', '.join(sclera_refs)}}};\n")
    c_parts.append(f"const lv_image_dsc_t *const liquid_pupil[{len(PALETTES)}] = {{{', '.join(pupil_refs)}}};\n")

    h_text = (
        "/* Pre-baked Liquid eye sprites stored in Flash (.rodata), drawn by LVGL without per-frame gradient math. */\n"
        "#pragma once\n"
        "#include \"lvgl.h\"\n\n"
        f"#define LIQ_PALETTES {len(PALETTES)}\n"
        f"#define LIQ_SCLERA_W {SCLERA_W}\n"
        f"#define LIQ_SCLERA_H {SCLERA_H}\n"
        f"#define LIQ_SCLERA_RX {int(SCLERA_RX)}\n"
        f"#define LIQ_SCLERA_RY {int(SCLERA_RY)}\n"
        f"#define LIQ_PUPIL_W {PUPIL_W}\n"
        f"#define LIQ_PUPIL_H {PUPIL_H}\n"
        f"#define LIQ_PUPIL_RX {int(PUPIL_RX)}\n"
        f"#define LIQ_PUPIL_RY {int(PUPIL_RY)}\n"
        f"#define LIQ_SPEC_W {SPEC_W}\n"
        f"#define LIQ_SPEC_H {SPEC_H}\n"
        f"#define LIQ_HEART_W {HEART_W}\n"
        f"#define LIQ_HEART_H {HEART_H}\n"
        f"#define LIQ_BLUSH_W {BLUSH_W}\n"
        f"#define LIQ_BLUSH_H {BLUSH_H}\n"
        f"#define LIQ_LID_W {LID_W}\n"
        f"#define LIQ_LID_H {LID_H}\n"
        f"#define LIQ_LID_EDGE_Y {LID_EDGE_Y}\n"
        f"#define LIQ_SMILE_W {SMILE_W}\n"
        f"#define LIQ_SMILE_H {SMILE_H}\n"
        f"#define LIQ_SMILE_EDGE_Y {SMILE_EDGE_Y}\n"
        f"#define LIQ_FLASH_BYTES {total_bytes}\n\n"
        "extern const lv_image_dsc_t *const liquid_sclera[LIQ_PALETTES];\n"
        "extern const lv_image_dsc_t *const liquid_pupil[LIQ_PALETTES];\n"
        "extern const lv_image_dsc_t liq_specular;\n"
        "extern const lv_image_dsc_t liq_heart;\n"
        "extern const lv_image_dsc_t liq_blush;\n"
        "extern const lv_image_dsc_t liq_lid;\n"
        "extern const lv_image_dsc_t liq_smile;\n"
    )

    with open(h_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(h_text)
    with open(c_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(c_parts))

    print(
        f"Generated ui/liquid_sprites.h & .c: total {total_bytes:,} bytes ({total_bytes / 1024:.1f} KB) in Flash\n"
        f"  6x sclera ({SCLERA_W}x{SCLERA_H} RGB565A8): {6 * SCLERA_W * SCLERA_H * 3 / 1024:.1f} KB\n"
        f"  6x pupil  ({PUPIL_W}x{PUPIL_H} RGB565A8): {6 * PUPIL_W * PUPIL_H * 3 / 1024:.1f} KB\n"
        f"  specular  ({SPEC_W}x{SPEC_H} A8): {len(spec_data) / 1024:.1f} KB\n"
        f"  heart     ({HEART_W}x{HEART_H} RGB565A8): {len(heart_data) / 1024:.1f} KB\n"
        f"  blush     ({BLUSH_W}x{BLUSH_H} A8): {len(blush_data) / 1024:.1f} KB\n"
        f"  lid       ({LID_W}x{LID_H} A8): {len(lid_data) / 1024:.1f} KB\n"
        f"  smile     ({SMILE_W}x{SMILE_H} A8): {len(smile_data) / 1024:.1f} KB"
    )


if __name__ == "__main__":
    main()
