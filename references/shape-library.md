# 形状库参考

源自 `next-ai-draw-io` 的形状库文档，提供最常用的 flowchart 形状语法。

## Flowchart 形状库

最通用的形状库，适用于流程图、决策树、状态机。

### 基础语法

```xml
<mxCell value="label" style="shape=mxgraph.flowchart.{shape};fillColor=#xxx;strokeColor=#yyy;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="120" height="60" as="geometry"/>
</mxCell>
```

### 常用形状

| 形状名称 | shape 值 | 用途 | 推荐配色 |
|---------|----------|------|---------|
| 流程 | `process` | 处理步骤 | `#dae8fc` / `#6c8ebf` |
| 决策 | `decision` | 条件判断 | `#fff2cc` / `#d6b656` |
| 开始/结束 | `terminator` | 起点/终点 | `#d5e8d4` / `#82b366` |
| 数据 | `data` | 输入/输出数据 | `#e1d5e7` / `#9673a6` |
| 文档 | `document` | 文档/报告 | `#ffe6cc` / `#d79b00` |
| 手动操作 | `manual_input` | 手动输入 | `#f8cecc` / `#b85450` |
| 准备 | `preparation` | 初始化/设置 | `#dae8fc` / `#6c8ebf` |
| 子流程 | `subprocess` | 调用子流程 | `#d5e8d4` / `#82b366` |
| 存储 | `delay` | 延迟/存储 | `#fff2cc` / `#d6b656` |
| 卡片 | `card` | 记录/卡片 | `#e1d5e7` / `#9673a6` |

### 示例：决策流程

```xml
<mxCell id="start" value="Start" style="shape=mxgraph.flowchart.terminator;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
  <mxGeometry x="200" y="40" width="120" height="50" as="geometry"/>
</mxCell>

<mxCell id="process1" value="Process Data" style="shape=mxgraph.flowchart.process;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="200" y="120" width="120" height="60" as="geometry"/>
</mxCell>

<mxCell id="decision1" value="Valid?" style="shape=mxgraph.flowchart.decision;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
  <mxGeometry x="200" y="220" width="120" height="80" as="geometry"/>
</mxCell>

<mxCell id="end_ok" value="Success" style="shape=mxgraph.flowchart.terminator;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
  <mxGeometry x="380" y="340" width="120" height="50" as="geometry"/>
</mxCell>

<mxCell id="end_err" value="Error" style="shape=mxgraph.flowchart.terminator;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
  <mxGeometry x="40" y="340" width="120" height="50" as="geometry"/>
</mxCell>
```

## Basic 形状库

简单几何形状，适用于概念图、装饰元素。

```xml
<mxCell value="label" style="shape=mxgraph.basic.{shape};fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="80" height="80" as="geometry"/>
</mxCell>
```

### 常用形状

| 形状 | shape 值 | 说明 |
|------|----------|------|
| 矩形 | `rect` | 基础矩形 |
| 圆角矩形 | `round_rect` | 圆角矩形 |
| 椭圆 | `ellipse` | 椭圆 |
| 菱形 | `rhombus` | 菱形 |
| 三角形 | `triangle` | 三角形 |
| 圆柱 | `cylinder` | 圆柱体 |
| 立方体 | `cube` | 3D 立方体 |
| 星形 | `star` | 五角星 |

## Arrows2 箭头库

装饰性箭头，适用于标注、指示。

```xml
<mxCell value="label" style="shape=mxgraph.arrows2.arrow;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="120" height="40" as="geometry"/>
</mxCell>
```

## 云平台形状库

### AWS (aws4)

```xml
<mxCell value="EC2" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#ED7100;strokeColor=#ffffff;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry"/>
</mxCell>
```

### Azure (mscae)

```xml
<mxCell value="App Service" style="shape=mxgraph.mscae.cloud.azure;fillColor=#0078D4;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry"/>
</mxCell>
```

### GCP (gcp2)

```xml
<mxCell value="Compute Engine" style="shape=mxgraph.gcp2.compute_engine;fillColor=#4285F4;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry"/>
</mxCell>
```

### Kubernetes (kubernetes)

```xml
<mxCell value="Pod" style="shape=mxgraph.kubernetes.icon;prIcon=pod;fillColor=#326CE5;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry"/>
</mxCell>
```
