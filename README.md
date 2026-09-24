# alimokhtar002

`alimokhtar002` is a lightweight Windows CMD utility that protects the source code inside HTML and JavaScript files while preserving their original filenames and extensions.

The tool creates a separate copy of a website, encrypts the selected HTML/JavaScript source into a runtime payload labeled `alimokhtar002`, and copies all other website assets unchanged.

## Features

- CMD-based interactive workflow.
- Process JavaScript files only, HTML files only, or both.
- Supports `.js`, `.html`, and `.htm` files.
- Keeps the original filenames and extensions.
- Preserves the original folder structure.
- Copies CSS, images, fonts, JSON, videos, and other files unchanged.
- Creates a new output folder without modifying the source website.
- Includes a runtime loader so supported pages can continue to run in the browser.
- Requires no password and no configuration file.
- Uses the `alimokhtar002` identifier inside the generated payload.

## Requirements

- Windows 10 or newer.
- Python 3.10 or newer.

The current implementation uses Python's standard library. `requirements.txt` is included so the project can be extended consistently in the future.

## Installation

Clone the repository or download the project, then open CMD or PowerShell inside the project folder.

```powershell
python --version
python alimokhtar_tool.py
```

The optional dependency installation command is:

```powershell
python -m pip install -r requirements.txt
```

You can also launch the tool with the included Windows script:

```cmd
run_alimokhtar.cmd
```

## Usage

1. Start `run_alimokhtar.cmd` or run `python alimokhtar_tool.py`.
2. Select `1 - Obfuscate files`.
3. Enter the full path to the website folder.
4. Select one of the processing modes:
   - `1` - JavaScript only
   - `2` - HTML only
   - `3` - JavaScript and HTML
5. The tool creates a new folder beside the source folder.

Example:

```text
Source folder: C:\Projects\my-site
Output folder: C:\Projects\my-site_alimokhtar002
```

If an output folder with the same name already exists, the tool creates a numbered folder such as `my-site_alimokhtar002_1` instead of overwriting anything.

## Output Structure

Given this source folder:

```text
my-site/
├── index.html
├── scripts/
│   └── app.js
├── styles/
│   └── site.css
└── assets/
	└── logo.png
```

The generated folder keeps the same structure:

```text
my-site_alimokhtar002/
├── index.html          # Contains an alimokhtar002 runtime payload
├── scripts/
│   └── app.js           # Contains an alimokhtar002 runtime payload
├── styles/
│   └── site.css         # Copied unchanged
└── assets/
	└── logo.png         # Copied unchanged
```

The source folder is never deleted or modified.

## Important Security Notes

This project is designed for lightweight source protection and distribution, not for protecting secrets from a determined reverse engineer.

The browser must receive the runtime loader and its decoding material in order to execute the site. Therefore, a user who can run the website can eventually inspect or recover the original HTML/JavaScript code.

Do not place passwords, API keys, private tokens, database credentials, or other secrets in frontend code. Frontend code is always delivered to the client and cannot be kept genuinely secret.

## Compatibility Notes

The generated output is intended for standard HTML pages and regular JavaScript files. Projects that depend on strict Content Security Policy rules, JavaScript module syntax such as `import`/`export`, unusual loading pipelines, or server-side rendering may require additional testing or configuration.

Always test the generated folder in the same environment where it will be deployed before replacing the original site.

## Project Files

```text
alimokhtar_tool.py    # Main CMD application
run_alimokhtar.cmd    # Windows launcher
requirements.txt      # Dependency list
README.md             # Documentation
```

## License

All Reverses Back To AliMokhtar
