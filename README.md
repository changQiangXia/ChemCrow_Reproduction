# ChemCrow 公开仓库兼容复现说明

本仓库基于 ChemCrow 官方公开仓库进行整理与兼容复现。

- 官方公开仓库地址：<https://github.com/ur-whitelab/chemcrow-public.git>
- 当前复现仓库地址：<https://github.com/changQiangXia/ChemCrow_Reproduction.git>
- 官方复现锚点：`e7ebd5193334ac1d8dea137b635721c7cb470d33`
- 官方原始 README 备份：[`README_ORIGINAL_PROJECT.md`](README_ORIGINAL_PROJECT.md)

当前工作的目标是让官方公开仓库在当前环境、当前模型接口和当前外部服务条件下恢复可安装、可导入、可验证的主线能力，并把改动依据、测试过程和结果证据保留到版本库中。

## 1. 项目定位

当前仓库对应的是官方公开仓库的兼容复现，不对应论文完整系统复现。

需要先区分三层对象：

| 层级 | 可确认的事实 | 当前结论 |
| --- | --- | --- |
| 论文 | ChemCrow 论文摘要将系统描述为一个面向化学任务的 agent，整合了 `18` 个专家设计工具，任务覆盖有机合成、药物发现和材料设计 | 论文讨论的是研究系统与论文实验 |
| 官方公开仓库 | 官方 README 已明确说明，公开仓库没有包含论文中的全部工具，原因与 API 使用限制有关，因此仓库结果不能直接等同于论文结果 | 官方仓库更接近论文系统的公开子集 |
| 当前仓库 | 当前仓库以官方公开仓库为基线，围绕当前环境进行兼容修补，并补充复现证据、差异记录和环境说明 | 当前结果可表述为官方公开仓库的受限兼容复现 |

从这三层关系出发，当前仓库适合支持以下说法：

- 官方公开仓库已经在当前环境下恢复到可运行、可留痕、可复查的状态。
- 论文层面的完整系统、完整工具集合和论文结果，不宜直接写成已经复现。

## 2. 与官方公开仓库相比，实际改了什么

相对官方公开仓库，当前源码改动集中在 `8` 个 Python 文件。改动主要落在兼容层、配置入口和异常处理层。agent 主体结构、工具体系主体、测试目录和项目骨架仍沿用官方公开仓库。

### 2.1 源码改动总表

| 文件 | 官方公开仓库在当前环境中的问题 | 当前处理 | 作用 |
| --- | --- | --- | --- |
| [`chemcrow/agents/chemcrow.py`](chemcrow/agents/chemcrow.py) | 模型名判断只接受 `gpt-*` 和 `text-*`，无法直接接入当前使用的 `Qwen` OpenAI-compatible 接口 | 放宽 chat 模型入口，新增 `openai_api_base` 配置透传 | `ChemCrow` 可在当前 `Qwen` 路径下初始化 |
| [`chemcrow/agents/tools.py`](chemcrow/agents/tools.py) | `RXN4CHEM_PROJECT_ID`、摘要模型、`OPENAI_API_BASE` 不能进入工具对象；默认 `Wikipedia` 工具在当前网络条件下容易中断链路 | 新增配置透传；将默认 `Wikipedia` 包装为 `SafeWikipedia` | 工具装配过程更适配当前环境 |
| [`chemcrow/utils.py`](chemcrow/utils.py) | `PubChem` 返回字段和旧代码假设不完全一致；部分查询缺少 URL 编码和超时控制 | 增加 URL 编码、字段回退和超时 | 名称转 `SMILES`、`CAS` 查询恢复可用 |
| [`chemcrow/tools/converters.py`](chemcrow/tools/converters.py) | 个别输出文本格式不清楚 | 调整提示文本 | 结果记录更容易直接引用 |
| [`chemcrow/tools/safety.py`](chemcrow/tools/safety.py) | `pkg_resources` 在新环境中不稳定；`PubChem` 安全信息层级已变化 | 改用 `importlib.resources`，递归解析 `GHS Classification` | 爆炸性判定和受控化学品判定恢复可用 |
| [`chemcrow/tools/search.py`](chemcrow/tools/search.py) | 文献工具链把若干依赖视为必然存在；`Wikipedia` 外部异常会打断链路；`PatentCheck` 依赖的本地 filter 下载不稳定 | 增加可选导入和降级返回；加入 `SafeWikipedia`；为 `PatentCheck` 增加 SureChEMBL 官方 API 回退路径 | 包导入更稳定，文献链路和专利检查在当前条件下可继续使用 |
| [`chemcrow/tools/rxn4chem.py`](chemcrow/tools/rxn4chem.py) | `project_id` 和摘要模型写死；当前 `RXN` 返回结构、空响应和 `429` 与旧代码假设不一致 | 参数化 `project_id`、摘要模型和 `openai_api_base`；兼容当前返回结构和轮询节奏 | `ReactionPredict` 与 `ReactionRetrosynthesis` 恢复到可测状态 |
| [`chemcrow/tools/reactions.py`](chemcrow/tools/reactions.py) | 本地逆合成摘要模型写死为历史 `GPT` 模型名 | 增加摘要模型和 `openai_api_base` 配置入口 | 本地路线与当前主线配置保持一致 |

### 2.2 新增的仓库材料

除源码修补外，当前仓库还新增了几类可追溯材料：

- [`README_ORIGINAL_PROJECT.md`](README_ORIGINAL_PROJECT.md)：保留官方原始 README，便于直接对照
- [`.env.example`](.env.example)：给出当前复现实际使用过的环境变量模板
- [`reproduction_records/00_baseline.md`](reproduction_records/00_baseline.md)：记录官方锚点、基线时间和起始状态
- [`reproduction_records/03_source_change_inventory.md`](reproduction_records/03_source_change_inventory.md)：逐文件说明源码改动
- [`reproduction_records/tests/2026-03-14_test_matrix.md`](reproduction_records/tests/2026-03-14_test_matrix.md)：汇总固定输入测试结果
- [`reproduction_records/tests/patentcheck_discrepancy_2026-03-14.md`](reproduction_records/tests/patentcheck_discrepancy_2026-03-14.md)：解释 `PatentCheck` 剩余分歧
- [`reproduction_records/diffs/2026-03-14_original_zip_vs_official_head.diff`](reproduction_records/diffs/2026-03-14_original_zip_vs_official_head.diff)：原始压缩包与官方仓库 `HEAD` 的零差异留痕
- [`reproduction_records/diffs/2026-03-14_current_vs_original.diff`](reproduction_records/diffs/2026-03-14_current_vs_original.diff)：当前仓库相对官方基线的源码差异

## 3. 相对论文和官方仓库，当前结果达到了什么程度

### 3.1 相对论文

当前结果与论文之间仍有明显距离，这一点需要单独说明。

- 论文展示的是研究系统层面的结果，涵盖更完整的工具集合和论文实验。
- 官方公开仓库已经声明，公开版本不包含论文中的全部工具，因此仓库结果本身就不等同于论文结果。
- 当前仓库的工作对象是官方公开仓库。当前完成的是公开仓库在当前环境下的兼容复现。

从证据范围看，当前最稳妥的表述是：

- 论文完整系统复现尚未成立。
- 官方公开仓库的主线可运行性已经在当前环境下恢复，并形成了较完整的证据链。

### 3.2 相对官方公开仓库

相对官方公开仓库，当前仓库已经补齐了三类内容：

- 当前模型接口兼容：`Qwen` 通过 OpenAI-compatible 路径接入成功
- 当前外部服务兼容：`PubChem`、`SureChEMBL`、`Wikipedia`、`RXN` 的返回结构或波动已被吸收
- 当前复现实证材料：环境、差异、日志、测试脚本和输出全部纳入版本库

因此，当前仓库相对官方公开仓库的提升，主要体现在：

- 公开仓库当前能否跑通，已经有直接证据
- 哪些地方做了兼容修补，已经能逐文件说明
- 哪些地方仍受限，已经能对应到具体测试和具体日志

## 4. 当前已经验证到什么程度

### 4.1 外部服务最小连通性

已经形成直接证据的外部服务包括：

- `Qwen`
- `RXN4Chem` 项目绑定
- `Serp`

对应记录见：

- [`reproduction_records/tests/smoke_qwen_chat.out`](reproduction_records/tests/smoke_qwen_chat.out)
- [`reproduction_records/tests/smoke_rxn_auth.out`](reproduction_records/tests/smoke_rxn_auth.out)
- [`reproduction_records/tests/smoke_serp_search.out`](reproduction_records/tests/smoke_serp_search.out)

### 4.2 工具级能力

已经形成直接证据的工具级能力包括：

- 名称转 `SMILES`
- `CAS` 查询
- 爆炸性判定
- 受控化学品判定
- `PatentCheck`
- `WebSearch`
- `ReactionPredict`
- `ReactionRetrosynthesis`

集中记录见：

- [`reproduction_records/tests/2026-03-14_test_matrix.md`](reproduction_records/tests/2026-03-14_test_matrix.md)

### 4.3 agent 级能力

已经形成直接证据的 agent 级任务包括：

- Tylenol 分子量问答
- 受控化学品与爆炸性联合判断
- 正向反应预测
- 专利与分子性质联合查询
- 网页信息与受控化学品联合查询

对应输出见：

- [`reproduction_records/tests/smoke_chemcrow_basic_qa.out`](reproduction_records/tests/smoke_chemcrow_basic_qa.out)
- [`reproduction_records/tests/smoke_chemcrow_control_agent.out`](reproduction_records/tests/smoke_chemcrow_control_agent.out)
- [`reproduction_records/tests/smoke_chemcrow_reactionpredict_agent.out`](reproduction_records/tests/smoke_chemcrow_reactionpredict_agent.out)
- [`reproduction_records/tests/smoke_chemcrow_patent_agent.out`](reproduction_records/tests/smoke_chemcrow_patent_agent.out)
- [`reproduction_records/tests/smoke_chemcrow_web_control_agent.out`](reproduction_records/tests/smoke_chemcrow_web_control_agent.out)

### 4.4 当前测试结果

当前仓库保留了两轮 `pytest` 记录。

- 第一轮结果：若按官方公开仓库原样执行，在当前环境中会出现多项失败
- 第二轮全量结果：`25 passed, 5 skipped, 1 failed`
- 剩余失败项：`tests/test_search.py::test_patentcheck_molset`

对应记录见：

- [`reproduction_records/pytest_round1.log`](reproduction_records/pytest_round1.log)
- [`reproduction_records/pytest_round2_full.log`](reproduction_records/pytest_round2_full.log)
- [`reproduction_records/pytest_round2_targeted.log`](reproduction_records/pytest_round2_targeted.log)

## 5. 当前边界

以下内容仍然需要保守描述：

- `ChemSpace` 相关链路还没有形成端到端验证结论
- `LiteratureSearch` 的完整链路仍依赖 `SEMANTIC_SCHOLAR_API_KEY` 和外部服务状态
- `ReactionRetrosynthesis` 当前已经有成功证据，但仍可能受到空响应和 `429` 影响
- `PatentCheck` 与历史测试中 `cumene` 样例存在时间快照分歧，当前更适合依据 `SureChEMBL` 官方当前数据解释
- `Qwen` 兼容已经形成成功证据，但这不等于历史 `GPT` 配置在所有行为上完全一致

因此，当前仓库适合采用的结论是：

- 官方公开仓库已经在当前环境中完成条件受限、证据可追溯的兼容复现
- 论文完整系统和论文结果不应直接写成已经复现

## 6. 目录说明

建议优先阅读以下文件：

- [`README_ORIGINAL_PROJECT.md`](README_ORIGINAL_PROJECT.md)：官方原始 README
- [`reproduction_records/00_baseline.md`](reproduction_records/00_baseline.md)：基线和官方锚点
- [`reproduction_records/01_current_status.md`](reproduction_records/01_current_status.md)：当前状态
- [`reproduction_records/02_stage_explanation.md`](reproduction_records/02_stage_explanation.md)：阶段性复现结论
- [`reproduction_records/03_source_change_inventory.md`](reproduction_records/03_source_change_inventory.md)：源码改动清单
- [`reproduction_records/tests/2026-03-14_test_matrix.md`](reproduction_records/tests/2026-03-14_test_matrix.md)：测试矩阵
- [`reproduction_records/tests/patentcheck_discrepancy_2026-03-14.md`](reproduction_records/tests/patentcheck_discrepancy_2026-03-14.md)：剩余分歧说明

## 7. 当前验证环境

当前仓库已经留痕的运行条件如下：

- Python：`3.10`
- 已验证主模型：`qwen3.5-plus-2026-02-15`
- 已验证工具模型：`qwen3.5-plus-2026-02-15`
- 已验证摘要模型：`qwen3.5-plus-2026-02-15`
- 接口形式：OpenAI-compatible

环境变量模板见：

- [`.env.example`](.env.example)

环境安装与依赖记录见：

- [`reproduction_records/env_setup.md`](reproduction_records/env_setup.md)
- [`reproduction_records/pip_freeze_2026-03-14.txt`](reproduction_records/pip_freeze_2026-03-14.txt)

## 8. 快速开始

### 8.1 创建环境

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda create -y -n chemcrow-repro python=3.10
conda activate chemcrow-repro
```

### 8.2 安装项目

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
python -m pip install 'paper-scraper@git+https://github.com/blackadad/paper-scraper.git'
python -m pip install pytest
```

### 8.3 配置环境变量

按 [`.env.example`](.env.example) 中的字段配置运行环境变量。

### 8.4 建议的最小验证顺序

1. `Qwen` 连通性
2. `RXN4Chem` 项目绑定
3. `Serp` 连通性
4. `ChemCrow` 基础问答
5. `ReactionPredict`
6. `ReactionRetrosynthesis`

对应脚本可从以下已提交文件开始：

- [`reproduction_records/tests/smoke_qwen_chat.py`](reproduction_records/tests/smoke_qwen_chat.py)
- [`reproduction_records/tests/smoke_rxn_auth.py`](reproduction_records/tests/smoke_rxn_auth.py)
- [`reproduction_records/tests/smoke_serp_search.py`](reproduction_records/tests/smoke_serp_search.py)
- [`reproduction_records/tests/smoke_chemcrow_basic_qa.py`](reproduction_records/tests/smoke_chemcrow_basic_qa.py)
- [`reproduction_records/tests/smoke_rxn_predict_tool.py`](reproduction_records/tests/smoke_rxn_predict_tool.py)
- [`reproduction_records/tests/smoke_rxn_retro_tool.py`](reproduction_records/tests/smoke_rxn_retro_tool.py)

## 9. 最小使用示例

```python
from chemcrow.agents import ChemCrow

chem_model = ChemCrow(
    model="qwen3.5-plus-2026-02-15",
    temp=0.1,
    streaming=False,
)

print(chem_model.run("What is the molecular weight of tylenol?"))
```

## 10. 原始资料

- ChemCrow 论文：<https://arxiv.org/abs/2304.05376>
- ChemCrow 官方公开仓库：<https://github.com/ur-whitelab/chemcrow-public.git>
