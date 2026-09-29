# Repository Guidelines

## 项目结构

本仓库是用于生成可编辑 draw.io 图表的技能包，而非传统应用。核心工作流和 XML 约定位于 `SKILL.md`；`themes/` 存放各视觉主题的配色与样式规则；`references/` 收录形状、布局、连线等按需参考资料；`examples/` 保存主题对应的 `.drawio` 成品；`scripts/` 包含 XML 修复与结构校验工具。根目录的 `README.md` 与 `README_ZH.md` 分别为英文和中文说明，修改功能时应同步核对相关说明。

## 开发与校验命令

项目没有构建步骤或包管理文件。运行 Python 脚本时优先使用 `uv run`；本机未安装 `uv` 时，再回退到 `python`：

```powershell
uv run python scripts/check-drawio.py examples/flat-icon-cicd-flow.drawio
uv run python scripts/fix-xml.py input.drawio output.drawio
# 未安装 uv 时：python scripts/check-drawio.py examples/flat-icon-cicd-flow.drawio
```

前者检查 XML 解析、`mxCell` ID、顶点几何信息及连线端点；后者修复常见的 AI 生成 XML 格式问题。提交图表或修改脚本后，至少对受影响的 `.drawio` 文件运行校验，并在 diagrams.net 中打开进行视觉检查。

## 编写风格与命名

Python 使用 4 空格缩进、类型注解和标准库优先的实现方式；保持函数小而职责明确。Markdown 使用清晰的层级标题，正文标题从 `#` 开始，不手写序号。主题文件以小写 kebab-case 命名，例如 `tech-blue.md`；示例文件采用 `<theme>-<diagram-purpose>.drawio`，例如 `mint-org-tree.drawio`。新增样式应复用主题调色板，避免在 XML 中随意增加颜色或复杂折线。

所有新图统一使用 24 号图形组件文字、18 号连线文字，标题和分组标题默认 30 号。节点尺寸与间距须按文字实际长度和行数扩展，不能通过缩小字号解决溢出；主题、XML 模板和示例中的字号应与 `SKILL.md` 保持一致。

## 测试与示例

目前没有独立测试框架；`scripts/check-drawio.py` 是主要自动化回归检查。变更校验逻辑时，应使用 `examples/` 中多个不同结构的图表验证成功路径，并覆盖损坏 XML 或失效端点等失败情形。新增主题应同时提供主题文档和至少一个可打开、可编辑的示例。

## 提交与合并请求

提交历史采用简短的 Conventional Commit 风格，如 `feat: add drawio themes`、`fix: skill描述更改`、`docs: clarify drawio export workflow`。使用 `feat:`、`fix:`、`docs:` 等前缀，说明单一、可审阅的改动。合并请求应说明目的、涉及的主题/脚本/示例、已执行的校验命令；若视觉效果有变化，附 diagrams.net 截图，并关联相关 issue（如有）。
