---
name: drawio-enhanced
description: >
  Generate professional drawio diagrams with structured workflow, 12 visual themes, and 12 layout algorithms.
  Use whenever the user asks to create a diagram, flowchart, architecture diagram, sequence diagram, comparison chart, timeline, mind map, or any visual representation of systems, processes, or concepts.
  Trigger on: "draw a diagram", "create a flowchart", "architecture diagram", "sequence diagram", "compare A vs B", "show the pipeline", "visualize the process", "make a chart", "diagram", "流程图", "架构图", "示意图", or any request to illustrate technical content.
  Also trigger when the user provides a document and asks for diagrams to be inserted, or mentions drawio/.drawio files.
  If unsure whether to use this or another diagramming skill, prefer this one — it includes quality checks and theme selection.
---

# Draw.io Enhanced

融合结构化工作流 + 12 套视觉风格 + 12 种布局算法 + 质量门禁的全能型图表生成 skill。
集成 `next-ai-draw-io` 项目的边路由规则、布局约束、配色系统和 XML 自修复能力。

## 工作流 (严格按顺序执行)

### 步骤 1: 理解需求

**如果给定文档**：

1. 阅读完整文档
2. 识别 1-3 个适合用图表表达的位置
3. 对每个位置列出：插入位置、图表主题、推荐图表类型
4. **等待用户确认**

**如果直接给出概念**：
1. 确认要传达的核心信息
2. 选择图表类型 (见下方图表类型参考)
3. 进入步骤 2

### 步骤 2: 选择风格

根据图表类型和用户场景，从 `themes/` 目录中推荐 2-3 个最匹配的风格（见下方风格推荐矩阵）。

**推荐后必须询问用户确认**：

> 推荐风格：**{style1}**、**{style2}**、**{style3}**。默认使用 **{style1}**，需要更换吗？

用户确认后进入步骤 3。完整风格定义见 `themes/{name}.md`。

### 步骤 3: ASCII 草图

生成 ASCII 草图，展示所有节点及标签、箭头方向及标签、分组/区域、颜色角色分配、近似尺寸和布局方向。

示例：
```
Direction: left-to-right | Nodes: 4 | Type: flow

[primary] Code Commit  →  [process] Build  →  [process] Test  →  [success] Deploy
                                                    ↓ (fail)
                                              [accent] Alert
```

**暂停 — 等待用户确认或修改后再进入 XML 生成。**

### 步骤 4: 计算坐标

1. 选择布局算法 (见 `drawio-layout-algorithms.md`)
2. 遵循布局约束 (见 `references/layout-constraints.md`)
   - 坐标对齐 20px 网格
   - X 范围 0-800, Y 范围 0-600
   - 水平间距 150-200px, 垂直间距 50-80px
3. 使用公式计算所有坐标
4. 读取 `references/color-palette.md` 应用配色方案
5. 读取 `themes/{name}.md` 应用选定风格的样式字符串

### 步骤 5: 生成前自检

**在生成 XML 之前，依次检查以下 4 个问题：**

1. **边是否穿越了非源/非目标的形状？** → 添加 waypoints
2. **两条边是否共享同一条路径？** → 调整 exit/entry 点 (使用不同比例值)
3. **连接点是否在角落？** → 改用边的中心点 (0.5)
4. **能否通过重新排列形状减少边交叉？** → 调整布局

详见 `references/edge-routing.md` 完整规则和自检清单。

### 步骤 6: 生成 XML

1. 使用元素模板 (见 `references/xml-templates.md`)
2. 应用风格定义的样式字符串 (见 `themes/{name}.md`)
3. 应用边样式模板 (见 `references/edge-styles.md`)
4. 需要特殊形状时参考形状库 (见 `references/shape-library.md`)
5. 确保 XML 格式正确 (无注释、实体已转义、ID 唯一)
6. 每条边必须显式指定 `exitX/Y` 和 `entryX/Y`

**⚠️ 关键转义规则**：
- 如果 `value` 属性包含 HTML 标签（如 `<font>`、`<b>`），标签内的所有双引号必须转义为 `&quot;`
- 正确示例：`value="Text&lt;br&gt;&lt;font color=&quot;#6e6e80&quot;&gt;Author&lt;/font&gt;"`
- 错误示例：`value="Text&lt;br&gt;&lt;font color="#6e6e80"&gt;Author&lt;/font&gt;"` （会导致 XML 解析失败）

### 步骤 7: 质量检查

按 `drawio-quality-checklist.md` 逐项检查。任何一项失败必须修复后再交付。

### 步骤 8: XML 自修复 (可选)

如果生成的 XML 有语法问题，使用 `scripts/fix-xml.py` 自动修复：

```bash
python scripts/fix-xml.py input.xml output.xml
```

支持 24 步自修复：JSON 转义、重复 ID、嵌套 mxCell、未闭合标签、非法字符等。

### 步骤 9: 保存与交付

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

| 类型 | 代码 | 适用场景 |
|------|------|---------|
| 线性流程 | `flow` | 顺序步骤 A→B→C |
| 垂直流程 | `flow-vertical` | 自上而下的过程 |
| 对比 | `compare` | A vs B 并排对比 |
| 层级堆叠 | `layers` | 技术栈分层 |
| 循环 | `loop` | 迭代过程 |
| 树形 | `tree` | 层级结构、分类法 |
| 中心辐射 | `hub` | 核心概念 + 分支 |
| 平行列 | `columns` | 3+ 并行概念 |
| 矩阵 | `matrix` | 多维度对比 |
| 漏斗 | `funnel` | 过滤、转化 |
| 时间线 | `timeline` | 版本演进、历史 |
| 时序图 | `sequence` | 组件交互 |

### 选择指南

| 内容模式 | 推荐类型 |
|---------|---------|
| 顺序步骤 | `flow` 或 `flow-vertical` |
| 两件事对比 | `compare` |
| 3+ 并行概念 | `columns` 或 `hub` |
| 分层系统 | `layers` |
| 迭代/循环过程 | `loop` |
| 一个核心，多个分支 | `hub` 或 `tree` |
| 组件通信 | `sequence` |
| 随时间变化 | `timeline` |
| 多标准评估 | `matrix` |
| 渐进过滤 | `funnel` |

---

## 风格推荐矩阵

| 图表类型 | 推荐风格 |
|---------|---------|
| 架构图 | flat-icon, openai, blueprint, tech-blue |
| 流程图 | flat-icon, tech-blue, mint, terracotta |
| 对比图 | openai, notion, tech-blue, morandi |
| 时序图 | openai, notion, blueprint, tech-blue |
| UML 类图 | openai, notion, blueprint, morandi |
| ER 图 | openai, notion, blueprint, tech-blue |
| 网络拓扑 | flat-icon, blueprint, tech-blue, indigo |
| 思维导图 | flat-icon, notion, mint, indigo |
| 数据流图 | flat-icon, blueprint, tech-blue, indigo |
| 时间线 | flat-icon, notion, mint, tech-blue |
| Agent 架构 | flat-icon, openai, glassmorphism, claude |

---

## 配色系统

详见 `references/color-palette.md`，包含三大类配色方案。

### 经典六色 (默认)

| 语义 | fillColor | strokeColor | 用途 |
|------|-----------|-------------|------|
| 蓝色 | `#dae8fc` | `#6c8ebf` | 主要元素、输入/输出 |
| 绿色 | `#d5e8d4` | `#82b366` | 成功、处理步骤 |
| 黄色 | `#fff2cc` | `#d6b656` | 警告、中间处理 |
| 红色 | `#f8cecc` | `#b85450` | 错误、终止节点 |
| 紫色 | `#e1d5e7` | `#9673a6` | 容器、分组 |
| 橙色 | `#ffe6cc` | `#d79b00` | 次要容器、特殊模块 |

### 语义颜色分配

| 节点类型 | 推荐颜色 |
|---------|---------|
| 用户输入/起点 | 蓝色 |
| 标准处理步骤 | 绿色 |
| 决策/分支点 | 黄色 |
| 关键转换/高亮 | 橙色 |
| 数据源/外部系统 | 紫色 |
| 成功输出/终点 | 绿色或蓝色 |
| 数据库/存储 | 紫色 |
| 错误/失败 | 红色 |

### 颜色预算

| 节点数量 | 颜色数 | 分配策略 |
|---------|--------|---------|
| 3-5 | 2-3 | 蓝色系主导 + 最多 1 个强调色 |
| 6-8 | 3-4 | 蓝色系 ~60%，语义转折点加 1-2 色 |
| 9+ | 4-5 | 蓝色系 ~50%，分散 2-3 个非蓝色 |

---

## 边路由核心规则

详见 `references/edge-routing.md` 完整 7 条规则。

1. **禁止共享路径**：同一对节点的多条边使用不同 exitX/Y 值
2. **双向连接 = 相反侧**：A→B 从右侧，B→A 从左侧
3. **显式指定连接点**：每条边必须指定 exitX/Y 和 entryX/Y
4. **使用 waypoints 避障**：绕过中间节点时使用 `<Array as="points">`
5. **分层布局规划**：形状间距 150-200px，为边路由留出通道
6. **自然连接点**：基于流向选择 (上→下 = 底部→顶部)
7. **多 waypoint 复杂路由**：2-3 个 waypoint 形成 L/U/Z 形路径

### 边样式模板

详见 `references/edge-styles.md`。

| 类型 | 关键样式 |
|------|---------|
| 标准 | `edgeStyle=orthogonalEdgeStyle;endArrow=classic;strokeWidth=2` |
| 粗边 | `strokeWidth=3` |
| 虚线 | `dashed=1;strokeWidth=1.5` |
| 动画 | `flowAnimation=1` |
| 曲线 | `curved=1` |
| 残差 | `strokeColor=#999999;dashed=1;strokeWidth=1.5` |

---

## 布局约束

详见 `references/layout-constraints.md`。

- **画布**：X 0-800, Y 0-600
- **网格**：20px 对齐
- **标准尺寸**：流程框 120×60, 决策 120×80, 小框 120×40
- **间距**：水平 150-200px, 垂直 50-80px, 容器内边距 20px

---

## 支持文件

| 文件/目录 | 何时读取 |
|------|---------|
| `themes/{name}.md` | 应用颜色时 — 12 套独立样式文件 |
| `references/color-palette.md` | 选择配色方案时 — 经典六色 + Material + 云平台 |
| `references/edge-routing.md` | 生成边时 — 7 条路由规则 + 自检清单 |
| `references/layout-constraints.md` | 计算坐标时 — 网格、间距、尺寸规范 |
| `references/edge-styles.md` | 应用边样式时 — 标准/粗/虚线/动画/曲线模板 |
| `references/shape-library.md` | 使用特殊形状时 — flowchart/basic/云平台形状 |
| `references/xml-templates.md` | 生成 XML 时 — 节点/箭头/容器模板 + 格式规则 |
| `references/xml-advanced.md` | 进阶需求时 — 推理规则/嵌套容器/图层/标签/元数据/ELK/暗黑模式 |
| `references/usage-guide.md` | 交付后 — 打开文件/导出 PNG/SVG/PDF/WSL2/Troubleshooting |
| `scripts/fix-xml.py` | XML 有语法问题时 — 24 步自动修复 |
| `drawio-layout-algorithms.md` | 计算坐标时 — 12 种布局算法及公式 |
| `examples/` 目录 | 参考完整图表 — 12 个 `.drawio` 示例 |
| `drawio-quality-checklist.md` | 交付前 — 16 项质量检查 |
