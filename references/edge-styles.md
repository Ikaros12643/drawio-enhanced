# 边样式模板

源自 `next-ai-draw-io` 的边样式库，覆盖所有常见连接场景。

## 标准边

### 基础正交边

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeWidth=2;"
```

### 带显式连接点

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
```

## 粗边

用于强调主流程。

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeWidth=3;"
```

## 虚线边

用于异步调用、可选路径、残差连接。

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeWidth=1.5;dashed=1;"
```

### 残差连接 (特定样式)

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeWidth=1.5;strokeColor=#999999;dashed=1;"
```

## 动画边

用于展示数据流向 (draw.io 支持 flowAnimation)。

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeWidth=2;flowAnimation=1;"
```

## 曲线边

用于非正交、柔和的连接。

```xml
style="curved=1;endArrow=classic;endFill=1;html=1;strokeWidth=2;"
```

## 无箭头边

用于分组、关联、装饰线。

```xml
style="endArrow=none;html=1;strokeWidth=1.5;strokeColor=#9E9E9E;"
```

## 双向箭头

```xml
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=classic;startFill=1;endArrow=classic;endFill=1;strokeWidth=2;"
```

## 箭头类型参考

| 箭头类型 | style 值 | 用途 |
|---------|----------|------|
| 经典实心 | `endArrow=classic;endFill=1` | 标准流向 |
| 空心 | `endArrow=classic;endFill=0` | 弱关联 |
| 块状 | `endArrow=block;endFill=1` | 强关联、继承 |
| 开放 | `endArrow=open;endFill=0` | 关联关系 |
| 菱形 | `endArrow=diamond;endFill=1` | 聚合/组合 |
| 无 | `endArrow=none` | 装饰线 |

## 完整边模板

```xml
<mxCell id="e1" value="" style="{style_string}" edge="1" source="{source_id}" target="{target_id}" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 带标签的边

```xml
<mxCell id="e1" value="Label" style="{style_string}" edge="1" source="{source_id}" target="{target_id}" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 带 waypoints 的边

```xml
<mxCell id="e1" value="" style="{style_string}" edge="1" source="{source_id}" target="{target_id}" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="150"/>
      <mxPoint x="200" y="300"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 带边标签的边 (标签在边上)

```xml
<mxCell id="e1_label" value="Yes" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=10;" vertex="1" connectable="0" parent="e1">
  <mxGeometry x="-0.5" y="0" relative="1" as="geometry">
    <mxPoint as="offset"/>
  </mxGeometry>
</mxCell>
```
