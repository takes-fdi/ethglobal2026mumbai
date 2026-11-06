"""
大人証明 (Adult Verification) - インタラクティブデモ
Streamlit版

起動方法:
  streamlit run demo/app.py

または：
  cd ethglobal2026mumbai && streamlit run demo/app.py
"""

import streamlit as st
import time
from datetime import datetime
import hashlib
import os

# ページ設定
st.set_page_config(
    page_title="大人証明 - Adult Verification",
    page_icon="🎫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS スタイル
st.markdown("""
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-size: 16px;
        padding: 12px;
        font-weight: 600;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 16px;
        border-radius: 8px;
        margin: 20px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 16px;
        border-radius: 8px;
        margin: 20px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 16px;
        border-radius: 8px;
        margin: 20px 0;
    }
    .jp-text {
        font-weight: 500;
    }
    .en-text {
        font-size: 0.88em;
        color: #666;
        display: block;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態を初期化
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = "0x1234567890abcdef1234567890abcdef12345678"
if "age_verified" not in st.session_state:
    st.session_state.age_verified = None
if "verification_history" not in st.session_state:
    st.session_state.verification_history = []
if "current_saas" not in st.session_state:
    st.session_state.current_saas = None

# ===================================
# Page 1: Splash Screen
# ===================================
def splash_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🎫 大人証明")
        st.markdown("### Adult Verification")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<span class="jp-text">18歳以上であることを安全に証明する</span>'
            '<span class="en-text">Safely prove you are 18 or older</span>',
            unsafe_allow_html=True
        )
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        if st.button("🚀 始める / Get Started", key="splash_start", use_container_width=True):
            st.session_state.page = "wallet_check"
            st.rerun()

# ===================================
# Page 2: Wallet Check
# ===================================
def wallet_check():
    st.markdown("# ウォレット確認")
    st.markdown(
        '<span class="en-text">Wallet Setup</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← 戻る / Back", key="back_wallet"):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("---")
    st.markdown(
        '<span class="jp-text">初回利用時にウォレットを作成します</span>'
        '<span class="en-text">Wallet will be created on first use</span>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<span class="jp-text">秘密鍵はスマートフォン内に安全に保管されます。</span>'
        '<span class="en-text">Private keys are securely stored within your smartphone.</span>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✨ ウォレットを生成する", use_container_width=True, key="create_wallet"):
        with st.spinner("⏳ Generating wallet..."):
            time.sleep(1.5)
            st.session_state.page = "mynumber_scan"
            st.rerun()

# ===================================
# Page 3: My Number Card Scan
# ===================================
def mynumber_scan_screen():
    st.markdown("# マイナンバーカード読取")
    st.markdown(
        '<span class="en-text">My Number Card Scan</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← 戻る / Back", key="back_mynumber"):
            st.session_state.page = "wallet_check"
            st.rerun()

    st.markdown("---")
    st.markdown(
        '<span class="jp-text">📱 NFC読取中...</span>'
        '<span class="en-text">📱 Reading via NFC...</span>',
        unsafe_allow_html=True
    )
    st.markdown("")
    st.markdown(
        '<span class="jp-text">スマートフォンの上部をマイナンバーカードにかざしてください</span>'
        '<span class="en-text">Hold your smartphone top to the My Number Card</span>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(101):
        progress_bar.progress(i)
        if i < 30:
            status_text.markdown(
                '<span class="jp-text">🔷 接触待機中...</span>'
                '<span class="en-text">🔷 Awaiting contact...</span>',
                unsafe_allow_html=True
            )
        elif i < 60:
            status_text.markdown(
                '<span class="jp-text">🔷 データ読込中...</span>'
                '<span class="en-text">🔷 Reading data...</span>',
                unsafe_allow_html=True
            )
        else:
            status_text.markdown(
                '<span class="jp-text">🔷 署名検証中...</span>'
                '<span class="en-text">🔷 Verifying signature...</span>',
                unsafe_allow_html=True
            )
        time.sleep(0.03)

    # Scan complete
    status_text.markdown(
        '<span class="jp-text">✅ 読取完了</span>'
        '<span class="en-text">✅ Scan complete</span>',
        unsafe_allow_html=True
    )
    time.sleep(0.5)

    # Set verified (first time always succeeds)
    st.session_state.age_verified = True
    st.session_state.page = "age_result"
    st.rerun()

# ===================================
# Page 4a: Age Verification Success
# ===================================
def age_result_success():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# ✅ 成功")
        st.markdown(
            '<span class="en-text">Success</span>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<span class="jp-text">18歳以上であることを確認しました</span>'
            '<span class="en-text">Verified you are 18 or older</span>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="info-box">
        <strong>
            <span class="jp-text">生年月日:</span>
            <span class="en-text">Date of Birth:</span>
        </strong> 2005年3月15日<br>
        <strong>
            <span class="jp-text">確認日時:</span>
            <span class="en-text">Verification Date:</span>
        </strong> 2024年1月1日<br>
        <strong>
            <span class="jp-text">ウォレット:</span>
            <span class="en-text">Wallet:</span>
        </strong> 0x1234...5678
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button("📌 メイン画面へ / Main Screen", use_container_width=True, key="to_main"):
            st.session_state.page = "main"
            st.rerun()

# ===================================
# Page 4b: Age Verification Failure
# ===================================
def age_result_failure():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# ❌ 失敗")
        st.markdown(
            '<span class="en-text">Failure</span>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<span class="jp-text">申し訳ありません</span>'
            '<span class="en-text">We apologize</span>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<span class="jp-text">18歳以上の確認ができません</span>'
            '<span class="en-text">Cannot verify you are 18 or older</span>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="error-box">
        <span class="jp-text">このアプリケーションは18歳以上のユーザーのみが使用できます</span>
        <span class="en-text">This application is for users 18 and older only</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.button("メイン画面へ / Main Screen", use_container_width=True)
        with col2:
            st.button("再度試す / Try Again", use_container_width=True)

# ===================================
# Page 5: Main Screen
# ===================================
def main_screen():
    st.markdown("# 大人証明")
    st.markdown(
        '<span class="en-text">Adult Verification</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("⚙️ 設定 / Settings", key="settings_btn"):
            st.session_state.page = "settings"
            st.rerun()

    st.markdown("---")

    # Status
    st.markdown("### 📊 状態 / Status")
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.markdown("✅ **18歳以上確認済 / 18+ Verified**")
    with status_col2:
        st.markdown("**ウォレット / Wallet:** `0x1234...5678`")

    status_col3, status_col4 = st.columns(2)
    with status_col3:
        st.markdown("**確認日時 / Date:** 2024/01/01")
    with status_col4:
        st.markdown(f"**トランザクション数 / TXs:** {len(st.session_state.verification_history)}")

    st.markdown("---")

    # Service usage history
    st.markdown("### 📋 サービス利用履歴 / Service History")

    if len(st.session_state.verification_history) == 0:
        st.info("📭 まだサービス利用履歴がありません / No history yet")
    else:
        for service in st.session_state.verification_history:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**{service['name']}**")
            with col2:
                st.markdown(f"日時 / Date: {service['date']}")
            with col3:
                st.markdown(f"✓ {service['status']}")

    st.markdown("---")

    # Test buttons
    st.markdown("### 🧪 テスト機能 / Test Functions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Netflix からリクエスト / Netflix Request",
            use_container_width=True,
            key="req_netflix"
        ):
            st.session_state.current_saas = "Netflix"
            st.session_state.page = "verification_request"
            st.rerun()
    with col2:
        if st.button(
            "Amazon Prime からリクエスト / Amazon Prime Request",
            use_container_width=True,
            key="req_amazon"
        ):
            st.session_state.current_saas = "Amazon Prime Video"
            st.session_state.page = "verification_request"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Go home button
    if st.button("🏠 トップに戻る / Return to Top", use_container_width=True, key="go_home"):
        st.session_state.page = "splash"
        st.session_state.current_saas = None
        st.rerun()

# ===================================
# Page 6: Verification Request
# ===================================
def verification_request_screen():
    st.markdown("# 年齢確認のリクエスト")
    st.markdown(
        '<span class="en-text">Age Verification Request</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← キャンセル / Cancel", key="cancel_req"):
            st.session_state.page = "main"
            st.session_state.current_saas = None
            st.rerun()

    st.markdown("---")

    saas_name = st.session_state.current_saas

    st.markdown(f"""
    <div class="info-box">
    <strong>
        <span class="jp-text">{saas_name} からのリクエスト</span>
        <span class="en-text">Request from {saas_name}</span>
    </strong><br><br>
    <span class="jp-text">18歳以上であることを証明してもよろしいですか？</span>
    <span class="en-text">Do you agree to prove you are 18 or older?</span><br>
    <span class="jp-text">個人情報は一切共有されません</span>
    <span class="en-text">No personal information will be shared</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**手数料 / Fee:** 0.001 ETH (約10円 / approx. $0.07)")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "❌ キャンセル / Cancel",
            use_container_width=True,
            key="cancel_verification"
        ):
            st.session_state.page = "main"
            st.session_state.current_saas = None
            st.rerun()
    with col2:
        if st.button(
            "✓ 許可する / Approve",
            use_container_width=True,
            key="approve_verification"
        ):
            st.session_state.page = "tx_processing"
            st.rerun()

# ===================================
# Page 7: Transaction Processing
# ===================================
def tx_processing_screen():
    st.markdown("# トランザクション送信中...")
    st.markdown(
        '<span class="en-text">Sending Transaction...</span>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<span class="jp-text">⛓️ ブロックチェーンに送信中...</span>'
            '<span class="en-text">⛓️ Sending to blockchain...</span>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(101):
            progress_bar.progress(i)
            if i < 33:
                status_text.markdown(
                    '<span class="jp-text">🔐 ウォレットから署名...</span>'
                    '<span class="en-text">🔐 Signing from wallet...</span>',
                    unsafe_allow_html=True
                )
            elif i < 66:
                status_text.markdown(
                    '<span class="jp-text">📤 トランザクション送信中...</span>'
                    '<span class="en-text">📤 Sending transaction...</span>',
                    unsafe_allow_html=True
                )
            else:
                status_text.markdown(
                    '<span class="jp-text">⏳ ブロック確認待機中...</span>'
                    '<span class="en-text">⏳ Waiting for block confirmation...</span>',
                    unsafe_allow_html=True
                )
            time.sleep(0.05)

        # Transaction complete
        tx_hash = "0x" + hashlib.sha256(
            f"{st.session_state.current_saas}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:40]

        st.success("✅ トランザクション送信完了！ / Transaction sent!")
        st.markdown(f"""
        <div class="info-box">
        <strong>
            <span class="jp-text">トランザクションハッシュ:</span>
            <span class="en-text">Transaction Hash:</span>
        </strong><br>
        <code>{tx_hash}</code>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1.5)
        st.session_state.page = "verification_complete"
        st.rerun()

# ===================================
# Page 8: Verification Complete
# ===================================
def verification_complete_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# ✅ 完了")
        st.markdown(
            '<span class="en-text">Complete</span>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<span class="jp-text">年齢確認が完了しました</span>'
            '<span class="en-text">Age verification completed</span>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="success-box">
        <strong>
            <span class="jp-text">{st.session_state.current_saas} が年齢確認を確認しています...</span>
            <span class="en-text">{st.session_state.current_saas} is verifying your age...</span>
        </strong><br><br>
        <strong>
            <span class="jp-text">ウォレットアドレス:</span>
            <span class="en-text">Wallet Address:</span>
        </strong><br>
        <code>0x1234567890abcdef1234567890abcdef12345678</code>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

        # Add to history
        st.session_state.verification_history.append({
            "name": st.session_state.current_saas,
            "date": datetime.now().strftime("%Y/%m/%d %H:%M"),
            "status": "アクセス許可"
        })

        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button(
            f"🔗 {st.session_state.current_saas} へ戻る / Return to {st.session_state.current_saas}",
            use_container_width=True,
            key="return_to_saas"
        ):
            st.session_state.page = "main"
            st.session_state.current_saas = None
            st.rerun()

# ===================================
# Page 9: Settings
# ===================================
def settings_screen():
    st.markdown("# ⚙️ 設定")
    st.markdown(
        '<span class="en-text">Settings</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← メイン画面 / Main Screen", key="back_to_main_settings"):
            st.session_state.page = "main"
            st.rerun()

    st.markdown("---")

    st.markdown(
        '<span class="jp-text">📱 デバイス情報</span>'
        '<span class="en-text">Device Information</span>',
        unsafe_allow_html=True
    )
    st.markdown("**ウォレットアドレス / Wallet:** `0x1234567890abcdef1234567890abcdef12345678`")
    st.markdown("**Ethereum ネットワーク / Network:** Sepolia (テストネット / Testnet)")

    st.markdown("---")

    st.markdown(
        '<span class="jp-text">🔐 セキュリティ</span>'
        '<span class="en-text">Security</span>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<span class="jp-text">秘密鍵はアプリ内で安全に管理されています</span>'
        '<span class="en-text">Private keys are securely managed within the app</span>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<span class="jp-text">ℹ️ その他</span>'
        '<span class="en-text">Other</span>',
        unsafe_allow_html=True
    )
    st.markdown(
        "[📄 ](https://example.com)"
        "[📜 ](https://github.com)",
        unsafe_allow_html=True
    )
    st.markdown("**バージョン:** v1.0.0 (Demo)")
    st.markdown(
        '<span class="en-text">Version: v1.0.0 (Demo)</span>',
        unsafe_allow_html=True
    )

# ===================================
# Main Logic
# ===================================
def main():
    page = st.session_state.page

    if page == "splash":
        splash_screen()
    elif page == "wallet_check":
        wallet_check()
    elif page == "mynumber_scan":
        mynumber_scan_screen()
    elif page == "age_result":
        if st.session_state.age_verified:
            age_result_success()
        else:
            age_result_failure()
    elif page == "main":
        main_screen()
    elif page == "verification_request":
        verification_request_screen()
    elif page == "tx_processing":
        tx_processing_screen()
    elif page == "verification_complete":
        verification_complete_screen()
    elif page == "settings":
        settings_screen()

if __name__ == "__main__":
    main()
