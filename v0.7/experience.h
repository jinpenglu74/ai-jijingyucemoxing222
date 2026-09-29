#ifndef EXPERIENCE_H
#define EXPERIENCE_H
#include "review.h"

#define EXPERIENCE_TEXT_CAP 224
#define EXPERIENCE_TYPE_SUCCESS 1
#define EXPERIENCE_TYPE_FAILURE 2
#define EXPERIENCE_TYPE_CAUTION 3
#define EXPERIENCE_STATUS_ACTIVE 1
#define EXPERIENCE_STATUS_OBSERVE 2
#define EXPERIENCE_STATUS_RETIRED 3
#define EXPERIENCE_LOAD_MAX 128
#define EXPERIENCE_INJECT_MAX 5

typedef struct ExperienceRecord {
    u64 rule_hash;
    u16 experience_id[ARCHIVE_ID_CAP];
    u16 source_prediction_id[ARCHIVE_ID_CAP];
    u16 fund_code[FUND_CODE_CAP];
    u16 fund_name[FUND_NAME_CAP];
    u16 fund_type[FUND_META_CAP];
    int source_horizon;
    int source_grade;
    int experience_type;
    int status;
    int score;
    int evidence_score;
    int review_confidence;
    int verified_count;
    int usage_count;
    u16 created_time[FUND_TIME_CAP];
    u16 last_verified_time[FUND_TIME_CAP];
    u16 lesson[EXPERIENCE_TEXT_CAP];
    u16 reusable_rule[EXPERIENCE_TEXT_CAP];
} ExperienceRecord;

typedef struct ExperienceStats {
    int total_count;
    int active_count;
    int observe_count;
    int retired_count;
    int success_count;
    int failure_count;
} ExperienceStats;

int experience_sync_reviews(const StorageContext* st,const FundStore* store,int* scanned_reviews,int* created,int* merged,int* rejected);
int experience_load_latest(const StorageContext* st,ExperienceRecord* out,int max_records);
int experience_search(const StorageContext* st,const FundRecord* fund,ExperienceRecord* out,int max_records);
int experience_get_stats(const StorageContext* st,ExperienceStats* out);
int experience_build_context_utf8(const StorageContext* st,const FundRecord* fund,char* out,int cap,int* used);
const WCHAR* experience_type_name(int type);
const WCHAR* experience_status_name(int status);

#endif
