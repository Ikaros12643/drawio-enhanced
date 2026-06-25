# gpt-image-architecture — GPT Image 架构图

参考 GPT Image 2 生成的正式架构图视觉：左侧垂直层级标签、右侧整层浅色容器、容器内部卡片化模块、蓝绿橙角色分区、细描边图标和轻量汇报感。适合系统架构、数据平台、业务能力地图和分层解决方案图。

## 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#EAF4FF` | `#0B63A5` | 应用层/核心能力/主入口 |
| process | `#F8FBFF` | `#6EA6D7` | 标准功能卡片 |
| accent | `#FFF3E8` | `#C75A11` | 服务支撑/资源/关键约束 |
| neutral | `#F7FAFC` | `#9AB6CC` | 外部系统/普通模块 |
| success | `#EAF7F1` | `#12805C` | 数据处理/分析/成功输出 |
| warning | `#FFF8E5` | `#D99A00` | 决策/风险/待确认内容 |
| error | `#FDECEC` | `#C43D3D` | 异常路径/失败状态 |
| secondary | `#EEF5FF` | `#477DB3` | 辅助能力/平台能力 |
| storage | `#FFF7EF` | `#D06A1A` | 数据库/数据资源/服务支撑 |
| group | `#FFFFFF` | `#7FB1D6` | 整层大容器/能力分组 |
| subGroup | `#F8FBFF` | `#9FC4E2` | 容器内子功能区 |

## 箭头颜色

| 流程类型 | 颜色 | 用途 |
|---------|------|------|
| 主数据流 | `#2F7DB8` | 层级调用/主流程 |
| 控制流 | `#C75A11` | 管理控制/配置下发 |
| 数据转换 | `#12805C` | 数据治理/模型计算 |
| 异步/事件 | `#5B8FB9` | 异步同步/接口对接 |
| 反馈/循环 | `#6B93B5` | 反馈闭环/状态回传 |

## 节点样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=8;strokeWidth=1.2;fontSize=13;fontColor=#23445E;shadow=0;
```

## 箭头样式

```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1.4;endArrow=classic;endFill=1;
```

## 文字样式

| 元素 | 颜色 | 字号 | 字重 |
|------|------|------|------|
| 标题 | `#1F4E79` | 16 | 600 |
| 节点 | `#23445E` | 13 | 400 |
| 副标题 | `#5B7184` | 11 | 400 |
| 箭头标签 | `#47708F` | 10 | 400 |

## 容器样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=3;strokeWidth=1.3;fillColor=#FFFFFF;strokeColor=#7FB1D6;shadow=0;
```

## 左侧层级标签样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=8;strokeWidth=0;fontSize=20;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=0;
```

## 使用建议

- 优先使用横向分层容器：左侧放深色垂直层级标签，右侧放对应的整层大容器。
- 每一层的大容器必须框住该层所有模块，模块不要散落在容器外。
- 单层内部使用等宽卡片、子功能区或小流程条排列，卡片内可用简短标题加 1-2 行说明。
- 层与层之间使用细长接口条，主路径用少量垂直箭头连接接口条和下一层核心模块。
- 蓝色用于应用/能力，绿色用于数据处理与分析，橙色用于数据资源与服务支撑。
- 适合少量细线图标；不建议使用大面积渐变或强阴影。
