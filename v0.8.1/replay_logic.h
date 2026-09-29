#ifndef REPLAY_LOGIC_H
#define REPLAY_LOGIC_H
#include "core.h"
int replay_time_text_leq(const u16* available_time,const u16* replay_time);
int replay_date_available(int available_yyyymmdd,int replay_yyyymmdd);
int replay_promotion_eligible(int status,int score,int verified_count,int evidence_score,int review_confidence,int unresolved_conflicts);
#endif
