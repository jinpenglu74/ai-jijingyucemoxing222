#ifndef REPLAY_LOGIC_H
#define REPLAY_LOGIC_H
#include "core.h"

/* Fixed-width ISO-like timestamps used by the app compare lexicographically.
   Empty/malformed values are treated as unavailable. */
int replay_time_text_leq(const u16* available_time,const u16* replay_time);
int replay_date_available(int available_yyyymmdd,int replay_yyyymmdd);

#endif
