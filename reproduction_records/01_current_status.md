# 当前状态说明

## 1. 截至时间

- `2026-03-14`

## 2. 已完成事项

- 已建立独立 conda 环境并完成项目安装。
- 已补齐 `paper-scraper` 与 `pytest`。
- 已完成第一批必要兼容补丁。
- 已完成第二批 RXN 返回结构兼容补丁。
- 已完成一轮 RXN 运行时配置轮换与新 `project_id` 绑定验证。
- 已完成导入验证、定向 smoke test、全量 pytest、配置透传 smoke test 与主线外部服务连通性测试。
- 已生成依赖快照与原始差异文件。

## 3. 当前复现状态

### 3.1 已证明可运行

- `chemcrow` 包导入
- `ChemCrow` 构造链路中的 OpenAI-compatible 模型兼容入口
- Qwen OpenAI-compatible 接口最小调用
- 名称转 SMILES
- CAS 与受控化学品相关工具
- 爆炸性判定
- `WebSearch`
- `ReactionPredict`
- `ReactionRetrosynthesis`
- `ChemCrow` 基础问答链路
- agent 级专利与性质联合查询
- agent 级网页信息与受控化学品联合查询
- 文献工具的可选依赖容错
- RXN `project_id` 与摘要模型配置透传
- 新一轮 RXN 配置下的 `ReactionPredict`

### 3.2 已证明受限可运行

- `PatentCheck`
  - 当前环境中 `molbloom` 的本地 filter 下载失败
  - 已启用 SureChEMBL 官方 API 回退路径
  - 当前存在一条与仓库测试快照不一致的样例

### 3.3 尚未进入端到端验证

- 更复杂的 agent 多轮任务
- 基于真实 `CHEMSPACE_API_KEY` 的采购与转换链路

### 3.4 当前受限

- `ReactionRetrosynthesis`
  - 旧一轮 RXN 配置下曾受配额边界约束
  - 新一轮 RXN 配置下已恢复成功证据
  - 当前仍存在服务端轻度波动，主要表现为空响应与 `429`
- agent 默认路由中的 `Wikipedia`
  - 当前环境下仍存在外部响应不稳定风险
  - 当前已通过工具级容错避免链路直接崩溃
- agent 默认路由中的 `LiteratureSearch`
  - 在无 `SEMANTIC_SCHOLAR_API_KEY` 条件下当前视为受限工具
  - 当前已通过工具级容错避免链路直接崩溃

## 4. 当前阻塞

- `CHEMSPACE_API_KEY` 与 `SEMANTIC_SCHOLAR_API_KEY` 仍缺失。

## 4.1 当前资源状态

- 用户在较早时点补充的 `RXN` 调用使用情况：`52/100`
- 该观测之后已执行若干受控复测，当前精确剩余额度未重新核验
- 当前执行策略：
  - 逆合成链路已形成成功证据后转入低频维护；
  - 后续优先扩充低消耗主线证据；
  - 避免无证据价值的重复 `RXN` 调用。

## 5. 当前风险判断

### 5.1 低风险

- 本地依赖安装
- 包导入
- 当前已验证测试的稳定复跑
- Qwen/OpenAI-compatible 参数透传

### 5.2 中风险

- 文献检索链路的实际可用度仍取决于外部 key 与下载链路
- `molbloom` 上游下载源不可达，当前依赖官方 API 回退路径
- `ReactionRetrosynthesis` 对 RXN 限速与节点动作延迟更加敏感

### 5.3 高风险

- 外部服务配额与限速仍可能在后续长链验证中成为不稳定因素

## 6. 下一阶段建议动作

- 继续扩展 agent 级任务样例，覆盖网页搜索与分子推理组合任务。
- 将逆合成在旧配置与新配置下的差异单独保留到最终边界说明。
- 对外部服务波动进行低频监控，避免无证据价值的重复调用。
- 已完成 `PatentCheck` 样例分歧调查，后续应将其写入最终边界说明，避免再把 `cumene` 样例表述为当前条件下的 `Novel`。
- 若继续扩展 agent 样例，优先围绕当前已经稳定的工具组合构建复合任务。
