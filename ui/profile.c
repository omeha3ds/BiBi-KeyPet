#include "profile.h"
#include "doodle.h"
#include <string.h>

/* defaults until configured from the panel: clean Ukrainian name and empty QR list */
profile_t profile = {
    .first = "Твоє",
    .last = "Ім'я",
    .org = "",
};
int profile_rev = 1;
static void (*on_change)(void);

int profile_links(void)
{
    int n = 0;
    for (int i = 0; i < PROFILE_LINKS; i++) n += profile.link[i].url[0] != 0;
    return n;
}

const profile_link_t *profile_link(int i)
{
    for (int k = 0; k < PROFILE_LINKS; k++)
        if (profile.link[k].url[0] && i-- == 0) return &profile.link[k];
    return &profile.link[0];
}

int profile_brand(const char *url)
{
    return url && url[0] ? BRAND_LINK : BRAND_NONE;
}

void profile_changed(void)
{
    profile_rev++;
    if (on_change) on_change();
}

void profile_on_change(void (*cb)(void)) { on_change = cb; }
