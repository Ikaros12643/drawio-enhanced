# Draw.io XML 模板参考

## 基础结构

每个 `.drawio` 文件必须包含此结构：

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- 图表元素放在这里，parent="1" -->
  </root>
</mxGraphModel>
```

- Cell `id="0"` 是根图层
- Cell `id="1"` 是默认父图层
- 所有图表元素使用 `parent="1"` (除非使用多层)

## 节点模板

**圆角矩形**：
```xml
<mxCell id="2" value="Label" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#xxx;strokeColor=#yyy;strokeWidth=1.5;fontSize=13;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="50" as="geometry"/>
</mxCell>
```

**菱形 (决策)**：
```xml
<mxCell id="3" value="Condition?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#xxx;strokeColor=#yyy;strokeWidth=1.5;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="80" as="geometry"/>
</mxCell>
```

**数据库圆柱**：
```xml
<mxCell id="4" value="Database" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#xxx;strokeColor=#yyy;strokeWidth=1.5;fontSize=13;" vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="120" height="80" as="geometry"/>
</mxCell>
```

**椭圆**：
```xml
<mxCell id="5" value="Start" style="ellipse;whiteSpace=wrap;html=1;fillColor=#xxx;strokeColor=#yyy;strokeWidth=1.5;fontSize=13;" vertex="1" parent="1">
  <mxGeometry x="100" y="400" width="80" height="60" as="geometry"/>
</mxCell>
```

## 箭头模板

**标准箭头**：
```xml
<mxCell id="e1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=1.5;strokeColor=#xxx;endArrow=classic;endFill=1;" edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**带标签箭头**：
```xml
<mxCell id="e2" value="Yes" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=1.5;strokeColor=#xxx;endArrow=classic;endFill=1;" edge="1" source="3" target="4" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**虚线箭头**：
```xml
<mxCell id="e3" value="async" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=1.5;strokeColor=#xxx;endArrow=classic;endFill=1;dashed=1;" edge="1" source="2" target="5" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 容器模板

**泳道 (有标题)**：
```xml
<mxCell id="lane1" value="Service A" style="swimlane;startSize=24;rounded=1;arcSize=8;fillColor=#xxx;strokeColor=#yyy;strokeWidth=1;strokeDashPattern=4 3;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="100" width="300" height="200" as="geometry"/>
</mxCell>
<mxCell id="n1" value="Component" style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#fff;strokeColor=#ddd;strokeWidth=1.5;fontSize=13;" vertex="1" parent="lane1">
  <mxGeometry x="20" y="40" width="140" height="50" as="geometry"/>
</mxCell>
```

**分组 (无标题)**：
```xml
<mxCell id="grp1" value="" style="group;pointerEvents=0;" vertex="1" parent="1">
  <mxGeometry x="40" y="100" width="300" height="200" as="geometry"/>
</mxCell>
```

## 标题模板

```xml
<mxCell id="title" value="&lt;b&gt;Diagram Title&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=16;fontStyle=1" vertex="1" parent="1">
  <mxGeometry x="300" y="20" width="200" height="30" as="geometry"/>
</mxCell>
```

## 关键规则

### XML 格式

- **绝不包含 XML 注释** (`<!-- -->`)
- 转义特殊字符：`&amp;`, `&lt;`, `&gt;`, `&quot;`
- 每个 `mxCell` 使用唯一 `id`
- 每个边必须有 `<mxGeometry relative="1" as="geometry" />` 子元素

### HTML 标签

- 任何包含 HTML 标签 (`<b>`, `<br>`, `<font>` 等) 的单元格必须包含 `html=1`
- HTML 必须 XML 转义：`<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`
- **HTML 标签内的双引号必须转义为 `&quot;`**
- 换行使用 `&#xa;` (兼容 `html=1` 和 `html=0`) 或 `&lt;br&gt;` (需要 `html=1`)

**转义示例对比**：

| 场景 | 正确写法 | 错误写法 |
|------|---------|---------|
| 纯文本标签 | `value="&lt;b&gt;Title&lt;/b&gt;"` | `value="<b>Title</b>"` |
| 带属性的标签 | `value="&lt;font color=&quot;#6e6e80&quot;&gt;Text&lt;/font&gt;"` | `value="&lt;font color="#6e6e80"&gt;Text&lt;/font&gt;"` |
| 多行带副标题 | `value="Title&lt;br&gt;&lt;font color=&quot;#999&quot;&gt;Subtitle&lt;/font&gt;"` | `value="Title&lt;br&gt;&lt;font color="#999"&gt;Subtitle&lt;/font&gt;"` |

**完整节点示例**：

```xml
<mxCell id="n1" value="1958&lt;br&gt;感知机&lt;br&gt;&lt;font color=&quot;#6e6e80&quot;&gt;Frank Rosenblatt&lt;/font&gt;" 
        style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#ffffff;strokeColor=#10a37f;strokeWidth=1.5;fontSize=13;" 
        vertex="1" parent="1">
  <mxGeometry x="300" y="80" width="200" height="60" as="geometry"/>
</mxCell>
```

### 箭头路由

- 所有箭头使用正交路由 (`edgeStyle=orthogonalEdgeStyle`)
- 无对角箭头
- 返回箭头沿外侧路由，不穿过无关节点
- 边路由由 ELK 自动处理，无需手动添加路径点

### 语言匹配

- 标签语言与用户语言一致
- 技术缩写 (API, LLM, CI/CD) 保持英文
