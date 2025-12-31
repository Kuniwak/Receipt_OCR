#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""JSONファイル修正ツール
output/*.jsonファイルがJSON文字列として保存されている問題を修正する

使用方法:
    python main_strip.py [folder]

引数:
    folder: 処理対象のフォルダ (デフォルト: 'output/')
"""

import sys
import os
import glob
import json


def strip_json_file(input_file, output_file=None):
    """JSON文字列として保存されているファイルを通常のJSONに変換

    Args:
        input_file (str): 入力ファイルパス
        output_file (str): 出力ファイルパス (Noneの場合は上書き)

    Returns:
        bool: 成功したかどうか
    """
    try:
        # ファイルを読み込む
        with open(input_file, 'r', encoding='utf-8') as f:
            # 外側のJSON（文字列）を読み込む
            json_string = json.load(f)

        # 文字列をJSONオブジェクトに変換
        json_object = json.loads(json_string)

        # 出力ファイルパスの決定
        if output_file is None:
            output_file = input_file

        # 通常のJSONとして保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_object, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        return False


def process_folder(folder):
    """フォルダ内の全JSONファイルを処理

    Args:
        folder (str): 処理対象フォルダ
    """
    # フォルダパスの末尾に/を追加
    if not folder.endswith('/'):
        folder = folder + '/'

    # JSONファイルのリストを取得
    json_files = glob.glob(folder + '*.json')

    if not json_files:
        print(f"No JSON files found in {folder}")
        return

    print(f"Found {len(json_files)} JSON files")

    success_count = 0
    fail_count = 0

    for json_file in json_files:
        print(f"Processing: {json_file}")
        if strip_json_file(json_file):
            success_count += 1
            print(f"  ✓ Success")
        else:
            fail_count += 1
            print(f"  ✗ Failed")

    print(f"\n=== Summary ===")
    print(f"Total: {len(json_files)} files")
    print(f"Success: {success_count} files")
    print(f"Failed: {fail_count} files")


def main(folder):
    """メイン処理

    Args:
        folder (str): 処理対象フォルダ
    """
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist")
        sys.exit(1)

    process_folder(folder)


if __name__ == "__main__":
    try:
        folder = sys.argv[1]
    except IndexError:
        folder = 'output/'

    main(folder)
