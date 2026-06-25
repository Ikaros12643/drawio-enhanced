# Draw.io 布局算法

12 种布局算法，适配 drawio 坐标系统。每种算法提供精确坐标计算公式，节点数量变化时自动适配。

## 全局常量

```
CANVAS_PAD    = 40       # 画布边距
NODE_W        = 160      # 默认节点宽度
NODE_H        = 50       # 单行标签节点高度
NODE_H_RICH   = 90       # 含标题+列表的节点高度
TITLE_H       = 0        # 默认不预留画布内标题；用户明确要求图内标题时设为 30
GAP_H         = 60       # 节点水平间距
GAP_V         = 50       # 节点垂直间距
DIAMOND_W     = 120      # 菱形宽度
DIAMOND_H     = 80       # 菱形高度
GROUP_PAD     = 20       # 分组容器内边距
```

**弹性调整**：
- 节点 > 6 个：`NODE_W` 降至 140 或 `GAP_H` 降至 40
- 文字较长：`NODE_W` 增至 200
- 富节点（标题+列表）：使用 `NODE_H_RICH` 替代 `NODE_H`
- 图表名称默认使用 draw.io 页签 `<diagram name="...">`，不要在画布顶部额外添加标题节点

---

## 算法 1: flow — 线性流程 (从左到右)

**适用**：顺序步骤 A→B→C、API 调用流程、数据管道

### 坐标公式

```
x[i] = CANVAS_PAD + i × (NODE_W + GAP_H)
y    = CANVAS_PAD + TITLE_H + GAP_V

Canvas width  = CANVAS_PAD × 2 + n × NODE_W + (n-1) × GAP_H
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + NODE_H
```

### 蛇形布局 (n > 5)

当节点超过 5 个时，自动换行到下一行，从右到左流动：

```
Row 0 (L→R): nodes 0..4
Row 1 (R→L): nodes 5..9
Row 2 (L→R): nodes 10..14

y[row] = CANVAS_PAD + TITLE_H + GAP_V + row × (NODE_H + GAP_V)
x[i] in even row = CANVAS_PAD + col × (NODE_W + GAP_H)
x[i] in odd row  = CANVAS_PAD + (4-col) × (NODE_W + GAP_H)
```

### XML 示例

```xml
<mxCell id="n0" value="Step 1" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="70" width="160" height="50" as="geometry"/>
</mxCell>
<mxCell id="n1" value="Step 2" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="260" y="70" width="160" height="50" as="geometry"/>
</mxCell>
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;" edge="1" source="n0" target="n1" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 算法 2: flow-vertical — 垂直流程 (从上到下)

**适用**：审批流程、决策链、自上而下的过程

### 坐标公式

```
x    = (Canvas width / 2) - NODE_W / 2
y[i] = CANVAS_PAD + TITLE_H + GAP_V + i × (NODE_H + GAP_V)

Canvas width  = CANVAS_PAD × 2 + NODE_W
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + n × NODE_H + (n-1) × GAP_V
```

---

## 算法 3: compare — 左右对比

**适用**：A vs B 对比、传统 vs AI 方案、优缺点对比

### 坐标公式

```
VS_W = 50   # "VS" 徽章宽度

Left column x  = CANVAS_PAD
Right column x = CANVAS_PAD + NODE_W + GAP_H + VS_W + GAP_H
VS badge x     = CANVAS_PAD + NODE_W + GAP_H

Header y = CANVAS_PAD + TITLE_H + GAP_V
Row y[j] = Header y + NODE_H + GAP_V/2 + j × (NODE_H + GAP_V/2)

Canvas width  = CANVAS_PAD × 2 + NODE_W × 2 + GAP_H × 2 + VS_W
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + (rows+1) × NODE_H + rows × GAP_V/2
```

---

## 算法 4: layers — 层级堆叠

**适用**：技术栈分层、系统架构层级、OSI 模型

### 坐标公式

```
LAYER_W = 400

x = (Canvas width - LAYER_W) / 2
y[i] = CANVAS_PAD + TITLE_H + GAP_V + i × (NODE_H_RICH + GAP_V/3)

Canvas width  = CANVAS_PAD × 2 + LAYER_W
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + n × NODE_H_RICH + (n-1) × GAP_V/3
```

层级横跨全宽，顶层 = 最高抽象层。

---

## 算法 5: loop — 循环/反馈环

**适用**：ML 训练循环、CI/CD 迭代、PDCA 循环

### 4 节点布局 (最常见)

```
Positions:
  [0] top-left:     (CANVAS_PAD, CANVAS_PAD + TITLE_H + GAP_V)
  [1] top-right:    (CANVAS_PAD + NODE_W + GAP_H × 2, same y)
  [2] bottom-right: (same x as [1], y + NODE_H + GAP_V)
  [3] bottom-left:  (same x as [0], same y as [2])

Arrows: 0→1 (top), 1→2 (right), 2→3 (bottom, R→L), 3→0 (left, bottom→top)

Canvas width  = CANVAS_PAD × 2 + NODE_W + GAP_H × 2
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V × 2 + NODE_H
```

### N 节点布局

将 N 个节点均匀分布在矩形的四条边上。

**关键**：返回箭头 (last→first) 必须沿矩形外侧路由，不能对角穿过中心。

---

## 算法 6: tree — 树形/层级

**适用**：组织架构图、决策树、分类法

### 坐标公式

```
Level spacing = GAP_V × 1.5
Sibling spacing = NODE_W + GAP_H / 2

Root: centered at top
Children: evenly distributed below parent, centered under parent

Subtree width = max(sum of children subtree widths, NODE_W)
Parent x = leftmost child x + (rightmost child x + NODE_W - leftmost child x) / 2 - NODE_W / 2
```

---

## 算法 7: hub — 中心辐射 (Hub & Spoke)

**适用**：产品功能图、核心概念+分支、平台生态

### 坐标公式

中心节点在画布中心。辐射节点均匀分布在周围。

**查找表** (直接使用，无需计算三角函数)：

| N 辐射 | 相对中心的位置 (dx, dy) |
|--------|------------------------|
| 3 | (0, -R), (R×0.87, R×0.5), (-R×0.87, R×0.5) |
| 4 | (0, -R), (R, 0), (0, R), (-R, 0) |
| 5 | (0, -R), (R×0.95, -R×0.31), (R×0.59, R×0.81), (-R×0.59, R×0.81), (-R×0.95, -R×0.31) |
| 6 | (0, -R), (R×0.87, -R×0.5), (R×0.87, R×0.5), (0, R), (-R×0.87, R×0.5), (-R×0.87, -R×0.5) |

其中 `R = 180` (半径)。辐射节点位置：
```
x[i] = cx + dx[i] - NODE_W / 2
y[i] = cy + dy[i] - NODE_H / 2
```

---

## 算法 8: columns — 平行列

**适用**：3+ 并行概念、多团队工作流、多环境部署

### 坐标公式

```
Column x[i] = CANVAS_PAD + i × (NODE_W + GAP_H)
Header y     = CANVAS_PAD + TITLE_H + GAP_V
Item y[j]    = Header y + NODE_H + GAP_V/2 + j × (NODE_H + GAP_V/3)

Canvas width  = CANVAS_PAD × 2 + cols × NODE_W + (cols-1) × GAP_H
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + NODE_H + max_items × (NODE_H + GAP_V/3)
```

每列有一个标题节点（着色）和垂直堆叠的项目节点。

---

## 算法 9: matrix — 对比矩阵

**适用**：多维度评估、功能对比矩阵、决策矩阵

### 坐标公式

```
CELL_W = 140
CELL_H = 45
HEADER_H = 40
HEADER_W = 140

Col header x[c] = CANVAS_PAD + HEADER_W + GAP_H/3 + c × (CELL_W + GAP_H/3)
Row header y[r] = CANVAS_PAD + TITLE_H + HEADER_H + GAP_V/3 + r × (CELL_H + GAP_V/3)
Cell (r,c): x = Col header x[c], y = Row header y[r]

Canvas width  = CANVAS_PAD × 2 + HEADER_W + GAP_H/3 + cols × (CELL_W + GAP_H/3)
Canvas height = CANVAS_PAD × 2 + TITLE_H + HEADER_H + GAP_V/3 + (rows+1) × (CELL_H + GAP_V/3)
```

---

## 算法 10: funnel — 漏斗图

**适用**：过滤流程、转化率、销售漏斗

### 坐标公式

```
MAX_W = 360
MIN_W = 120

w[i] = MAX_W - i × ((MAX_W - MIN_W) / (n - 1))
x[i] = (Canvas width - w[i]) / 2
y[i] = CANVAS_PAD + TITLE_H + GAP_V + i × (NODE_H + GAP_V / 3)

Canvas width  = CANVAS_PAD × 2 + MAX_W
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + n × NODE_H + (n-1) × GAP_V/3
```

居中堆叠，宽度递减的带状节点。

---

## 算法 11: timeline — 时间线

**适用**：版本演进、历史事件、产品路线图

### 坐标公式

```
LINE_Y = canvas vertical center
Node spacing = NODE_W + GAP_H

Event nodes alternate above and below the timeline:
  Above: y = LINE_Y - NODE_H - GAP_V/2
  Below: y = LINE_Y + GAP_V/2
  x[i]  = CANVAS_PAD + i × (NODE_W + GAP_H)

Canvas width  = CANVAS_PAD × 2 + n × NODE_W + (n-1) × GAP_H
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V × 2 + NODE_H × 2
```

在 LINE_Y 处画一条水平线贯穿全宽。为每个节点画垂直刻度线。

---

## 算法 12: sequence — 时序图

**适用**：组件交互、API 调用序列、消息传递

### 坐标公式

```
LIFELINE_GAP = 180
MESSAGE_GAP  = 50
PARTICIPANT_Y = CANVAS_PAD + TITLE_H + GAP_V
PARTICIPANT_W = 140
PARTICIPANT_H = 40

Participant x[i] = CANVAS_PAD + i × LIFELINE_GAP
Lifeline: vertical dashed line from bottom of participant box downward

Message y[j] = PARTICIPANT_Y + PARTICIPANT_H + GAP_V + j × MESSAGE_GAP

Canvas width  = CANVAS_PAD × 2 + participants × LIFELINE_GAP
Canvas height = CANVAS_PAD × 2 + TITLE_H + GAP_V + PARTICIPANT_H + messages × MESSAGE_GAP
```

消息：参与者生命线之间的水平箭头，时间顺序从上到下。

---

## 布局选择指南

| 内容模式 | 推荐算法 |
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
