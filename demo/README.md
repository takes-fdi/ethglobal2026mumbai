# 大人証明（Adult Verification）- インタラクティブデモ

## 🚀 クイックスタート（30秒で開始）

### 1. 依存パッケージをインストール

```bash
cd ethglobal2026mumbai/demo
pip install -r requirements.txt
```

または、Streamlit のみ：
```bash
pip install streamlit==1.28.1
```

### 2. デモアプリを起動

```bash
streamlit run app.py
```

### 3. ブラウザで開く

自動的にブラウザが開きます。開かない場合は以下のURLにアクセス：

```
http://localhost:8501
```

---

## 🎮 デモの使い方

### 画面フロー

```
スプラッシュ 
   ↓
ウォレット生成 
   ↓
シードフレーズ表示 
   ↓
マイナンバーカード読取（シミュレーション） 
   ↓
年齢確認結果（成功） 
   ↓
メイン画面 
   ↓
SaaS企業からのリクエスト（Netflix/Amazon）
   ↓
年齢確認の承認・トランザクション送信
   ↓
完了
```

### 各画面での操作

#### 1️⃣ スプラッシュスクリーン
- 【🚀 始める】ボタンをクリック

#### 2️⃣ ウォレット確認画面
- 【✨ ウォレットを生成する】ボタンをクリック

#### 3️⃣ シードフレーズ画面
- 【✓ 確認しました】ボタンをクリック

#### 4️⃣ マイナンバーカード読取画面
- 自動でプログレスバーが進行します
- 読取完了後、年齢確認結果画面へ自動遷移

#### 5️⃣ 年齢確認成功画面
- 【📌 メイン画面へ】ボタンをクリック

#### 6️⃣ メイン画面
- **Netflix からリクエスト** または **Amazon Prime からリクエスト** ボタンをクリック
- サービス利用履歴が表示されます

#### 7️⃣ 年齢確認リクエスト画面
- 【✓ 許可する】ボタンをクリック

#### 8️⃣ トランザクション送信中
- 自動でプログレスバーが進行
- トランザクション完了後、完了画面へ自動遷移

#### 9️⃣ 年齢確認完了画面
- 【🔗 戻る】ボタンでメイン画面に戻る

---

## 🎯 デモで確認できる機能

✅ **画面遷移**
- 9個の主要画面を操作できます
- 戻るボタンで前の画面に戻れます

✅ **ステート管理**
- ウォレットアドレス（デモ用：0x1234...5678）
- ユーザー状態（18歳以上確認済）
- サービス利用履歴の表示・更新

✅ **プログレスバー・ローディング**
- マイナンバーカード読取
- トランザクション送信

✅ **フォーム入力・ボタン操作**
- 各画面でのユーザーインタラクション
- エラーハンドリング表示

✅ **データ永続化**
- セッション内でのデータ保持
- サービス利用履歴の追加

---

## 📱 デモ用ウォレット・データ

### ウォレット情報
```
ウォレットアドレス: 0x1234567890abcdef1234567890abcdef12345678
シードフレーズ: abandon ability able about above absent absorb abstract abuse access accident account
ネットワーク: Ethereum Sepolia (テストネット)
```

### ユーザー情報
```
生年月日: 2005年3月15日（18歳以上）
年齢確認状態: ✅ 確認済
確認日時: 2024年1月1日
```

### テスト用SaaS企業
- Netflix
- Amazon Prime Video

---

## ⚙️ トラブルシューティング

### Q: `streamlit: command not found`

**A:** Streamlit がインストールされていません。以下を実行：
```bash
pip install streamlit==1.28.1
```

### Q: ポート 8501 が既に使用されている

**A:** 以下で別のポートで起動：
```bash
streamlit run app.py --server.port 8502
```

### Q: ブラウザが自動で開かない

**A:** 手動で以下を開く：
```
http://localhost:8501
```

### Q: 画面が正しく表示されない

**A:** キャッシュをクリア：
```bash
streamlit cache clear
```

---

## 📊 デモの画面一覧

| # | 画面名 | 説明 |
|---|--------|------|
| 1 | スプラッシュスクリーン | アプリの開始画面 |
| 2 | ウォレット確認 | ウォレット生成の確認 |
| 3 | シードフレーズ | バックアップ用フレーズ表示 |
| 4 | マイナンバーカード読取 | NFC読取シミュレーション |
| 5 | 年齢確認成功 | 18歳以上確認結果 |
| 6 | メイン画面 | ホーム画面・サービス利用履歴 |
| 7 | 年齢確認リクエスト | SaaS企業からのリクエスト |
| 8 | トランザクション送信中 | NFT発行処理中 |
| 9 | 完了 | 年齢確認完了通知 |
| 10 | 設定 | ユーザー設定画面 |

---

## 🎨 UI/UX の特徴

✅ **モバイルファースト設計**
- レスポンシブレイアウト
- スマートフォン最適化

✅ **インタラクティブなアニメーション**
- プログレスバー
- 遷移アニメーション

✅ **分かりやすいビジュアル**
- 絵文字によるアイコン
- 色分けされたメッセージ

✅ **明確なユーザーフロー**
- 各ステップでの指示
- エラーメッセージ表示

---

## 🔧 カスタマイズ例

### 企業ロゴを追加

`app.py` の `splash_screen()` 関数を編集：

```python
st.image("logo.png", width=200)
st.markdown("# 🎫 大人証明")
```

### 手数料を変更

`main_screen()` 関数内の以下を編集：

```python
st.markdown("**手数料:** 0.0005 ETH (約5円)")  # 変更前: 0.001 ETH
```

### テスト用SaaS企業を追加

`main_screen()` 関数内に追加：

```python
if st.button("Disney+ からリクエスト", use_container_width=True, key="req_disney"):
    st.session_state.current_saas = "Disney+"
    st.session_state.page = "verification_request"
    st.rerun()
```

---

## 📝 デモ用データフロー（実装なし）

本デモではシミュレーションのみです。実装時に追加予定：

- [ ] マイナンバーカード実際の読取
- [ ] ECDSA署名検証
- [ ] スマートコントラクトへの実際の呼び出し
- [ ] Ethereum ブロックチェーンとの連携
- [ ] リアルトランザクション処理

---

## 🎬 デモの実行例

```bash
$ cd ethglobal2026mumbai/demo
$ streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

ブラウザが自動で開き、以下の画面が表示されます：

```
┌─────────────────────────────────┐
│                                 │
│        🎫 大人証明               │
│      Adult Verification         │
│                                 │
│    18歳以上であることを         │
│    安全に証明する               │
│                                 │
│                                 │
│       [    🚀 始める    ]        │
│                                 │
└─────────────────────────────────┘
```

---

## 🌐 デプロイ方法（オプション）

### Streamlit Cloud（無料）でデプロイ

1. GitHub にコードをプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud) にサインイン
3. "New app" を選択して GitHub リポジトリを指定
4. 自動デプロイ完了

---

## 📞 サポート

### ドキュメント参照

- 全体仕様: `../SPECIFICATION.md`
- API設計: `../API_DESIGN.md`
- UI設計: `../ui-mockups/UI_MOCKUP.md`

### Streamlit ドキュメント

- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Community](https://discuss.streamlit.io/)

---

## ✨ 次のステップ

デモの動作確認後：

1. **スマートコントラクトの実装** → `../contracts/AgeVerificationContract.sol` を参照
2. **バックエンド API の構築** → `../API_DESIGN.md` を参照
3. **本格的な iOS/Android アプリ開発** → `../ui-mockups/UI_MOCKUP.md` を参照

---

**Made with ❤️ for ETHGlobal 2026 Mumbai**
