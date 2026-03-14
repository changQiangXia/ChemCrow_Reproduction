# CHANGE 002

## 1. 基本信息

- 编号：`CHANGE_002`
- 日期：`2026-03-14`
- 作用阶段：主线功能验证阶段
- 改动性质：次级兼容补丁

## 2. 触发背景

在完成 Qwen、Serp 与 RXN 项目绑定的最小连通性验证后，`ReactionRetrosynthesis` 的主线 smoke test 暴露出当前 RXN 服务返回结构与仓库实现之间的兼容性问题。

## 3. 触发该改动的具体问题

### 3.1 `get_reaction_settings` 的返回结构漂移

- 现象：工具在 `get_reaction_settings` 阶段因 `response["response"]` 为字符串而抛出 `AttributeError`。
- 实际观测到的返回形态包括：
  - `{"response": ""}`
  - `{"response": {"status": 429, "message": "Too fast requests"}}`
  - `{"response": {"status": 429, "message": "Too many requests per minute"}}`
- 原始实现仅处理 `response["response"]["error"] == "Too Many Requests"`。

### 3.2 单节点异常导致整条逆合成链路中断

- 现象：即使部分 node 在延时后可以返回有效 `actions`，其余 node 的空响应或限速响应仍会让整条链路失败。
- 实际探测表明：
  - 合成节点动作生成存在延迟；
  - 过于激进的逐节点重试会放大 RXN 分钟级限速。

## 4. 改动范围

- 文件：
  - `chemcrow/tools/rxn4chem.py`

## 5. 具体修改

### 5.1 `get_reaction_settings` 兼容当前返回形态

位置：

- `chemcrow/tools/rxn4chem.py:254-276`

改动内容：

- 兼容空字符串响应；
- 兼容 `status=429` 与 `message` 风格的限速提示；
- 兼容嵌套在 `payload` 中的动作数据。

### 5.2 `get_action_sequence` 增加节点级等待与容错

位置：

- `chemcrow/tools/rxn4chem.py:218-234`

改动内容：

- 在读取节点动作前加入短暂等待；
- 对单个 node 的 `KeyError` 进行跳过处理；
- 当全部 node 都未返回动作时，明确返回 `Tool error`。

### 5.3 降低单节点重试强度

位置：

- `chemcrow/tools/rxn4chem.py:254`

改动内容：

- 将 `get_reaction_settings` 的装饰器重试次数从 `20` 下调为 `3`，降低分钟级限速触发概率。

## 6. 为什么该改动归类为次级兼容补丁

- 该补丁不属于 `/root/autodl-tmp/chemcrow_reproduction_plan.md` 第 7.1 节列出的四类主线最小修改。
- 该补丁的目标是兼容外部 RXN 服务在当前时间点的返回结构与限速行为变化。
- 该补丁不会改变 agent 框架和工具链入口，但会改变对外部 API 异常的处理方式。

## 7. 恢复效果与当前边界

- 恢复效果：
  - 已消除原始的 `AttributeError`；
  - 逆合成工具在当前环境下可进入更深层的服务交互阶段；
  - 当前失败已从“代码解析错误”收敛为“外部服务限额/配额约束”。

- 当前边界：
  - 进一步的失败原因经 HTTP 级探测确认，来自 RXN 返回：
    - `{"status":401,"message":"Calls with API Key is limited to 100 for free plan; please upgrade your plan to remove this limitation"}`
  - 当前证据支持“工具链已适配当前返回形态”，不支持“逆合成功能已完全恢复”。
