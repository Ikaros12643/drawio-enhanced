<p align="right">
  <strong>中文</strong> | <a href="./README.md">English</a>
</p>

# Draw.io Enhanced Skill

快速生成可编辑 draw.io 图表的 skill。默认使用轻量网格、边预算和有限手动路由，避免在运行时反复进行坐标优化，让 AI 处理图表的布局、配色、连线和 XML 生成，人专注于内容表达。

## 为什么做这个 Skill

在编写文档的过程中，画图是一件非常繁琐的事。手工绘图往往会耗费大量精力在配色、布局、对齐和连线上，反而让人无法专注于真正重要的内容结构。

已有的画图 skill 大多基于 SVG 或 HTML，生成效果可以很好，但通常难以在 draw.io 中继续手动编辑。draw.io 本身具备优秀的可编辑性和通用性，但内置风格相对有限，自动布局与视觉表现也需要大量手工调整。

因此，`drawio-enhanced` 希望集百家之长：借鉴优秀开源项目在布局算法、视觉风格、XML 生成、质量检查和 AI 编辑方面的经验，让 AI 解放人类，减少机械性的手工劳作。

## 设计目标

1. **可编辑优先** - 输出 `.drawio` 文件，而不是只生成难以二次编辑的 SVG 或 HTML。
2. **内容优先** - 让 AI 负责布局、配色、连线和样式，让用户专注于表达什么。
3. **风格丰富** - 提供多套适合文档、架构、流程、对比和演示场景的视觉风格。
4. **轻量实用** - 使用稳定的网格、边预算和检查规则，避免过度复杂的运行时优化。
5. **面向文档** - 生成的图表应当适合放进技术文档、产品说明、报告和演示材料中。

## 特性

- **14 套视觉风格** - 融合 fireworks-tech-graph、FlowForge、Material Design 与云厂商品牌风格启发
- **轻量网格布局** - 直接放置节点，画布随内容自然扩展
- **边预算与精简** - 主路径优先，复杂关系用合并边、注释、图例表达
- **结构化工作流** - 需求理解 → 风格选择 → ASCII 草图 → 边精简 → XML 生成 → 轻量检查 → 交付
- **颜色预算规则** - 防止“彩虹效应”，保持视觉层次清晰
- **按需参考资料** - 密集图读取边路由参考，质量检查仅在出问题时读取
- **draw.io 原生输出** - 生成可继续在 diagrams.net / draw.io 中手动编辑的 XML 图表

## 文件结构

```text
drawio-enhanced/
├── SKILL.md                          # 主 skill 文件: 工作流、XML 参考、关键规则
├── themes/                           # 14 套样式定义: 色板、节点样式、箭头样式、文字样式
├── drawio-style-examples.md          # 6 套完整 XML 示例: 可直接复制使用
├── drawio-layout-algorithms.md       # 复杂布局参考: 坐标公式、适用场景
├── drawio-quality-checklist.md       # 故障排查清单: 布局/文本/XML/样式
├── examples/
│   ├── flow-flat-icon.drawio         # 流程图: flat-icon 风格
│   ├── compare-openai.drawio         # 对比图: openai 风格
│   └── architecture-tech-blue.drawio # 架构图: tech-blue 风格
├── README.md                         # 英文 README
└── README_ZH.md                      # 中文 README
```

## 快速开始

1. 将 `drawio-enhanced/` 文件夹复制到你的 skills 目录
2. 在对话中引用：`使用 drawio-enhanced skill 生成图表`
3. 或直接描述需求：`画一个 CI/CD 流程图，用 openai 风格`

## 风格列表

| # | 名称 | 来源 | 最佳场景 |
|---|------|------|---------|
| 1 | flat-icon | fireworks-tech-graph | 博客、文档、演示（默认） |
| 2 | dark-terminal | fireworks-tech-graph | 技术博客、开发者文档 |
| 3 | blueprint | fireworks-tech-graph | 正式架构文档、技术规范 |
| 4 | notion | fireworks-tech-graph | 文档内嵌、笔记、知识库 |
| 5 | glassmorphism | fireworks-tech-graph | 产品演示、演讲、官网 |
| 6 | claude | fireworks-tech-graph | Anthropic 风格演示 |
| 7 | openai | fireworks-tech-graph | API 文档、技术报告 |
| 8 | tech-blue | FlowForge | 技术内容、现代设计（默认） |
| 9 | morandi | FlowForge | 高级感、低调优雅 |
| 10 | mint | FlowForge | 清新、轻松设计 |
| 11 | terracotta | FlowForge | 商务、战略内容 |
| 12 | indigo | FlowForge | bold、权威设计 |
| 13 | material | Material Design | 正式文档、演示、产品流程 |
| 14 | cloud-brand | 云厂商品牌 | AWS/Azure/GCP 云架构图 |

## 图表类型

flow, flow-vertical, compare, layers, loop, tree, hub, columns, matrix, funnel, timeline, sequence

## 设计原则

1. **结构决定内容** - 先确认 ASCII 草图，再生成 XML
2. **网格决定布局** - 使用简单网格直接放置，画布随内容扩展
3. **主题决定颜色** - 从主题色板选色，不随机十六进制
4. **少边优先清晰** - 边过多时删减、合并或改成注释，不把所有关系都连出来
5. **可编辑性优先于装饰性** - 优先使用 draw.io 原生形状、文本和连接器，保证后续可维护

## 致谢

`drawio-enhanced` 受到多个优秀开源项目的启发。感谢这些项目及其作者为 AI 图表生成、draw.io 集成和技术图表设计所做的贡献。

- **[jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)** - 提供了 draw.io MCP 集成、CLI 导出、浏览器 URL 生成、基础 XML 骨架和跨平台处理思路。
- **[FlowForge](https://github.com/wentong2022-arch/flowforge-skill)** - 在布局算法、颜色预算、主题色板、ASCII 草图流程、质量检查和技术图表设计方法上提供了重要启发。
- **[fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)** - 其 SVG 技术图表系统中的语义形状、语义箭头、视觉风格、图标库和避障路由思路，为 draw.io 风格扩展提供了参考。
- **[DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io)** - 在 AI 驱动 draw.io 编辑、XML 校验修复、形状库、版本历史、MCP 架构和视觉校验流程方面提供了有价值的工程参考。
