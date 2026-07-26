from pathlib import Path
import json
import re
from urllib.request import Request, urlopen

MODEL = "qwen2.5:1.5b-instruct"
ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "eval" / "questions.md"
MATERIALS_PATH = ROOT / "eval" / "materials.md"
OUTPUT_PATH = ROOT / "eval" / "runs" / "day05_qwen_base.md"


def section(text: str, name: str) -> str:
    pattern = rf"^## {re.escape(name)}.*?(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"素材が見つかりません: {name}")
    return match.group(0)


questions_text = QUESTIONS_PATH.read_text(encoding="utf-8")
materials_text = MATERIALS_PATH.read_text(encoding="utf-8")

questions = re.findall(
    r"^### (Q\d+)\. (.+?)\n\n(.*?)(?=^### Q|\Z)",
    questions_text,
    flags=re.MULTILINE | re.DOTALL,
)

materials_for_question = {
    "Q6": [section(materials_text, "素材A: 会議メモ")],
    "Q7": [section(materials_text, "素材B: 架空サービスFAQ")],
    "Q8": [section(materials_text, "素材C: 申請手順メモ")],
    "Q9": [section(materials_text, "素材D: 仕様メモ")],
    "Q10": [
        section(materials_text, "素材A: 会議メモ"),
        section(materials_text, "素材C: 申請手順メモ"),
    ],
}


def ask_qwen(prompt: str) -> str:
    body = json.dumps(
        {
            "model": MODEL,
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    request = Request(
        "http://localhost:11434/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )

    with urlopen(request) as response:
        return json.loads(response.read())["message"]["content"]


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_PATH.open("w", encoding="utf-8") as output:
    output.write(f"# Day 05 Qwen Base Run\n\nモデル: `{MODEL}`\n\n")

    for question_id, title, question in questions:
        prompt_parts = materials_for_question.get(question_id, [])
        prompt_parts.append(question.strip())
        prompt = "\n\n".join(prompt_parts)

        print(f"{question_id} を実行中...")
        answer = ask_qwen(prompt)

        output.write(f"## {question_id}. {title}\n\n")
        output.write(f"### Prompt\n\n{prompt}\n\n")
        output.write(f"### Answer\n\n{answer}\n\n")

print(f"保存しました: {OUTPUT_PATH}")