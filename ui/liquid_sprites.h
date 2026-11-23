/* Pre-baked Liquid eye sprites stored in Flash (.rodata), drawn by LVGL without per-frame gradient math. */
#pragma once
#include "lvgl.h"

#define LIQ_PALETTES 6
#define LIQ_SCLERA_W 148
#define LIQ_SCLERA_H 172
#define LIQ_SCLERA_RX 64
#define LIQ_SCLERA_RY 76
#define LIQ_PUPIL_W 76
#define LIQ_PUPIL_H 100
#define LIQ_PUPIL_RX 26
#define LIQ_PUPIL_RY 38
#define LIQ_SPEC_W 76
#define LIQ_SPEC_H 64
#define LIQ_HEART_W 88
#define LIQ_HEART_H 84
#define LIQ_BLUSH_W 104
#define LIQ_BLUSH_H 42
#define LIQ_LID_W 240
#define LIQ_LID_H 216
#define LIQ_LID_EDGE_Y 182
#define LIQ_SMILE_W 240
#define LIQ_SMILE_H 152
#define LIQ_SMILE_EDGE_Y 28
#define LIQ_FLASH_BYTES 714736

extern const lv_image_dsc_t *const liquid_sclera[LIQ_PALETTES];
extern const lv_image_dsc_t *const liquid_pupil[LIQ_PALETTES];
extern const lv_image_dsc_t liq_specular;
extern const lv_image_dsc_t liq_heart;
extern const lv_image_dsc_t liq_blush;
extern const lv_image_dsc_t liq_lid;
extern const lv_image_dsc_t liq_smile;
