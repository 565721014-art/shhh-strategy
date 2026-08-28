# 知识库目录结构

- `README.md`：总入口与使用说明。
- `catalog.html`：离线可视化总目录，按题号、题型、母问题和风险筛选。
- `打开知识库.cmd`：双击打开离线总目录。
- `国一论文成品教材/`：Codex首选读取层；包含23个完整题名章节、58篇国一经验、合并总教材、机器清单与终检报告。
- `新题迁移分析引擎/`：任意新题的首选推理层；从 `从这里开始_给Codex.md` 进入，先通过读题理解深度审计，再按结构指纹组合国一经验，并用置信度、冲突裁决、同题多材料对抗审计和通用规则准入防止浅层理解与照搬。
- `problems/`：23道原题，每题包含原题、附件、题目卡和对应国一论文。
- `index/corpus.sqlite`：全文检索数据库。
- `index/corpus_manifest.json`：全库清单与数量统计。
- `index/logic_index.json`：58篇论文的问题分析、章节、术语和视觉页逻辑索引。
- `index/quality_report.md`：完整性和异常检查。
- `index/navigation_quality_report.md`：离线导航、逻辑索引和所有本地链接的终检报告。
- `search.py`：快速全文检索工具。
- `refresh_navigation.py`：由既有语料刷新总目录、题目逻辑索引和视觉缩略页，不重新处理原PDF。
- `audit_navigation.py`：复查23题、58篇逻辑层以及所有HTML本地链接。
