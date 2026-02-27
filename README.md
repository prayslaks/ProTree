# protree

Print a directory tree in markdown/README style.
Designed for Unreal Engine projects, but works with any directory.

```
MyProject/
├── Config/
├── Content/
│   ├── Characters/
│   └── Maps/
├── Source/
│   ├── MyProject/
│   └── MyProjectEditor/
└── MyProject.uproject
```

---

## Installation

### Option A — Run as Python script
```
python protree.py [root] [options]
```

### Option B — Build a standalone .exe (Windows)
```
build.bat
```
This will:
1. Install PyInstaller
2. Build `dist/protree.exe` (single file, no Python required)
3. Optionally copy to `%USERPROFILE%\tools\` and register in user PATH

After installation, use from anywhere:
```
protree C:\MyProject
```

---

## Usage

```
protree [root] [options]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--depth N` | `-d N` | Limit tree depth (default: unlimited) |
| `--output FILE` | `-o FILE` | Write output to file instead of stdout |
| `--version` | `-v` | Show version and exit |
| `--help` | `-h` | Show help message |

### Examples

```
protree                          # current directory, full depth
protree C:\MyProject             # specific directory
protree . --depth 3              # limit to 3 levels
protree . --output tree.txt      # save to file
protree -v                       # protree 1.0.0
```

---

## Config Files

Place these files in the target directory to control the output.

### `.gitignore` — hide entries completely
Files and directories matching `.gitignore` patterns are excluded from the tree entirely.

```
# .gitignore
Binaries/
Intermediate/
Saved/
*.pdb
```

### `.ptignore` — collapse directories
Directories matching `.ptignore` patterns are shown in the tree but **not expanded** (their contents are hidden). Useful for large folders you want to acknowledge but not detail.

```
# .ptignore
Plugins/
Content/
```

Result:
```
MyProject/
├── Content/        ← shown, not expanded
├── Plugins/        ← shown, not expanded
└── Source/
    └── MyProject/
```

---

## Always Excluded

Regardless of any config files, the following are always hidden:
- `.git/`
- `__pycache__/`
- `node_modules/`
