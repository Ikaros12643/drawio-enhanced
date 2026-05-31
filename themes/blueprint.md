# blueprint — 蓝图

源自 fireworks Style 3，适合正式架构文档、技术规范。

## 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#1e3a5f` | `#3b82f6` | 起点/终点 |
| process | `#1a2e4a` | `#2563eb` | 标准处理 |
| accent | `#7c2d12` | `#ea580c` | 关键转折 |
| neutral | `#1e293b` | `#64748b` | 外部系统 |
| success | `#064e3b` | `#10b981` | 成功输出 |
| warning | `#78350f` | `#f59e0b` | 决策/分支 |
| error | `#7f1d1d` | `#ef4444` | 错误路径 |
| secondary | `#312e81` | `#6366f1` | 辅助步骤 |
| storage | `#134e4a` | `#14b8a6` | 数据库/存储 |
| group | `#1e3a5f` | `#2563eb` | 分组容器 |

## 箭头颜色

| 流程类型 | 颜色 |
|---------|------|
| 主数据流 | `#60a5fa` |
| 控制流 | `#f87171` |
| 数据转换 | `#34d399` |
| 异步/事件 | `#a78bfa` |
| 反馈/循环 | `#c084fc` |

## 节点样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=4;strokeWidth=1;fontSize=13;fontColor=#bfdbfe;
```

## 箭头样式

```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=1;endArrow=classic;endFill=1;
```

## 文字样式

| 元素 | 颜色 | 字号 | 字重 |
|------|------|------|------|
| 标题 | `#93c5fd` | 16 | 600 |
| 节点 | `#bfdbfe` | 13 | 400 |
| 副标题 | `#60a5fa` | 11 | 400 |
| 箭头标签 | `#93c5fd` | 10 | 400 |

## 容器样式

```
swimlane;startSize=24;rounded=0;strokeWidth=1;strokeDashPattern=6 3;html=1;fontColor=#93c5fd;
```
