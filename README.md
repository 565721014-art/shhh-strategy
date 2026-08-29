# shhh-strategy

一个面向数学建模竞赛新题的独立读题与建模策略技能。它从完整题面和附件出发，锁定分问交付物、信息边界、变量与约束，建立有证据触发的模型路线，检查可辨识性与验证方式，并设置停止加模型的门槛。

当前版本为 `V27.2 stability-guarded`。它在 V27.1 推理核心上增加来源清单、跨轮状态账本、渐进式结构门路由和可复用行为回归协议，不改变“先独立分析、历史比较仅按明确请求启用”的边界。

## 主要能力

- 完整读取题面、表格、图片和附件后再建模；
- 区分描述、预测、机制、因果、情景和候选结论；
- 对逆问题检查可辨识性、对优化问题检查可行性与目标闭合；
- 允许必要的分支、上下界、独立核验和多阶段路线，但拒绝没有题面触发的复杂度；
- 在形成可执行路线后进行压力测试、完整回读和最小修正；
- 对本地文件生成逐文件 SHA-256、机器元数据和待完成的文本/视觉/公式/数据/结构检查；
- 对长任务保存可校验的题意锁、歧义、路线、质量状态和哈希链，防止跨轮漂移；
- 先读取18项结构门的触发索引，只加载被当前题面证据触发的详细专题，并在路线完成前做全门复扫；
- 默认独立分析新题，不自动搜索或推荐往年获奖论文。

## 安装

将整个 `shhh-strategy` 目录复制到 Codex 技能目录：

```text
<CODEX_HOME>/skills/shhh-strategy/
```

保留 `SKILL.md`、`agents/`、`references/` 和 `scripts/` 的相对结构。

## 历史资料（可选）

核心策略不依赖外部历史资料。仓库附带一个约 8 MB 的文本优先 `knowledge/` 轻量层，包含 23 道题的结构化题目卡、逻辑图、58 篇论文卡、章节教材、迭代记录与检索索引，适合自动读取。原始 PDF、Excel/CSV、逐页图片、整篇 OCR 和其他大体积证据仍应留在本地外接档案中。

若用户明确请求往年题复盘，或需要核对公式、表格、几何和原题附件，可将完整知识库放在 `knowledge/`，或通过环境变量指定：

```text
SHHH_STRATEGY_KNOWLEDGE_ROOT=<archive-root>
```

环境变量指定的路径优先于仓库内轻量层。原始知识库不会由本技能删除或覆盖，也不会随仓库自动公开上传。

### 轻量层的完整性

仓库内轻量层完整保留23道题目卡、23份逻辑图、58篇论文卡与对应分析摘录、23章教材、迭代记录、盲测记录和检索索引。为了可移植读取，只排除原始PDF、表格附件、逐页图片、完整OCR、完整论文正文、缓存和临时产物；这些精确证据通过外接档案按需核对，不属于可公开分发的Skill运行核心。

轻量层使用 `compact_manifest.json` 登记全部文件、字节数和SHA-256。构建脚本统一使用LF换行，验证脚本会逐文件检查清单和哈希，避免格式优化后发生内容漂移。

## 使用边界

本技能输出的是独立读题、建模策略和验证路线，不自动保证竞赛奖项，也不替代数值实现、完整论文排版或投稿合规审查。历史论文比较是明确请求后才启用的独立回顾模式。

## V27.2 稳定性工具

本地题面和附件先建立来源清单：

```bash
python scripts/inventory_problem.py scan --source <problem-path> --output source-inventory.json
python scripts/inventory_problem.py summary source-inventory.json
python scripts/inventory_problem.py mark source-inventory.json --file-id <id> --inspection visual --status complete --note "已逐页检查图、轴、图例和方向"
python scripts/inventory_problem.py validate source-inventory.json --require-complete
```

多附件、多确认点或跨会话任务建立状态账本：

```bash
python scripts/analysis_state.py init --case-id <id> --inventory source-inventory.json --output analysis-state.json
python scripts/analysis_state.py seal analysis-state.json --reason "记录本轮已核对的题意和路线"
python scripts/analysis_state.py transition analysis-state.json --to route_executable --reason "所有分问已有数学产生器和验证接口"
python scripts/analysis_state.py validate analysis-state.json
```

状态文件由模型或使用者按 `references/analysis-state.schema.json` 填充。`seal` 只封存当前语义状态并追加哈希事件，不替代人工或模型判断。维护技能版本时，使用 `references/behavior-regression.md` 与 `scripts/evaluate_regression.py`；开发用例不得冒充盲测证据。

## License

MIT License，详见 [`LICENSE`](LICENSE)。

## 验证

```bash
python scripts/validate_skill.py
python <path-to-skill-creator>/scripts/quick_validate.py .
python scripts/query_knowledge.py "你的机制词" --limit 5
python scripts/stability_self_test.py
```

`validate_skill.py` 会识别轻量模式和完整外接模式：轻量模式逐文件检查结构化层、卡片和清单哈希，完整模式再检查逐页视觉证据和来源哈希。若要从新的完整档案重新生成轻量层：

```bash
python scripts/build_compact_knowledge.py --source <full-knowledge> --destination <new-knowledge>
```
