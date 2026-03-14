# 00 Baseline

## 1. 记录目的

本文件用于冻结当前公开仓库复现工作的起点状态，避免后续环境变化、代码修改与实验结果之间失去对应关系。

## 2. 基线时间

- 记录日期：`2026-03-14`

## 3. 工作空间与仓库路径

- 工作空间：`/root/autodl-tmp`
- 仓库路径：`/root/autodl-tmp/chemcrow-public-main`

## 4. 仓库来源状态

- 当前目录来源于压缩包解压结果。
- 当前目录未包含 `.git` 元数据。
- 已补充官方公开仓库比对。
- 原始压缩包快照与官方仓库 `HEAD` 树内容一致。
- 官方版本锚点为：`e7ebd5193334ac1d8dea137b635721c7cb470d33`
- 官方最近提交时间：`2024-12-19 18:47:03 +0100`
- 官方最近提交摘要：`Merge pull request #52 from ur-whitelab/local-rxn`

对应留痕：

- 官方仓库克隆目录：`/root/autodl-tmp/chemcrow-public-official`
- 零差异比对文件：`/root/autodl-tmp/chemcrow-public-main/reproduction_records/diffs/2026-03-14_original_zip_vs_official_head.diff`

## 5. 当前已知复现对象

- 复现对象：ChemCrow 公开仓库版本
- 复现主线：公开仓库受限兼容复现
- 执行依据：
  - `/root/autodl-tmp/chemcrow_reproduction_plan.md`
  - `/root/autodl-tmp/instructions.md`

## 6. 当前环境基线

- Python：`3.10.8`
- Conda：`22.11.1`

## 7. API 与外部配置状态

当前 shell 中未检测到以下环境变量：

- `OPENAI_API_KEY`
- `OPENAI_API_BASE`
- `RXN4CHEM_API_KEY`
- `RXN4CHEM_PROJECT_ID`
- `SERP_API_KEY`
- `CHEMSPACE_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`

说明：

- `chemcrow_reproduction_plan.md` 中记录了部分 key 已做独立连通性验证。
- 当前执行 shell 尚未继承相应环境变量，因此实际实验前仍需重新核验可用配置来源。

## 8. 已知源码约束摘要

- 模型名判断当前仅接受 `gpt-*` 与 `text-*` 前缀。
- `RXN4Chem` 的 `project_id` 当前为写死值。
- 逆合成总结与本地反应总结模型当前为写死值。
- `paperscraper` 在源码中直接导入，安装依赖列表中未启用对应安装项。
- `search` 模块在工具包初始化阶段直接导入。

## 9. 当前阶段结论

- 基线路径已固定。
- 基线时间已固定。
- 官方公开版本锚点已固定。
- 运行环境的基础版本信息已固定。
- 关键外部配置尚未在当前 shell 中就位。
- 项目进入环境核验与安装排障阶段。
