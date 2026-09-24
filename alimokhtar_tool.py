import base64
import hashlib
import secrets
import shutil
import sys
from pathlib import Path

CIPHER_NAME = "alimokhtar002"
KEY = hashlib.sha256(CIPHER_NAME.encode("utf-8")).digest()
SUPPORTED_TYPES = {
    "1": ({".js"}, "JavaScript"),
    "2": ({".html", ".htm"}, "HTML"),
    "3": ({".js", ".html", ".htm"}, "JavaScript + HTML"),
}


def encrypt_code(source: Path) -> str:
    source_code = source.read_bytes()
    nonce = secrets.token_bytes(12)
    encrypted = bytes(value ^ KEY[index % len(KEY)] for index, value in enumerate(source_code))
    payload = f"{CIPHER_NAME}:" + base64.b64encode(nonce + encrypted).decode("ascii")
    key_hex = KEY.hex()
    if source.suffix.lower() == ".js":
        return (
            f"/* {CIPHER_NAME} */\n"
            f"(function(){{const p='{payload}',k='{key_hex}';"
            "const b=Uint8Array.from(atob(p.split(':')[1]),c=>c.charCodeAt(0)),n=b.slice(0,12),"
            "d=b.slice(12),x=Uint8Array.from(k.match(/../g),h=>parseInt(h,16));"
            "for(let i=0;i<d.length;i++)d[i]^=x[i%x.length];"
            "(0,eval)(new TextDecoder().decode(d));})();"
        )
    return (
        f"<!-- {CIPHER_NAME} -->\n"
        f"<script>(function(){{const p='{payload}',k='{key_hex}';"
        "const b=Uint8Array.from(atob(p.split(':')[1]),c=>c.charCodeAt(0)),d=b.slice(12),"
        "x=Uint8Array.from(k.match(/../g),h=>parseInt(h,16));"
        "for(let i=0;i<d.length;i++)d[i]^=x[i%x.length];"
        "document.write(new TextDecoder().decode(d));})();</script>"
    )


def process_file(source: Path, target: Path, encrypt: bool) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if encrypt:
        target.write_text(encrypt_code(source), encoding="utf-8", newline="")
    else:
        shutil.copy2(source, target)


def ask_choice() -> tuple[set[str], str]:
    print("\nChoose the file types to obfuscate:")
    print("  1 - JavaScript only (.js)")
    print("  2 - HTML only (.html and .htm)")
    print("  3 - JavaScript and HTML")
    while True:
        choice = input("\nYour choice [1/2/3]: ").strip()
        if choice in SUPPORTED_TYPES:
            return SUPPORTED_TYPES[choice]
        print("Invalid choice. Enter 1, 2, or 3.")


def unique_output_folder(source: Path) -> Path:
    base = source.parent / f"{source.name}_{CIPHER_NAME}"
    output = base
    counter = 1
    while output.exists():
        output = source.parent / f"{base.name}_{counter}"
        counter += 1
    return output


def obfuscate_folder(source: Path, extensions: set[str]) -> tuple[Path, int]:
    output = unique_output_folder(source)
    files = [path for path in source.rglob("*") if path.is_file()]
    protected = [path for path in files if path.suffix.lower() in extensions]
    if not protected:
        raise ValueError("No files matching your selection were found.")
    print(f"\nFound {len(protected)} code file(s). Encrypting selected code...")
    for number, path in enumerate(files, start=1):
        relative = path.relative_to(source)
        target = output / relative
        process_file(path, target, path in protected)
        print(f"[{number}/{len(files)}] {relative}")
    return output, len(protected)


def main() -> int:
    print("=" * 58)
    print(" alimokhtar002 | HTML and JavaScript code protection via CMD")
    print("=" * 58)
    print("\n1 - Obfuscate files")
    operation = input("\nYour choice [1]: ").strip()
    source = Path(input("Source folder path: ").strip().strip('"')).expanduser()
    if not source.is_dir():
        print("Error: The source folder does not exist.")
        return 1
    try:
        if operation != "1":
            print("Error: Choose 1.")
            return 1
        extensions, label = ask_choice()
        output, count = obfuscate_folder(source, extensions)
        print(f"\nEncrypted {count} {label} code file(s). Other files were copied unchanged.")
        print(f"Output folder: {output}")
        print("The original files were not changed or deleted.")
        return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 1
    except Exception as error:
        print(f"\nOperation failed: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())