# ChemCrow 公开仓库阶段性复现说明

## 1. 说明定位

本文用于汇总截至 `2026-03-14` 的阶段性复现结果。说明范围限定为 `ChemCrow` 公开仓库版本。说明内容仅覆盖已有证据直接支持的结论。

## 2. 复现对象

- 复现对象：`ChemCrow` 公开仓库版本
- 仓库路径：`/root/autodl-tmp/chemcrow-public-main`
- 官方版本锚点：`e7ebd5193334ac1d8dea137b635721c7cb470d33`
- 官方最近提交时间：`2024-12-19 18:47:03 +0100`
- 官方最近提交摘要：`Merge pull request #52 from ur-whitelab/local-rxn`

版本锚点证据：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/00_baseline.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/diffs/2026-03-14_original_zip_vs_official_head.diff`

## 3. 执行边界

- 当前结论仅对应公开仓库版本。
- 当前结论仅对应 `Qwen` 固定快照与当前可获得外部服务条件。
- 论文完整系统相关结论未纳入本文。

边界依据：

- `/root/autodl-tmp/chemcrow_reproduction_plan.md`
- `/root/autodl-tmp/instructions.md`

## 4. 当前运行条件

- Python：`3.10`
- 独立环境：`chemcrow-repro`
- 主模型：`qwen3.5-plus-2026-02-15`
- 工具模型：`qwen3.5-plus-2026-02-15`
- 摘要模型：`qwen3.5-plus-2026-02-15`
- `Qwen` 接口形式：`OpenAI-compatible`

环境与配置记录：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/env_setup.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_freeze_2026-03-14.txt`

## 5. 改动分类

### 5.1 主线最小兼容补丁

已完成并有记录的主线最小兼容补丁包括：

- `Qwen` 模型兼容入口
- `RXN4CHEM_PROJECT_ID` 参数化
- 摘要模型参数化
- 文献工具链可选依赖容错

记录文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_001_compatibility_patch.md`

### 5.2 次级兼容补丁

已完成并单独标记的次级兼容补丁包括：

- `PubChem` 返回结构漂移兼容
- `PatentCheck` 的 `SureChEMBL` 官方 API 回退
- `RXN` node 动作提取节奏兼容
- `Wikipedia` 与 `LiteratureSearch` 的工具级容错

记录文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_002_rxn_compatibility_patch.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_004_rxn_retro_stabilization.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_005_search_tool_hardening.md`

## 6. 已验证能力

### 6.1 外部服务最小连通性

已完成直接验证的外部服务如下：

- `Qwen`
- `RXN4Chem` 项目绑定
- `Serp`

证据文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_qwen_chat.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_auth.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_serp_search.out`

### 6.2 工具级能力

已形成直接证据的工具级能力如下：

- 名称转 `SMILES`
- `CAS` 查询
- 爆炸性判定
- 受控化学品判定
- `WebSearch`
- `ReactionPredict`
- `ReactionRetrosynthesis`
- `PatentCheck`

证据文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/2026-03-14_test_matrix.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_websearch_tool.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_predict_tool.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_predict_tool_new.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_retro_tool.out`

### 6.3 agent 级能力

已形成直接证据的 agent 级能力如下：

- 基础问答
- 受控化学品与爆炸性联合判断
- 正向反应预测
- 专利与分子性质联合查询
- 网页信息与受控化学品联合查询

证据文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_basic_qa.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_control_agent.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_reactionpredict_agent.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_patent_agent.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_web_control_agent.out`

## 7. 逆合成功能的当前结论

`ReactionRetrosynthesis` 已在新一轮 `RXN` 配置下形成成功证据。

当前成功证据包含：

- `prediction_id` 非空
- `path_count = 6`
- 输出为非空合成步骤文本
- 运行结果中的 `error = null`

证据文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_retro_tool.out`

当前边界如下：

- 旧一轮 `RXN` 配置曾出现配额边界约束。
- 新一轮 `RXN` 配置已恢复成功样例。
- 当前链路仍存在轻度服务端波动，主要表现为空响应与 `429`。

边界证据：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_retro_http_probe.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_retro_tool.out`

## 8. 专利检查分歧的当前解释

仓库测试中的 `cumene` 样例与 `2026-03-14` 当前 `SureChEMBL` 官方数据存在时间快照分歧。

当前可直接支持的事实包括：

- `caffeine` 的 exact structure 命中与专利文档命中均存在
- `choline_like_testcase` 的 exact structure 命中不存在
- `cumene` 的 exact structure 命中存在
- `cumene` 的至少一个 exact `chemical_id` 当前可返回大量专利文档

当前最稳妥结论：

- 当前条件下，`cumene` 不宜写成 `Novel`
- 该分歧更符合外部专利语料状态变化或上游索引演化

证据文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/patentcheck_discrepancy_2026-03-14.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/investigate_patentcheck_discrepancy.out`

## 9. 当前受限项

当前仍处于受限状态的内容如下：

- `ChemSpace` 相关链路
- 依赖 `SEMANTIC_SCHOLAR_API_KEY` 的完整文献检索链路
- 默认 agent 路由中对 `Wikipedia` 与 `LiteratureSearch` 的外部依赖稳定性

当前已完成的受限处理如下：

- `Wikipedia` 异常已收敛为工具级失败输出
- `LiteratureSearch` 在无 `SEMANTIC_SCHOLAR_API_KEY` 条件下已收敛为工具级失败输出
- 上述两类失败当前不会直接中断整条 agent 链路

证据文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_web_control_agent.out`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_005_search_tool_hardening.md`

## 10. 当前可支持的阶段性表述

当前证据支持如下表述：

- `ChemCrow` 公开仓库版本已在当前环境中完成条件受限、可追溯的兼容性复现。
- `Qwen` 固定快照 `qwen3.5-plus-2026-02-15` 已在公开仓库调用路径下稳定接入。
- 基础问答、`WebSearch`、`ReactionPredict`、`ReactionRetrosynthesis` 已形成直接成功证据。
- agent 已形成多步工具调用证据，覆盖基础问答、受控化学品判断、正向反应预测、专利与性质联合查询、网页信息与受控化学品联合查询。
- `PatentCheck` 的剩余测试分歧与当前 `SureChEMBL` 官方数据状态存在时间快照差异。

## 11. 当前不宜采用的表述

当前证据范围之外的表述包括：

- 论文完整系统已复现
- 公开仓库全部功能已无差异恢复
- `ReactionRetrosynthesis` 在所有时间点均稳定无波动
- `PatentCheck` 已与仓库历史测试完全一致
- `Qwen` 与原始 `GPT` 配置行为完全等价

## 12. 证据索引

- 基线记录：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/00_baseline.md`
- 环境记录：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/env_setup.md`
- 当前状态：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/01_current_status.md`
- 测试矩阵：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/2026-03-14_test_matrix.md`
- 改动记录：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_001_compatibility_patch.md`
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_002_rxn_compatibility_patch.md`
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_003_rxn_credentials_rotation.md`
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_004_rxn_retro_stabilization.md`
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_005_search_tool_hardening.md`
