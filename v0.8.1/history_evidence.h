#ifndef HISTORY_EVIDENCE_H
#define HISTORY_EVIDENCE_H
#include "archive.h"
#include "snapshot.h"
#define HISTORY_EVIDENCE_ID_CAP 112
#define HISTORY_EVIDENCE_LOAD_MAX 4096
typedef struct HistoryEvidenceRecord {
    u16 evidence_id[HISTORY_EVIDENCE_ID_CAP];
    u16 fund_code[FUND_CODE_CAP];
    u16 fund_name[FUND_NAME_CAP];
    u16 replay_time[FUND_TIME_CAP];
    u16 snapshot_id[SNAPSHOT_ID_CAP];
    int base_nav_x10000;
    int base_nav_date;
    int data_completeness;
    int data_confidence;
    int matured_horizons;
    int has_prediction_source;
    int eligible;
} HistoryEvidenceRecord;
typedef struct HistoryEvidenceStats {
    int total_snapshots;
    int indexed_snapshots;
    int eligible_snapshots;
    int extra_replay_candidates;
    int prediction_backed_snapshots;
} HistoryEvidenceStats;
int history_evidence_refresh(const StorageContext* st,HistoryEvidenceStats* out);
int history_evidence_load(const StorageContext* st,HistoryEvidenceRecord* out,int max_records);
int history_evidence_get_stats(const StorageContext* st,HistoryEvidenceStats* out);
void history_evidence_make_source_id(const u16* snapshot_id,u16* out,int cap);
int history_evidence_parse_snapshot_time(const u16* snapshot_id,u16* out,int cap);
#endif
