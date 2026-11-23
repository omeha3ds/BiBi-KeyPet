/* Pre-baked Liquid eye sprites stored in Flash (.rodata), drawn by LVGL without per-frame gradient math. */
#pragma once
#include "lvgl.h"

#define LIQ_PALETTES 6
#define LIQ_SCLERA_W 152
#define LIQ_SCLERA_H 198
#define LIQ_SCLERA_RX 66
#define LIQ_SCLERA_RY 88
#define LIQ_PUPIL_W 84
#define LIQ_PUPIL_H 132
#define LIQ_PUPIL_RX 30
#define LIQ_PUPIL_RY 54
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
#define LIQ_WET_W 136
#define LIQ_WET_H 52
#define LIQ_VEINS_W 128
#define LIQ_VEINS_H 172
#define LIQ_VEINS_RX 62
#define LIQ_VEINS_RY 83
#define LIQ_FLASH_BYTES 904272

extern const lv_image_dsc_t *const liquid_sclera[LIQ_PALETTES];
extern const lv_image_dsc_t *const liquid_pupil[LIQ_PALETTES];
extern const lv_image_dsc_t liq_specular;
extern const lv_image_dsc_t liq_heart;
extern const lv_image_dsc_t liq_blush;
extern const lv_image_dsc_t liq_lid;
extern const lv_image_dsc_t liq_smile;
extern const lv_image_dsc_t liq_wet;
extern const lv_image_dsc_t liq_veins;
