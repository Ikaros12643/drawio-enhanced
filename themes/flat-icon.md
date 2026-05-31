# flat-icon — 扁平图标 (默认)

源自 fireworks Style 1，适合博客、文档、演示。
使用经典六色配色系统。

## 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#dae8fc` | `#6c8ebf` | 起点/终点/用户输入 |
| process | `#d5e8d4` | `#82b366` | 标准处理步骤 |
| accent | `#fff2cc` | `#d6b656` | 关键转折点/决策 |
| neutral | `#e1d5e7` | `#9673a6` | 外部系统/数据源 |
| success | `#d5e8d4` | `#82b366` | 成功输出 |
| warning | `#fff2cc` | `#d6b656` | 决策/分支 |
| error | `#f8cecc` | `#b85450` | 错误路径 |
| secondary | `#ffe6cc` | `#d79b00` | 辅助步骤 |
| storage | `#e1d5e7` | `#9673a6` | 数据库/存储 |
| group | `#e1d5e7` | `#9673a6` | 分组容器 |

## 箭头颜色

| 流程类型 | 颜色 | 用途 |
|---------|------|------|
| 主数据流 | 跟随源节点 strokeColor | 主要请求/响应路径 |
| 控制流 | `#b85450` | 系统间触发 |
| 数据转换 | `#82b366` | 数据处理/转换 |
| 异步/事件 | `#9673a6` | 非阻塞/事件驱动 |
| 残差连接 | `#999999` | 跳跃连接 (dashed) |

## 节点样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=8;strokeWidth=1.5;fontSize=13;
```

## 箭头样式

```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;endArrow=classic;endFill=1;
```

## 文字样式

| 元素 | 颜色 | 字号 | 字重 |
|------|------|------|------|
| 标题 | `#111827` | 16 | 600 (fontStyle=1) |
| 节点 | `#111827` | 13 | 400 |
| 副标题 | `#6b7280` | 11 | 400 |
| 箭头标签 | `#6b7280` | 10 | 400 |

## 容器样式

```
swimlane;startSize=24;rounded=1;arcSize=8;strokeWidth=1;strokeDashPattern=4 3;html=1;
```
