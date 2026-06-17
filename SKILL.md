---
name: drawio-enhanced
description: >
  Generate editable draw.io diagrams quickly with a lightweight workflow, visual themes, and reusable XML templates.
  Use when the user asks for draw.io/.drawio output, flowcharts, architecture diagrams, sequence diagrams, comparison charts, timelines, mind maps, or technical process diagrams.
  Trigger on: "draw a diagram", "create a flowchart", "architecture diagram", "sequence diagram", "compare A vs B", "show the pipeline", "visualize the process", "make a chart", "diagram", "流程图", "架构图", "示意图", or any request to illustrate technical content.
  Also trigger when the user provides a document and asks for diagrams to be inserted, or mentions drawio/.drawio files.
  Prefer simple grid placement, sparse readable edges, and limited manual routing for dense diagrams. Do not perform detailed coordinate optimization unless explicitly requested.
---
# Draw.io Enhanced

融合轻量工作流 + 14 套视觉风格 + draw.io XML 模板 + 故障排查资料的图表生成 skill。
默认目标是快速生成可打开、可编辑、结构清晰的 `.drawio` 文件；精确坐标优化仅在用户明确要求或排查渲染问题时进行。

## 工作流

### 步骤 1: 理解需求

**如果给定文档**：

1. 阅读完整文档
2. 识别 1-3 个适合用图表表达的位置
3. 对每个位置列出：插入位置、图表主题、推荐图表类型
4. 如果插图位置会改变文档结构，等待用户确认；否则选择最合理的位置继续

**如果直接给出概念**：

1. 确认要传达的核心信息
2. 选择图表类型 (见下方图表类型参考)
3. 进入步骤 2

### 步骤 2: 选择风格

根据图表类型和用户场景，从 `themes/` 目录中推荐 2-3 个最匹配的风格（见下方风格推荐矩阵）。

如果用户要求云厂商架构图，且明确指定 AWS、Azure 或 GCP，使用 `themes/cloud-brand.md` 中对应厂商的色板。如果用户只说“云架构图”但没有指定厂商，先询问使用哪个云厂商，不要默认猜测。

如果用户未指定风格，直接使用推荐矩阵中的 `flat-icon` 风格。在用户明确要求选择、对风格敏感、或图表用于正式交付时询问确认。

完整风格定义见 `themes/{name}.md`。

### 步骤 3: ASCII 草图

生成 ASCII 草图，展示所有节点及标签、箭头方向及标签、分组/区域、颜色角色分配、近似尺寸和布局方向。同时标出哪些边是主路径、哪些边可以省略或合并。

示例：

```
Direction: left-to-right | Nodes: 4 | Type: flow

[primary] Code Commit  →  [process] Build  →  [process] Test  →  [success] Deploy
                                                    ↓ (fail)
                                              [accent] Alert
```

如果用户已经明确要求直接生成文件，不要停在草图确认；将草图作为内部结构检查后继续生成 XML。只有在图表结构含糊、节点很多、或将插入现有文档时才暂停等待确认。

### 步骤 4: 边预算与精简

整体观感优先于完整表达所有关系。生成 XML 前先精简边：

- 只保留对读者理解结构必要的边：主流程、关键依赖、跨层调用、异常/反馈路径。
- 节点数 `n <= 8`：边数尽量不超过 `n + 2`。
- 节点数 `n > 8`：边数尽量不超过 `1.5n`，复杂系统图优先使用分组、说明文字、图例、编号或虚线区域表达次要关系。
- 同一组节点之间有多条同类关系时，合并为一条带标签的边，不画多条平行边。
- 全局关系、弱关联、背景依赖不要逐条连线；用容器标题、注释、图例、颜色、虚线框或“代表性边”表达。
- 如果边让图变乱，删除次要边，而不是继续添加 waypoint。
- 对于密集架构图，先画横向/纵向主干通道，再把少量关键节点接入主干。

### 步骤 5: 布局放置

使用固定网格快速放置节点，不要在回复或内部推理中展开逐点坐标计算。

默认网格：

- 起点：`x=40, y=80`
- 列间距：180px
- 行间距：120px
- 普通节点：140x60
- 富文本节点：180x80
- 决策节点：140x80
- 短标签/状态节点：120x40

布局原则：

- 节点超过 6 个时优先换行、分组或改用垂直/分层布局，不要压缩到固定画布范围。
- 画布随内容自然扩展；不要限制在固定 X/Y 范围内。
- 坐标只需整齐、可读、可编辑；不追求像素级最优。
- 仅当用户要求严格布局、复杂树形/矩阵/时序图，或默认网格无法表达结构时，读取 `drawio-layout-algorithms.md`。
- 相邻层之间保留明显的水平或垂直“边通道”。不要把节点排成让大量边斜穿中间节点的形态。
- 对于层级架构图，优先让边在层与层之间垂直流动；跨列关系尽量减少，必要时放到层外侧绕行。

### 步骤 6: 边路由规划

在生成边之前做一次有限路由规划，目标是少而清楚，不是完全最优。

默认策略：

- 简单图：边只写 `source` / `target` + `edgeStyle=orthogonalEdgeStyle`。
- 层级图：主路径使用中心到中心的自然连接点，如上到下用底部到顶部，左到右用右侧到左侧。
- 密集图：对主路径和跨层长边显式设置 `exitX/Y`、`entryX/Y`；对次要边使用虚线或删除。
- 返回边、跨越多个分组的边、会穿过中间节点的边，优先沿画布外侧或分组外侧路由。
- 每条手动路由边最多使用 2 个 waypoint；超过 2 个仍然很乱时，删边或改成注释/图例。

需要避免：

- 不要让一条边穿过非源/非目标节点。
- 不要画大量横贯全图的虚线。
- 不要为弱关系添加长距离连线。
- 不要让多个边标签堆在同一条水平线上。

只有在边数较多、层级复杂、或主路径需要明确表达时，读取 `references/edge-routing.md`。

### 步骤 7: 生成 XML

1. 使用元素模板 (见 `references/xml-templates.md`)
2. 应用风格定义的样式字符串 (见 `themes/{name}.md`)
3. 应用边样式模板 (见 `references/edge-styles.md`)
4. 需要特殊形状时参考形状库 (见 `references/shape-library.md`)
5. 确保 XML 格式正确 (无注释、实体已转义、ID 唯一)
6. 按“边路由规划”生成边：简单边交给 draw.io，关键边显式指定连接点，必要时少量 waypoint
7. 如果一条边需要复杂绕行，先考虑删除、合并、改成注释或放入图例

**⚠️ 关键转义规则**：

- 如果 `value` 属性包含 HTML 标签（如 `<font>`、`<b>`），标签内的所有双引号必须转义为 `&quot;`
- 正确示例：`value="Text&lt;br&gt;&lt;font color=&quot;#6e6e80&quot;&gt;Author&lt;/font&gt;"`
- 错误示例：`value="Text&lt;br&gt;&lt;font color="#6e6e80"&gt;Author&lt;/font&gt;"` （会导致 XML 解析失败）

### 步骤 8: 轻量交付检查

交付前只检查这些会导致文件不可用的问题：

- XML 格式合法
- `id` 唯一
- 边的 `source` / `target` 都存在
- 每条边包含 `<mxGeometry relative="1" as="geometry"/>`
- 节点没有明显重叠
- 没有明显穿越节点的主路径边
- 边数没有压过节点和分组的可读性

不要为了间距细节、文本估算宽度或配色微调反复重算坐标。若边过多或明显穿插，优先精简边；不要通过继续加 waypoint 解决所有关系。

`drawio-quality-checklist.md` 仅作为故障排查资料：当用户反馈图表打不开、渲染异常、节点明显重叠、文本严重溢出、或导出失败时再读取。

### 步骤 9: XML 自修复 (可选)

如果生成的 XML 有语法问题，使用 `scripts/fix-xml.py` 自动修复：

如果 `uv`可用，优先使用uv，否则回退到使用 `python`

```
uv run scripts/fix-xml.py input.xml output.xml
```

```
python scripts/fix-xml.py input.xml output.xml
```

支持 24 步自修复：JSON 转义、重复 ID、嵌套 mxCell、未闭合标签、非法字符等。

### 步骤 10: 保存与交付

保存 `.drawio` 文件到 `./diagrams/{diagram-name}.drawio` 或用户指定路径。

**如果用户要求导出** (PNG/SVG/PDF)：

1. 检测环境并定位 draw.io CLI (见 `references/usage-guide.md`)
2. 使用 `--embed-diagram` 导出，保留可编辑性
3. 导出成功后删除中间 `.drawio` 文件

**打开文件**：使用对应平台的打开命令 (见 `references/usage-guide.md`)。如果命令失败，打印绝对文件路径。

### 迭代

如果用户需要修改：读取当前文件 → 按反馈修改 XML → 保存为 `{name}_v2.drawio`。

---

## 图表类型参考

| 类型     | 代码              | 适用场景         |
| -------- | ----------------- | ---------------- |
| 线性流程 | `flow`          | 顺序步骤 A→B→C |
| 垂直流程 | `flow-vertical` | 自上而下的过程   |
| 对比     | `compare`       | A vs B 并排对比  |
| 层级堆叠 | `layers`        | 技术栈分层       |
| 循环     | `loop`          | 迭代过程         |
| 树形     | `tree`          | 层级结构、分类法 |
| 中心辐射 | `hub`           | 核心概念 + 分支  |
| 平行列   | `columns`       | 3+ 并行概念      |
| 矩阵     | `matrix`        | 多维度对比       |
| 漏斗     | `funnel`        | 过滤、转化       |
| 时间线   | `timeline`      | 版本演进、历史   |
| 时序图   | `sequence`      | 组件交互         |

### 选择指南

| 内容模式           | 推荐类型                      |
| ------------------ | ----------------------------- |
| 顺序步骤           | `flow` 或 `flow-vertical` |
| 两件事对比         | `compare`                   |
| 3+ 并行概念        | `columns` 或 `hub`        |
| 分层系统           | `layers`                    |
| 迭代/循环过程      | `loop`                      |
| 一个核心，多个分支 | `hub` 或 `tree`           |
| 组件通信           | `sequence`                  |
| 随时间变化         | `timeline`                  |
| 多标准评估         | `matrix`                    |
| 渐进过滤           | `funnel`                    |

---

## 风格推荐矩阵

| 图表类型       | 推荐风格                                             |
| -------------- | ---------------------------------------------------- |
| 架构图         | flat-icon, openai, material, blueprint, tech-blue    |
| 云厂商架构图   | cloud-brand（需指定 AWS/Azure/GCP）, blueprint, tech-blue |
| 流程图         | flat-icon, material, tech-blue, mint, terracotta     |
| 对比图         | openai, material, notion, tech-blue, morandi         |
| 时序图         | openai, material, notion, blueprint, tech-blue       |
| UML 类图       | openai, material, notion, blueprint, morandi         |
| ER 图          | openai, material, notion, blueprint, tech-blue       |
| 网络拓扑       | flat-icon, blueprint, tech-blue, indigo              |
| 思维导图       | flat-icon, notion, mint, indigo                      |
| 数据流图       | flat-icon, blueprint, tech-blue, indigo              |
| 时间线         | flat-icon, notion, mint, tech-blue                   |
| Agent 架构     | flat-icon, openai, glassmorphism, claude             |

---

## 边路由策略

边的视觉清晰度是图表质量的一部分。默认先控制边数量，再决定是否手动路由。

边精简优先级：

1. 保留主路径和关键跨层关系。
2. 合并同类边为一条带标签边。
3. 用分组、颜色、注释、图例表达弱关系。
4. 删除不影响理解的次要边。

简单图可使用 draw.io 自动路由。生成简单边时只需要：

- `edgeStyle=orthogonalEdgeStyle`
- `source`
- `target`
- `<mxGeometry relative="1" as="geometry"/>`

密集图、层级架构图、跨层长边需要有限手动路由：

- 按流向设置自然连接点：上到下、左到右、右到左、下到上。
- 主路径用实线，弱关系用虚线，背景关联用图例或注释替代。
- 跨多个分组的边沿外侧绕行，不穿过中间节点。
- 每条手动边最多 2 个 waypoint。
- 如果边仍然混乱，删边或合并边，而不是继续增加路径点。

`references/edge-routing.md` 可在生成密集图或排查边穿越时读取。

### 边样式模板

详见 `references/edge-styles.md`。

| 类型 | 关键样式                                                         |
| ---- | ---------------------------------------------------------------- |
| 标准 | `edgeStyle=orthogonalEdgeStyle;endArrow=classic;strokeWidth=2` |
| 粗边 | `strokeWidth=3`                                                |
| 虚线 | `dashed=1;strokeWidth=1.5`                                     |
| 动画 | `flowAnimation=1`                                              |
| 曲线 | `curved=1`                                                     |
| 残差 | `strokeColor=#999999;dashed=1;strokeWidth=1.5`                 |

---

## 默认布局

默认使用轻量网格，不限制画布宽高：

- **起点**：x=40, y=80
- **列间距**：180px
- **行间距**：120px
- **普通节点**：140x60
- **富文本节点**：180x80
- **决策节点**：140x80
- **容器内边距**：20px
- **画布**：随内容自然扩展

---

## 支持文件

| 文件/目录                            | 何时读取                                                           |
| ------------------------------------ | ------------------------------------------------------------------ |
| `themes/{name}.md`                 | 应用颜色时 — 14 套独立样式文件                                    |
| `references/edge-routing.md`       | 密集图或故障排查时 — 主路径路由、边穿越严重、双向边重叠、路由异常 |
| `references/layout-constraints.md` | 故障排查或复杂布局时 — 网格、间距、尺寸规范                       |
| `references/edge-styles.md`        | 应用边样式时 — 标准/粗/虚线/动画/曲线模板                         |
| `references/shape-library.md`      | 使用特殊形状时 — flowchart/basic/云平台形状                       |
| `references/xml-templates.md`      | 生成 XML 时 — 节点/箭头/容器模板 + 格式规则                       |
| `references/xml-advanced.md`       | 进阶需求时 — 推理规则/嵌套容器/图层/标签/元数据/ELK/暗黑模式      |
| `references/usage-guide.md`        | 交付后 — 打开文件/导出 PNG/SVG/PDF/WSL2/Troubleshooting           |
| `scripts/fix-xml.py`               | XML 有语法问题时 — 24 步自动修复                                  |
| `drawio-layout-algorithms.md`      | 复杂布局或用户要求严格布局时 — 12 种布局算法及公式                |
| `examples/` 目录                   | 参考完整图表 — 12 个 `.drawio` 示例                             |
| `drawio-quality-checklist.md`      | 故障排查时 — 图表打不开、渲染异常、导出失败、明显布局问题         |
