#include "doodle.h"
#include <math.h>
#include <stdbool.h>
#include <string.h>

static float clamp01(float v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
static float circle(float x, float y, float cx, float cy, float r) { return hypotf(x - cx, y - cy) - r; }
static float ellipse(float x, float y, float rx, float ry) /* approximate SDF, fine for small sprites */
{
    float k = sqrtf(x * x / (rx * rx) + y * y / (ry * ry));
    return (k - 1) * fminf(rx, ry);
}
static float rot_ellipse(float x, float y, float cx, float cy, float rx, float ry, float c, float s)
{
    float dx = x - cx, dy = y - cy;
    return ellipse(dx * c + dy * s, -dx * s + dy * c, rx, ry);
}
/* smooth union: puffs of a cloud melt into one shape */
static float smin(float a, float b, float k)
{
    float h = clamp01(0.5f + 0.5f * (b - a) / k);
    return b + (a - b) * h - k * h * (1 - h);
}

/* lay color c with coverage a over the pixel (straight, non-premultiplied ARGB) */
static void over(uint32_t *p, uint32_t c, float a)
{
    if (a <= 0) return;
    float da = (*p >> 24) / 255.0f, oa = a + da * (1 - a);
    uint32_t o = (uint32_t)(oa * 255 + 0.5f) << 24;
    for (int sh = 0; sh < 24; sh += 8) {
        float s = (c >> sh) & 255, d = (*p >> sh) & 255;
        o |= (uint32_t)((s * a + d * da * (1 - a)) / oa + 0.5f) << sh;
    }
    *p = o;
}

static float cloud(float x, float y, const float (*puffs)[3], int n)
{
    float d = 1e9f;
    for (int i = 0; i < n; i++) d = smin(d, circle(x, y, puffs[i][0], puffs[i][1], puffs[i][2]), 10);
    return d;
}

void doodle_rain_cloud(uint32_t *px, int w, int h)
{
    static const float puffs[][3] = {{40, 50, 24}, {72, 34, 30}, {108, 38, 28}, {134, 52, 22}, {86, 56, 22}};
    memset(px, 0, (size_t)w * h * 4);
    for (int y = 0; y < h; y++)
        for (int x = 0; x < w; x++) {
            float fx = x + 0.5f, fy = y + 0.5f, d = cloud(fx, fy, puffs, 5);
            float top = clamp01((44 - fy) / 30) * clamp01(-d / 10); /* a little light on top */
            uint8_t g = (uint8_t)(92 + 36 * top);
            over(&px[y * w + x], 0xFF000000u | g << 16 | (g + 4) << 8 | (g + 12), clamp01(0.5f - d));
        }
}

/* ---------- app icons ---------- */

static float box(float x, float y, float hw, float hh, float r) /* rounded box SDF */
{
    float qx = fabsf(x) - hw + r, qy = fabsf(y) - hh + r;
    return hypotf(fmaxf(qx, 0), fmaxf(qy, 0)) + fminf(fmaxf(qx, qy), 0) - r;
}
static float segment(float x, float y, float ax, float ay, float bx, float by, float r) /* capsule from a to b */
{
    float px = x - ax, py = y - ay, dx = bx - ax, dy = by - ay;
    float t = clamp01((px * dx + py * dy) / (dx * dx + dy * dy));
    return hypotf(px - dx * t, py - dy * t) - r;
}
static float ring(float x, float y, float r, float thick) { return fabsf(hypotf(x, y) - r) - thick; }

/* the white symbol, in a 100-unit box centred on 0 (y down); negative inside */
static float glyph(int icon, float x, float y)
{
    switch (icon) {
    case ICON_CLOCK:
        return fminf(ring(x, y, 30, 4.5f), fminf(segment(x, y, 0, 0, 0, -20, 4.5f), segment(x, y, 0, 0, 14, 8, 4.5f)));
    case ICON_TIMER: { /* hourglass with sand running down */
        float frame = fminf(box(x, y + 36, 26, 4, 2), box(x, y - 36, 26, 4, 2));
        float ax = fabsf(x), glass = fmaxf(fabsf(y) - 32, ax - (4 + fabsf(y) * 0.62f));
        float hollow = fmaxf(fabsf(y) - 27, ax - (fabsf(y) * 0.62f - 1));
        float sand = fminf(fmaxf(-y - 2, fmaxf(y + 27, ax - (-y) * 0.62f + 3)), fmaxf(y - 14, fmaxf(-y + 26 - 52, ax - y * 0.62f + 3)));
        sand = fminf(fmaxf(fmaxf(y - 26, 12 - y), ax - (y * 0.62f - 3)), fmaxf(fmaxf(-y - 26, y + 14), ax - (-y * 0.62f - 3)));
        float stream = box(x, y - 2, 1.5f, 14, 1);
        return fminf(fminf(frame, fmaxf(glass, -hollow)), fminf(sand, stream));
    }
    case ICON_STOPWATCH: {
        float d = fminf(ring(x, y - 6, 28, 4.5f), segment(x, y, 0, -40, 0, -33, 4.5f));
        d = fminf(d, box(x, y + 44, 10, 3.5f, 2));                    /* button on top */
        float wedge = fmaxf(hypotf(x, y - 6) - 20, fmaxf(-x, y - 6)); /* the elapsed quarter */
        return fminf(d, wedge);
    }
    case ICON_TORCH: { /* a torch pointing up-right with three rays */
        float body = segment(x, y, -26, 26, -4, 4, 9);
        float head = fmaxf(circle(x, y, 6, -6, 15), -(x - y + 4) * 0.7071f - 2);
        float rays = fminf(segment(x, y, 22, -22, 34, -34, 3.5f), fminf(segment(x, y, 12, -30, 16, -44, 3.5f), segment(x, y, 30, -12, 44, -16, 3.5f)));
        return fminf(fminf(body, head), rays);
    }
    case ICON_QR: {
        float d = 1e9f;
        static const float finders[][2] = {{-22, -22}, {22, -22}, {-22, 22}};
        for (int i = 0; i < 3; i++) {
            float fx = x - finders[i][0], fy = y - finders[i][1];
            d = fminf(d, fmaxf(box(fx, fy, 12, 12, 2), -box(fx, fy, 7.5f, 7.5f, 1)));
            d = fminf(d, box(fx, fy, 4.5f, 4.5f, 1));
        }
        static const signed char dots[][2] = {{5, 5}, {14, 5}, {23, 14}, {5, 23}, {14, 32}, {32, 23}, {23, 32}, {32, 5}};
        for (int i = 0; i < 8; i++) d = fminf(d, box(x - dots[i][0] - 1, y - dots[i][1] - 1, 4, 4, 1));
        return d;
    }
    case ICON_PIP: { /* two eyes with pupils looking right: cut-outs */
        float eyes = fminf(ellipse(x + 17, y, 13, 17), ellipse(x - 17, y, 13, 17));
        float pupils = fminf(circle(x, y, -12, 2, 6), circle(x, y, 22, 2, 6));
        return fmaxf(eyes, -pupils);
    }
    case ICON_GAME: { /* a ball rolling toward a star */
        float ball = circle(x, y, -14, 12, 15);
        float ang = atan2f(y + 18, x - 20) + 1.5708f, r = hypotf(x - 20, y + 18);
        float star = r - (7 + 11 * powf(fabsf(cosf(2.5f * ang)), 3)); /* five pointy arms */
        float trail = fminf(segment(x, y, -42, 4, -34, 4, 2.5f), segment(x, y, -44, 16, -34, 16, 2.5f));
        return fminf(fminf(ball, star), trail);
    }
    case ICON_BELL: {
        float dome = fmaxf(ellipse(x, y + 2, 24, 30), y - 14);
        float rim = box(x, y - 16, 30, 4, 4), clapper = circle(x, y, 0, 26, 6);
        return fminf(fminf(dome, rim), clapper);
    }
    case ICON_MUSIC: { /* clean flat rounded double eighth-note (tilted heads, rounded stems & angled beam) */
        const float c18 = 0.95106f, s18 = 0.30902f; /* -18 deg musical head slant */
        float heads = fminf(rot_ellipse(x, y, -18.0f, 23.0f, 11.5f, 8.8f, c18, -s18),
                            rot_ellipse(x, y, 16.0f, 16.0f, 11.5f, 8.8f, c18, -s18));
        float stems = fminf(segment(x, y, -9.5f, 20.5f, -9.5f, -22.5f, 4.2f),
                            segment(x, y, 24.5f, 13.5f, 24.5f, -29.5f, 4.2f));
        float beam = segment(x, y, -9.5f, -22.5f, 24.5f, -29.5f, 5.6f);
        return fminf(fminf(heads, stems), beam);
    }
    case ICON_CAMERA: {
        float body = box(x, y - 4, 34, 22, 6), top = box(x + 4, y + 22, 12, 6, 2);
        float lens = ring(x, y - 4, 13, 4);
        return fmaxf(fminf(body, top), -(hypotf(x, y - 4) - 17)) < lens ? fmaxf(fminf(body, top), -(hypotf(x, y - 4) - 17)) : lens;
    }
    case ICON_THEME: { /* a palette: a ring of paint dots */
        float d = ring(x, y, 36, 4);
        for (int i = 0; i < 4; i++) {
            float a = i * 1.5708f + 0.785f;
            d = fminf(d, circle(x, y, cosf(a) * 17, sinf(a) * 17, 8.5f));
        }
        return d;
    }
    case ICON_BADGE: { /* a name tag on a lanyard (y down): slot on top, a person, a name line */
        float tag = box(x, y - 8, 30, 38, 7);
        float slot = box(x, y + 22, 9, 2.5f, 2);
        float person = fminf(circle(x, y, 0, 0, 8.5f), fmaxf(ellipse(x, y - 21, 16, 9), y - 21));
        float name = box(x, y - 33, 15, 3.2f, 1.6f);
        float strap = fminf(segment(x, y, -8, -27, -20, -48, 3), segment(x, y, 8, -27, 20, -48, 3));
        return fminf(fmaxf(tag, -fminf(fminf(slot, person), name)), strap);
    }
    case ICON_XO: { /* a cross and a nought */
        float cross = fminf(segment(x, y, -38, -14, -10, 14, 5), segment(x, y, -38, 14, -10, -14, 5));
        return fminf(cross, ring(x - 24, y, 14, 5));
    }
    case ICON_EIGHT: { /* a ball with its window and an 8 in it */
        float ball = hypotf(x, y) - 38, window = hypotf(x, y + 6) - 18;
        float eight = fminf(ring(x, y + 12, 5.5f, 2.6f), ring(x, y, 7, 2.6f));
        return fminf(fmaxf(ball, -window), eight);
    }
    case ICON_COIN: { /* a coin: a rim and a one */
        float rim = ring(x, y, 34, 5);
        float one = fminf(box(x, y, 3.5f, 18, 1.5f), segment(x, y, 0, -18, -9, -10, 3.5f));
        return fminf(rim, one);
    }
    case ICON_DICE: { /* a die showing three */
        float body = box(x, y, 34, 34, 9);
        float pips = fminf(hypotf(x + 17, y + 17) - 7, fminf(hypotf(x, y) - 7, hypotf(x - 17, y - 17) - 7));
        return fmaxf(body, -pips);
    }
    case ICON_MAZE: { /* two square rings, each with a way through (top, then bottom), and the goal in the middle */
        float outer = fmaxf(fabsf(box(x, y, 36, 36, 6)) - 4, -box(x, y + 36, 9, 9, 0));
        float inner = fmaxf(fabsf(box(x, y, 19, 19, 4)) - 4, -box(x, y - 19, 7, 9, 0));
        return fminf(fminf(outer, inner), hypotf(x, y) - 6);
    }
    case ICON_REMOTE: { /* a presenter: a slim body with two buttons, three rays from its tip */
        float body = fmaxf(box(x, y - 16, 17, 27, 15), -fminf(hypotf(x, y - 6) - 6.5f, hypotf(x, y - 26) - 6.5f));
        float rays = fminf(segment(x, y, 0, -22, 0, -40, 4), fminf(segment(x, y, -10, -20, -24, -34, 4), segment(x, y, 10, -20, 24, -34, 4)));
        return fminf(body, rays);
    }
    case ICON_BT: { /* the Bluetooth rune, one stroke */
        static const float p[6][2] = {{-17, -14}, {17, 16}, {0, 32}, {0, -32}, {17, -16}, {-17, 14}};
        float d = 1e9f;
        for (int i = 0; i < 5; i++) d = fminf(d, segment(x, y, p[i][0] * 1.1f, p[i][1] * 1.1f, p[i + 1][0] * 1.1f, p[i + 1][1] * 1.1f, 4.5f));
        return d;
    }
    case ICON_NOISE: { /* a sound wave as five level bars */
        static const float hs[5] = {10, 22, 34, 24, 14};
        float d = 1e9f;
        for (int i = 0; i < 5; i++) d = fminf(d, box(x - (i - 2) * 16.0f, y, 4.5f, hs[i], 4.5f));
        return d;
    }
    case ICON_INFO: { /* clean flat circle with 'i' */
        float ring = fabsf(hypotf(x, y) - 34.0f) - 4.5f;
        float stem = box(x, y - 9.0f, 4.5f, 14.0f, 4.5f);
        float dot = hypotf(x, y + 16.5f) - 5.2f;
        return fminf(ring, fminf(stem, dot));
    }
    }
    return 1e9f;
}

void doodle_icon_mask(int icon, uint8_t *a8, int stride, int size)
{
    float k = 100.0f / size;
    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++)
            a8[y * stride + x] = (uint8_t)(255 * clamp01(0.5f - glyph(icon, (x + 0.5f - size * 0.5f) * k, (y + 0.5f - size * 0.5f) * k) / k));
}

/* Flat tilted Pixel mini eyes for the minimalist Badge (exact 1:1 match with web Digital Twin) */
void doodle_mini_eyes(uint32_t *px, int w, int h, uint32_t sclera, uint32_t pupil, uint32_t stroke, bool slim_pupil)
{
    memset(px, 0, (size_t)w * h * 4);
    const float c13 = 0.97437f, s13 = 0.22495f; /* 13 deg */
    const float c7 = 0.99255f, s7 = 0.12187f;   /* 7 deg */
    const float prx = slim_pupil ? 8.4f : 12.0f, pry = slim_pupil ? 17.4f : 24.6f;
    for (int y = 0; y < h; y++)
        for (int x = 0; x < w; x++) {
            float fx = x + 0.5f - w * 0.5f, fy = y + 0.5f - h * 0.5f;
            float dl = rot_ellipse(fx, fy, -24.6f, 0.0f, 21.0f, 28.2f, c13, -s13);
            float dr = rot_ellipse(fx, fy, 24.6f, 0.0f, 21.0f, 28.2f, c13, s13);
            float d = fminf(dl, dr);
            if (d > 2.5f) continue;
            uint32_t *p = &px[y * w + x];
            float cov = clamp01(0.5f - d);
            over(p, 0xFF000000u | sclera, cov);
            if (cov > 0.01f) {
                float pl = rot_ellipse(fx, fy, -22.8f, 0.6f, prx, pry, c7, -s7);
                float pr = rot_ellipse(fx, fy, 22.8f, 0.6f, prx, pry, c7, s7);
                over(p, 0xFF000000u | pupil, clamp01(0.5f - fminf(pl, pr)) * cov);
            }
            if (stroke) {
                float rim = clamp01(0.5f - (fabsf(d + 0.9f) - 1.0f));
                over(p, 0xFF000000u | stroke, rim);
            }
        }
}

/* color: the disc (glass) or the cell panel (blocks); ink: the symbol (outline, blocks); line: the outline ring */
void doodle_icon(int icon, int style, uint32_t color, uint32_t ink, uint32_t line, uint32_t *px, int w, int h)
{
    memset(px, 0, (size_t)w * h * 4);
    float r = fminf(w, h) * 0.5f - 1, k = 100.0f / (2 * r * 0.78f); /* symbol spans ~78% of the disc */
    uint32_t dark = 0xFF000000u | (((color >> 16 & 255) * 3 / 4) << 16) | (((color >> 8 & 255) * 3 / 4) << 8) | ((color & 255) * 3 / 4);
    const float cell = 10; /* blocks: mosaic pitch, px */
    for (int y = 0; y < h; y++)
        for (int x = 0; x < w; x++) {
            float dx = x + 0.5f - w * 0.5f, dy = y + 0.5f - h * 0.5f;
            uint32_t *p = &px[y * w + x];
            float disc = hypotf(dx, dy) - r;
            if (style == ICON_STYLE_GLASS) {
                over(p, dark, clamp01(0.5f - disc));
                over(p, 0xFF000000u | color, clamp01(0.5f - disc) * clamp01((-dy + r * 0.2f) / (r * 0.9f) + 0.5f)); /* lit from the top */
                float gloss = ellipse(dx, dy + r * 0.6f, r * 0.5f, r * 0.22f);                                /* soft specular sheen */
                over(p, 0xFFFFFFFF, 0.10f * clamp01(0.5f - gloss / 10) * clamp01(0.5f - disc));
                over(p, 0xFFFFFFFF, 0.30f * clamp01(1.2f - fabsf(disc + 1.5f)) * clamp01(-dy / r + 0.1f));      /* thin bright rim on top */
                over(p, 0xFFFFFFFF, clamp01(0.5f - glyph(icon, dx * k, dy * k) / k));
            } else if (style == ICON_STYLE_FLAT) { /* flat matte circle + crisp solid symbol (Pixel theme) */
                over(p, 0xFF000000u | color, clamp01(0.5f - disc));
                over(p, 0xFF000000u | ink, clamp01(0.5f - glyph(icon, dx * k, dy * k) / k));
            } else if (style == ICON_STYLE_OUTLINE) { /* thin lines: the ring and the symbol's outline */
                over(p, 0xFF000000u | line, clamp01(1.0f - fabsf(disc + 1.5f)));
                over(p, 0xFF000000u | ink, clamp01(1.4f - fabsf(glyph(icon, dx * k, dy * k) / k)));
            } else { /* blocks: a square panel, the symbol sampled on a grid of cells */
                float half = r * 0.86f;
                if (fabsf(dx) > half || fabsf(dy) > half) continue;
                over(p, 0xFF000000u | color, 1);
                float gx = (floorf(dx / cell) + 0.5f) * cell, gy = (floorf(dy / cell) + 0.5f) * cell;
                bool inside = fabsf(dx - gx) < cell * 0.4f && fabsf(dy - gy) < cell * 0.4f;
                if (inside && glyph(icon, gx * k, gy * k) < 0) over(p, 0xFF000000u | ink, 1);
            }
        }
}

/* ---------- neutral QR link badge ---------- */

/* Neutral chain-link symbol for QR codes (no third-party brand marks) */
static float link_glyph(float fx, float fy, float k)
{
    float u = (fx + fy) * 0.7071068f, v = (-fx + fy) * 0.7071068f;
    float left = fmaxf(fabsf(box(u + 11.5f * k, v, 10.5f * k, 7.8f * k, 7.8f * k)) - 2.8f * k, u + 3.8f * k);
    float right = fmaxf(fabsf(box(u - 11.5f * k, v, 10.5f * k, 7.8f * k, 7.8f * k)) - 2.8f * k, -(u - 3.8f * k));
    float bar = box(u, v, 8.8f * k, 2.7f * k, 2.7f * k);
    return fminf(fminf(left, right), bar);
}

void doodle_brand(int brand, uint32_t *px, int stride, int x0, int y0, int size)
{
    if (!brand) return;
    float r = size * 0.5f, k = 100.0f / size; /* draw in a 100-unit box */
    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++) {
            uint32_t *p = &px[(y0 + y) * stride + x0 + x];
            float fx = (x + 0.5f - r) * k, fy = (y + 0.5f - r) * k, aa = 1 / k;
            over(p, 0xFFFFFFFF, clamp01(0.5f - (hypotf(fx, fy) - 50) / k)); /* white halo keeps the code readable */
            over(p, 0xFF1E2428, clamp01(0.5f - (hypotf(fx, fy) - 41) * aa));
            over(p, 0xFFFFFFFF, clamp01(0.5f - link_glyph(fx, fy, 1.0f) * aa));
        }
}

void doodle_brand_ink(int brand, uint32_t *px, int stride, int x0, int y0, int size, uint32_t ink, uint32_t paper)
{
    if (!brand) return;
    float r = size * 0.5f, k = 100.0f / size;
    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++) {
            uint32_t *p = &px[(y0 + y) * stride + x0 + x];
            *p = paper; /* a clear square: no modules run into the mark */
            float fx = (x + 0.5f - r) * k, fy = (y + 0.5f - r) * k, aa = 1 / k;
            over(p, ink, clamp01(0.5f - link_glyph(fx, fy, 1.35f) * aa));
        }
}
