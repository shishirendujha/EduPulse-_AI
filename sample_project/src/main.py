from pathlib import Path

from utils import load_numbers, summarize_numbers


def main() -> None:
    data_path = Path(__file__).resolve().parents[1] / "data" / "numbers.csv"
    numbers = load_numbers(data_path)
    summary = summarize_numbers(numbers)
    print("Sample Project Summary")
    print(f"Count: {summary['count']}")
    print(f"Total: {summary['total']}")
    print(f"Average: {summary['average']:.2f}")


if __name__ == "__main__":
    main()
