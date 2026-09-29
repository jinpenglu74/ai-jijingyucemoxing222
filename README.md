# AI基金预测 V0.7 — AI经验闭环基础版

Windows x64 免安装基金预测工具。继续使用既有持久化目录：`D:\\AI基金预测\\`。

## V0.7 新增

- AI经验库：`data\\experience_store_v1.bin`
- AI复盘通过质量门控后自动提取经验
- 同规则经验按 reusable_rule 指纹合并，避免重复污染
- 经验评分与 ACTIVE / OBSERVE / RETIRED 状态
- 预测前最多召回 5 条同基金或同类型高质量经验
- DeepSeek Prompt 版本升级为 2，明确历史经验只能作为参考，不能覆盖当前 Snapshot 事实
- 左侧“经验库”页面正式启用
- 日志新增：`EXPERIENCE_EXTRACT`、`EXPERIENCE_SAVE`、`EXPERIENCE_INJECT`

## 经验质量门控

以下复盘不会进入有效经验库：

- 冻结 Snapshot 缺失
- 幸运命中
- reasoning_quality = UNSUPPORTED
- evidence_score < 55
- review_confidence < 55
- D级复盘

## 完整主链

真实数据 → Quant → Data Gate → World Snapshot → DeepSeek六周期预测 → 预测档案 → 自动判卷 → AI复盘 → 经验提取 → 下一次预测召回。

## 构建

仓库保留 GitHub Actions 构建工作流：`.github/workflows/build-windows-exe.yml`。
当前源码基线为 V0.6 ZIP + `v0.7/` overlay；`v0.7/apply_v07.py` 会在构建时生成完整 V0.7 源码。

> AI输出仅用于研究与预测复盘，不构成投资建议。
