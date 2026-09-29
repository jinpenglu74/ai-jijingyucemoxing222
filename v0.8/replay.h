#ifndef REPLAY_H
#define REPLAY_H
#include "archive.h"

#define REPLAY_STATUS_OK 1
#define REPLAY_STATUS_MODEL_FAIL 2
#define REPLAY_STATUS_SNAPSHOT_MISSING 3
#define REPLAY_STATUS_NO_KEY 4
#define REPLAY_STATUS_NO_CANDIDATE 5

typedef struct ReplayAuditRecord {
    u16 source_prediction_id[ARCHIVE_ID_CAP];
    u16 replay_prediction_id[ARCHIVE_ID_CAP];
    u16 fund_code[FUND_CODE_CAP];
    u16 fund_name[FUND_NAME_CAP];
    u16 replay_time[FUND_TIME_CAP];
    u16 run_time[FUND_TIME_CAP];
    int status;
    int snapshot_guard_passed;
    int experience_cutoff_guard_passed;
    int production_experiences_used;
    int replay_experiences_used;
    int future_experiences_filtered;
    int outcome_revealed_after_prediction;
    int horizons_graded;
    int horizons_correct;
    int ranges_hit;
    int reviews_created;
    int candidate_experiences_created;
} ReplayAuditRecord;

typedef struct ReplayStats {
    int source_predictions;
    int source_judgments;
    int replayed_sources;
    int replay_judgments;
    int replay_direction_correct;
    int replay_range_hit;
    int replay_reviews;
    int candidate_experiences;
    int audit_runs;
    int future_experiences_filtered;
    int snapshot_blocked;
} ReplayStats;

/* Runs exactly one oldest eligible archived snapshot. The model is called before
   any realized outcome is read into the replay pipeline. Returns 1 on success,
   0 when no eligible case exists, negative on an execution failure. */
int replay_run_next(const StorageContext* production,ReplayAuditRecord* out_audit);
int replay_get_stats(const StorageContext* production,ReplayStats* out);
void replay_make_storage(const StorageContext* production,StorageContext* replay);

#endif
