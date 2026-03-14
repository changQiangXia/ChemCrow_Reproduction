# CHANGE 004

## 1. 基本信息

- 编号：`CHANGE_004`
- 日期：`2026-03-14`
- 改动类型：次级兼容补丁

## 2. 触发背景

在切换到新的 RXN 配置后，逆合成能力排查进入更细粒度阶段。此时已确认：

- 官方 wrapper 路径可以成功返回 `prediction_id`
- `get_predict_automatic_retrosynthesis_results()` 可以成功返回 `retrosynthetic_paths`
- 失败集中在后半段的 synthesis node 动作提取

## 3. 已识别的异常链条

### 3.1 旧 key 的配额边界

- 旧配置下，HTTP 级探测返回：
  - `401`
  - `Calls with API Key is limited to 100 for free plan; please upgrade your plan to remove this limitation`

### 3.2 手写探测请求的结构偏差

- 在新配置排查早期，手写 HTTP probe 的 payload 结构与 `RXN4ChemistryWrapper.predict_automatic_retrosynthesis()` 的真实请求结构不一致。
- 因此，早期观察到的 `500 + payload=null` 不能直接视为官方调用路径失败。

### 3.3 当前服务端的真实波动形态

在 synthesis node 动作提取阶段，已实际观察到以下返回：

- `{"response": ""}`
- `{"response": {"status": 429, "message": "Too fast requests"}}`
- `{"response": {"status": 429, "message": "Too many requests per minute"}}`
- 某些 node 在后续延时查询中会变为有效 `actions`

结论：

- 当前问题集中在“动作节点渐进可用”与“短时间密集访问触发限速”的组合效应。

## 4. 改动范围

- 文件：
  - `chemcrow/tools/rxn4chem.py`
  - `reproduction_records/tests/smoke_rxn_retro_tool.py`

## 5. 具体修改

### 5.1 增加 `get_reaction_settings` 归一化逻辑

- 引入 `_normalize_reaction_settings`
- 统一处理：
  - 直接 `actions/product` 响应
  - 空字符串响应
  - `429` 与多种限速消息
  - 嵌套 `payload` 中的动作数据

### 5.2 将动作提取改为低频多轮轮询

- `get_action_sequence` 不再对每个 node 做高密度重试
- 改为少轮次、低请求密度轮询
- 只保留首次成功返回的 node 动作

### 5.3 优化逆合成 smoke script

- `smoke_rxn_retro_tool.py` 改为分步输出：
  - `prediction_id`
  - `path_count`
  - `stage`
  - `result`
  - `error`

## 6. 恢复效果

- 新配置下，`ReactionRetrosynthesis` 已形成一次成功的端到端证据。
- 成功证据文件：
  - `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_rxn_retro_tool.out`

## 7. 当前边界

- 逆合成链路当前仍存在轻度服务端波动。
- `get_paths` 阶段仍可能出现少量重试日志。
- 节点动作提取对限速较为敏感，但当前已可在受控节奏下稳定返回结果。
