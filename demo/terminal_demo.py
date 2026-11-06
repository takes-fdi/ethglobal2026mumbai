#!/usr/bin/env python3
"""
大人証明デモ - ターミナル版シミュレーター
実際のStreamlitアプリの動作をターミナルで可視化
"""

import time
import sys
import os

class Colors:
    """ANSI カラーコード"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """画面をクリア"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_centered(text, width=60):
    """中央揃えで表示"""
    lines = text.split('\n')
    for line in lines:
        print(line.center(width))

def print_progress_bar(current, total, label="", length=40):
    """プログレスバーを表示"""
    percent = current / total
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    print(f"\r{label} [{bar}] {int(percent*100)}%", end='', flush=True)
    if current == total:
        print()

def screen_splash():
    """画面1: スプラッシュスクリーン"""
    clear_screen()
    print()
    print_centered("┌" + "─" * 58 + "┐")
    print_centered("│" + " " * 58 + "│")
    print_centered("│" + "🎫 大人証明".center(58) + "│")
    print_centered("│" + "Adult Verification".center(58) + "│")
    print_centered("│" + " " * 58 + "│")
    print_centered("│" + "18歳以上であることを安全に証明する".center(58) + "│")
    print_centered("│" + " " * 58 + "│")
    print_centered("│" + " " * 58 + "│")
    print_centered("│" + "[🚀 始める]".center(58) + "│")
    print_centered("│" + " " * 58 + "│")
    print_centered("└" + "─" * 58 + "┘")
    print()
    input(">>> プレスして次へ")

def screen_wallet():
    """画面2: ウォレット生成"""
    clear_screen()
    print()
    print("  ウォレットを作成")
    print()
    print("  初回利用時にウォレットを作成します。")
    print("  秘密鍵はスマートフォン内に安全に保管されます。")
    print()
    print("  [✨ ウォレットを生成する]")
    print()
    print("  生成中...")
    for i in range(101):
        print_progress_bar(i, 100, "  ", 30)
        time.sleep(0.015)
    print()
    input(">>> プレスして次へ")

def screen_seed_phrase():
    """画面3: シードフレーズ"""
    clear_screen()
    print()
    print("  シードフレーズ")
    print("  (必ず安全にバックアップ)")
    print()
    
    seed_words = [
        ("abandon", "ability"), ("able", "about"),
        ("above", "absent"), ("absorb", "abstract"),
        ("abuse", "access"), ("accident", "account")
    ]
    
    for i, (word1, word2) in enumerate(seed_words, 1):
        print(f"  {i:2d}. {word1:10s}  {i+6:2d}. {word2}")
    
    print()
    print("  [📋 コピー]  [✓ 確認しました]")
    print()
    input(">>> プレスして次へ")

def screen_mynumber_scan():
    """画面4: マイナンバーカード読取"""
    clear_screen()
    print()
    print("  マイナンバーカード読取")
    print()
    print("  📱 NFC読取中...")
    print()
    print("  スマートフォンの上部をマイナンバーカードにかざしてください")
    print()
    
    print("  読取進行中...")
    for i in range(101):
        status = ["接触待機中...", "データ読込中...", "署名検証中..."][i // 33]
        print_progress_bar(i, 100, f"  🔷 {status}", 30)
        time.sleep(0.02)
    
    print()
    print("  ✅ 読取完了")
    print()
    time.sleep(1)

def screen_age_success():
    """画面5a: 年齢確認成功"""
    clear_screen()
    print()
    print_centered("┌" + "─" * 58 + "┐", 70)
    print_centered("│", 70) + "  " + Colors.GREEN + "✅ 成功" + Colors.END
    print_centered("│", 70)
    print_centered("│" + "18歳以上であることを確認しました".center(58) + "│", 70)
    print_centered("│", 70)
    print_centered("│", 70)
    print_centered("│" + Colors.CYAN + "生年月日: 2005年3月15日".center(58) + Colors.END + "│", 70)
    print_centered("│" + "確認日時: 2024年1月1日".center(58) + "│", 70)
    print_centered("│", 70)
    print_centered("│" + "[📌 メイン画面へ]".center(58) + "│", 70)
    print_centered("└" + "─" * 58 + "┘", 70)
    print()
    input(">>> プレスして次へ")

def screen_main():
    """画面6: メイン画面"""
    clear_screen()
    print()
    print("  🎫 大人証明                                             ⚙️")
    print()
    print("  " + Colors.GREEN + "✅ 18歳以上確認済" + Colors.END)
    print("  ウォレット: 0x1234...5678")
    print("  確認日時: 2024/01/01")
    print()
    print("  ─" * 30)
    print()
    print("  📋 サービス利用履歴")
    print()
    print("  📭 まだサービス利用履歴がありません")
    print()
    print("  ─" * 30)
    print()
    print("  🧪 テスト機能")
    print()
    print("  [Netflix からリクエスト]")
    print("  [Amazon Prime からリクエスト]")
    print()
    input(">>> Netflix をクリック (プレスして次へ)")

def screen_verification_request():
    """画面7: 年齢確認リクエスト"""
    clear_screen()
    print()
    print("  年齢確認のリクエスト")
    print()
    print_centered("┌" + "─" * 50 + "┐")
    print_centered("│" + " " * 50 + "│")
    print_centered("│" + "Netflix からのリクエスト".center(50) + "│")
    print_centered("│" + " " * 50 + "│")
    print_centered("│" + "18歳以上であることを証明してもよろしいですか？".center(50) + "│")
    print_centered("│" + "個人情報は一切共有されません".center(50) + "│")
    print_centered("│" + " " * 50 + "│")
    print_centered("└" + "─" * 50 + "┘")
    print()
    print(f"  手数料: 0.001 ETH (約10円)")
    print()
    print("  [❌ キャンセル]  [✓ 許可する]")
    print()
    input(">>> 許可 をクリック (プレスして次へ)")

def screen_tx_processing():
    """画面8: トランザクション送信中"""
    clear_screen()
    print()
    print("  トランザクション送信中...")
    print()
    print("  ⛓️ ブロックチェーンに送信中...")
    print()
    
    statuses = ["🔐 ウォレットから署名...", "📤 トランザクション送信中...", "⏳ ブロック確認待機中..."]
    
    for i in range(101):
        status = statuses[min(i // 33, 2)]
        print_progress_bar(i, 100, f"  {status}", 30)
        time.sleep(0.02)
    
    print()
    print("  ✅ トランザクション送信完了！")
    print()
    print(f"  トランザクションハッシュ:")
    print(f"  0x1234567890abcdef1234567890abcdef12345678")
    print()
    time.sleep(1)

def screen_verification_complete():
    """画面9: 完了"""
    clear_screen()
    print()
    print_centered("┌" + "─" * 58 + "┐", 70)
    print_centered("│", 70) + "  " + Colors.GREEN + "✅ 完了" + Colors.END
    print_centered("│", 70)
    print_centered("│" + "年齢確認が完了しました".center(58) + "│", 70)
    print_centered("│", 70)
    print_centered("│" + Colors.CYAN + "Netflix が年齢確認を確認しています...".center(58) + Colors.END + "│", 70)
    print_centered("│", 70)
    print_centered("│" + "ウォレットアドレス:".center(58) + "│", 70)
    print_centered("│" + "0x1234567890abcdef12345678".center(58) + "│", 70)
    print_centered("│", 70)
    print_centered("│" + "[🔗 Netflix へ戻る]".center(58) + "│", 70)
    print_centered("└" + "─" * 58 + "┘", 70)
    print()
    time.sleep(2)

def screen_main_updated():
    """画面10: メイン画面（更新）"""
    clear_screen()
    print()
    print("  🎫 大人証明                                             ⚙️")
    print()
    print("  " + Colors.GREEN + "✅ 18歳以上確認済" + Colors.END)
    print("  ウォレット: 0x1234...5678")
    print()
    print("  ─" * 30)
    print()
    print("  📋 サービス利用履歴")
    print()
    print_centered("┌" + "─" * 40 + "┐", 60)
    print_centered("│ Netflix".center(40) + " │", 60)
    print_centered("│ 確認日時: 2024/01/01 12:34".center(40) + " │", 60)
    print_centered("│ " + Colors.GREEN + "✓ アクセス許可" + Colors.END.center(39) + " │", 60)
    print_centered("└" + "─" * 40 + "┘", 60)
    print()
    print("  🧪 テスト機能")
    print()
    print("  [Netflix からリクエスト]")
    print("  [Amazon Prime からリクエスト]")
    print()
    input(">>> プレスして完了")

def run_demo():
    """デモシーケンスを実行"""
    print(Colors.BOLD + Colors.BLUE)
    print("╔" + "═" * 58 + "╗")
    print("║" + "🎫 大人証明デモ - ターミナル版".center(58) + "║")
    print("║" + "Adult Verification - Terminal Demo".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print(Colors.END)
    print()
    print("このデモは大人証明アプリの完全なユーザーフローをシミュレートします。")
    print("各画面でプレスキーして次の画面に進んでください。")
    print()
    input(">>> プレスしてデモを開始...")
    
    screens = [
        ("スプラッシュスクリーン", screen_splash),
        ("ウォレット生成", screen_wallet),
        ("シードフレーズ", screen_seed_phrase),
        ("マイナンバーカード読取", screen_mynumber_scan),
        ("年齢確認成功", screen_age_success),
        ("メイン画面", screen_main),
        ("年齢確認リクエスト", screen_verification_request),
        ("トランザクション送信", screen_tx_processing),
        ("完了", screen_verification_complete),
        ("メイン画面（更新）", screen_main_updated),
    ]
    
    for i, (screen_name, screen_func) in enumerate(screens, 1):
        try:
            print(f"\n[{i}/{len(screens)}] {screen_name}を表示中...")
            screen_func()
        except KeyboardInterrupt:
            print("\n\nデモを中断しました。")
            return
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            return
    
    clear_screen()
    print()
    print_centered("╔" + "═" * 58 + "╗", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("║" + Colors.GREEN + "✅ デモ完了！" + Colors.END.center(52) + "║", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("║" + "大人証明の完全なフローを体験しました。".center(58) + "║", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("║" + "このデモはStreamlitで実装されています。".center(58) + "║", 70)
    print_centered("║" + "本番環境では以下を実装します：".center(58) + "║", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("║" + "✓ マイナンバーカード実読取".center(58) + "║", 70)
    print_centered("║" + "✓ ECDSA署名検証".center(58) + "║", 70)
    print_centered("║" + "✓ スマートコントラクト呼び出し".center(58) + "║", 70)
    print_centered("║" + "✓ Ethereumブロックチェーン連携".center(58) + "║", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("║" + Colors.BOLD + "🚀 Streamlit版デモの起動方法:" + Colors.END.center(58) + "║", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("║" + "1. pip install streamlit".center(58) + "║", 70)
    print_centered("║" + "2. streamlit run app.py".center(58) + "║", 70)
    print_centered("║" + " " * 58 + "║", 70)
    print_centered("╚" + "═" * 58 + "╝", 70)
    print()

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nデモを中断しました。")
        sys.exit(0)
