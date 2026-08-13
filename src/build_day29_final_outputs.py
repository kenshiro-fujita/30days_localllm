"""Day29で使う保存済みモデル出力を、質問単位の1ファイルへ統合する。"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "eval" / "runs"


def split_questions(path: Path) -> list[tuple[str, str]]:
    """MarkdownをQ見出しごとの本文へ分割する。"""
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## Q(\d+)(?:\.[^\n]*)?\n", text, re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1), text[match.end() : end].strip()))
    return sections


def field(section: str, heading: str, next_headings: tuple[str, ...] = ()) -> str:
    """指定したH3見出しから、次の対象H3見出しまでを抜き出す。"""
    start_match = re.search(rf"^### {re.escape(heading)}\n", section, re.MULTILINE)
    if not start_match:
        raise ValueError(f"見出しが見つかりません: {heading}")

    end = len(section)
    for next_heading in next_headings:
        next_match = re.search(
            rf"^### {re.escape(next_heading)}\n",
            section[start_match.end() :],
            re.MULTILINE,
        )
        if next_match:
            end = min(end, start_match.end() + next_match.start())
    return section[start_match.end() : end].strip()


def by_number(path: Path) -> dict[str, str]:
    return dict(split_questions(path))


def main() -> None:
    general_base = by_number(RUNS / "day27_qwen_base_general.md")
    general_tuned = by_number(RUNS / "day27_qwen_tuned_general.md")
    general_tiny = by_number(RUNS / "day28_tinyswallow_general.md")
    ft_base = by_number(RUNS / "day27_qwen_base_ft.md")
    ft_tuned = by_number(RUNS / "day27_qwen_tuned_ft.md")

    lines = [
        "# Day29 最終比較用の統合出力",
        "",
        "保存済みのモデル出力を、モデル別ではなく質問別に並べ直したファイルです。",
        "モデルは再実行していません。回答本文も要約せず、そのまま収録しています。",
        "",
        "## 早見表",
        "",
        "| 評価 | ケース | 比較対象 |",
        "| --- | ---: | --- |",
        "| 汎用評価 | 10件 | TinySwallow / base Qwen / tuned Qwen |",
        "| FTタスク評価 | 10件 | reference / base Qwen / tuned Qwen |",
        "",
        "## 汎用評価",
        "",
    ]

    for number in map(str, range(1, 11)):
        base_section = general_base[number]
        question = field(base_section, "モデルへ渡した入力", ("base Qwenの出力",))
        base_output = field(base_section, "base Qwenの出力")
        tuned_output = field(general_tuned[number], "tuned Qwenの出力")
        tiny_output = field(general_tiny[number], "TinySwallowの出力")
        lines.extend(
            [
                f"### 汎用Q{number}",
                "",
                "#### 入力",
                "",
                question,
                "",
                "#### TinySwallow",
                "",
                tiny_output,
                "",
                "#### base Qwen",
                "",
                base_output,
                "",
                "#### tuned Qwen",
                "",
                tuned_output,
                "",
            ]
        )

    lines.extend(["## FTタスク評価", ""])
    for number in map(str, range(1, 11)):
        base_section = ft_base[number]
        user_input = field(base_section, "user入力", ("reference出力", "base Qwenの出力"))
        reference = field(base_section, "reference出力", ("base Qwenの出力",))
        base_output = field(base_section, "base Qwenの出力")
        tuned_output = field(ft_tuned[number], "tuned Qwenの出力")
        lines.extend(
            [
                f"### FT Q{number}",
                "",
                "#### 入力",
                "",
                user_input,
                "",
                "#### reference",
                "",
                reference,
                "",
                "#### base Qwen",
                "",
                base_output,
                "",
                "#### tuned Qwen",
                "",
                tuned_output,
                "",
            ]
        )

    output = RUNS / "day29_final_outputs.md"
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"作成しました: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
