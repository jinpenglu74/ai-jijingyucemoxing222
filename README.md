# AI基金预测 V0.6 — AI复盘基础版

Windows x64 免安装版本。继续使用现有持久化目录：`D:\AI基金预测\`（D盘不可用时回退 C 盘）。

## V0.6 新增

### 1. AI复盘正式接入
当某个预测周期已经完成“自动判卷”后，V0.6 会自动进入 AI 复盘：

预测档案 → 实际净值判卷 → 冻结预测时 Snapshot → DeepSeek 结构化复盘 → A/B/C/D 等级

复盘不会读取或保存隐藏思维链，只保存结构化结论：
- reasoning_quality：SUPPORTED / PARTIAL / UNSUPPORTED
- evidence_score：0–100
- review_confidence：0–100
- summary
- supported / weak / missed
- lesson
- reusable_rule

### 2. A/B/C/D 由程序确定
DeepSeek 负责评估“推理质量”，最终等级由程序按固定规则计算：
- A：结果正确 + 推理成立
- B：结果正确 + 推理部分成立/不足
- C：结果错误 + 推理仍有部分或较强依据
- D：结果错误 + 推理不足

“幸运命中”只在结果正确但推理被判定为 UNSUPPORTED 时标记，不会把所有 B 级都当成幸运命中。

### 3. 复盘证据边界
V0.6 只使用：
- 预测时冻结的 World Snapshot
- 当时六周期预测概率 / 区间 / 理由
- 实际 NAV 与自动判卷结果

当前尚未接入完整“事后新闻/宏观事件时间线”，因此 AI 被明确禁止虚构新闻、政策或宏观因果。UI 也会明确提示此证据范围。

### 4. 不重复复盘
复盘唯一键：`Prediction ID + Horizon`。
同一判卷只会生成一份正式复盘，后续同步直接跳过。

### 5. 新增持久化文件
`D:\AI基金预测\data\reviews_v1.bin`

原有文件保持：
- `prediction_archive_v1.bin`
- `judgments_v1.bin`
- `funds.bin`
- snapshots / logs / cache 等

Fund Store Schema 仍为 v6，不破坏 V0.4.4 / V0.5 的现有基金数据和 DeepSeek Key。

## UI
左侧“AI复盘”页面已从占位页变为正式页面，可查看：
- 已复盘
- 待复盘
- A / B / C / D 分布
- 最近复盘
- 实际收益
- 推理评价
- 复盘总结与教训

## 关键日志
无成熟判卷时：
`[AI_REVIEW_QUEUE] judgments=0 pending=0 existing=0`

有待复盘判卷时会看到：
`[AI_REVIEW_REQUEST]`
`[AI_REVIEW_API]`
`[AI_REVIEW_JSON]`
`[AI_REVIEW] APPENDED ... grade=A/B/C/D ...`

## 注意
AI 输出仅用于研究与预测复盘，不构成投资建议。
