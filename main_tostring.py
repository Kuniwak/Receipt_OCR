#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""OCR結果JSONからテキストを抽出
Google Vision APIのOCR結果JSONファイルから、
認識されたテキストを単一の文字列として抽出する

使用方法:
    python main_tostring.py <json_file>

引数:
    json_file: Google Vision APIのOCR結果JSONファイル

出力:
    標準出力にテキストを出力
"""

import sys
import json


def extract_text_from_json(json_file):
    """JSONファイルからテキストを抽出

    Args:
        json_file (str): JSONファイルパス

    Returns:
        str: 抽出されたテキスト
    """
    try:
        # JSONファイルを読み込む
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 二重エンコードされている場合の対応
        # （文字列として読み込まれた場合は、再度デコード）
        if isinstance(data, str):
            data = json.loads(data)

        # textAnnotationsの最初の要素からdescriptionを取得
        if 'textAnnotations' in data and len(data['textAnnotations']) > 0:
            text = data['textAnnotations'][0].get('description', '')
            return text
        else:
            print(f"Warning: No text annotations found in {json_file}", file=sys.stderr)
            return ""

    except FileNotFoundError:
        print(f"Error: File not found: {json_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン処理"""
    # コマンドライン引数のチェック
    if len(sys.argv) < 2:
        print("Usage: python main_tostring.py <json_file>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  python main_tostring.py output/receipt.json", file=sys.stderr)
        sys.exit(1)

    json_file = sys.argv[1]

    # テキストを抽出
    text = extract_text_from_json(json_file)

    # 標準出力に出力
    print(text)


if __name__ == "__main__":
    main()
