# AI基金预测 V0.8.1 — 历史证据扩展 + 候选经验晋级版

V0.8.1 的目标不是伪造更多历史数据，而是把软件**已经真实冻结过的历史证据利用率提高**，并给 replay 候选经验增加正式晋级门槛。

## 这版做什么

- 新增 `history_evidence_v1.bin`：扫描并索引过去保存的全部不可变 World Snapshot。
- 历史重演不再只依赖“当时已经产生过正式预测档案”的 Snapshot。
- 缓存命中等情况下虽然没有新预测档案，但只要当时 Snapshot 真实存在、后续 NAV 已成熟，也可以成为额外训练案例。
- 继续保持：模型预测 JSON 校验通过以前，不读取未来真实结果。
- replay 候选经验只有满足以下条件才允许晋级正式经验库：
  - ACTIVE
  - score >= 75
  - verified_count >= 3
  - evidence_score >= 65
  - review_confidence >= 65
  - unresolved_conflicts = 0
- 新增 `experience_promotion_v1.bin` 保存候选经验晋级审计。
- 晋级正式经验时，把 `created_time` / `last_verified_time` 重置为真实晋级时间，防止未来经验泄漏回过去。

## 为什么做

V0.8 已经能历史重演，但样本来源主要是过去真正形成过预测档案的 Snapshot。V0.8.1 开始利用“真实存在但未形成新预测档案”的历史 Snapshot，提高已有证据的训练利用率；同时阻止未经重复验证的 replay 经验直接污染线上预测。

## 仍然没有做

本版不会凭空补造 2023/2024 等从未采集过的历史持仓、新闻、政策或宏观事件。真正多年历史训练仍需要后续接入带 published_at / known_at 的真实历史证据源。

## 下一版

V0.9：历史证据导入规范 + 训练批次调度 + challenger/production 策略对比基础层。

> 本软件用于概率研究、预测记录和复盘，不构成投资建议。
