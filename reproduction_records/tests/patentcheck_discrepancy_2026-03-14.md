# PatentCheck 分歧调查

## 1. 记录目的

本文件用于调查 `tests/test_search.py::test_patentcheck_molset` 与当前 `SureChEMBL` 官方数据之间的分歧来源。

## 2. 调查对象

仓库测试中的关键分歧样例：

- `CC(C)c1ccccc1`

配套参照样例：

- `Cn1c(=O)c2c(ncn2C)n(C)c1=O`
- `CCCCCCCCC[NH+]1C[C@@H]([C@H]([C@@H]([C@H]1CO)O)O)O`

## 3. 调查方法

- 使用 `SureChEMBL` 官方结构检索 API。
- 检索方式：`exact structure`
- 对 exact 命中的 `chemical_id` 再请求 `documents_for_structures`。

原始输出文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/investigate_patentcheck_discrepancy.out`

脚本文件：

- `/root/autodl-tmp/chemcrow-public-main/reproduction_records/tests/investigate_patentcheck_discrepancy.py`

## 4. 调查结果

### 4.1 caffeine

- exact structure 总命中：`1`
- exact structure id：`5671`
- 文档总数：`155781`

结论：

- 当前官方数据明确支持 `Patented`

### 4.2 choline_like_testcase

- exact structure 总命中：`0`
- exact structure id：空

结论：

- 当前官方数据明确支持 `Novel`

### 4.3 cumene

- exact structure 总命中：`3`
- 与输入完全相同的 exact structure id：
  - `11254813`
  - `6568`
- 其中：
  - `11254813` 的文档查询返回 `500`
  - `6568` 的文档查询返回 `200`
  - `6568` 的文档总数为 `89523`

结论：

- 当前官方数据支持 `cumene` 被 `SureChEMBL` 收录。
- 至少存在一个与输入完全相同的 exact structure id 可以稳定返回大量专利文档。

## 5. 对分歧的当前解释

当前最稳妥的解释为：

- 仓库测试快照中的 `Novel` 结论与 `2026-03-14` 的官方数据状态不一致。
- 这更符合外部专利语料时间漂移或上游索引演化，当前证据不足以支持将该现象直接归结为当前工具实现错误。

当前不宜写成：

- 当前 `PatentCheck` 已与仓库历史测试完全一致。

当前可以写成：

- 当前 `PatentCheck` 的 SureChEMBL 官方数据回退路径在 `caffeine`、`choline_like_testcase`、`cumene` 三个代表性样例上给出了自洽结果。
- 其中 `cumene` 与仓库测试期望存在时间快照分歧。

## 6. 当前边界

- 当前调查基于 `SureChEMBL` 官方 API 的当前返回。
- 当前调查不证明仓库测试期望是错误的。
- 当前调查证明的是：在 `2026-03-14` 当前官方数据条件下，`cumene` 不能被稳妥地写成 `Novel`。
