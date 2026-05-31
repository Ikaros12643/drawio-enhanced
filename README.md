# Draw.io Enhanced Skill

快速生成可编辑 draw.io 图表的 skill。默认使用轻量网格、边预算和有限手动路由，避免在运行时反复进行坐标优化。

## 特性

- **12 套视觉风格** — 7 套源自 fireworks-tech-graph (SVG 转换) + 5 套源自 FlowForge，统一整合
- **轻量网格布局** — 直接放置节点，画布随内容自然扩展
- **边预算与精简** — 主路径优先，复杂关系用合并边、注释、图例表达
- **结构化工作流** — 需求理解 → 风格选择 → ASCII 草图 → 边精简 → XML 生成 → 轻量检查 → 交付
- **颜色预算规则** — 防止"彩虹效应"，保持视觉层次清晰
- **按需参考资料** — 密集图读取边路由参考，质量检查仅在出问题时读取

## 文件结构

```
drawio-enhanced/
├── SKILL.md                          # 主 skill 文件 — 工作流、XML 参考、关键规则
├── drawio-themes.md                  # 12 套样式定义 — 色板、节点样式、箭头样式、文字样式
├── drawio-style-examples.md          # 6 套完整 XML 示例 — 可直接复制使用
├── drawio-layout-algorithms.md       # 复杂布局参考 — 坐标公式、适用场景
├── drawio-quality-checklist.md       # 故障排查清单 — 布局/文本/XML/样式
├── examples/
│   ├── flow-flat-icon.drawio         # 流程图 — flat-icon 风格
│   ├── compare-openai.drawio         # 对比图 — openai 风格
│   └── architecture-tech-blue.drawio # 架构图 — tech-blue 风格
└── README.md                         # 本文件
```

## 快速开始

1. 将 `drawio-enhanced/` 文件夹复制到你的 skills 目录
2. 在对话中引用：`使用 drawio-enhanced skill 生成图表`
3. 或直接描述需求：`画一个 CI/CD 流程图，用 openai 风格`

## 风格列表

| # | 名称 | 来源 | 最佳场景 |
|---|------|------|---------|
| 1 | flat-icon | fireworks | 博客、文档、演示 (默认) |
| 2 | dark-terminal | fireworks | 技术博客、开发者文档 |
| 3 | blueprint | fireworks | 正式架构文档、技术规范 |
| 4 | notion | fireworks | 文档内嵌、笔记、知识库 |
| 5 | glassmorphism | fireworks | 产品演示、演讲、官网 |
| 6 | claude | fireworks | Anthropic 风格演示 |
| 7 | openai | fireworks | API 文档、技术报告 |
| 8 | tech-blue | FlowForge | 技术内容、现代设计 (默认) |
| 9 | morandi | FlowForge | 高级感、低调优雅 |
| 10 | mint | FlowForge | 清新、轻松设计 |
| 11 | terracotta | FlowForge | 商务、战略内容 |
| 12 | indigo | FlowForge | bold、权威设计 |

## 图表类型

flow, flow-vertical, compare, layers, loop, tree, hub, columns, matrix, funnel, timeline, sequence

## 设计原则

1. **结构决定内容** — 先确认 ASCII 草图，再生成 XML
2. **网格决定布局** — 使用简单网格直接放置，画布随内容扩展
3. **主题决定颜色** — 从主题色板选色，不随机十六进制
4. **少边优先清晰** — 边过多时删减、合并或改成注释，不把所有关系都连出来
