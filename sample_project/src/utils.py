from pathlib import Path


def load_numbers(path: Path) -> list[int]:
    raw = path.read_text(encoding="utf-8").strip().splitlines()
    values = [line.strip() for line in raw[1:] if line.strip()]
    return [int(value) for value in values]


def summarize_numbers(numbers: list[int]) -> dict[str, float]:
    total = sum(numbers)
    average = total / len(numbers)
    return {
        "count": float(len(numbers)),
        "total": float(total),
        "average": float(average),
    }
