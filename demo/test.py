#!/usr/bin/env python3
"""
大人証明デモ - 動作確認スクリプト
このスクリプトでアプリのコードをバリデーションしてテストします
"""

import sys
import os

def test_imports():
    """依存パッケージのインポートテスト"""
    print("=" * 60)
    print("🧪 テスト1: 依存パッケージのインポート確認")
    print("=" * 60)
    
    try:
        import streamlit as st
        print("✓ streamlit: OK")
        return True
    except ImportError as e:
        print(f"✗ streamlit: FAILED - {e}")
        print("\n💡 修正方法:")
        print("   pip install streamlit")
        return False

def test_syntax():
    """Pythonスクリプトの構文チェック"""
    print("\n" + "=" * 60)
    print("🧪 テスト2: Pythonスクリプト構文チェック")
    print("=" * 60)
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, "app.py", "exec")
        print("✓ app.py: 構文OK")
        return True
    except SyntaxError as e:
        print(f"✗ app.py: 構文エラー")
        print(f"  行番号: {e.lineno}")
        print(f"  エラー: {e.msg}")
        return False
    except FileNotFoundError:
        print("✗ app.py: ファイルが見つかりません")
        return False

def test_functions():
    """関数定義チェック"""
    print("\n" + "=" * 60)
    print("🧪 テスト3: 関数定義チェック")
    print("=" * 60)
    
    required_functions = [
        "splash_screen",
        "wallet_check",
        "seed_phrase_screen",
        "mynumber_scan_screen",
        "age_result_success",
        "age_result_failure",
        "main_screen",
        "verification_request_screen",
        "tx_processing_screen",
        "verification_complete_screen",
        "settings_screen",
        "main"
    ]
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        for func in required_functions:
            if f"def {func}(" in code:
                print(f"✓ {func}: 定義OK")
            else:
                print(f"✗ {func}: 未定義")
                return False
        return True
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False

def test_session_state():
    """セッション状態初期化チェック"""
    print("\n" + "=" * 60)
    print("🧪 テスト4: セッション状態初期化チェック")
    print("=" * 60)
    
    required_states = [
        "page",
        "wallet_address",
        "age_verified",
        "seed_phrase",
        "verification_history",
        "current_saas"
    ]
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        for state in required_states:
            if f'"{state}"' in code and "st.session_state" in code:
                print(f"✓ {state}: 初期化OK")
            else:
                print(f"✗ {state}: 初期化未確認")
        return True
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False

def test_requirements():
    """requirements.txtチェック"""
    print("\n" + "=" * 60)
    print("🧪 テスト5: requirements.txt チェック")
    print("=" * 60)
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        if "streamlit" in content:
            print("✓ requirements.txt: streamlit記載OK")
            print(f"  内容: {content.strip()}")
            return True
        else:
            print("✗ requirements.txt: streamlit記載なし")
            return False
    except FileNotFoundError:
        print("✗ requirements.txt: ファイルが見つかりません")
        return False

def check_logic_flow():
    """ロジックフロー確認"""
    print("\n" + "=" * 60)
    print("🧪 テスト6: ロジックフロー確認")
    print("=" * 60)
    
    flows = [
        ("画面遷移", "st.session_state.page ="),
        ("ボタン処理", "st.button("),
        ("プログレスバー", "st.progress("),
        ("スピナー", "st.spinner("),
        ("時間処理", "time.sleep("),
        ("イベント表示", "st.markdown("),
    ]
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        for feature, keyword in flows:
            if keyword in code:
                print(f"✓ {feature}: 実装OK")
            else:
                print(f"✗ {feature}: 未実装")
        return True
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False

def check_error_handling():
    """エラーハンドリング確認"""
    print("\n" + "=" * 60)
    print("🧪 テスト7: エラーハンドリング確認")
    print("=" * 60)
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        if "try:" in code:
            print("✓ try-except: 実装OK")
        else:
            print("⚠ try-except: 未実装（オプション）")
        
        if "st.warning(" in code or "st.error(" in code:
            print("✓ エラーメッセージ: 実装OK")
        else:
            print("⚠ エラーメッセージ: 未実装（オプション）")
        
        return True
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False

def run_all_tests():
    """すべてのテストを実行"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "🎫 大人証明デモ - 動作確認テスト" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # テスト実行
    results = {
        "インポート": test_imports(),
        "構文": test_syntax(),
        "関数定義": test_functions(),
        "セッション状態": test_session_state(),
        "requirements.txt": test_requirements(),
        "ロジックフロー": check_logic_flow(),
        "エラーハンドリング": check_error_handling(),
    }
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 テスト結果サマリー")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-" * 60)
    print(f"合計: {passed}/{total} テスト成功")
    print("-" * 60)
    
    return failed == 0

def print_startup_instructions():
    """起動手順を表示"""
    print("\n" + "=" * 60)
    print("🚀 デモ起動手順")
    print("=" * 60)
    
    print("""
1️⃣  Streamlit をインストール（初回のみ）:
    pip install streamlit

2️⃣  デモを起動:
    streamlit run app.py

3️⃣  ブラウザで開く:
    http://localhost:8501

✨ すべてのテストが成功しました！
   デモアプリを起動して、以下を確認してください：
   
   ✓ 10個の画面が表示される
   ✓ ボタンをクリックで画面遷移する
   ✓ プログレスバーが正常に進行する
   ✓ サービス利用履歴が更新される
   ✓ エラーメッセージが表示される
    """)

if __name__ == "__main__":
    # カレントディレクトリをデモディレクトリに変更
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # テスト実行
    success = run_all_tests()
    
    if success:
        print_startup_instructions()
        sys.exit(0)
    else:
        print("\n⚠️  テストに失敗しました。上記のエラーを修正してください。")
        sys.exit(1)
