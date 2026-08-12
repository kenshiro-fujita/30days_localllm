import argparse
import re
import subprocess
from pathlib import Path


SYSTEM_PROMPT = (
    "質問に日本語で回答してください。与えられた素材がある場合は、"
    "素材にない情報を推測せず、素材を根拠に回答してください。"
)

MATERIALS_BY_QUESTION = {
    6: ["A"],
    7: ["B"],
    8: ["C"],
    9: ["D"],
    10: ["A", "C"],
}


def parse_args():
    """モデル、adapter、保存先などの評価条件を受け取る。"""
    parser = argparse.ArgumentParser(
        description="固定した汎用質問10件をMLX-LMで評価する"
    )
    parser.add_argument("--model", required=True, help="ベースモデルのパス")
    parser.add_argument(
        "--adapter-path",
        help="LoRA adapterのパス。base評価では指定しない",
    )
    parser.add_argument(
        "--questions",
        default="eval/questions.md",
        help="固定評価質問のMarkdown",
    )
    parser.add_argument(
        "--materials",
        default="eval/materials.md",
        help="固定評価素材のMarkdown",
    )
    parser.add_argument("--output", required=True, help="評価結果の保存先")
    parser.add_argument("--label", required=True, help="評価するモデルの表示名")
    return parser.parse_args()


def parse_questions(text):
    """Q1〜Q10の見出しと質問本文をMarkdownから取り出す。"""
    pattern = re.compile(
        r"^### Q(\d+)\. (.+?)\n\n(.*?)(?=^### Q\d+\.|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    questions = []

    for number, title, body in pattern.findall(text):
        questions.append(
            {
                "number": int(number),
                "title": title.strip(),
                "body": body.strip(),
            }
        )

    if [question["number"] for question in questions] != list(range(1, 11)):
        raise ValueError("eval/questions.md からQ1〜Q10を取得できませんでした")

    return questions


def parse_materials(text):
    """素材A〜Dを、それぞれ次の素材見出しまでの範囲で取り出す。"""
    pattern = re.compile(
        r"^## 素材([A-D]):.*?\n(.*?)(?=^## 素材[A-D]:|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    materials = {name: body.strip() for name, body in pattern.findall(text)}

    if set(materials) != {"A", "B", "C", "D"}:
        raise ValueError("eval/materials.md から素材A〜Dを取得できませんでした")

    return materials


def build_prompt(question, materials):
    """素材が必要な質問では、該当素材と質問本文を一つにまとめる。"""
    material_names = MATERIALS_BY_QUESTION.get(question["number"], [])
    parts = []

    for name in material_names:
        parts.extend([f"【素材{name}】", materials[name], ""])

    parts.extend(["【質問】", question["body"]])
    return "\n".join(parts)


def extract_response(stdout):
    """CLIの区切り線に挟まれたモデル回答だけを取得する。"""
    sections = stdout.split("==========")
    if len(sections) < 3:
        raise ValueError("モデル回答の区切りを検出できませんでした")
    return sections[1].strip()


def generate(prompt, model, adapter_path):
    """同じsystem指示と生成条件で1問を実行する。"""
    command = [
        "mlx_lm.generate",
        "--model",
        model,
        "--system-prompt",
        SYSTEM_PROMPT,
        "--prompt",
        prompt,
        "--max-tokens",
        "512",
        "--temp",
        "0",
    ]

    if adapter_path:
        command.extend(["--adapter-path", adapter_path])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )
    return extract_response(result.stdout)


def build_markdown(questions, prompts, responses, label):
    """条件、実際の入力、モデル回答をMarkdownへまとめる。"""
    lines = [
        f"# Day27 汎用評価出力：{label}",
        "",
        "- 質問：`eval/questions.md`",
        "- 素材：`eval/materials.md`",
        "- 最大生成トークン数：512",
        "- temperature：0",
        "",
    ]

    for question, prompt, response in zip(questions, prompts, responses):
        lines.extend(
            [
                f"## Q{question['number']}. {question['title']}",
                "",
                "### モデルへ渡した入力",
                "",
                prompt,
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
    questions = parse_questions(Path(args.questions).read_text(encoding="utf-8"))
    materials = parse_materials(Path(args.materials).read_text(encoding="utf-8"))

    prompts = []
    responses = []
    for index, question in enumerate(questions, start=1):
        prompt = build_prompt(question, materials)
        print(f"[{index}/{len(questions)}] Q{question['number']} 生成中...")
        prompts.append(prompt)
        responses.append(generate(prompt, args.model, args.adapter_path))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_markdown(questions, prompts, responses, args.label),
        encoding="utf-8",
    )
    print(f"評価完了: {output_path}")


if __name__ == "__main__":
    main()
