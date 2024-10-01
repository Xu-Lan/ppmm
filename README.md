# PPMM - Python Pip Mirror Manager

English documentation: [README.md](https://github.com/Xu-Lan/ppmm/blob/main/README.md)

中文文档: [README-zh.md](https://github.com/Xu-Lan/ppmm/blob/main/README-zh.md)

ppmm is a command-line tool for managing Python package manager (pip) sources. It allows you to easily list, switch, test pip sources, as well as add, edit,delete, and rename sources.

## Features

- Use `mm ls` to list available sources
- Use `mm use <name>` to switch sources
- Use `mm test` to test the response time of sources
- Use `mm current` to display the currently used source
- Use `mm add <name> <URL>` to add a new source
- Use `mm edit <名称> <URL>` to modify a specified source
- Use `mm rm <name>` to delete a specified source
- Use `mm rename <old name> <new name>` to rename a source
- Use `mm help` to display help information

## Installation

You can install ppmm using pip:

```bash
pip install ppmm
```

## Usage

### Listing Sources

List all available sources:

```bash
mm ls
```

### Switching Sources

Switch to a specific source, for example, Alibaba Cloud:

```bash
mm use ali
```

### Testing Sources

Test the response time of all sources:

```bash
mm test
```

### Viewing Current Source

Check the currently used source:

```bash
mm current
```

### Adding a New Source

Add a new source:

```bash
mm add <name> <URL>
```

### Edit a mirror

Edit the URL of a mirror:

```bash
mm edit <name> <URL>
```

### Deleting a Source

Delete an existing source:

```bash
mm rm <name>
```

### Renaming a Source

Rename a source:

```bash
mm rename <old name> <new name>
```

### Help

Display help information:

```bash
mm help
```

## Contributing

Contributions are welcome! Please raise issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Xu-Lan/ppmm/blob/main/LICENSE) file for details.
