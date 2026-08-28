# shhh-strategy

一个面向数学建模竞赛新题的独立读题与建模策略技能。它从完整题面和附件出发，锁定分问交付物、信息边界、变量与约束，建立有证据触发的模型路线，检查可辨识性与验证方式，并设置停止加模型的门槛。

## 主要能力

- 完整读取题面、表格、图片和附件后再建模；
- 区分描述、预测、机制、因果、情景和候选结论；
- 对逆问题检查可辨识性、对优化问题检查可行性与目标闭合；
- 允许必要的分支、上下界、独立核验和多阶段路线，但拒绝没有题面触发的复杂度；
- 在形成可执行路线后进行压力测试、完整回读和最小修正；
- 默认独立分析新题，不自动搜索或推荐往年获奖论文。

## 安装

将整个 `shhh-strategy` 目录复制到 Codex 技能目录：

```text
<CODEX_HOME>/skills/shhh-strategy/
```

保留 `SKILL.md`、`agents/`、`references/` 和 `scripts/` 的相对结构。

## 历史资料（可选）

核心策略不依赖外部历史资料。若用户明确请求往年题复盘，可将具有相同结构的知识库放在 `knowledge/`，或通过环境变量指定：

```text
SHHH_STRATEGY_KNOWLEDGE_ROOT=<archive-root>
```

知识库不是本仓库的默认内容；本仓库不包含私人或受版权约束的整套论文档案。

## 使用边界

本技能输出的是独立读题、建模策略和验证路线，不自动保证竞赛奖项，也不替代数值实现、完整论文排版或投稿合规审查。历史论文比较是明确请求后才启用的独立回顾模式。

## License

MIT License，详见 [`LICENSE`](LICENSE)。

## 验证

```bash
python scripts/validate_skill.py
python <path-to-skill-creator>/scripts/quick_validate.py .
```

没有可选知识库时，`validate_skill.py` 会报告警告，但仍验证核心技能文件。
