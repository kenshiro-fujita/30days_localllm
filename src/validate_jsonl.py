"""JSONLデータセットの構造とデータリークを検証する。"""

import argparse
import json
from pathlib import Path
from typing import Any


# 今回のデータセットで必要な会話の順序
EXPECTED_ROLES = ["system", "user", "assistant"]


def load_and_validate_jsonl(path: Path) -> list[dict[str, Any]]:
    """JSONLを読み込み、各データの構造を検証する。"""
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            # 空行は1件のデータとして扱わず、明示的にエラーにする
            if not line.strip():
                errors.append(f"{path}:{line_number}: 空行があります")
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(
                    f"{path}:{line_number}: JSONとして読み込めません: {error}"
                )
                continue

            if not isinstance(record, dict):
                errors.append(
                    f"{path}:{line_number}: 最上位はobjectである必要があります"
                )
                continue

            if "messages" not in record:
                errors.append(
                    f"{path}:{line_number}: messagesキーがありません"
                )
                continue

            messages = record["messages"]

            if not isinstance(messages, list):
                errors.append(
                    f"{path}:{line_number}: messagesはlistである必要があります"
                )
                continue

            roles = [
                message.get("role")
                for message in messages
                if isinstance(message, dict)
            ]

            if roles != EXPECTED_ROLES or len(messages) != 3:
                errors.append(
                    f"{path}:{line_number}: roleは"
                    "system → user → assistantの順で3件必要です"
                )
                continue

            # userとassistantは、学習の入力・正解として空では困る
            for message_index in (1, 2):
                message = messages[message_index]
                content = message.get("content")

                if not isinstance(content, str) or not content.strip():
                    role = EXPECTED_ROLES[message_index]
                    errors.append(
                        f"{path}:{line_number}: {role}のcontentが空です"
                    )

            records.append(record)

    if errors:
        raise ValueError("\n".join(errors))

    return records


def collect_user_contents(
    records: list[dict[str, Any]],
) -> set[str]:
    """リーク確認に使うuser入力の集合を作る。"""
    return {
        record["messages"][1]["content"]
        for record in records
    }


def check_overlap(
    first_name: str,
    first_records: list[dict[str, Any]],
    second_name: str,
    second_records: list[dict[str, Any]],
) -> list[str]:
    """2分割間で完全一致するuser入力を探す。"""
    first_users = collect_user_contents(first_records)
    second_users = collect_user_contents(second_records)
    overlaps = first_users & second_users

    return [
        f"{first_name}と{second_name}でuser入力が重複しています: {user}"
        for user in sorted(overlaps)
    ]


def parse_args() -> argparse.Namespace:
    """コマンドラインから3分割のパスを受け取る。"""
    parser = argparse.ArgumentParser(
        description="JSONLの構造と分割間のデータリークを検証します"
    )
    parser.add_argument("train", type=Path)
    parser.add_argument("valid", type=Path)
    parser.add_argument("eval", type=Path)
    return parser.parse_args()


def main() -> None:
    """3ファイルを検証し、結果を表示する。"""
    args = parse_args()

    try:
        train_records = load_and_validate_jsonl(args.train)
        valid_records = load_and_validate_jsonl(args.valid)
        eval_records = load_and_validate_jsonl(args.eval)
    except (OSError, ValueError) as error:
        raise SystemExit(f"検証エラー:\n{error}") from error

    # 評価の独立性を守るため、3分割すべての組み合わせを確認する
    overlap_errors = [
        *check_overlap("train", train_records, "valid", valid_records),
        *check_overlap("train", train_records, "eval", eval_records),
        *check_overlap("valid", valid_records, "eval", eval_records),
    ]

    if overlap_errors:
        raise SystemExit(
            "データリークを検出しました:\n" + "\n".join(overlap_errors)
        )

    print("検証成功")
    print(f"train: {len(train_records)}件")
    print(f"valid: {len(valid_records)}件")
    print(f"eval: {len(eval_records)}件")
    print("分割間のuser入力の完全一致: なし")


if __name__ == "__main__":
    main()