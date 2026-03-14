# 源码改动说明

## 1. 文档目的

本文用于说明当前工作副本相对原始压缩包快照的源码改动内容、触发问题、修改必要性、解决效果与当前边界。本文只讨论源码改动，不讨论复现记录、日志、缓存文件、测试输出和环境配置文件。

## 2. 比对范围

- 原始快照路径：`/root/autodl-tmp/original_snapshot_2026-03-14/chemcrow-public-main`
- 当前工作副本路径：`/root/autodl-tmp/chemcrow-public-main`
- 当前被人工修改的源码文件集中在 `8` 个 Python 文件

## 3. 总体判断

当前源码改动属于“定向兼容修补”。改动的主要目标有四类：

- 让公开仓库在 `Qwen` 的 `OpenAI-compatible` 接口下可运行
- 让 `RXN4Chem` 的 `project_id` 与摘要模型配置可外部传入
- 让文献工具链在缺少可选依赖或缺少外部 key 时可降级
- 让 `PubChem`、`SureChEMBL`、`Wikipedia`、`RXN` 等外部服务的当前返回结构和波动状态可被当前仓库吸收

当前没有发生下列类型的改动：

- agent 框架重写
- 工具体系重构
- 自定义新路由替换原始工具链
- 大规模 prompt 重写

## 4. 改动分类

### 4.1 主线最小兼容补丁

以下改动直接对应 `/root/autodl-tmp/chemcrow_reproduction_plan.md` 第 7.1 节中允许的最小修改范围：

- `Qwen` 模型兼容入口
- `RXN4CHEM_PROJECT_ID` 参数化
- 摘要模型参数化
- 文献依赖与文献工具链容错

### 4.2 次级兼容补丁

以下改动用于处理当前外部服务状态与历史仓库假设之间的偏差：

- `PubChem` 返回结构变化
- `SureChEMBL` 数据访问路径变化
- `Wikipedia` 工具的外部不稳定性
- `RXN` node 动作提取阶段的返回结构和限速行为

## 5. 按文件说明改动内容

### 5.1 `chemcrow/agents/chemcrow.py`

#### 触发问题

- 原始 `_make_llm` 只接受 `gpt-*` 和 `text-*` 模型名。
- 当前复现路线固定使用 `Qwen`。
- 公开仓库原始调用路径依赖 `ChatOpenAI` / `OpenAI` 风格接口。

#### 修改内容

- 放宽 chat 模型名入口，使 `qwen3.5-plus-2026-02-15` 这类模型可直接进入 `ChatOpenAI`
- 新增 `openai_api_base` 参数
- 在 `ChemCrow` 初始化阶段将 `OPENAI_API_BASE` 继续向工具模型路径透传

#### 修改必要性

- 当前复现主线要求使用 `Qwen`
- 保留公开仓库原始调用路径的前提下，最直接的兼容方式就是保留 `OpenAI-compatible` 接口形态

#### 解决效果

- `ChemCrow` 已在 `Qwen` 固定快照条件下成功初始化
- agent 级基础问答、正向反应预测、逆合成与复合任务样例均已形成直接证据

### 5.2 `chemcrow/agents/tools.py`

#### 触发问题

- 原始工具装配逻辑无法读取 `RXN4CHEM_PROJECT_ID`
- 原始工具装配逻辑无法透传摘要模型和 `OPENAI_API_BASE`
- 默认 `Wikipedia` 工具在当前环境下容易因外部响应异常导致链路中断

#### 修改内容

- 新增 `RXN4CHEM_PROJECT_ID`、`OPENAI_API_BASE`、`CHEMCROW_SUMMARY_MODEL` 读取
- 将这些配置透传给 `RXNPredict`、`RXNRetrosynthesis`、`RXNRetrosynthesisLocal`
- 将默认 `Wikipedia` 工具替换为本地定义的 `SafeWikipedia`

#### 修改必要性

- `RXN` 相关能力是否可调用，与 `project_id` 是否匹配直接相关
- 逆合成步骤总结链路需要使用当前可用的 `Qwen` 模型
- `Wikipedia` 的外部异常会直接影响 agent 主线复现

#### 解决效果

- `RXN` 正向反应与逆合成当前都已在新配置下形成证据
- `Wikipedia` 工具当前即使失败，也不会直接打断整条 agent 链路

### 5.3 `chemcrow/utils.py`

#### 触发问题

- 原始 `PubChem` 查询逻辑假设返回字段固定为 `IsomericSMILES`
- 当前 `PubChem` 返回中可见 `SMILES`、`CanonicalSMILES` 等字段
- 部分查询在未做 URL 编码时稳定性较差

#### 修改内容

- 对 `PubChem` 查询参数做 URL 编码
- `pubchem_query2smiles` 同时兼容 `IsomericSMILES`、`CanonicalSMILES`、`SMILES`
- 相关请求增加超时控制

#### 修改必要性

- 名称转 `SMILES` 和 `CAS` 是公开仓库主线中的基础能力
- 当前公开仓库的多个工具都依赖这层基础查询

#### 解决效果

- `Query2SMILES("caffeine")`
- `Query2SMILES("4-(4-hydroxyphenyl)butan-2-one")`
- `Mol2CAS`

上述链路当前均已恢复成功证据

### 5.4 `chemcrow/tools/converters.py`

#### 触发问题

- 控制化学品提示语在部分返回中表达不够清楚

#### 修改内容

- 调整 `Query2CAS` 与 `Query2SMILES` 的提示文本

#### 修改必要性

- 当前文件本身没有承担大规模兼容逻辑
- 修改目标主要是让返回信息更清楚地区分“结果值”与“附加控制化学品提示”

#### 解决效果

- 当前返回文本在记录和证据说明中更容易直接引用

### 5.5 `chemcrow/tools/safety.py`

#### 触发问题

- 原始实现依赖 `pkg_resources`
- 当前环境下该依赖已不稳定
- `ExplosiveCheck` 对 `PubChem` 的 GHS 数据层级有固定假设
- 当前 `PubChem` 安全信息层级已发生变化

#### 修改内容

- 用 `importlib.resources` 替换 `pkg_resources`
- 新增 `_data_file` 辅助函数，统一读取内置 CSV 数据
- 将 `ghs_classification` 改为递归遍历当前 `PubChem` 安全结构
- 为 `PubChem` 请求增加超时

#### 修改必要性

- 当前环境中 `pkg_resources` 问题会直接导致导入失败
- `ExplosiveCheck` 是公开仓库安全工具链中的核心能力

#### 解决效果

- `chemcrow` 当前可在新环境中稳定导入
- `ExplosiveCheck("118-96-7")` 当前可成功返回爆炸性判断
- `ControlChemCheck("10025-87-3")` 当前可成功返回受控化学品判断

### 5.6 `chemcrow/tools/search.py`

#### 触发问题

- 原始文献工具链将 `paperqa`、`paperscraper`、`OpenAIEmbeddings` 视为必然可用
- 当前环境缺少 `SEMANTIC_SCHOLAR_API_KEY`
- 当前 `Wikipedia` 查询会发生超时或 JSON 解析异常
- `PatentCheck` 原始实现依赖 `molbloom` 的本地 filter 下载
- 当前 `molbloom` 访问的 Dropbox 路径不可稳定使用

#### 修改内容

- 将 `paperqa`、`paperscraper`、`OpenAIEmbeddings` 改为可选导入
- `LiteratureSearch` 在缺少 `SEMANTIC_SCHOLAR_API_KEY` 或出现 embedding / 文献流水线异常时直接返回受限说明
- 新增 `SafeWikipedia`
- `PatentCheck` 新增 `SureChEMBL` 官方 API 回退路径

#### 修改必要性

- 当前公开仓库在工具包初始化阶段就会导入 `search` 模块
- 只要该模块不具备容错，整个包导入和 agent 初始化都可能失败
- `PatentCheck` 当前需要一个不依赖 Dropbox filter 的工作路径

#### 解决效果

- 文献工具链在缺少外部条件时已降级为“受限工具”，不再直接打断 agent
- `Wikipedia` 当前即使查询失败，也会返回受控的工具提示
- `PatentCheck` 当前已恢复为可执行工具
- `PatentCheck` 与仓库测试快照之间仍保留一条 `cumene` 分歧，当前已确认该分歧更符合时间快照差异

### 5.7 `chemcrow/tools/rxn4chem.py`

#### 触发问题

- 原始实现将 `project_id` 写死
- 原始实现将逆合成摘要模型写死
- 当前 `RXN` 服务在 node 动作提取阶段会返回空响应和 `429`
- 原始实现对 `get_reaction_settings` 的返回形态假设过窄

#### 修改内容

- `RXN4Chem` 构造函数支持 `project_id` 参数与环境变量读取
- `RXNRetrosynthesis` 支持 `summary_model` 与 `openai_api_base`
- 新增 `_normalize_reaction_settings`
- 将 node 动作提取改成低频轮询
- 将 `429`、空响应和嵌套 payload 统一纳入兼容处理

#### 修改必要性

- `RXN4Chem` 是公开仓库中正向反应预测与逆合成的默认实现
- 当前若不参数化 `project_id`，新账号与新项目无法直接接入
- 当前若不兼容 node 动作的渐进生成与限速行为，逆合成后半段无法形成稳定证据

#### 解决效果

- 新 `RXN4CHEM_API_KEY + project_id` 组合当前已恢复正向反应预测能力
- 新配置下 `ReactionRetrosynthesis` 已成功返回完整步骤文本
- 当前仍保留“轻度服务端波动”这一边界

### 5.8 `chemcrow/tools/reactions.py`

#### 触发问题

- 原始本地逆合成摘要链路将摘要模型写死为 `gpt-3.5-turbo-16k`

#### 修改内容

- `RXNRetrosynthesisLocal` 支持 `openai_api_key`、`summary_model`、`openai_api_base`

#### 修改必要性

- 公开仓库 README 明确保留本地反应路线作为可选路径
- 当前摘要链路若仍写死历史模型，将无法与 `Qwen` 主线保持一致

#### 解决效果

- 本地反应路线的摘要链路当前具备与主线一致的配置入口

## 6. 当前改动的客观评价

当前源码改动已经超过“极小补丁”规模。更贴近实际的描述是：

- 改动集中在少数关键文件
- 改动目标明确围绕兼容性修补
- 当前仍保留公开仓库原有 agent 结构与工具链主体

当前表述中适合采用的措辞包括：

- 定向兼容修补
- 条件受限下的兼容性修改
- 主线最小兼容补丁与次级兼容补丁并存

当前表述中不适合采用的措辞包括：

- 完全没有改动源码
- 原项目原封不动运行
- 只有极少量源码改动

## 7. 关联记录

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_001_compatibility_patch.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_002_rxn_compatibility_patch.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_004_rxn_retro_stabilization.md`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/changes/CHANGE_005_search_tool_hardening.md`
