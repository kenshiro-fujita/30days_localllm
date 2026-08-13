import re
import time
from pathlib import Path

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    timeout=300.0,
)

MODEL = "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF:Q5_K_M"
OUTPUT_PATH = Path("eval/runs/day28_tinyswallow_general.md")
MAX_TOKENS = 512
TEMPERATURE = 0


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


def generate(prompt):
    """Ollama上のTinySwallowへ、固定した条件で1問を送る。"""
    started_at = time.perf_counter()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    elapsed = time.perf_counter() - started_at
    return completion.choices[0].message.content or "", elapsed


def build_markdown(questions, prompts, responses, elapsed_times):
    """条件、実際の入力、モデル回答をMarkdownへまとめる。"""
    lines = [
        "# Day28 汎用評価出力：TinySwallow 1.5B Q5_K_M / Ollama",
        "",
        f"- モデル：`{MODEL}`",
        "- 質問：`eval/questions.md`",
        "- 素材：`eval/materials.md`",
        f"- 最大生成トークン数：{MAX_TOKENS}",
        f"- temperature：{TEMPERATURE}",
        "",
    ]

    for question, prompt, response, elapsed in zip(
        questions, prompts, responses, elapsed_times
    ):
        lines.extend(
            [
                f"## Q{question['number']}. {question['title']}",
                "",
                "### モデルへ渡した入力",
                "",
                prompt,
                "",
                "### TinySwallowの出力",
                "",
                response,
                "",
                f"生成時間：{elapsed:.2f}秒",
                "",
            ]
        )

    return "\n".join(lines)


def main():
    questions = parse_questions(
        Path("eval/questions.md").read_text(encoding="utf-8")
    )
    materials = parse_materials(
        Path("eval/materials.md").read_text(encoding="utf-8")
    )

    prompts = []
    responses = []
    elapsed_times = []
    for index, question in enumerate(questions, start=1):
        prompt = build_prompt(question, materials)
        print(f"[{index}/{len(questions)}] Q{question['number']} 生成中...")
        response, elapsed = generate(prompt)
        prompts.append(prompt)
        responses.append(response)
        elapsed_times.append(elapsed)
        print(f"完了: {elapsed:.2f}秒")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        build_markdown(questions, prompts, responses, elapsed_times),
        encoding="utf-8",
    )
    print(f"評価完了: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
