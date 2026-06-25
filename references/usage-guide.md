# Draw.io 使用指南

## 打开文件

生成 `.drawio` 文件后，使用以下命令打开：

| 环境 | 命令 |
|------|------|
| macOS | `open <file>` |
| Linux (native) | `xdg-open <file>` |
| WSL2 | `cmd.exe /c start "" "$(wslpath -w <file>)"` |
| Windows | `start <file>` |

### WSL2 特殊处理

- `wslpath -w <file>` 将 WSL 路径转换为 Windows 路径（如 `/home/user/diagram.drawio` → `C:\Users\...`）
- 空字符串 `""` 在 `start` 后是必需的，防止将文件名误认为窗口标题

**WSL2 示例**：
```bash
cmd.exe /c start "" "$(wslpath -w diagram.drawio)"
```

---

## 导出格式

用户要求导出，或交付结果适合直接预览时，使用 draw.io CLI 进行导出。默认导出 PNG，300% 缩放，透明背景，并嵌入 diagram XML。

### 支持的格式

| 格式 | 嵌入 XML | 适用场景 |
|------|----------|---------|
| PNG | ✅ `-e` | 通用查看、嵌入文档 |
| SVG | ✅ `-e` | 矢量缩放、网页嵌入 |
| PDF | ✅ `-e` | 打印、正式文档 |
| JPG | ❌ | 有损压缩，不推荐 |

PNG、SVG、PDF 都支持 `--embed-diagram` — 导出文件包含完整的 diagram XML，在 draw.io 中打开可恢复编辑。

### 导出命令

```bash
drawio -x -f <format> -e -b 10 -o <output> <input.drawio>
```

默认 PNG 导出：

```bash
drawio -x -f png -e -t -s 3 -o <output.png> <input.drawio>
```

| 参数 | 说明 |
|------|------|
| `-x` / `--export` | 导出模式 |
| `-f` / `--format` | 输出格式 (png, svg, pdf, jpg) |
| `-e` / `--embed-diagram` | 嵌入 diagram XML (PNG/SVG/PDF) |
| `-o` / `--output` | 输出文件路径 |
| `-b` / `--border` | 图表周围边框宽度 (默认 0) |
| `-t` / `--transparent` | 透明背景 (PNG only) |
| `-s` / `--scale` | 缩放比例 |
| `--width` / `--height` | 指定尺寸 (保持宽高比) |
| `-a` / `--all-pages` | 导出所有页面 (PDF only) |
| `-p` / `--page-index` | 指定页面 (1-based) |

### CLI 定位

检测环境后，按以下路径查找 draw.io CLI：

| 环境 | CLI 路径 |
|------|---------|
| WSL2 | `/mnt/c/Program Files/draw.io/draw.io.exe` |
| WSL2 (备用) | `/mnt/c/Users/$WIN_USER/AppData/Local/Programs/draw.io/draw.io.exe` |
| macOS | `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Linux (native) | `drawio` (通常在 PATH 上) |
| Windows | `C:\Program Files\draw.io\draw.io.exe` |

**检测命令**：
```bash
# 检查是否在 WSL2
grep -qi microsoft /proc/version 2>/dev/null && echo "WSL2"

# 检查 CLI 是否在 PATH 上
which drawio 2>/dev/null || where drawio 2>/dev/null
```

**WSL2 默认 PNG 导出示例**：
```bash
`/mnt/c/Program Files/draw.io/draw.io.exe` -x -f png -e -t -s 3 -o diagram.drawio.png diagram.drawio
```

---

## 文件命名

- 使用描述性名称，基于图表内容 (如 `login-flow`, `database-schema`)
- 使用小写字母和连字符 (如 `ci-cd-pipeline.drawio`)
- 导出时使用双扩展名：`name.drawio.png`, `name.drawio.svg`, `name.drawio.pdf` — 表示文件包含嵌入的 diagram XML
- 保留 `.drawio` 源文件，便于后续继续编辑

---

## 选择输出格式

根据用户请求判断格式偏好：

- `/drawio create a flowchart` → `flowchart.drawio`
- `/drawio png flowchart for login` → `login-flow.drawio.png`
- `/drawio svg: ER diagram` → `er-diagram.drawio.svg`
- `/drawio pdf architecture overview` → `architecture-overview.drawio.pdf`

如果用户没有指定格式，保存 `.drawio` 文件；如适合直接预览，另行默认导出 PNG（300% 缩放、透明背景）。

---

## Troubleshooting

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| draw.io CLI 找不到 | 桌面版未安装或不在 PATH | 保留 `.drawio` 文件，提示用户安装 draw.io 桌面版或手动打开 |
| 导出空白/损坏文件 | XML 格式错误 (如注释中的双连字符、未转义字符) | 导出前验证 XML；使用 `scripts/fix-xml.py` 修复 |
| 图表打开后空白 | 缺少 root cells `id="0"` 和 `id="1"` | 确保 mxGraphModel 结构完整 |
| 边不渲染 | 边 mxCell 是自关闭标签 (缺少子 mxGeometry) | 每条边必须有 `<mxGeometry relative="1" as="geometry" />` 子元素 |
| 导出后无法打开 | 文件路径错误或缺少文件关联 | 打印绝对文件路径供用户手动打开 |
| WSL2 打开失败 | 路径未转换 | 使用 `wslpath -w` 将 WSL 路径转为 Windows 路径 |
