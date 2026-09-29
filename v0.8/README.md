# AI基金预测 V0.8 — 历史重演 / AI训练场版

V0.8 的核心目标：让预测系统开始用**真实冻结过的历史 World Snapshot**重新做预测，并在预测完成后才揭晓真实净值结果，构建可审计的历史训练闭环。

## 这版做什么

- 左侧“历史重演”页面正式启用。
- 每次点击“运行下一历史重演”只运行 1 个历史案例，避免无意产生大量 API 消耗。
- 只允许重演已经存在不可变 Snapshot 且至少有一个成熟判卷结果的历史预测。
- DeepSeek 调用前只加载历史冻结 Snapshot 与当时已经可用的经验。
- 模型六周期 JSON 校验通过后，才读取历史真实 NAV 进行自动判卷。
- 自动进入独立的 replay AI复盘。
- 自动形成独立的 replay 候选经验，不直接污染线上正式经验库。

## 防未来泄漏

硬规则：
1. `known_at <= replay_time`
2. `experience_available_from <= replay_time`

没有历史 Snapshot 的日期直接阻断，绝不使用当前数据伪造过去。历史真实结果不会进入模型请求。

## replay 独立数据

- `data\replay_prediction_archive_v1.bin`
- `data\replay_judgments_v1.bin`
- `data\replay_reviews_v1.bin`
- `data\replay_experience_candidates_v1.bin`
- `data\replay_experience_usage_v1.bin`
- `data\replay_experience_conflict_v1.bin`
- `data\replay_experience_baseline_v1.bin`
- `data\replay_audit_v1.bin`

所有历史训练数据与正式线上 prediction/judgment/review/experience 隔离。

## 当前边界

V0.8 不伪造多年历史证据。当前只能重演本软件过去真正冻结过的 Snapshot。更久历史需要下一阶段接入带时间戳的历史持仓、市场、宏观/新闻证据归档。

## 下一版

V0.8.1：历史证据扩展 + replay候选经验验证晋级。

> 本软件只做概率研究、预测记录与复盘，不构成投资建议。
