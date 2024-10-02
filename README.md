# PPMM - Python Pip Mirror Manager

English documentation: [README.md](https://github.com/Xu-Lan/ppmm/blob/main/README.md)

中文文档: [README-zh.md](https://github.com/Xu-Lan/ppmm/blob/main/README-zh.md)

ppmm is a command-line tool for managing Python package manager (pip) mirrors. It allows you to easily list、switch、 test pip mirrors, as well as add、 edit、delete、and rename mirrors.

## Features

- Use `mm ls` to list available mirrors
- Use `mm use <name>` to switch mirrors
- Use `mm test` to test the response time of mirrors
- Use `mm current` to display the currently used mirror
- Use `mm add <name> <URL>` to add a new mirror
- Use `mm edit <name> <URL>` to modify a specified mirror
- Use `mm rm <name>` to delete a specified mirror
- Use `mm rename <old name> <new name>` to rename a mirror
- Use `mm help` to display help information

## Installation

You can install ppmm using pip:

```bash
pip install ppmm
```

## Usage

### Listing mirrors

List all available mirrors:

```bash
mm ls
```

### Switching mirrors

Switch to a specific mirror, for example，Alibaba Cloud:

```bash
mm use ali
```

### Testing mirrors

Test the response time of all mirrors:

```bash
mm test
```

### Viewing Current mirror

Check the currently used mirror:

```bash
mm current
```

### Adding a New mirror

Add a new mirror:

```bash
mm add <name> <URL>
```

### Edit a mirror

Edit the URL of a mirror:

```bash
mm edit <name> <URL>
```

### Deleting a mirror

Delete an existing mirror:

```bash
mm rm <name>
```

### Renaming a mirror

Rename a mirror:

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
