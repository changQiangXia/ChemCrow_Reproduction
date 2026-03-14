# 环境配置记录

## 1. 记录范围

本文件记录环境创建、依赖安装、安装失败现象、解决措施与当前可复用命令。

## 2. 当前环境结果

- conda 环境名称：`chemcrow-repro`
- Python 版本：`3.10`
- 当前 `setuptools` 版本：`82.0.1`
- 安装方式：`editable install`

## 3. 执行命令

### 3.1 创建独立环境

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda create -y -n chemcrow-repro python=3.10
```

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/env_create.log`

### 3.2 安装基础打包工具

```bash
source /etc/network_turbo >/dev/null 2>&1 || true
source /root/miniconda3/etc/profile.d/conda.sh
conda activate chemcrow-repro
python -m pip install --upgrade pip setuptools wheel
```

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_bootstrap.log`

### 3.3 安装项目本体

```bash
source /etc/network_turbo >/dev/null 2>&1 || true
source /root/miniconda3/etc/profile.d/conda.sh
conda activate chemcrow-repro
python -m pip install -e /root/autodl-tmp/chemcrow-public-main
```

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_install_editable.log`

### 3.4 补充可选依赖与测试依赖

```bash
source /etc/network_turbo >/dev/null 2>&1 || true
source /root/miniconda3/etc/profile.d/conda.sh
conda activate chemcrow-repro
python -m pip install 'paper-scraper@git+https://github.com/blackadad/paper-scraper.git'
python -m pip install pytest
```

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_install_paperscraper.log`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_install_pytest.log`

### 3.5 `setuptools` 兼容性验证

初始导入阶段曾出现 `pkg_resources` 缺失问题。后续已通过源码兼容补丁移除该依赖，并将环境恢复到较新版本进行复测：

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate chemcrow-repro
python -m pip install setuptools==82.0.1
```

日志：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_setuptools_downgrade.log`
- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_setuptools_reupgrade.log`

### 3.6 RXN 运行时配置轮换

- `2026-03-14` 已接收新的 `RXN4CHEM_API_KEY` 与新的 `RXN4CHEM_PROJECT_ID`。
- `.env` 已更新。
- 已执行一次低消耗项目绑定验证，结果见：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_auth.out`
- 当前策略：
  - 优先保留额度给后续必要验证；
  - 暂不重复执行高消耗逆合成链路。

## 4. 安装阶段发现与处理

### 4.1 `paperscraper` 缺失

- 现象：`import chemcrow` 在 `chemcrow/tools/search.py` 处因 `ModuleNotFoundError: No module named 'paperscraper'` 失败。
- 处理：补装 `paper-scraper`，来源为 GitHub 仓库安装。
- 结果：导入链继续向前推进。

### 4.2 `pkg_resources` 缺失

- 现象：`chemcrow/tools/safety.py` 依赖 `pkg_resources`，在 `setuptools 82.0.1` 下出现导入失败。
- 初步处理：临时回退 `setuptools<81` 以继续定位问题。
- 最终处理：通过源码改动改为 `importlib.resources`，随后将 `setuptools` 恢复到 `82.0.1` 并完成复测。
- 结果：环境不再依赖旧版 `setuptools`。

### 4.3 `molbloom` 的 SureChEMBL filter 下载失败

- 现象：`PatentCheck` 执行 `molbloom.buy(..., catalog="surechembl")` 时尝试访问 Dropbox 下载 filter，当前环境多次失败。
- 已记录失败模式：
  - `URLError <urlopen error [Errno 99] Cannot assign requested address>`
  - `ConnectTimeout` 到 `www.dropbox.com`
- 处理：在源码中增加 SureChEMBL 官方 API 回退路径。
- 结果：专利检查能力已恢复为可运行状态，当前仍存在一条与仓库测试快照不一致的样例，详见测试记录。

## 5. 当前冻结文件

- 运行时配置文件：
  - `/root/autodl-tmp/chemcrow-public-main/.env`
  - 已设置为 `600` 权限
  - 文档中仅记录变量用途，不记录明文值
- 依赖快照：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/pip_freeze_2026-03-14.txt`
- 原始版本与当前版本差异：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/diffs/2026-03-14_current_vs_original.diff`

## 6. 当前边界

- 当前根目录已提供 `.env.example` 模板。
- 当前工作副本本地存在 `.env` 运行时配置文件，脚本执行时通过 `source .env` 或 `load_dotenv()` 注入变量。
- `Qwen`、`RXN4Chem`、`Serp` 的最小连通性验证已完成。
- `ChemCrow` 基础问答、`ReactionPredict`、`ReactionRetrosynthesis` 的端到端验证已形成证据。
- `CHEMSPACE_API_KEY` 与 `SEMANTIC_SCHOLAR_API_KEY` 当前仍缺失，因此相关能力仍处于受限状态。
