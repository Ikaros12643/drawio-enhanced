# visio-minimal — 简洁 Visio

参考 Visio 风格的极简工程流程图：白底、黑灰线框、基础流程形状、正交连线和低装饰文本。主题不包含网格背景；截图中的网格应视为编辑器背景，而不是图表风格的一部分。

## 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#FFFFFF` | `#2F3437` | 开始/结束/主要步骤 |
| process | `#FFFFFF` | `#3C4145` | 标准处理步骤 |
| accent | `#FFFFFF` | `#2F3437` | 关键动作/人工操作 |
| neutral | `#FFFFFF` | `#5A6268` | 注释/外部系统 |
| success | `#FFFFFF` | `#3C4145` | 成功路径/正常输出 |
| warning | `#FFFFFF` | `#2F3437` | 决策/分支 |
| error | `#FFFFFF` | `#3C4145` | 异常路径/失败状态 |
| secondary | `#FFFFFF` | `#5A6268` | 辅助步骤 |
| storage | `#FFFFFF` | `#3C4145` | 数据库/存储 |
| group | `#FFFFFF` | `#AEB4B8` | 注释分组/泳道 |

## 箭头颜色

| 流程类型 | 颜色 | 用途 |
|---------|------|------|
| 主数据流 | `#2F3437` | 主流程 |
| 控制流 | `#2F3437` | 条件跳转/控制路径 |
| 数据转换 | `#3C4145` | 数据处理 |
| 异步/事件 | `#5A6268` | 辅助触发 |
| 反馈/循环 | `#5A6268` | 回退/重试 |

## 节点样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=8;strokeWidth=1.6;fontSize=13;fontColor=#22272A;shadow=0;fillColor=#FFFFFF;
```

## 箭头样式

```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1.6;endArrow=classic;endFill=1;strokeColor=#2F3437;
```

## 文字样式

| 元素 | 颜色 | 字号 | 字重 |
|------|------|------|------|
| 标题 | `#1F2326` | 15 | 600 |
| 节点 | `#22272A` | 13 | 400 |
| 副标题 | `#5A6268` | 11 | 400 |
| 箭头标签 | `#2F3437` | 11 | 400 |

## 容器样式

```
swimlane;startSize=24;rounded=0;strokeWidth=1;html=1;fontSize=13;fontColor=#22272A;fillColor=#FFFFFF;strokeColor=#AEB4B8;
```

## 使用建议

- 画布保持白底，不添加网格、纹理、阴影或渐变。
- 使用基础流程图形：圆角矩形表示开始/结束，矩形表示处理，菱形表示判断。
- 连接线使用正交折线，尽量减少颜色和装饰。
- 注释可放在流程左侧或右侧，用括号线、浅灰线框或普通文本表达。
