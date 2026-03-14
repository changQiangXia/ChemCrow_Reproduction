# CHANGE 001

## 1. 基本信息

- 编号：`CHANGE_001`
- 日期：`2026-03-14`
- 作用阶段：阶段 2 至阶段 4
- 改动前仓库标识：压缩包解压版本，无 `.git` 元数据
- 触发背景：安装成功后，导入与测试阶段暴露出多类兼容性障碍

## 2. 触发该改动的具体问题

### 2.1 PubChem 名称转 SMILES 结果失效

- 现象：`Query2SMILES("caffeine")` 与 `Query2SMILES("4-(4-hydroxyphenyl)butan-2-one")` 返回“Could not find a molecule matching the text”。
- 根因：PubChem 当前返回字段使用 `SMILES`，原代码仅提取 `IsomericSMILES`。
- 证据位置：
  - 修改后兼容入口位于 `chemcrow/utils.py:63-94`

### 2.2 爆炸性判定失效

- 现象：`ExplosiveCheck("118-96-7")` 返回 `Explosive Check Error`。
- 根因：PubChem 安全信息的顶层结构与旧实现假设不一致，原逻辑只检查 `Chemical Safety`，当前数据中 `GHS Classification` 位于 `Safety and Hazards` 层级。
- 证据位置：
  - 修改后兼容逻辑位于 `chemcrow/tools/safety.py:51-84`

### 2.3 `pkg_resources` 依赖导致新环境导入失败

- 现象：在 `setuptools 82.0.1` 下导入 `chemcrow` 失败。
- 根因：`pkg_resources` 已不再适合作为稳定依赖。
- 证据位置：
  - 数据路径读取替换位于 `chemcrow/tools/safety.py:20-22`
  - 相关调用位于 `chemcrow/tools/safety.py:251-252` 与 `chemcrow/tools/safety.py:291-292`

### 2.4 `PatentCheck` 依赖的本地 bloom filter 下载失败

- 现象：`molbloom` 在下载 SureChEMBL filter 时多次失败，导致 `PatentCheck` 返回错误结果。
- 根因：当前环境对 Dropbox 下载链路不可用。
- 证据位置：
  - 回退实现位于 `chemcrow/tools/search.py:162-217`

### 2.5 Qwen 与 OpenAI-compatible 模型名无法通过校验

- 现象：原 `_make_llm` 仅接受 `gpt-*` 与 `text-*` 前缀。
- 根因：模型名判断过窄，与当前复现路线的 OpenAI-compatible 接口不兼容。
- 证据位置：
  - 兼容实现位于 `chemcrow/agents/chemcrow.py:15-35`
  - `openai_api_base` 接入位于 `chemcrow/agents/chemcrow.py:48-68`

### 2.6 RXN `project_id` 与摘要模型被写死

- 现象：`RXN4Chem` 的 `project_id` 和逆合成摘要模型固定为历史值。
- 根因：源码缺少环境变量或参数入口。
- 证据位置：
  - `project_id` 参数化位于 `chemcrow/tools/rxn4chem.py:30-42`
  - 远程逆合成摘要模型可配置位于 `chemcrow/tools/rxn4chem.py:139-157` 与 `chemcrow/tools/rxn4chem.py:283-292`
  - 本地逆合成摘要模型可配置位于 `chemcrow/tools/reactions.py:61-77` 与 `chemcrow/tools/reactions.py:118-127`
  - tool 装配透传位于 `chemcrow/agents/tools.py:9-73`

### 2.7 文献检索可选依赖缺失时缺少容错

- 现象：文献链路依赖 `paperqa`、`paperscraper`、`OpenAIEmbeddings`，任一缺失都会影响导入或运行。
- 根因：源码默认其必然存在。
- 证据位置：
  - 可选导入与运行期容错位于 `chemcrow/tools/search.py:15-28`、`chemcrow/tools/search.py:31-90`、`chemcrow/tools/search.py:111-119`

## 3. 改动文件范围

- `chemcrow/utils.py`
- `chemcrow/tools/converters.py`
- `chemcrow/tools/safety.py`
- `chemcrow/tools/search.py`
- `chemcrow/agents/chemcrow.py`
- `chemcrow/agents/tools.py`
- `chemcrow/tools/rxn4chem.py`
- `chemcrow/tools/reactions.py`

完整差异文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/diffs/2026-03-14_current_vs_original.diff`

## 4. 为什么这些改动属于必要兼容修补

- 改动对象均位于接口层、配置层或可选依赖容错层。
- agent 主体结构、工具集合、任务路由与提示词框架均保持原项目路径。
- 改动的目的均指向“恢复原有能力在当前环境中的可运行性”。
- 当前改动未引入新的替代式 agent 框架，也未用另一套系统重写核心流程。

## 5. 恢复的能力

- `Query2SMILES` 在当前 PubChem 返回结构下恢复可用。
- `ExplosiveCheck` 在当前 PubChem 安全信息层级下恢复可用。
- `chemcrow` 在较新 `setuptools` 环境下恢复可导入。
- `PatentCheck` 在 `molbloom` filter 下载失败时恢复为可调用状态。
- `ChemCrow` 可接受 `qwen-*` 等 OpenAI-compatible chat 模型名。
- `RXN4CHEM_PROJECT_ID`、`OPENAI_API_BASE`、`CHEMCROW_SUMMARY_MODEL` 等配置可透传到实际工具对象。

## 6. 当前已知偏差与风险

- `PatentCheck` 的 SureChEMBL 官方 API 回退路径与仓库测试中的单个历史样例存在分歧。
- 该分歧目前更接近“外部专利语料或检索语义的时间漂移”，不宜写成“代码已与历史结果完全一致”。
- 在 `CHANGE_001` 形成时，真实 API 端到端能力尚未进入执行阶段。

## 7. 验证方式

- 导入验证：`chemcrow`、`ChemCrow`、`PatentCheck`、`ExplosiveCheck`、`Query2SMILES`
- 配置透传 smoke test：Qwen 模型名、`openai_api_base`、`RXN4CHEM_PROJECT_ID`、`CHEMCROW_SUMMARY_MODEL`
- 全量 pytest：`25 passed, 5 skipped, 1 failed`

详细验证结果见：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/2026-03-14_test_matrix.md`
