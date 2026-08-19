import pathlib
import re

root = pathlib.Path('.')
pattern = re.compile(r'scroll=ft\\.ScrollMode\\.AUTO,\\s*\\r?\\n\\s*scroll=ft\\.ScrollMode\\.AUTO,')

for path in sorted(root.rglob('*.py')):
    text = path.read_text(encoding='utf-8')
    new_text, count = pattern.subn('scroll=ft.ScrollMode.AUTO,', text)
    if count:
        print(f'fixed {path}: {count}')
        path.write_text(new_text, encoding='utf-8')
