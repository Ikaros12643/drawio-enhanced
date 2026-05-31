# Draw.io XML 进阶参考

整合推理规则、样式属性、容器高级用法、图层、标签、元数据、暗黑模式和 ELK 自动路由。

---

## 1. 推理预算 (生成前必读)

生成 XML 时的推理约束，减少 token 浪费。

### ❌ 不要在推理中做

- 不要辩论话题，直接选择具体场景并执行
- 不要辩论布局方向（水平/垂直），选择第一个合理方案
- 不要在推理中计算坐标，直接在 XML 中写出
- 不要重新推导 draw.io 机制（swimlane 坐标、容器尺寸等）
- 不要枚举列位置，放置节点后继续
- 不要添加 `<Array as="points">` waypoints — ELK 自动处理
- 不要设置 `exitX/Y` / `entryX/Y` 除非有明确的几何意图
- 不要放置节点后验证/调整坐标
- 不要叙述"正在构建图表/最终化 XML"，直接输出 XML
- 不要以规划文本形式列出节点位置，直接写 `<mxCell>` 元素

### ✅ 应该在推理中做

- 识别图表类型 + 参与者/阶段（1-2 句话）
- 识别分组（泳道？容器？无？）
- 直接进入 XML 生成

### 刚性网格

```
列 x = col_index * 180 + 40  (col 0 = 40, col 1 = 220, col 2 = 400, ...)
行 y = row_index * 120 + 40  (row 0 = 40, row 1 = 160, row 2 = 280, ...)
```

| 形状 | 尺寸 |
|------|------|
| 矩形 | 140×60 |
| 菱形 | 140×80 |
| 圆形 | 60×60 |
| 文档 | 120×80 |
| 圆柱 | 100×70 |

---

## 2. 样式属性速查表

| 属性 | 值 | 用途 |
|------|-----|------|
| `rounded=1` | 0 或 1 | 圆角 |
| `whiteSpace=wrap` | wrap | 文本换行 |
| `fillColor=#dae8fc` | 十六进制 | 背景色 |
| `strokeColor=#6c8ebf` | 十六进制 | 边框色 |
| `fontColor=#333333` | 十六进制 | 文本色 |
| `shape=cylinder3` | 形状名 | 数据库圆柱 |
| `shape=mxgraph.flowchart.document` | 形状名 | 文档形状 |
| `ellipse` | 样式关键字 | 圆形/椭圆 |
| `rhombus` | 样式关键字 | 菱形 |
| `edgeStyle=orthogonalEdgeStyle` | 样式关键字 | 直角连接线 |
| `edgeStyle=elbowEdgeStyle` | 样式关键字 | 肘形连接线 |
| `dashed=1` | 0 或 1 | 虚线 |
| `swimlane` | 样式关键字 | 泳道容器 |
| `group` | 样式关键字 | 不可见容器 (pointerEvents=0) |
| `container=1` | 0 或 1 | 启用容器行为 |
| `pointerEvents=0` | 0 或 1 | 防止容器捕获子连接 |
| `html=1` | 0 或 1 | 启用 HTML 渲染 (需要 `<b>`, `<br>`, `<font>` 等) |
| `shape=umlLifeline;perimeter=lifelinePerimeter;size=16` | 形状 | UML 时序图生命线 |

### 字体样式

| 值 | 效果 |
|-----|------|
| `fontStyle=1` | 粗体 |
| `fontStyle=2` | 斜体 |
| `fontStyle=4` | 下划线 |
| `fontStyle=3` | 粗体+斜体 (位或) |

---

## 3. 容器高级用法

### 3.1 容器类型

| 类型 | 样式 | 使用场景 |
|------|------|---------|
| **Group** (不可见) | `group;` | 不需要可见边框，容器无连接 |
| **Swimlane** (有标题) | `swimlane;startSize=30;` | 需要可见标题栏，或容器本身有连接 |
| **自定义容器** | 任意形状 + `container=1;pointerEvents=0;` | 无自身连接的形状作为容器 |

### 3.2 关键规则

- **边到容器内元素自然穿越容器边界** — 这是正确的，不要添加额外 waypoints
- **始终添加 `pointerEvents=0;`** 到不应捕获子连接的容器
- 子元素必须设置 `parent="containerId"` 并使用**相对坐标**
- 跨容器边必须设置 `parent="1"`（不在容器内）

### 3.3 嵌套架构容器

用于 VPC → AZ → EC2、Datacenter → Rack → Server 等嵌套分组。

**规则**：
- 每个容器是 `swimlane` + `startSize=24`
- 子元素设置 `parent="<container_id>"`，坐标相对于父容器 (0,0 是父容器左上角，标题下方)
- **不同容器间的边必须 `parent="1"`** — 否则会在容器内渲染并被裁剪

```xml
<mxCell id="vpc" value="VPC" style="swimlane;startSize=24;fillColor=#dae8fc;strokeColor=#6c8ebf;html=1;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="720" height="360" as="geometry"/>
</mxCell>
<mxCell id="az1" value="AZ us-east-1a" style="swimlane;startSize=24;fillColor=#fff2cc;strokeColor=#d6b656;html=1;" vertex="1" parent="vpc">
  <mxGeometry x="20" y="36" width="320" height="300" as="geometry"/>
</mxCell>
<mxCell id="web1" value="web-1" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="az1">
  <mxGeometry x="30" y="40" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="e1" edge="1" parent="1" source="web1" target="web2" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 3.4 BPMN 泳道

**固定值 — 不要计算或辩论**：
- 泳道尺寸：`x=0, y=lane_index*150, width=CANVAS_W, height=150`
- 泳道样式：`swimlane;horizontal=0;startSize=110;fillColor=<pastel>;html=1;`
- 泳道内节点：`parent="<lane_id>"`, `x = 120 + col*180`, `y = 45` (始终 45), 尺寸 140×60
- 跨泳道边：`parent="1"` (不在泳道内)

选择 `CANVAS_W = max_col * 180 + 300`。泳道颜色按顺序使用：`#f5f5f5, #e8f4f8, #fff0e6, #e8f5e9, #fff9e6, #fce4ec`。

### 3.5 跨职能流程图 (表格布局)

用于同时展示**两个维度** — 参与者 (行) 和阶段 (列)。

**结构**：
- 外层容器：`shape=table;childLayout=tableLayout;startSize=0;collapsible=0;fillColor=none;`
- 行是表格的子元素：`shape=tableRow;horizontal=0;startSize=0;collapsible=0;`
- 单元格是行的子元素 — 常规顶点，每个 (参与者, 阶段) 交叉点一个
- 行高和单元格宽度通过 `mxGeometry` 设置，自动平铺
- 第一行 = 阶段标题；其他行的第一个单元格 = 参与者标签
- 流程节点放在对应单元格内 (parent = 单元格 id)，坐标相对于单元格
- 跨单元格边必须使用 `parent="1"`

**何时使用**：
- 平面泳道 — 一维 (仅参与者或仅阶段)。更简单。
- 跨职能表格 — 二维 (参与者 AND 阶段)。当**两者**都重要时使用。

---

## 4. 图层 (Layers)

图层控制可见性和 z-order。每个单元格属于且仅属于一个图层。

**用途**：管理图表复杂度 — 用户可切换图层可见性来显示或隐藏元素组。

**场景**：
- 网络架构：同时显示"物理拓扑"和"逻辑拓扑"
- 系统设计：显示"核心流程"和"异常处理"
- 安全架构：显示"网络层"和"安全层"分离展示

```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="2" value="Annotations" parent="0"/>
    <mxCell id="10" value="Server" style="rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="20" value="Note: deprecated" style="text;" vertex="1" parent="2">
      <mxGeometry x="100" y="170" width="120" height="30" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

- 图层是 `parent="0"` 且无 `vertex` 或 `edge` 属性的 `mxCell`
- 通过设置 `parent` 为图层 id 将形状分配到图层
- 后面的图层渲染在上面的图层之上 (z-order 更高)
- 在图层单元格上添加 `visible="0"` 属性默认隐藏
- 当图表有不同的概念分组且用户可能想独立切换时使用

---

## 5. 标签 (Tags)

标签是视觉过滤器，让用户按类别显示或隐藏元素。单个元素可有多个标签。

**场景**：
- 微服务架构：标注 `critical` + `v2` + `backend`
- 代码迁移：标注 `deprecated` + `to-remove`
- 监控视图：标注 `high-cpu` + `needs-scaling`

```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <object id="2" label="Auth Service" tags="critical v2">
      <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
        <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
      </mxCell>
    </object>
    <object id="3" label="Legacy API" tags="critical deprecated">
      <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
        <mxGeometry x="300" y="100" width="120" height="60" as="geometry"/>
      </mxCell>
    </object>
  </root>
</mxGraphModel>
```

- 标签需要 `<object>` 包装 — 普通 `mxCell` 不能有标签
- `<object>` 的 `label` 属性替代 `mxCell` 的 `value`
- 标签在 `tags` 属性中以空格分隔
- 用户在 draw.io UI 中通过 Edit > Tags 过滤
- 标签不影响 z-order 或结构分组 — 纯可见性过滤

---

## 6. 元数据与占位符 (Metadata & Placeholders)

在形状上存储自定义键值属性，结合占位符可在标签中显示这些值。

**场景**：
- 服务器清单：显示 `%ip%`、`%owner%`、`%status%`
- 项目管理：显示 `%progress%`、`%deadline%`
- 配置管理：显示 `%version%`、`%config%`

```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <object id="2" label="&lt;b&gt;%component%&lt;/b&gt;&lt;br&gt;Owner: %owner%&#xa;Status: %status%"
            placeholders="1" component="Auth Service" owner="Backend Team" status="Active">
      <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
        <mxGeometry x="100" y="100" width="160" height="80" as="geometry"/>
      </mxCell>
    </object>
  </root>
</mxGraphModel>
```

- 自定义属性是 `<object>` 上的普通 XML 属性
- 设置 `placeholders="1"` 启用 `%key%` 替换
- 标签使用 `html=1` 样式时需要 HTML 格式化
- 占位符沿包含层次解析：形状属性 → 父容器 → 图层 → 根
- 预定义占位符无需自定义属性：`%id%`, `%width%`, `%height%`, `%date%`, `%time%`, `%timestamp%`, `%page%`, `%pagenumber%`, `%pagecount%`, `%filename%`
- 使用 `%%` 表示字面百分号
- 标签、元数据和占位符可组合在同一 `<object>` 上

---

## 7. 暗黑模式颜色

draw.io 支持自动暗黑模式渲染。

- **`strokeColor`, `fillColor`, `fontColor`** 默认为 `"default"`，亮色主题渲染为黑色，暗色主题渲染为白色。未设置显式颜色时自动适应。
- **显式颜色** (如 `fillColor=#DAE8FC`) 指定亮色主题颜色。暗色主题颜色通过反转 RGB 值 (93% 混合) 和旋转色相 180° 自动计算。
- **`light-dark()` 函数** — 显式指定两种颜色：`light-dark(lightColor,darkColor)`，如 `fontColor=light-dark(#7EA6E0,#FF0000)`。第一个参数亮色主题，第二个暗色主题。

启用暗黑模式颜色适应：`mxGraphModel` 必须包含 `adaptiveColors="auto"`。

通常不需要指定暗色主题颜色 — 自动反转处理大多数情况。仅在自动反转颜色不理想时使用 `light-dark()`。

---

## 8. ELK 自动边路由

每个 XML 图表渲染后自动运行 ELK (Eclipse Layout Kernel) 边路由：

1. 顶点位置固定 (尊重 AI 的放置 — 顶点不移动)
2. ELK 重新计算每条边的弯折点 + 连接点 (正交路由)
3. 指标 (边-顶点交叉) 比较前后。如果 ELK 使碰撞更糟，边路由恢复原始
4. 导出的 XML 反映最终显示内容

**这意味着**：
- 不需要添加 `<mxPoint>` waypoints
- 不需要设置 `exitX/Y` / `entryX/Y`
- 不需要绕开障碍物
- 不需要担心边-顶点碰撞或平行边间距
- 只需声明 `source` 和 `target`，让 ELK 处理路由

### 边风格选择

| 风格 | 语法 | 适用场景 |
|------|------|---------|
| **正交** | `edgeStyle=orthogonalEdgeStyle` | 流程图、架构图、网络图、BPMN |
| **直线** | 无 `edgeStyle` | UML 类/时序图、直接点对点连接 |
| **实体关系** | `edgeStyle=entityRelationEdgeStyle` | ER 图 — 两端垂直短桩 |
| **曲线** | `curved=1` | 思维导图、非正式图表 |
| **肘形** | `edgeStyle=elbowEdgeStyle;elbow=vertical;` | 简单单弯折线性流 |

**在同一图表中使用一致的边风格**。

### 有用边属性

- `rounded=1` — 弯折点圆角 (正交推荐)
- `endArrow=classic` / `endArrow=none` — 箭头
- `dashed=1` — 虚线
- `strokeColor=#...`, `strokeWidth=2` — 颜色/宽度
- 边标签：直接在边单元格上设置 `value`

---

## 9. 形状选择原则

- **使用语义正确的形状** — 为每个元素选择语义正确的形状 (数据库用 `cylinder3`，决策用 `rhombus`)
- **跳过形状搜索** 用于标准图表类型：流程图、UML、ERD、组织图、思维导图、维恩图、时间线、线框图
- **使用形状搜索** 用于行业特定或品牌图标：云架构 (AWS/Azure/GCP)、网络拓扑、P&ID、电气图、Kubernetes、BPMN

---

## 10. 语言匹配

- 标签语言与用户语言一致
- 技术缩写 (API, LLM, CI/CD) 保持英文
