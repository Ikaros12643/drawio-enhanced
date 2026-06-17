# cloud-brand — 云厂商品牌

云架构图专用主题。只有用户明确要求云厂商架构图时使用，并且必须明确云厂商：AWS、Azure 或 GCP。若用户只说“云架构图”但没有指定厂商，先询问使用哪个云厂商，不要默认猜测。

## AWS 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#FFF4E6` | `#ED7100` | EC2/计算/核心服务 |
| process | `#EAF4D3` | `#7AA116` | S3/存储/数据处理 |
| accent | `#E0F7F4` | `#01A88D` | Bedrock/AI/关键服务 |
| neutral | `#F2F3F3` | `#232F3E` | VPC/通用资源/容器 |
| success | `#EAF4D3` | `#7AA116` | 成功输出 |
| warning | `#FFF4E6` | `#ED7100` | 队列/异步/提示 |
| error | `#FDE8E8` | `#D13212` | 错误/告警 |
| secondary | `#F8E7FA` | `#C925D1` | DynamoDB/特殊数据服务 |
| storage | `#F8E7FA` | `#C925D1` | 数据库/持久化 |
| group | `#FFFFFF` | `#232F3E` | 账号/VPC/可用区边界 |

## Azure 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#E5F1FB` | `#0078D4` | 核心 Azure 服务 |
| process | `#E8F5E9` | `#4CAF50` | 资源组/处理服务 |
| accent | `#FFF4E5` | `#F7630C` | 关键转换/集成服务 |
| neutral | `#F3F2F1` | `#605E5C` | 通用资源/外部系统 |
| success | `#E8F5E9` | `#107C10` | 成功输出 |
| warning | `#FFF8E1` | `#FFB900` | 提示/队列/风险 |
| error | `#FDE7E9` | `#D13438` | 错误/告警 |
| secondary | `#F3E5F5` | `#8661C5` | 辅助服务/特殊模块 |
| storage | `#E6F2FB` | `#0078D4` | Storage/Cosmos DB/SQL |
| group | `#FFFFFF` | `#0078D4` | 订阅/资源组/VNet 边界 |

## GCP 色板

| 角色 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| primary | `#E8F0FE` | `#4285F4` | 计算/核心 GCP 服务 |
| process | `#E6F4EA` | `#34A853` | 数据处理/正常流程 |
| accent | `#FEF7E0` | `#FBBC04` | 关键转换/提示 |
| neutral | `#F4F4F4` | `#5F6368` | 通用资源/外部系统 |
| success | `#E6F4EA` | `#34A853` | 成功输出 |
| warning | `#FEF7E0` | `#FBBC04` | 决策/风险 |
| error | `#FCE8E6` | `#EA4335` | 错误/告警 |
| secondary | `#F3E8FD` | `#A142F4` | 辅助服务/特殊模块 |
| storage | `#E8F0FE` | `#4285F4` | Cloud Storage/数据库 |
| group | `#FFFFFF` | `#5C85DE` | 项目/VPC/区域边界 |

## 箭头颜色

按指定云厂商使用对应主品牌色：AWS `#232F3E`，Azure `#0078D4`，GCP `#4285F4`。控制流和错误路径使用对应 error 边框色，弱关系使用 `#9E9E9E` 虚线。

## 节点样式

```
rounded=1;whiteSpace=wrap;html=1;arcSize=6;strokeWidth=1.5;fontSize=13;
```

## 箭头样式

```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;endArrow=classic;endFill=1;
```

## 文字样式

| 元素 | 颜色 | 字号 | 字重 |
|------|------|------|------|
| 标题 | `#202124` | 16 | 600 |
| 节点 | `#202124` | 13 | 400 |
| 副标题 | `#5F6368` | 11 | 400 |
| 箭头标签 | `#5F6368` | 10 | 400 |

## 容器样式

```
swimlane;startSize=26;rounded=1;arcSize=6;strokeWidth=1.3;strokeDashPattern=4 3;html=1;
```
