# Draw.io Enhanced Skill

融合三家之长的全能型 drawio 图表生成 skill。

## 特性

- **12 套视觉风格** — 7 套源自 fireworks-tech-graph (SVG 转换) + 5 套源自 FlowForge，统一整合
- **12 种布局算法** — 流程图、对比图、架构图、时序图、思维导图等全覆盖
- **结构化工作流** — 需求理解 → 风格选择 → ASCII 草图确认 → 坐标计算 → XML 生成 → 质量检查 → 交付
- **颜色预算规则** — 防止"彩虹效应"，保持视觉层次清晰
- **16 项质量检查** — 布局、文本、XML、样式全方位验证

## 文件结构

```
drawio-enhanced/
├── SKILL.md                          # 主 skill 文件 — 工作流、XML 参考、关键规则
├── drawio-themes.md                  # 12 套样式定义 — 色板、节点样式、箭头样式、文字样式
├── drawio-style-examples.md          # 6 套完整 XML 示例 — 可直接复制使用
├── drawio-layout-algorithms.md       # 12 种布局算法 — 坐标公式、适用场景
├── drawio-quality-checklist.md       # 16 项质量检查 — 布局/文本/XML/样式
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
2. **公式决定坐标** — 使用布局算法公式，不手动计算
3. **主题决定颜色** — 从主题色板选色，不随机十六进制
4. **检查决定交付** — 16 项质量检查全部通过后才交付
