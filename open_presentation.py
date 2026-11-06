#!/usr/bin/env python3
"""
presentation.html をブラウザで開く
"""

import webbrowser
import os
import sys

# HTMLファイルのパス
html_file = os.path.join(os.path.dirname(__file__), 'demo', 'presentation.html')

# ファイルの存在確認
if not os.path.exists(html_file):
    print(f"❌ エラー: {html_file} が見つかりません")
    sys.exit(1)

# ファイルを絶対パスに変換
abs_path = os.path.abspath(html_file)
file_url = f'file://{abs_path}'

print(f"🌐 ブラウザでプレゼンテーションを開いています...")
print(f"📄 ファイル: {abs_path}")
print(f"🔗 URL: {file_url}")
print()
print("💡 操作方法:")
print("   - 次へ: 右矢印キー または 『次へ』ボタン")
print("   - 戻る: 左矢印キー または 『前へ』ボタン")
print()

# ブラウザで開く
try:
    webbrowser.open(file_url)
    print("✅ ブラウザで開きました！")
except Exception as e:
    print(f"❌ ブラウザで開けませんでした: {e}")
    print(f"\n手動で以下をブラウザで開いてください:")
    print(f"  {file_url}")
    sys.exit(1)
