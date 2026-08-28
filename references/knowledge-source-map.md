# Local Knowledge Source Map

## Root and override

Default archive root:

`knowledge` (optional directory beside this skill)

For portability, set environment variable `SHHH_STRATEGY_KNOWLEDGE_ROOT` to another archive root with the same structure. If the archive is unavailable, the skill's core protocol and 34-case transfer index remain usable, but exact paper/page verification is unavailable and must not be invented.

## Coverage

- 23 primary training problems;
- 58 paper records;
- 2,876 paper pages;
- 47 statement pages;
- 97 attachments;
- 1,494 visually indexed evidence pages;
- 2018B pilot plus 5 held-out and 5 historical isolated cases;
- 34-case anti-overpruning replay.

## Authoritative manifests

| Purpose | Path relative to root |
|---|---|
| complete paper/chapter inventory | `国一论文成品教材/textbook_manifest.json` |
| all local problem and paper card paths | `index/corpus_manifest.json` |
| sequential 23-problem/58-paper training order | `迭代训练/iteration_manifest.json` |
| per-problem iteration records | `迭代训练/records/*.json` |
| 23 chapter textbook | `国一论文成品教材/chapters/*.md` |
| original problem cards and logic maps | `problems/<ID>/problem_card.md`, `logic_map.json`, `data_structure.md` |
| paper cards and visual galleries | `problems/<ID>/papers/<paper>/paper_card.md`, `gallery.html` |
| held-out evaluation | `heldout_evaluation/heldout_evaluation_summary.md` |
| 2016–2017 pre-unlock freeze | `AI时代读题训练/v27_blind_freeze_2016_2017.md` |
| 2016–2017 unlocked comparison | `AI时代读题训练/v27_unlocked_comparison_2016_2017.md` |
| V27.1 historical anti-overpruning matrix | `model_versions/v27_1_complexity_guarded/往届34题防误删训练.md` |

## Runtime engine sources

Read these only for maintenance or when a skill behavior cannot be explained by the packaged references:

- `model_versions/v26_post_23_iteration_frozen/任意新题分析协议.md`
- `model_versions/v26_post_23_iteration_frozen/读题理解深度审计.md`
- `model_versions/v26_post_23_iteration_frozen/置信度_冲突与缺失信息协议.md`
- `model_versions/v26_post_23_iteration_frozen/模型组件与国一经验库.md`
- `model_versions/v26_post_23_iteration_frozen/新题分析输出规范.md`
- `model_versions/v26_post_23_iteration_frozen/对抗性误判测试.md`
- `model_versions/v27_formal_problem_reader/从这里开始_给Codex.md`
- `model_versions/v27_1_complexity_guarded/复杂度_证据_停止门.md`

Do not load all files for an ordinary new problem. The packaged references contain the operational rules. Use the source archive for precise evidence and maintenance.

## Primary 23-problem paper routing

| ID | Title | Paper IDs | Chapter |
|---|---|---:|---|
| 2020A | 炉温曲线 | 01 | `chapters/01_炉温曲线.md` |
| 2020C | 中小微企业的信贷决策 | 02–03 | `chapters/02_中小微企业的信贷决策.md` |
| 2021A | FAST主动反射面的形状调节 | 04–06 | `chapters/03_FAST主动反射面的形状调节.md` |
| 2021B | 乙醇偶合制备C4烯烃 | 07–10 | `chapters/04_乙醇偶合制备C4烯烃.md` |
| 2021C | 生产企业原材料的订购与运输 | 11–14 | `chapters/05_生产企业原材料的订购与运输.md` |
| 2021D | 连铸切割的在线优化 | 15–17 | `chapters/06_连铸切割的在线优化.md` |
| 2021E | 中药材的鉴别 | 18–20 | `chapters/07_中药材的鉴别.md` |
| 2022C | 古代玻璃制品的成分分析与鉴别 | 21–22 | `chapters/08_古代玻璃制品的成分分析与鉴别.md` |
| 2023A | 定日镜场的优化设计 | 23–25 | `chapters/09_定日镜场的优化设计.md` |
| 2023B | 多波束测线问题 | 26–28 | `chapters/10_多波束测线问题.md` |
| 2023C | 蔬菜类商品的自动定价与补货决策 | 29–31 | `chapters/11_蔬菜类商品的自动定价与补货决策.md` |
| 2023D | 圈养湖羊的空间利用率 | 32 | `chapters/12_圈养湖羊的空间利用率.md` |
| 2023E | 黄河水沙监测数据分析 | 33–34 | `chapters/13_黄河水沙监测数据分析.md` |
| 2024A | 板凳龙闹元宵 | 35–39 | `chapters/14_板凳龙闹元宵.md` |
| 2024B | 生产过程中的决策问题 | 40–42 | `chapters/15_生产过程中的决策问题.md` |
| 2024C | 农作物的种植策略 | 43–46 | `chapters/16_农作物的种植策略.md` |
| 2024D | 反潜航空深弹命中概率问题 | 47 | `chapters/17_反潜航空深弹命中概率问题.md` |
| 2024E | 交通流量管控 | 48–50 | `chapters/18_交通流量管控.md` |
| 2025A | 烟幕干扰弹的投放策略 | 51 | `chapters/19_烟幕干扰弹的投放策略.md` |
| 2025B | 碳化硅外延层厚度的确定 | 52–54 | `chapters/20_碳化硅外延层厚度的确定.md` |
| 2025C | NIPT的时点选择与胎儿异常判定 | 55–56 | `chapters/21_NIPT的时点选择与胎儿异常判定.md` |
| 2025D | 矿井突水水流漫延模型与逃生方案 | 57 | `chapters/22_矿井突水水流漫延模型与逃生方案.md` |
| 2025E | 立定跳远动作技术分析与训练建议 | 58 | `chapters/23_立定跳远动作技术分析与训练建议.md` |

The textbook manifest is the source of exact titles, page counts, visual counts, and paper-card paths. Prefer it over OCR titles in less-curated indexes.

## Retrieval discipline

1. Form the current problem's independent mother problem and structural triggers.
2. Run `scripts/query_knowledge.py` with mechanism terms, not the historical title.
3. Read only the top relevant problem/iteration cards.
4. Open individual paper cards or galleries only for a precise formula, figure, implementation detail, or claimed result.
5. Record what the history tests; never transfer constants, answers, or unsupported assumptions.
