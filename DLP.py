import re
import os
from pathlib import Path

# Пути привязываем к папке, где лежит сам скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "dlp.log")
DATA_FILE = os.path.join(BASE_DIR, "data", "test.txt")

# Регулярки (карта, почта, ключ)
PATTERNS = {
    "card": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "api_key": re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
}


def main():
    # Открываем лог-файл. 'a' значит "добавлять в конец" (не стирать старое)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write("\n=== НОВЫЙ ЗАПУСК ===\n")

        p = Path(DATA_FILE)
        if not p.is_file():
            msg = f"Файл не найден: {p}"
            print(msg)
            log.write(msg + "\n")
            return

        text = p.read_text(encoding="utf-8", errors="ignore")
        log.write(f"Сканирую: {p} ({len(text)} символов)\n")

        hits = 0
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                hits += 1
                frag = match.group(0)
                log.write(f"  Найдено ({name}): {frag}\n")

        log.write(f"Итого совпадений: {hits}\n")
        print(f"Готово! Результат в файле: {LOG_FILE}")


if __name__ == "__main__":
    main()