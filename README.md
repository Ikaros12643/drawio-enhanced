<p align="right">
  <a href="./README_ZH.md">中文</a> | <strong>English</strong>
</p>

# Draw.io Enhanced Skill

A skill for quickly generating editable draw.io diagrams. It uses a lightweight grid, an edge budget, and limited manual routing by default, avoiding repeated runtime coordinate optimization so AI can handle layout, color, connectors, and XML generation while humans focus on content.

## Why This Skill Exists

Creating diagrams while writing documentation is tedious. Manual diagramming often consumes too much energy on colors, layout, alignment, and connector routing, which distracts from the actual information structure.

Many existing diagram-generation skills are based on SVG or HTML. They can produce good-looking results, but the output is usually difficult to edit manually in draw.io. draw.io itself has excellent editability and broad adoption, but its built-in styles are relatively limited, and polished layouts still require a lot of manual work.

`drawio-enhanced` was created to combine the strengths of multiple excellent open-source projects: layout algorithms, visual styles, XML generation, quality checks, and AI-assisted editing. The goal is to let AI free humans from repetitive manual work and keep the author focused on the message.

## Design Goals

1. **Editability first** - Output `.drawio` files instead of SVG or HTML that are hard to revise later.
2. **Content first** - Let AI handle layout, color, connectors, and style while users focus on what to communicate.
3. **Rich visual styles** - Provide multiple styles for documentation, architecture diagrams, flows, comparisons, and presentations.
4. **Lightweight and practical** - Use stable grids, edge budgets, and checking rules instead of overly complex runtime optimization.
5. **Documentation-oriented** - Generate diagrams that fit technical docs, product notes, reports, and slide decks.

## Features

- **16 visual styles** - Inspired by fireworks-tech-graph, FlowForge, Material Design, GPT Image-style architecture diagrams, Visio-style engineering flows, and cloud vendor brand styles
- **Lightweight grid layout** - Places nodes directly and lets the canvas expand naturally with content
- **Edge budget and simplification** - Prioritizes the main path and uses merged edges, notes, or legends for complex relationships
- **Structured workflow** - Requirement understanding → style selection → ASCII sketch → edge simplification → XML generation → lightweight checks → delivery
- **Color budget rules** - Prevents the “rainbow effect” and keeps visual hierarchy clear
- **Structural validation script** - Checks generated `.drawio` XML, IDs, edge endpoints, and geometry before delivery when Python is available
- **References on demand** - Reads dense edge-routing references and quality checklists only when needed
- **Native draw.io output** - Generates XML diagrams that can continue to be edited manually in diagrams.net / draw.io

## File Structure

```text
drawio-enhanced/
├── SKILL.md                          # Main skill file: workflow, XML reference, key rules
├── themes/                           # 16 style definitions: palettes, node styles, edge styles, text styles
├── drawio-style-examples.md          # 6 complete XML examples, ready to copy
├── drawio-layout-algorithms.md       # Complex layout reference: coordinate formulas and use cases
├── drawio-quality-checklist.md       # Troubleshooting checklist: layout, text, XML, style
├── scripts/check-drawio.py           # Structural validation for generated .drawio files
├── examples/
│   ├── flat-icon-cicd-flow.drawio              # Flow diagram in flat-icon style
│   ├── gpt-image-architecture-sample.drawio    # Layered architecture in GPT Image style
│   └── visio-minimal-sample.drawio             # Minimal Visio-style engineering flow
├── README.md                         # English README
└── README_ZH.md                      # Chinese README
```

## Quick Start

1. Copy the `drawio-enhanced/` folder into your skills directory
2. Reference it in a conversation: `use the drawio-enhanced skill to generate a diagram`
3. Or describe the request directly: `draw a CI/CD flowchart in the openai style`

## Style List

| # | Name | Source | Best For |
|---|------|--------|----------|
| 1 | flat-icon | fireworks-tech-graph | Blogs, docs, presentations (default) |
| 2 | dark-terminal | fireworks-tech-graph | Technical blogs, developer docs |
| 3 | blueprint | fireworks-tech-graph | Formal architecture docs, technical specifications |
| 4 | notion | fireworks-tech-graph | Embedded docs, notes, knowledge bases |
| 5 | glassmorphism | fireworks-tech-graph | Product demos, talks, websites |
| 6 | claude | fireworks-tech-graph | Anthropic-style presentations |
| 7 | openai | fireworks-tech-graph | API docs, technical reports |
| 8 | tech-blue | FlowForge | Technical content, modern design (default) |
| 9 | morandi | FlowForge | Premium, subtle, elegant diagrams |
| 10 | mint | FlowForge | Fresh, lightweight designs |
| 11 | terracotta | FlowForge | Business and strategy content |
| 12 | indigo | FlowForge | Bold, authoritative diagrams |
| 13 | material | Material Design | Formal docs, presentations, product flows |
| 14 | cloud-brand | Cloud vendor brands | AWS/Azure/GCP cloud architecture diagrams |
| 15 | gpt-image-architecture | GPT Image-style architecture | Formal layered architecture, platform capability maps, data platform diagrams |
| 16 | visio-minimal | Visio-style minimalism | Clean engineering flows, operations procedures, low-decoration process diagrams |

## Diagram Types

flow, flow-vertical, compare, layers, loop, tree, hub, columns, matrix, funnel, timeline, sequence

## Design Principles

1. **Structure determines content** - Confirm the ASCII sketch before generating XML
2. **Grid determines layout** - Use a simple grid and let the canvas expand with content
3. **Theme determines color** - Select colors from the theme palette instead of random hex values
4. **Fewer edges are clearer** - When there are too many edges, reduce, merge, or turn them into notes instead of connecting everything
5. **Editability over decoration** - Prefer native draw.io shapes, text, and connectors to keep diagrams maintainable

## Acknowledgements

`drawio-enhanced` is inspired by several excellent open-source projects. Thanks to these projects and their authors for their contributions to AI diagram generation, draw.io integration, and technical diagram design.

- **[jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)** - Inspired the draw.io MCP integration, CLI export flow, browser URL generation, basic XML skeleton, and cross-platform handling.
- **[FlowForge](https://github.com/wentong2022-arch/flowforge-skill)** - Provided valuable ideas for layout algorithms, color budgets, theme palettes, ASCII sketching, quality checks, and technical diagram design workflows.
- **[fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)** - Its SVG technical diagram system, including semantic shapes, semantic arrows, visual styles, icon libraries, and obstacle-aware routing, informed the draw.io style expansion.
- **[DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io)** - Provided useful engineering references for AI-driven draw.io editing, XML validation and repair, shape libraries, version history, MCP architecture, and visual validation workflows.

This project is not intended to replace those projects. It absorbs their design ideas and combines them around one goal: editable draw.io diagrams that are more useful for documentation workflows.
