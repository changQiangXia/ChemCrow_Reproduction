# CHANGE 005

## 1. 基本信息

- 编号：`CHANGE_005`
- 日期：`2026-03-14`
- 改动类型：次级兼容补丁

## 2. 触发背景

在扩充低消耗 agent 样例时，出现了一条典型脆弱链路：

- agent 先调用 `Wikipedia`
- `Wikipedia` 因外部网络或响应格式问题抛异常
- 早期修补后，agent 改为继续执行，但随后又调用 `LiteratureSearch`
- `LiteratureSearch` 在缺少 `SEMANTIC_SCHOLAR_API_KEY` 的条件下继续深入执行，并因外部限速与 embedding 模型兼容性问题崩溃

## 3. 异常来源

### 3.1 Wikipedia

- 当前环境下，`wikipedia` Python 包访问维基接口时可能出现超时或 JSON 解析异常。
- 原始异常会直接中断整条 agent 链路。

### 3.2 LiteratureSearch

- 在无 `SEMANTIC_SCHOLAR_API_KEY` 的条件下，原实现仍会尝试执行文献抓取与 embedding。
- 当前条件下额外暴露出：
  - `Semantic Scholar` 限速
  - `text-embedding-ada-002` 在当前 Qwen 兼容接口下不可用

## 4. 改动范围

- `chemcrow/tools/search.py`
- `chemcrow/agents/tools.py`

## 5. 具体修改

### 5.1 引入 `SafeWikipedia`

- 保留工具名 `Wikipedia`
- 保留原有工具语义与描述
- 在网络异常或外部响应异常时，不再抛出异常
- 改为返回：
  - `Wikipedia lookup failed due to an external service or network issue. Use WebSearch or another chemistry-specific tool for this query.`

### 5.2 强化 `LiteratureSearch` 的缺失前提容错

- 若未配置 `SEMANTIC_SCHOLAR_API_KEY`，直接返回受限说明
- 若文献流水线或 embedding 后端异常，返回受限说明，不再中断 agent 链路

## 6. 恢复效果

- agent 不再因为 `Wikipedia` 或 `LiteratureSearch` 的外部异常直接崩溃
- 在同一条失败样例上，agent 已成功继续回退到：
  - `WebSearch`
  - `Mol2CAS`
  - `Python_REPL`

成功回归证据：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/smoke_chemcrow_web_control_agent.out`

## 7. 当前边界

- 当前改动不能保证 agent 总是优先走 `WebSearch`
- 当前改动证明的是：当 `Wikipedia` 与 `LiteratureSearch` 不可用时，链路可退化而不至于直接失败
