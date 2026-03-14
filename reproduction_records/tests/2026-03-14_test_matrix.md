# 2026-03-14 测试矩阵

## 1. 记录目标

本记录用于给出当前公开仓库兼容复现的功能级证据矩阵，明确哪些能力已经通过固定输入验证，哪些能力仍受限。

## 2. 运行前提

- conda 环境：`chemcrow-repro`
- 代码状态：已应用 `CHANGE_001` 至 `CHANGE_005`
- 运行脚本时通过 `.env` 注入 `OPENAI`、`RXN4CHEM`、`SERP` 运行时配置

## 3. 声明与验收标准

### 3.1 声明 A

- 声明：公开仓库中的本地可测工具链已经恢复到可导入、可执行、可返回非空结果的状态。
- 验收标准：固定输入下，名称转 SMILES、爆炸性判定、受控化学品判定、专利检查的核心调用不再因导入或解析错误失败。

### 3.2 声明 B

- 声明：面向 OpenAI-compatible 接口的模型兼容层已经建立。
- 验收标准：`qwen-*` 模型名可以通过构造链路；`OPENAI_API_BASE`、`RXN4CHEM_PROJECT_ID` 与摘要模型配置可以进入对应对象。

### 3.3 声明 C

- 声明：当前版本的公开仓库在现有环境下已经接近可测稳定状态。
- 验收标准：仓库测试集中，绝大多数无需真实 API 的测试通过。

## 4. 固定输入 smoke test

### 4.1 名称与表示转换

- 输入：`Query2SMILES("caffeine")`
- 输出：`Cn1c(=O)c2c(ncn2C)n(C)c1=O`
- 结论：通过

- 输入：`Query2SMILES("4-(4-hydroxyphenyl)butan-2-one")`
- 输出：`CC(=O)CCc1ccc(O)cc1`
- 结论：通过

### 4.2 安全相关工具

- 输入：`ExplosiveCheck("118-96-7")`
- 输出：`Molecule is explosive`
- 结论：通过

- 输入：`ControlChemCheck("10025-87-3")`
- 输出：`The molecule 10025-87-3 appears in a list of controlled chemicals.`
- 结论：通过

### 4.3 专利检查

- 输入：`PatentCheck("O=C1N(C)C(C2=C(N=CN2C)N1C)=O")`
- 输出：`Patented`
- 结论：通过

- 输入：`PatentCheck("CCCCCCCCC[NH+]1C[C@@H]([C@H]([C@@H]([C@H]1CO)O)O)O")`
- 输出：`Novel`
- 结论：通过

- 输入：`PatentCheck("CC(C)c1ccccc1")`
- 输出：`Patented`
- 结论：与仓库测试期望存在分歧

## 5. 配置透传 smoke test

### 5.1 Qwen 模型兼容

- 输入条件：
  - `model="qwen-max"`
  - `openai_api_base="https://example.com/v1"`
  - 使用 `python_repl` 作为最小工具集
- 验收结果：
  - `ChemCrow` 构造成功
  - 内部 LLM 类型为 `ChatOpenAI`
  - `model_name` 为 `qwen-max`
- 结论：通过

边界：

- 当前仅证明构造链路与参数透传已恢复。
- 真实 API 返回行为尚未测试。

### 5.2 RXN 参数化

- 输入条件：
  - `RXNPredict(..., project_id="project-test-123")`
  - `RXNRetrosynthesis(..., project_id="project-test-456", summary_model="qwen-plus", openai_api_base="https://example.com/v1")`
- 验收结果：
  - `project_id` 与摘要模型配置被对象正确接收
- 结论：通过

边界：

- 当前仅证明对象级配置有效。
- 真实 RXN API 调用尚未执行。

## 6. 外部服务最小连通性验证

### 6.1 Qwen

- 脚本：`reproduction_records/tests/smoke_qwen_chat.py`
- 固定输入：`Reply with the exact string CHEMCROW_QWEN_OK.`
- 输出摘要：
  - `model = qwen3.5-plus-2026-02-15`
  - `message = CHEMCROW_QWEN_OK`
- 结论：通过

边界：

- 该证据证明 Qwen OpenAI-compatible 接口在当前环境下可被旧版 `openai==0.27.8` 成功调用。
- 该证据不直接证明 agent 级工具调用稳定性。

### 6.2 RXN 项目绑定

- 脚本：`reproduction_records/tests/smoke_rxn_auth.py`
- 输出摘要：
  - `project_id` 与当前配置一致
  - `project_count = 1`
  - `project_found = true`
- 结论：通过

补充说明：

- `2026-03-14` 已完成一次 RXN 配置轮换。
- 当前 `smoke_rxn_auth.out` 对应的是轮换后的新 `project_id` 验证结果。

边界：

- 该证据证明 key 与 `project_id` 组合可访问项目列表。
- 该证据不保证具体预测接口不存在配额或限速。

### 6.3 Serp

- 脚本：`reproduction_records/tests/smoke_serp_search.py`
- 固定输入：`acetaminophen molecular weight`
- 输出摘要：
  - `organic_count = 2`
  - 首条结果指向 PubChem
- 结论：通过

## 7. 主线功能验证

### 7.1 基础问答

- 脚本：`reproduction_records/tests/smoke_chemcrow_basic_qa.py`
- 固定输入：`What is the molecular weight of tylenol?`
- 观测到的工具链：
  - `Name2SMILES`
  - `SMILES2Weight`
  - `Mol2CAS`
  - `ControlChemCheck`
- 输出结论：
  - 返回 Tylenol 分子量约 `151.16 g/mol`
  - 返回 CAS `103-90-2`
- 结论：通过

边界：

- 该证据证明 `ChemCrow` 在 Qwen 条件下可以初始化、选择工具并完成一次多步问答。
- 该证据不外推到所有复杂任务。

### 7.2 WebSearch

- 脚本：`reproduction_records/tests/smoke_websearch_tool.py`
- 固定输入：`What is the molecular weight of acetaminophen?`
- 输出摘要：
  - 返回非空搜索摘要
  - 结果内容含分子量信息
- 结论：通过

补充说明：

- 已追加 agent 级 web-search 倾向性样例：
  - `reproduction_records/tests/smoke_chemcrow_websearch_agent.out`
- 该样例中，agent 虽收到“使用 WebSearch”的显式提示，仍优先选择了更专用的化学工具链：
  - `Name2SMILES`
  - `Mol2CAS`
  - `ControlChemCheck`
  - `SMILES2Weight`
- 当前可支持的结论是：agent 工具路由会优先选择更专用的化学工具，未必严格服从“优先使用 WebSearch”的提示。

### 7.3 ReactionPredict

- 脚本：`reproduction_records/tests/smoke_rxn_predict_tool.py`
- 固定输入：`CCO.O=O`
- 输出摘要：
  - `product = CC(=O)O`
- 结论：通过

补充说明：

- 在 RXN 配置轮换后，已再次执行一次低消耗复测。
- 新配置下的输出见：
  - `reproduction_records/tests/smoke_rxn_predict_tool_new.out`
- 新配置下同样返回：
  - `product = CC(=O)O`
- 当前可支持的最稳妥结论是：新 `RXN4CHEM_API_KEY + project_id` 组合具备正向反应预测能力。

边界：

- 该证据证明当前 RXN key、project id 与公开仓库正向反应工具链可以在固定输入下返回非空产物。

### 7.4 ReactionRetrosynthesis

- 脚本：`reproduction_records/tests/smoke_rxn_retro_tool.py`
- 固定输入：`CC(=O)Oc1ccccc1C(=O)O`
- 当前成功证据：
  - `prediction_id` 非空
  - `path_count = 6`
  - `result` 为非空合成步骤文本
  - `error = null`
- 结论：通过

补充说明：

- 旧一轮 RXN 配置下的受限证据见：
  - `reproduction_records/tests/smoke_rxn_retro_http_probe.out`
- 新一轮 RXN 配置下的早期最低消耗预测入口探测结果见：
  - `reproduction_records/tests/smoke_rxn_retro_http_probe_new.out`
- 该早期 `500 + payload = null` 结果来自手写 probe，后续已确认其请求体结构与官方 wrapper 不一致。
- 改用官方 wrapper 路径并对 node 动作提取节奏做兼容处理后，逆合成已在新配置下形成成功证据。
- 当前仍应记录其服务端波动边界：
  - `get_paths` 可能出现少量重试
  - node 动作阶段可能出现空响应与 `429`

### 7.5 Agent 级受控化学品与爆炸性检查

- 脚本：`reproduction_records/tests/smoke_chemcrow_control_agent.py`
- 固定输入：
  - `Determine whether phosphorus oxychloride with CAS number 10025-87-3 is a controlled chemical and whether it is explosive. Answer briefly.`
- 实际工具链：
  - `ControlChemCheck`
  - `ExplosiveCheck`
- 输出结论：
  - `Phosphorus oxychloride (CAS 10025-87-3) is a controlled chemical.`
  - `It is not known to be explosive.`
- 结论：通过

### 7.6 Agent 级正向反应预测

- 脚本：`reproduction_records/tests/smoke_chemcrow_reactionpredict_agent.py`
- 固定输入：
  - `What is the product of the reaction between styrene and dibromine? Answer briefly.`
- 实际工具链：
  - `Name2SMILES`
  - `Mol2CAS`
  - `ControlChemCheck`
  - `ExplosiveCheck`
  - `ReactionPredict`
- 输出结论：
- 产品为 `1,2-dibromo-1-phenylethane`
- 产品 SMILES 为 `BrCC(Br)c1ccccc1`
- 结论：通过

### 7.7 Agent 级专利与性质联合查询

- 脚本：`reproduction_records/tests/smoke_chemcrow_patent_agent.py`
- 固定输入：
  - `For caffeine, provide the molecular weight and whether the molecule is patented. Answer briefly.`
- 实际工具链：
  - `Name2SMILES`
  - `SMILES2Weight`
  - `PatentCheck`
  - `Mol2CAS`
  - `ControlChemCheck`
- 输出结论：
  - 分子量约 `194.19 g/mol`
  - 专利状态为 `Patented`
  - 非受控化学品
- 结论：通过

### 7.8 Agent 级 Web 与受控化学品联合查询

- 脚本：`reproduction_records/tests/smoke_chemcrow_web_control_agent.py`
- 固定输入：
  - `Find the boiling point of phosphorus oxychloride and determine whether CAS 10025-87-3 is a controlled chemical. Answer briefly.`
- 实际工具链：
  - `ControlChemCheck`
  - `Name2SMILES`
  - `Wikipedia`（返回受限说明）
  - `LiteratureSearch`（返回受限说明）
  - `WebSearch`
  - `Mol2CAS`
  - `Python_REPL`
- 输出结论：
  - 沸点约 `105.8°C`
  - `10025-87-3` 为受控化学品
- 结论：通过

边界：

- 该证据证明：默认 agent 路由仍可能先尝试 `Wikipedia` 或 `LiteratureSearch`。
- 该证据同时证明：在当前补丁后，这些工具即使失败也不会直接中断链路，agent 可以继续回退到 `WebSearch` 与其他工具。

## 8. pytest 结果

### 8.1 定向测试

执行范围：

- `tests/test_converters.py`
- `tests/test_safety_tools.py`
- `tests/test_search.py`

结果：

- `15 passed`
- `4 skipped`
- `1 failed`

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pytest_round2_targeted.log`

### 8.2 全量测试

执行范围：

- `tests/`

结果：

- `25 passed`
- `5 skipped`
- `1 failed`

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pytest_round2_full.log`

## 9. 唯一剩余失败项分析

失败项：

- `tests/test_search.py::test_patentcheck_molset`

失败现象：

- 仓库测试期望 `CC(C)c1ccccc1` 为 `Novel`
- 当前工具输出为 `Patented`

当前证据：

- `molbloom` 的 SureChEMBL filter 下载链路在当前环境中不可达，已触发官方 API 回退路径。
- SureChEMBL 官方 `POST /api/search/structure` 与 `GET /api/search/{hash}/results` 的 exact structure 查询，在 `2026-03-14` 对 `CC(C)c1ccccc1` 返回 `total_hits = 3`。
- 同一套官方 API 对咖啡因 exact structure 查询返回 `total_hits = 1`，对 choline 查询返回 `total_hits = 0`。

当前最稳妥结论：

- `PatentCheck` 已从“无法执行”恢复为“可执行”。
- 该单条失败更符合“当前专利语料或检索语义与仓库测试快照不一致”的特征。
- 当前证据不足以把该分歧写成代码缺陷已完全排除。

## 10. 当前可支持的结论边界

- 可以写：公开仓库版本的本地可测核心工具链已大面积恢复。
- 可以写：当前环境下全量测试为 `25 passed, 5 skipped, 1 failed`。
- 可以写：Qwen、Serp、RXN 项目绑定、基础问答、`WebSearch`、`ReactionPredict`、`ReactionRetrosynthesis` 已形成直接证据。
- 可以写：agent 已形成多步工具调用证据，覆盖基础问答、受控化学品检查与正向反应预测。
- 可以写：agent 级专利与性质联合查询已形成成功证据。
- 可以写：`Wikipedia` 与 `LiteratureSearch` 的外部失败已被收敛为可退化链路，不再直接导致 agent 崩溃。
- 可以写：剩余失败点集中在专利检查与外部专利语料时间漂移的交界位置。
- 可以写：默认 agent 路由对 `Wikipedia` 与 `LiteratureSearch` 仍存在外部依赖风险，但当前已有容错。
- 当前不宜写：全部能力已经与仓库历史测试期完全一致。
- 当前不宜写：逆合成功能在所有时间点都稳定无波动。
