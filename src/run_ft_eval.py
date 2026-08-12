import argparse
import json
import subprocess
from pathlib import Path


def parse_args():
    """評価条件をコマンドラインから受け取る。"""
    parser = argparse.ArgumentParser(
        description="固定評価データをMLX-LMへ渡し、結果をMarkdownで保存する"
    )
    parser.add_argument("--model", required=True, help="ベースモデルのパス")
    parser.add_argument(
        "--adapter-path",
        help="LoRA adapterのパス。baseモデルの評価では指定しない",
    )
    parser.add_argument(
        "--data",
        default="dataset/eval.jsonl",
        help="評価用messages形式JSONL",
    )
    parser.add_argument("--output", required=True, help="評価結果の保存先")
    parser.add_argument(
        "--label",
        required=True,
        help="出力Markdownに記録するモデル名",
    )
    return parser.parse_args()


def load_cases(data_path):
    """JSONLを読み込み、system・user・referenceを取り出す。"""
    cases = []

    with data_path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)
            messages = record["messages"]
            messages_by_role = {
                message["role"]: message["content"] for message in messages
            }

            required_roles = {"system", "user", "assistant"}
            if not required_roles.issubset(messages_by_role):
                raise ValueError(
                    f"{data_path} の{line_number}行目に必要なroleがありません"
                )

            cases.append(
                {
                    "system": messages_by_role["system"],
                    "user": messages_by_role["user"],
                    "reference": messages_by_role["assistant"],
                }
            )

    return cases


def extract_response(stdout):
    """CLI出力から、区切り線に挟まれたモデル回答だけを取り出す。"""
    sections = stdout.split("==========")

    if len(sections) < 3:
        raise ValueError("モデル回答の区切りをCLI出力から検出できませんでした")

    return sections[1].strip()


def generate(case, model, adapter_path):
    """1件の評価問題をMLX-LMへ渡す。"""
    command = [
        "mlx_lm.generate",
        "--model",
        model,
        "--system-prompt",
        case["system"],
        "--prompt",
        case["user"],
        "--max-tokens",
        "512",
        "--temp",
        "0",
    ]

    # tunedモデルの場合だけ、学習済み差分をベースモデルへ重ねる。
    if adapter_path:
        command.extend(["--adapter-path", adapter_path])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    return extract_response(result.stdout)


def build_markdown(cases, responses, label):
    """入力・reference・モデル回答を比較しやすい形へまとめる。"""
    lines = [
        f"# Day27 FT評価出力：{label}",
        "",
        "- 評価データ：`dataset/eval.jsonl`",
        "- 最大生成トークン数：512",
        "- temperature：0",
        "",
    ]

    for index, (case, response) in enumerate(
        zip(cases, responses), start=1
    ):
        lines.extend(
            [
                f"## Q{index}",
                "",
                "### user入力",
                "",
                case["user"],
                "",
                "### reference出力",
                "",
                case["reference"],
                "",
                f"### {label}の出力",
                "",
                response,
                "",
            ]
        )

    return "\n".join(lines)


def main():
    args = parse_args()
    data_path = Path(args.data)
    output_path = Path(args.output)

    cases = load_cases(data_path)
    responses = []

    for index, case in enumerate(cases, start=1):
        print(f"[{index}/{len(cases)}] 生成中...")
        response = generate(case, args.model, args.adapter_path)
        responses.append(response)

    markdown = build_markdown(cases, responses, args.label)

    # 保存先のディレクトリがなければ作り、評価結果を書き出す。
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"評価完了: {output_path}")


if __name__ == "__main__":
    main()