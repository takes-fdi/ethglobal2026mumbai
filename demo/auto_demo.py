#!/usr/bin/env python3
"""
大人証明デモ - 自動ターミナル版
入力不要な完全自動デモンストレーション
"""

import time
import sys
import os

class Colors:
    """ANSIカラーコード"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    """画面をクリア"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_progress_bar(current, total, label="", length=40):
    """プログレスバーを表示"""
    percent = current / total
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    print(f"\r{label} [{bar}] {int(percent*100)}%", end='', flush=True)
    if current == total:
        print()

def demo_screen(title, content, duration=2):
    """デモ画面を表示"""
    clear_screen()
    print()
    print(Colors.BOLD + Colors.BLUE + "  " + title + Colors.END)
    print()
    print(content)
    print()
    time.sleep(duration)

def run_auto_demo():
    """自動デモを実行"""
    
    # タイトル
    clear_screen()
    print()
    print(Colors.BOLD + Colors.BLUE)
    print("╔" + "═" * 60 + "╗")
    print("║" + "🎫 大人証明デモ - 自動デモンストレーション".center(60) + "║")
    print("║" + "Adult Verification Auto Demo".center(60) + "║")
    print("╚" + "═" * 60 + "╝")
    print(Colors.END)
    print()
    print("  完全なユーザーフローをシミュレートしています...")
    print()
    time.sleep(2)
    
    # 画面1: スプラッシュスクリーン
    demo_screen(
        "1️⃣  スプラッシュスクリーン",
        """
  ┌────────────────────────────────────┐
  │                                    │
  │        🎫 大人証明                 │
  │      Adult Verification           │
  │                                    │
  │  18歳以上であることを安全に       │
  │  証明する                          │
  │                                    │
  │      [🚀 始める]                   │
  │                                    │
  └────────────────────────────────────┘
  """,
        1
    )
    
    # 画面2: ウォレット生成
    print(Colors.BOLD + "  2️⃣  ウォレットを生成中..." + Colors.END)
    print()
    for i in range(101):
        print_progress_bar(i, 100, "  ", 30)
        time.sleep(0.01)
    time.sleep(1)
    
    # 画面3: シードフレーズ
    demo_screen(
        "3️⃣  シードフレーズを表示",
        """
  バックアップ用シードフレーズ（12単語）:
  
   1. abandon      2. ability      3. able
   4. about        5. above        6. absent
   7. absorb       8. abstract     9. abuse
  10. access      11. accident    12. account
  """,
        2
    )
    
    # 画面4: マイナンバーカード読取
    print(Colors.BOLD + "  4️⃣  マイナンバーカード読取中..." + Colors.END)
    print()
    for i in range(101):
        status = ["接触待機中", "データ読込中", "署名検証中"][min(i // 33, 2)]
        print_progress_bar(i, 100, f"  🔷 {status}", 30)
        time.sleep(0.015)
    time.sleep(1)
    
    # 画面5: 年齢確認成功
    demo_screen(
        "5️⃣  年齢確認成功",
        f"""
  {Colors.GREEN}✅ 成功{Colors.END}
  
  18歳以上であることを確認しました
  
  {Colors.CYAN}生年月日: 2005年3月15日
  確認日時: 2024年1月1日
  ウォレット: 0x1234...5678{Colors.END}
  """,
        2
    )
    
    # 画面6: メイン画面
    demo_screen(
        "6️⃣  メイン画面",
        f"""
  {Colors.GREEN}✅ 18歳以上確認済{Colors.END}
  ウォレット: 0x1234...5678
  確認日時: 2024/01/01
  
  📋 サービス利用履歴
  📭 まだサービス利用履歴がありません
  
  🧪 テスト機能
  [Netflix からリクエスト]
  [Amazon Prime からリクエスト]
  """,
        2
    )
    
    # 画面7: 年齢確認リクエスト
    demo_screen(
        "7️⃣  Netflix からのリクエスト確認",
        """
  Netflix からのリクエスト
  
  18歳以上であることを証明してもよろしいですか？
  個人情報は一切共有されません
  
  手数料: 0.001 ETH (約10円)
  
  [❌ キャンセル]  [✓ 許可する]
  """,
        2
    )
    
    # 画面8: トランザクション送信
    print(Colors.BOLD + "  8️⃣  トランザクション送信中..." + Colors.END)
    print()
    statuses = ["🔐 ウォレットから署名", "📤 トランザクション送信", "⏳ ブロック確認待機"]
    for i in range(101):
        status = statuses[min(i // 33, 2)]
        print_progress_bar(i, 100, f"  {status}", 30)
        time.sleep(0.015)
    print()
    print("  ✅ トランザクション送信完了！")
    print("  🔗 トランザクションハッシュ: 0x1234567890...")
    print()
    time.sleep(2)
    
    # 画面9: 完了
    demo_screen(
        "9️⃣  年齢確認完了",
        f"""
  {Colors.GREEN}✅ 完了{Colors.END}
  
  年齢確認が完了しました！
  
  {Colors.CYAN}Netflix が年齢確認を確認中...
  
  ウォレットアドレス:
  0x1234567890abcdef1234567890abcdef12345678{Colors.END}
  """,
        2
    )
    
    # 画面10: メイン画面更新
    demo_screen(
        "🔟 メイン画面（更新）",
        f"""
  {Colors.GREEN}✅ 18歳以上確認済{Colors.END}
  
  📋 サービス利用履歴
  
  ┌──────────────────────────────┐
  │ Netflix                      │
  │ 確認日時: 2024/01/01 12:34   │
  │ {Colors.GREEN}✓ アクセス許可{Colors.END}            │
  └──────────────────────────────┘
  """,
        2
    )
    
    # 完了画面
    clear_screen()
    print()
    print(Colors.BOLD + Colors.GREEN)
    print("╔" + "═" * 62 + "╗")
    print("║" + " " * 62 + "║")
    print("║" + "✅ デモ完了！".center(62) + "║")
    print("║" + " " * 62 + "║")
    print("║" + "大人証明の完全なユーザーフローをシミュレートしました。".center(62) + "║")
    print("║" + " " * 62 + "║")
    print("╚" + "═" * 62 + "╝")
    print(Colors.END)
    print()
    
    # 統計情報
    print(Colors.BOLD + "📊 デモ実行統計" + Colors.END)
    print()
    print("  ✅ 表示された画面数: 10個")
    print("  ✅ 実行されたアニメーション: 3個")
    print("  ✅ 処理の進行表示: 2個のプログレスバー")
    print("  ✅ ステップ数: 9ステップ")
    print()
    
    # 次のステップ
    print(Colors.BOLD + "🚀 Streamlit版デモの起動方法" + Colors.END)
    print()
    print("  1️⃣  Streamlit をインストール:")
    print("     pip install streamlit")
    print()
    print("  2️⃣  デモを起動:")
    print("     streamlit run app.py")
    print()
    print("  3️⃣  ブラウザで確認:")
    print("     http://localhost:8501")
    print()
    
    # 完了メッセージ
    print(Colors.BOLD + Colors.BLUE)
    print("  " + "=" * 58)
    print("  " + "デモンストレーション完了".center(58))
    print("  " + "=" * 58)
    print(Colors.END)
    print()

if __name__ == "__main__":
    try:
        run_auto_demo()
    except KeyboardInterrupt:
        print("\n\nデモを中断しました。")
        sys.exit(0)
