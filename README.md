# ChemCrow 公开仓库复现说明

## 1. 文档定位

本文用于说明当前仓库的复现目标、运行条件、已完成验证、证据目录与当前边界。

原始公开仓库自带说明已保留到：

- [README_ORIGINAL_PROJECT.md](README_ORIGINAL_PROJECT.md)

## 2. 复现对象

- 复现对象：`ChemCrow` 公开仓库版本
- 公开版本锚点：`e7ebd5193334ac1d8dea137b635721c7cb470d33`
- 当前路线：在 `Qwen` 与当前可获得外部服务条件下，对公开仓库进行受限兼容复现

说明边界：

- 当前说明对应公开仓库版本
- 当前说明不覆盖论文完整系统

## 3. 当前仓库结构

- 原项目原始说明：`README_ORIGINAL_PROJECT.md`
- 复现记录总目录：`reproduction_records/`
- 阶段性说明：`reproduction_records/02_stage_explanation.md`
- 源码改动说明：`reproduction_records/03_source_change_inventory.md`
- 测试矩阵：`reproduction_records/tests/2026-03-14_test_matrix.md`

## 4. 当前运行条件

- Python：`3.10`
- 独立环境名称：`chemcrow-repro`
- 主模型：`qwen3.5-plus-2026-02-15`
- 工具模型：`qwen3.5-plus-2026-02-15`
- 摘要模型：`qwen3.5-plus-2026-02-15`
- `Qwen` 接口形式：`OpenAI-compatible`

环境变量模板：

- [`.env.example`](.env.example)

说明：

- `.env.example` 中已用中文注释标记本次复现已实际使用的变量
- 真实 `.env` 文件不纳入版本控制

## 5. 快速开始

### 5.1 环境准备

建议先创建独立 conda 环境：

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda create -y -n chemcrow-repro python=3.10
conda activate chemcrow-repro
```

### 5.2 安装项目

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
python -m pip install 'paper-scraper@git+https://github.com/blackadad/paper-scraper.git'
python -m pip install pytest
```

安装记录与依赖快照：

- `reproduction_records/env_setup.md`
- `reproduction_records/pip_freeze_2026-03-14.txt`

### 5.3 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

然后填写真实值。

### 5.4 建议的最小验证顺序

1. `Qwen` 连通性
2. `RXN4Chem` 项目绑定
3. `Serp` 连通性
4. `ChemCrow` 基础问答
5. `ReactionPredict`
6. `ReactionRetrosynthesis`

对应脚本位于：

- `reproduction_records/tests/`

## 6. 当前已形成的直接证据

### 6.1 外部服务

- `Qwen`：`reproduction_records/tests/smoke_qwen_chat.out`
- `RXN4Chem` 项目绑定：`reproduction_records/tests/smoke_rxn_auth.out`
- `Serp`：`reproduction_records/tests/smoke_serp_search.out`

### 6.2 工具级能力

- `WebSearch`
- `ReactionPredict`
- `ReactionRetrosynthesis`
- `PatentCheck`
- 名称转 `SMILES`
- `CAS` 查询
- 爆炸性与受控化学品判断

集中记录：

- `reproduction_records/tests/2026-03-14_test_matrix.md`

### 6.3 agent 级能力

- 基础问答
- 受控化学品与爆炸性联合判断
- 正向反应预测
- 专利与分子性质联合查询
- 网页信息与受控化学品联合查询

对应输出文件位于：

- `reproduction_records/tests/smoke_chemcrow_basic_qa.out`
- `reproduction_records/tests/smoke_chemcrow_control_agent.out`
- `reproduction_records/tests/smoke_chemcrow_reactionpredict_agent.out`
- `reproduction_records/tests/smoke_chemcrow_patent_agent.out`
- `reproduction_records/tests/smoke_chemcrow_web_control_agent.out`

## 7. 当前源码改动的定位

当前源码改动集中于兼容性修补。

改动目标主要包括：

- 让公开仓库接入 `Qwen`
- 让 `RXN4CHEM_PROJECT_ID` 与摘要模型可配置
- 让文献工具链在缺少可选依赖或缺少外部 key 时可降级
- 让当前 `PubChem`、`SureChEMBL`、`Wikipedia`、`RXN` 的外部服务状态可被当前仓库吸收

详细说明位于：

- `reproduction_records/03_source_change_inventory.md`

## 8. 当前边界

### 8.1 已明确受限

- `ChemSpace` 相关链路
- 依赖 `SEMANTIC_SCHOLAR_API_KEY` 的完整文献检索链路

### 8.2 当前存在波动

- `ReactionRetrosynthesis` 在当前服务条件下仍可能出现空响应与 `429`
- `Wikipedia` 与 `LiteratureSearch` 仍依赖外部服务状态

说明：

- 当前已通过工具级容错避免 `Wikipedia` 与 `LiteratureSearch` 直接打断 agent 链路

## 9. 当前最稳妥的阶段结论

当前证据支持如下表述：

- `ChemCrow` 公开仓库版本已在当前环境中完成条件受限、可追溯的兼容性复现
- `Qwen` 固定快照 `qwen3.5-plus-2026-02-15` 已在公开仓库调用路径下接入成功
- 基础问答、`WebSearch`、`ReactionPredict`、`ReactionRetrosynthesis` 已形成直接成功证据
- `PatentCheck` 的剩余样例分歧已完成外部数据层面的解释

## 10. 关键证据目录

- 基线记录：`reproduction_records/00_baseline.md`
- 当前状态：`reproduction_records/01_current_status.md`
- 阶段性说明：`reproduction_records/02_stage_explanation.md`
- 源码改动说明：`reproduction_records/03_source_change_inventory.md`
- 测试矩阵：`reproduction_records/tests/2026-03-14_test_matrix.md`
- 专利分歧调查：`reproduction_records/tests/patentcheck_discrepancy_2026-03-14.md`
- 差异文件：`reproduction_records/diffs/`

## 11. 提交说明

当前仓库建议保留：

- 源码改动
- `reproduction_records/` 下的文档、脚本、输出、日志、差异文件与依赖快照

当前仓库建议忽略：

- `.env`
- `__pycache__/`
- `.pytest_cache/`
- `*.egg-info/`
- `.ipynb_checkpoints/`

当前 `.gitignore` 已按上述原则调整。
