"""
大人証明 (Adult Verification) - インタラクティブデモ
Streamlit版 - 実契約連携版

起動方法:
  streamlit run demo/app.py
"""

import streamlit as st
import time
import hashlib
import json
import webbrowser
from datetime import datetime
from web3 import Web3
from eth_account import Account
import os

# ===================================
# ファイルパス
# ===================================
WALLET_FILE = os.path.join(os.path.dirname(__file__), ".wallet")

def save_wallet(address, private_key):
    """ウォレットを安全なファイルに保存"""
    with open(WALLET_FILE, "w") as f:
        f.write(f"address={address}\n")
        f.write(f"private_key={private_key}\n")
    os.chmod(WALLET_FILE, 0o600)  # 読み取り専用（自分だけ）

def load_wallet():
    """保存されたウォレットを読み込み"""
    if not os.path.exists(WALLET_FILE):
        return None, None
    try:
        with open(WALLET_FILE, "r") as f:
            address = None
            private_key = None
            for line in f:
                if line.startswith("address="):
                    address = line.split("=", 1)[1].strip()
                elif line.startswith("private_key="):
                    private_key = line.split("=", 1)[1].strip()
            if address and private_key:
                return address, private_key
    except Exception:
        pass
    return None, None

def delete_wallet():
    """保存されたウォレットを削除"""
    if os.path.exists(WALLET_FILE):
        os.remove(WALLET_FILE)

# ===================================
# 契約情報（Sepolia）
# ===================================
CONTRACT_ADDRESS = "0xFaD9fCA2D707142A3dD6B3F3e35A1765765a6005"
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

ABI = [
    {
        "inputs": [{"internalType": "bytes", "name": "initialPublicKey", "type": "bytes"}],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"indexed": False, "internalType": "bytes32", "name": "transactionHash", "type": "bytes32"}
        ],
        "name": "AgeVerificationIssued",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "admin",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddress", "type": "address"}],
        "name": "ageVerifiedNFT",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getGovernmentPublicKey",
        "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "issueAgeVerificationNFT",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalFeeCollected",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddress", "type": "address"}],
        "name": "getUserVerificationStatus",
        "outputs": [
            {"internalType": "bool", "name": "isVerified", "type": "bool"},
            {"internalType": "uint256", "name": "verificationTime", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "newFee", "type": "uint256"}],
        "name": "setVerificationFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "verificationFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddress", "type": "address"}],
        "name": "verifyAgeVerification",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddress", "type": "address"}],
        "name": "revokeAgeVerification",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

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
    .network-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        background-color: #e8f5e9;
        color: #2e7d32;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態を初期化
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "wallet_address" not in st.session_state:
    # ファイルからウォレットを読み込み
    loaded_addr, loaded_key = load_wallet()
    if loaded_addr:
        st.session_state.wallet_address = loaded_addr
        st.session_state.private_key = loaded_key
    else:
        st.session_state.wallet_address = None
        st.session_state.private_key = None
if "age_verified" not in st.session_state:
    st.session_state.age_verified = None
if "verification_history" not in st.session_state:
    st.session_state.verification_history = []
if "current_saas" not in st.session_state:
    st.session_state.current_saas = None
if "contract_connected" not in st.session_state:
    st.session_state.contract_connected = False

# Web3接続関数
def get_contract():
    """契約に接続"""
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            return None, None
        contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)
        return w3, contract
    except Exception as e:
        return None, None

# ===================================
# Page 1: Splash Screen
# ===================================
def splash_screen():
    w3, contract = get_contract()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if w3 and contract:
            try:
                chain_id = w3.eth.chain_id
                fee = contract.functions.verificationFee().call()
                fee_eth = w3.from_wei(fee, 'ether')
                admin = contract.functions.admin().call()
                
                st.markdown('<div class="network-badge">✅ Connected to Sepolia (Chain ID: ' + str(chain_id) + ')</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="info-box">
                <strong>📡 Contract Status</strong><br>
                <strong>Address:</strong> `" + CONTRACT_ADDRESS + "`<br>
                <strong>Fee:</strong> " + str(fee_eth) + " ETH<br>
                <strong>Admin:</strong> `" + admin[:10] + "..." + admin[-8:] + "`<br>
                <strong>Network:</strong> Ethereum Sepolia Testnet
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown('<div class="network-badge" style="background-color: #fff3e0; color: #e65100;">⚠️ Sepolia (Error: ' + str(e)[:30] + ')</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="network-badge" style="background-color: #fff3e0; color: #e65100;">⚠️ Sepolia (Offline)</div>', unsafe_allow_html=True)
        
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
    w3, contract = get_contract()
    
    st.markdown("# ウォレット確認")
    st.markdown(
        '<span class="en-text">Wallet Setup</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🏠 ホーム / Home", key="home_wallet"):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("---")
    
    # 既存ウォレットがある場合
    if st.session_state.wallet_address:
        st.markdown(
            '<span class="jp-text">✅ ウォレットが保存されています</span>'
            '<span class="en-text">✅ Wallet already saved</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="jp-text">初回利用時にウォレットを作成します</span>'
            '<span class="en-text">Wallet will be created on first use</span>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<span class="jp-text">秘密鍵はアプリ内で安全に保管されます。</span>'
            '<span class="en-text">Private keys are securely stored within the app.</span>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # コントラクト接続状態表示
    if w3 and contract:
        try:
            chain_id = w3.eth.chain_id
            fee = contract.functions.verificationFee().call()
            fee_eth = w3.from_wei(fee, 'ether')
            
            st.success(f"✅ Contract Connected | Chain: {chain_id} | Fee: {fee_eth} ETH")
            st.caption(f"Contract: `{CONTRACT_ADDRESS}`")
        except Exception as e:
            st.error(f"Contract connection error: {e}")
    else:
        st.warning("⚠️ Contract not connected")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 既存のウォレットがある場合
    if st.session_state.wallet_address:
        st.markdown("### 🎉 ウォレット生成完了")
        st.markdown(
            '<span class="en-text">Wallet Generated Successfully!</span>',
            unsafe_allow_html=True
        )
        st.code(st.session_state.wallet_address, language=None)
        st.caption(
            '<span class="jp-text">このアドレスがあなたのウォレットアドレスです</span>'
            '<span class="en-text">This is your wallet address</span>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✅ ウォレットは既に存在します / Wallet already exists")
        
        # ウォレット既に存在する場合、wallet_ready画面に進む
        if st.button("➡️ 下一步に進む / Continue", use_container_width=True, key="continue_after_wallet"):
            st.session_state.page = "wallet_ready"
            st.rerun()
    else:
        # ウォレット生成ボタン
        if st.button("✨ ウォレットを生成する", use_container_width=True, key="create_wallet"):
            with st.spinner("⏳ Generating wallet..."):
                time.sleep(1.5)
                try:
                    # 実際のウォレットを生成
                    account = Account.create()
                    st.session_state.wallet_address = account.address
                    st.session_state.private_key = account.key.hex()
                    st.session_state.wallet_created = True
                    # ファイルに保存
                    save_wallet(account.address, account.key.hex())
                    st.success("✅ Wallet generated and saved!")
                except Exception as e:
                    st.error(f"Failed to generate wallet: {e}")
                    st.stop()
            # ウォレット生成後、確実にページ遷移
            st.session_state.page = "wallet_ready"
            st.session_state.wallet_just_created = True
            st.rerun()

# ===================================
# Page 2b: Wallet Ready - Charge ETH
# ===================================
def wallet_ready_screen():
    w3, contract = get_contract()
    
    st.markdown("# ウォレット準備完了")
    st.markdown(
        '<span class="en-text">Wallet Ready</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🏠 ホーム / Home", key="home_wallet_ready"):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("---")

    # Step 1: Copy Wallet Address
    st.markdown("### 📋 ステップ1: アドレスをコピー")
    st.markdown(
        '<span class="jp-text">以下のアドレスをクリックしてコピーしてください</span>'
        '<span class="en-text">Click the address below to copy</span>',
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.code(st.session_state.wallet_address, language=None)
    with col2:
        if st.button("📋 コピー / Copy", key="copy_address", type="primary"):
            st.session_state.address_copied = True
            st.rerun()
    
    if st.session_state.get('address_copied'):
        st.success("✅ コピーしました！ / Address copied!")
        st.session_state.address_copied = False

    st.markdown("---")
    
    # Step 2: Get Test ETH
    st.markdown("### 💰 ステップ2: テストETHを入手")
    
    st.markdown(
        '<div class="info-box">' +
        '<span class="jp-text">年齢確認には0.001 ETHが必要です</span>' +
        '<span class="en-text">Age verification requires 0.001 ETH</span>' +
        '</div>',
        unsafe_allow_html=True
    )
    
    # Faucet link (always visible)
    st.markdown(
        '<a href="https://sepoliafaucet.com/" target="_blank">'
        '🚰 テストETHを入手 / Get Test ETH (sepoliafaucet.com)</a>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<div class="info-box">' +
        "<strong>手順 / Steps:</strong><br>" +
        "1. 上のリンクでファウセットを開く<br>" +
        "2. このアドレスを貼り付ける<br>" +
        "3. 「Claim」をクリック<br>" +
        "4. 5〜10分でETHが入ります" +
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Step 3: Verify Balance
    st.markdown("### 🔍 ステップ3: バランス確認")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰 バランスを確認 / Check Balance", key="check_balance"):
            if w3 and contract:
                try:
                    balance = w3.eth.get_balance(st.session_state.wallet_address)
                    balance_eth = w3.from_wei(balance, 'ether')
                    st.session_state.eth_balance = float(balance_eth)
                    st.session_state.balance_checked = True
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Contract not connected")
    
    with col2:
        if st.button("✅ チャージ完了 / I've Charged ETH", key="charge_complete"):
            st.session_state.page = "mynumber_scan"
            st.rerun()
    
    # Show balance if checked
    if st.session_state.get('balance_checked'):
        if st.session_state.eth_balance > 0:
            st.success(f"✅ **Balance: {st.session_state.eth_balance} ETH**")
        else:
            st.warning("⚠️ Balance: 0 ETH — Still waiting for faucet")
    
    st.markdown("---")

    # Continue button
    if st.button(
        "➡️ 次に進む / Continue to Verification",
        use_container_width=True,
        key="continue_to_scan",
        type="primary"
    ):
        st.session_state.page = "mynumber_scan"
        st.rerun()
def mynumber_scan_screen():
    w3, contract = get_contract()
    
    st.markdown("# マイナンバーカード読取")
    st.markdown(
        '<span class="en-text">My Number Card Scan</span>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🏠 ホーム / Home", key="home_mynumber"):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("---")
    
    st.markdown(
        '<span class="jp-text">📱 スマートフォンの上部をマイナンバーカードにかざして、下のボタンをクリック</span>'
        '<span class="en-text">Hold your smartphone top to the My Number Card, then click the button below</span>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Two buttons side by side
    col_scan1, col_scan2 = st.columns(2)
    
    with col_scan1:
        # Real scan button (for NFC hardware)
        st.button(
            "📲 NFCスキャン開始\n(ハードウェア必要)",
            use_container_width=True,
            type="primary",
            key="start_mynumber_scan",
            disabled=True
        )
        st.caption("💡 デモ版では下のエミュレートボタンを使用してください")
    
    with col_scan2:
        # Emulate scan button (for demo)
        if st.button(
            "🖥️ エミュレートスキャン\nEmulate Scan",
            use_container_width=True,
            type="primary",
            key="emulate_mynumber_scan"
        ):
            # Simulated birth date (1990-01-01 = 36 years old)
            simulated_birthdate = "1990-01-01"
            simulated_name = "Test User"
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            st.markdown("---")
            st.success(f"✅ **エミュレート開始 / Emulate Start**")
            st.caption(f"📅 生年月日: {simulated_birthdate} | 📝 氏名: {simulated_name}")
            st.markdown("")

            for i in range(101):
                progress_bar.progress(i)
                if i < 30:
                    status_text.markdown(
                        '<span class="jp-text">🔷 カード情報読取中...</span>'
                        '<span class="en-text">🔷 Reading card data...</span>',
                        unsafe_allow_html=True
                    )
                elif i < 60:
                    status_text.markdown(
                        '<span class="jp-text">🔷 生年月日検証中...</span>'
                        '<span class="en-text">🔷 Verifying birth date...</span>',
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
                '<span class="jp-text">✅ エミュレーション読取完了</span>'
                '<span class="en-text">✅ Emulation complete</span>',
                unsafe_allow_html=True
            )
            st.success(f"✅ **生年月日: {simulated_birthdate} (36歳) / Age: 36 years old**")
            time.sleep(0.5)

            # Set verified (first time always succeeds)
            st.session_state.age_verified = True
            st.session_state.simulated_birthdate = simulated_birthdate
            st.session_state.page = "age_result"
            st.rerun()

# ===================================
# Page 4a: Age Verification Success
# ===================================
def age_result_success():
    w3, contract = get_contract()
    
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

        # Simulated birth date from emulation
        birthdate = st.session_state.get('simulated_birthdate', '1990-01-01')
        
        if w3 and contract:
            try:
                # 契約から情報を取得
                fee = contract.functions.verificationFee().call()
                fee_eth = w3.from_wei(fee, 'ether')
                admin = contract.functions.admin().call()
                
                # Calculate age from birthdate
                from datetime import datetime
                birth_dt = datetime.strptime(birthdate, "%Y-%m-%d")
                age = (datetime.now() - birth_dt).days // 365
                
                st.markdown(f"""
                <div class="info-box">
                <strong>
                    <span class="jp-text">生年月日:</span>
                    <span class="en-text">Date of Birth:</span>
                </strong> {birthdate} ({age}歳)<br>
                <strong>
                    <span class="jp-text">確認日時:</span>
                    <span class="en-text">Verification Date:</span>
                </strong> {datetime.now().strftime("%Y/%m/%d %H:%M")}<br>
                <strong>
                    <span class="jp-text">ウォレット:</span>
                    <span class="en-text">Wallet:</span>
                </strong> {st.session_state.wallet_address}<br>
                <strong>
                    <span class="jp-text">手数料:</span>
                    <span class="en-text">Fee:</span>
                </strong> {fee_eth} ETH<br>
                <strong>
                    <span class="jp-text">契約アドレス:</span>
                    <span class="en-text">Contract:</span>
                </strong> {CONTRACT_ADDRESS}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Contract error: {str(e)}")
        else:
            st.markdown(f"""
            <div class="info-box">
            <strong>
                <span class="jp-text">ウォレット:</span>
                <span class="en-text">Wallet:</span>
            </strong> {st.session_state.wallet_address}
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
    w3, contract = get_contract()
    
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

    # Contract connection status
    if w3 and contract:
        try:
            chain_id = w3.eth.chain_id
            fee = contract.functions.verificationFee().call()
            fee_eth = w3.from_wei(fee, 'ether')
            st.success(f"✅ Connected to Sepolia (Chain {chain_id}) | Fee: {fee_eth} ETH")
        except Exception as e:
            st.error(f"Contract read error: {e}")
    else:
        st.warning("⚠️ Not connected to contract")

    st.markdown("---")

    # Status
    st.markdown("### 📊 状態 / Status")
    
    wallet_addr = st.session_state.wallet_address or "Not created"
    
    if w3 and contract and st.session_state.wallet_address:
        try:
            # 契約から実際の状態を取得
            is_verified, verify_time = contract.functions.getUserVerificationStatus(
                Web3.to_checksum_address(st.session_state.wallet_address)
            ).call()
            
            if is_verified and verify_time > 0:
                verify_date = datetime.fromtimestamp(verify_time).strftime("%Y/%m/%d %H:%M")
                st.markdown("✅ **18歳以上確認済 / 18+ Verified**")
                st.markdown(f"**確認日時 / Date:** {verify_date}")
            else:
                st.markdown("⏳ **確認待ち / Pending** (Contract: Not yet verified)")
                st.markdown("**確認日時 / Date:** -")
        except Exception as e:
            st.error(f"Contract error: {e}")
            st.markdown("⚠️ Could not read from contract")
    else:
        st.info("📝 Generate a wallet first / ウォレットを生成してください")

    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.markdown("**ウォレット / Wallet:**")
        st.code(st.session_state.wallet_address, language=None)
    
    with status_col2:
        st.markdown("**トランザクション数 / TXs:**")
        st.metric("", len(st.session_state.verification_history))

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
    w3, contract = get_contract()
    
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
    
    if w3 and contract:
        try:
            fee = contract.functions.verificationFee().call()
            fee_eth = w3.from_wei(fee, 'ether')
            st.markdown(f"**手数料 / Fee:** {fee_eth} ETH (約10円 / approx. $0.07)")
        except:
            st.markdown("**手数料 / Fee:** 0.001 ETH (約10円 / approx. $0.07)")
    else:
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
    w3, contract = get_contract()
    tx_hash = None
    
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

        # Send actual transaction or generate mock
        if w3 and contract:
            try:
                # 実際のトランザクションを送信（デモ用：仮の秘密鍵を使用）
                # 本番ではユーザーのウォレットから送信
                fee = contract.functions.verificationFee().call()
                
                tx = contract.functions.issueAgeVerificationNFT().build_transaction({
                    'from': st.session_state.wallet_address,
                    'value': fee,
                    'gas': 200000,
                    'gasPrice': w3.eth.gas_price,
                    'nonce': w3.eth.get_transaction_count(st.session_state.wallet_address),
                    'chainId': w3.eth.chain_id,
                })
                
                # デモ用：秘密鍵なしなので署名スキップ
                tx_hash = "0x" + hashlib.sha256(
                    f"{st.session_state.current_saas}_{datetime.now().isoformat()}".encode()
                ).hexdigest()[:64]
                
                st.info("📝 デモモード: 実際のトランザクション送信にはウォレット接続が必要です")
            except Exception as e:
                st.error(f"Transaction error: {str(e)}")
                tx_hash = "0x" + hashlib.sha256(
                    f"{st.session_state.current_saas}_{datetime.now().isoformat()}".encode()
                ).hexdigest()[:64]
        else:
            tx_hash = "0x" + hashlib.sha256(
                f"{st.session_state.current_saas}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:64]

        st.success("✅ トランザクション送信完了！ / Transaction sent!")
        st.markdown(f"""
        <div class="info-box">
        <strong>
            <span class="jp-text">トランザクションハッシュ:</span>
            <span class="en-text">Transaction Hash:</span>
        </strong><br>
        <code>{tx_hash}</code><br>
        <br>
        <span class="en-text">🔗 <a href="https://sepolia.etherscan.io/tx/{tx_hash}" target="_blank">View on Etherscan</a></span>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1.5)
        st.session_state.page = "verification_complete"
        st.rerun()

# ===================================
# Page 8: Verification Complete
# ===================================
def verification_complete_screen():
    w3, contract = get_contract()
    
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

        if w3 and contract:
            try:
                is_verified, verify_time = contract.functions.getUserVerificationStatus(
                    Web3.to_checksum_address(st.session_state.wallet_address)
                ).call()
                
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
                <code>{st.session_state.wallet_address}</code><br>
                <br>
                <strong>
                    <span class="jp-text">状態:</span>
                    <span class="en-text">Status:</span>
                </strong> {'✅ ' if is_verified else '❌ '}{'確認済み / Verified' if is_verified else '未確認 / Not Verified'}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Contract error: {str(e)}")
        else:
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
            <code>{st.session_state.wallet_address}</code>
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
    w3, contract = get_contract()
    
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
    st.markdown("**ウォレットアドレス / Wallet:**")
    st.code(st.session_state.wallet_address, language=None)
    st.markdown("**Ethereum ネットワーク / Network:** Sepolia (テストネット / Testnet)")
    
    if w3 and contract:
        try:
            chain_id = w3.eth.chain_id
            fee = contract.functions.verificationFee().call()
            fee_eth = w3.from_wei(fee, 'ether')
            admin = contract.functions.admin().call()
            
            st.markdown(f"**Chain ID:** {chain_id}")
            st.markdown(f"**手数料 / Fee:** {fee_eth} ETH")
            st.markdown(f"**管理者 / Admin:** {admin}")
            st.markdown(f"**契約アドレス / Contract:** {CONTRACT_ADDRESS}")
        except Exception as e:
            st.warning(f"Contract read error: {str(e)}")
    else:
        st.warning("⚠️ Contract not connected")

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
        '<span class="jp-text">🗑️ dangerゾーン</span>'
        '<span class="en-text">danger Zone</span>',
        unsafe_allow_html=True
    )
    if st.session_state.wallet_address:
        if st.button(
            "🗑️ ウォレットを削除 / Delete Wallet",
            use_container_width=True,
            type="primary"
        ):
            delete_wallet()
            st.session_state.wallet_address = None
            st.session_state.private_key = None
            st.warning("✅ ウォレットを削除しました。アプリを再読み込みしてください。")
            st.rerun()

    st.markdown("---")

    st.markdown(
        '<span class="jp-text">ℹ️ その他</span>'
        '<span class="en-text">Other</span>',
        unsafe_allow_html=True
    )
    st.markdown(
        "[📄 プライバシーポリシー / Privacy Policy](https://example.com)"
        "[📜 ライセンス / License](https://github.com)",
        unsafe_allow_html=True
    )
    st.markdown("**バージョン / Version:** v1.0.0 (Demo)")

# ===================================
# Main Logic
# ===================================
def main():
    page = st.session_state.page

    if page == "splash":
        splash_screen()
    elif page == "wallet_check":
        wallet_check()
    elif page == "wallet_ready":
        wallet_ready_screen()
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
