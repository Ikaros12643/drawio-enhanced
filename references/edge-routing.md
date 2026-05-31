# 边路由与精简参考

源自 `next-ai-draw-io` 的边路由规则，用于密集图、层级架构图或故障排查。简单图默认只写 `source` / `target` 和 `edgeStyle=orthogonalEdgeStyle`，让 draw.io 自动路由。

使用本文件时，目标是提升整体观感，不是保留所有关系。先删边、合并边，再对少量关键边手动路由。

## 边预算与精简

边越多，图越难读。生成密集图前先做删减：

- 节点数 `n <= 8`：边数尽量不超过 `n + 2`
- 节点数 `n > 8`：边数尽量不超过 `1.5n`
- 保留主流程、关键依赖、跨层调用、异常/反馈路径
- 删除弱关系、背景关联、重复依赖和可由分组/颜色表达的关系
- 同一组节点之间的多条同类关系合并为一条带标签边
- 多个节点共同依赖同一能力时，优先画到分组/容器，不逐个节点连线
- 全局策略、观测、权限、配置等横切关注点优先用图例、虚线区域或注释表达
- 如果某条边需要超过 2 个 waypoint 才能看清，通常应该删掉或改成注释

## 规则 1: 禁止共享路径

同一对节点之间的多条边必须使用不同的 `exitX/Y`/`entryX/Y` 值。

```
错误: 两条边都使用 exitX=0.5, exitY=0 (从同一点出发)
正确: 边 A 使用 exitX=0.3, exitY=0；边 B 使用 exitX=0.7, exitY=0
```

## 规则 2: 双向连接 = 相反侧

A→B 和 B→A 必须从相反侧连接。

```
A→B: exitX=1, exitY=0.5 (右侧) → entryX=0, entryY=0.5 (左侧)
B→A: exitX=0, exitY=0.5 (左侧) → entryX=1, entryY=0.5 (右侧)
```

## 规则 3: 显式指定 exitX/Y 和 entryX/Y

只对主路径、双向边、跨层长边和容易穿越节点的边显式指定连接点。简单边可以依赖 draw.io 自动路由。

```xml
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;..." edge="1" source="nodeA" target="nodeB">
```

### exitX/Y 和 entryX/Y 含义

- `exitX`: 出口 X 位置比例 (0=左, 0.5=中, 1=右)
- `exitY`: 出口 Y 位置比例 (0=上, 0.5=中, 1=下)
- `exitDx/Dy`: 出口偏移量 (像素)，通常为 0
- `entryX/Y/Dx/Dy`: 同上，用于入口

## 规则 4: 少量 waypoints 避障

当关键边需要绕过中间节点时，使用 `<Array as="points">` 定义路径点。每条边最多 2 个 waypoint；超过这个数量时，优先删边、合并边或移动节点。

```xml
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;..." edge="1" source="A" target="B">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="150"/>
      <mxPoint x="200" y="300"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### Waypoint 策略

- 单 waypoint: L 形路径 (一次转弯)
- 双 waypoint: U 形路径 (两次转弯)
- waypoint 坐标对齐 20px 网格

## 规则 5: 分层布局规划

将图表组织为视觉层/区域，形状间距 150-200px，为边路由留出通道。

```
层 1 (y=80):    [Node A]        [Node B]        [Node C]
                    ↓               ↓               ↓
层 2 (y=200):   [Node D]        [Node E]        [Node F]
                    ↓               ↓
层 3 (y=320):               [Node G]
```

## 规则 6: 自然连接点

基于流向选择连接点：

| 流向 | exit 位置 | entry 位置 |
|------|----------|-----------|
| 自上而下 | exitX=0.5, exitY=1 (底部) | entryX=0.5, entryY=0 (顶部) |
| 自左向右 | exitX=1, exitY=0.5 (右侧) | entryX=0, entryY=0.5 (左侧) |
| 自右向左 | exitX=0, exitY=0.5 (左侧) | entryX=1, entryY=0.5 (右侧) |
| 自下而上 | exitX=0.5, exitY=0 (顶部) | entryX=0.5, entryY=1 (底部) |

**禁止**：使用角落作为连接点 (如 exitX=0, exitY=0)

## 规则 7: 复杂路由先删减

对于复杂图表，先减少边数，再用 1-2 个 waypoint 形成正交 L/U 形路径。Z 形路径只用于少数关键跨列连接。

```xml
<!-- U 形路由：绕过中间节点 -->
<Array as="points">
  <mxPoint x="300" y="100"/>
  <mxPoint x="300" y="400"/>
</Array>

<!-- Z 形路由：仅用于极少数关键长距离跨列连接 -->
<Array as="points">
  <mxPoint x="100" y="200"/>
  <mxPoint x="500" y="200"/>
  <mxPoint x="500" y="350"/>
</Array>
```

---

## 生成前自检清单

生成边之前，依次检查：

1. **这条边是否必须存在？** → 不必须就删除或改成注释/图例
2. **是否能和同类边合并？** → 合并为一条带标签边
3. **边是否穿越了非源/非目标的形状？** → 主路径添加 1-2 个 waypoint；次要边删除
4. **两条边是否共享同一条路径？** → 主路径调整 exit/entry 点；次要边改虚线或删除
5. **连接点是否在角落？** → 改用边的中心点
6. **能否通过重新排列形状减少边交叉？** → 只做一次局部调整，不重算全图
