# PPMM - Python Pip Mirror Manager

ppmm 是一个命令行工具，用于管理 Python 包管理器（pip）的源。它允许您轻松地列出、切换、测试 pip 源，以及添加、删除和重命名源。

## 特性

- 使用 `mm ls` 列出可用源
- 使用 `mm use <名称>` 切换源
- 使用 `mm test` 测试源的响应时间
- 使用 `mm current` 显示当前使用的源
- 使用 `mm add <名称> <URL>` 添加新的源
- 使用 `mm rm <名称>` 删除指定的源
- 使用 `mm rename <旧名称> <新名称>` 重命名源
- 使用 `mm help` 显示帮助信息

## 安装

您可以使用 pip 安装 ppmm：

```bash
pip install ppmm
```

## 使用方法

### 列出源

列出所有可用源：

```bash
mm ls
```

### 切换源

切换到特定源，例如 阿里云：

```bash
mm use ali
```

### 测试源

测试所有源的响应时间：

```bash
mm test
```

### 查看当前源

检查当前使用的源：

```bash
mm current
```

### 添加新的源

添加一个新的源：

```bash
mm add <名称> <URL>
```

### 删除源

删除一个已存在的源：

```bash
mm rm <名称>
```

### 重命名源

重命名一个源：

```bash
mm rename <旧名称> <新名称>
```

### 帮助

显示帮助信息：

```bash
mm help
```

## 贡献

欢迎贡献！请提出问题或提交拉取请求。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件。
