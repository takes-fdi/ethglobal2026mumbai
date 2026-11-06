# 大人証明（Adult Verification） - ETHGlobal 2026 Mumbai

## 📋 プロジェクト概要

**大人証明**は、日本のマイナンバーカードとEthereumスマートコントラクトを組み合わせた、プライバシーファーストな年齢確認サービスです。

SaaS企業はユーザーが本当に18歳以上であることを確認でき、ユーザーの個人情報はスマートフォンに留まります。

### 🎯 ミッション

- ✅ **プライバシー保護**: マイナンバー情報はクラウドに保存されない
- ✅ **信頼性**: 政府公開鍵による暗号学的検証
- ✅ **効率性**: ユーザーは一度の確認で複数のSaaS企業で利用可能
- ✅ **低コスト**: 確認手数料は約10円（0.001 ETH）

---

## 🏗️ システム構成

```
┌─────────────────────────┐
│   大人証明アプリ          │ ← iOS / Android
│ (ユーザーのスマートフォン) │
└────────────┬────────────┘
             │
             ├─→ スマートコントラクト ← 政府公開鍵管理
             │     (Ethereum)            課金・NFT発行
             │
             └─→ SaaS企業              ← サービス提供
                  (年齢確認検証)
```

---

## 📁 ファイル構成

```
ethglobal2026mumbai/
├── README.md                          # このファイル
├── SPECIFICATION.md                   # 詳細仕様書
├── API_DESIGN.md                      # API・シーケンス設計
│
├── contracts/
│   └── AgeVerificationContract.sol    # スマートコントラクト
│
└── ui-mockups/
    └── UI_MOCKUP.md                   # UIモック画面
```

---

## 🚀 クイックスタート

### 仕様を確認する

1. **全体概要**: [SPECIFICATION.md](./SPECIFICATION.md)
   - プロジェクト目的、システムアーキテクチャ、ユーザージャーニー

2. **API詳細**: [API_DESIGN.md](./API_DESIGN.md)
   - スマートコントラクト関数仕様
   - アプリ⇔SaaS企業間の通信プロトコル
   - エラーハンドリング

3. **UI/UX**: [ui-mockups/UI_MOCKUP.md](./ui-mockups/UI_MOCKUP.md)
   - 12個の画面モック
   - UIコンポーネント仕様
   - 画面遷移図

### スマートコントラクトを確認する

```bash
# コントラクトコード
cat contracts/AgeVerificationContract.sol
```

主要な機能:
- `getGovernmentPublicKey()`: 政府公開鍵取得
- `issueAgeVerificationNFT()`: NFT発行（Ether送金）
- `verifyAgeVerification(address)`: NFT検証（SaaS企業向け）

---

## 🔑 主な特徴

### 1. プライバシー優先

```
個人情報フロー:
  マイナンバーカード 
    ↓ (スマートフォンのみで読取・検証)
  生年月日・署名を抽出
    ↓ (政府公開鍵で検証)
  18歳以上 / 以下 のフラグ のみ保持
    ↓ (マイナンバー情報は削除)
  スマートコントラクトでNFT発行
    ↓ (NFT保有確認のみ)
  SaaS企業が「大人である」ことのみ確認
```

### 2. スマートコントラクトベース

- 政府公開鍵をスマートコントラクト上で管理
- NFTで年齢確認済みを表現
- 検証はブロックチェーン上で実施
- 改ざん不可

### 3. 効率的な利用フロー

**初回**:
- マイナンバーカード読取 → 年齢判定 → ウォレット生成

**2回目以降**:
- 同じウォレットアドレスなら再確認不要
- 複数のSaaS企業で同じNFTを利用可能

### 4. 低コスト

- 手数料: 0.001 ETH（約10円）
- ユーザー負担のみ
- SaaS企業の実装コストは最小限

---

## 💰 ビジネスモデル

### 収益源

1. **取引手数料**: 1回の年齢確認で約10円
2. **スケーラビリティ**: ボリュームディスカウント可能
3. **B2B営業**: SaaS企業向けの導入支援サービス

### コスト構造

- スマートコントラクトデプロイ: 1回
- ガス代: 1回あたり数円～数十円
- アプリ開発・運用コスト
- 政府公開鍵管理

---

## 🔐 セキュリティ考慮事項

### 暗号化

- ✅ ECDSA P-256署名検証
- ✅ 秘密鍵: iOS Keychain / Android KeyStore
- ✅ HTTPS/TLS 1.3通信

### スマートコントラクトセキュリティ

- ✅ リエントランシー対策
- ✅ アクセス制御（onlyAdmin）
- ⚠️ 監査推奨: 本番デプロイ前

### 既知の課題

**ウォレットアドレスの乱用**:
- 課題: ユーザーはいくらでもウォレットを生成可能
- 対応: SaaS企業が複数アカウント作成を検出・防止

---

## 🛠️ 技術スタック

### バックエンド

- **スマートコントラクト**: Solidity 0.8.19+
- **ネットワーク**: Ethereum Sepolia (テスト) / Ethereum Mainnet (本番)

### モバイルアプリ

- **クロスプラットフォーム**: React Native / Flutter
- **Web3ライブラリ**: ethers.js / web3.js
- **OS対応**: iOS 14+, Android 10+

### SaaS企業向け

- **SDK**: JavaScript / Python
- **エンドポイント**: REST API / GraphQL (検討中)

---

## 📊 ユーザージャーニー

### フェーズ1: 初期登録（初回のみ）

```
1. アプリインストール
2. Ethereumウォレット自動生成
3. マイナンバーカード読取
4. 公開鍵検証（オフライン）
5. 18歳判定・ローカル保存
6. マイナンバー情報削除
```

### フェーズ2: SaaS利用

```
1. SaaS企業で「年齢確認」ボタン押下
2. アプリが確認ダイアログ表示
3. ユーザー承認
4. スマートコントラクトにNFT発行リクエスト
5. Ether送金（約10円）
6. NFT発行完了
7. SaaS企業が検証 → サービス提供開始
```

---

## 🧪 テスト・デプロイ

### テストネット

**Ethereum Sepolia**
- 目的: 機能検証・スマートコントラクト動作確認
- テスト用Faucet: https://sepoliafaucet.com

**Polygon Mumbai** (将来検討)
- 目的: ガス代削減
- テスト用Faucet: https://faucet.polygon.technology

### 本番環境

- **Ethereum Mainnet** (予定)
- セキュリティ監査完了後のデプロイ

---

## 📈 ロードマップ

| Phase | 内容 | 期限 |
|-------|------|------|
| **Phase 1** | スマートコントラクト開発・テスト | 2026 Q1 |
| **Phase 2** | モバイルアプリ開発（iOS/Android） | 2026 Q2 |
| **Phase 3** | SaaS企業向けSDK開発 | 2026 Q2 |
| **Phase 4** | テストネットデプロイ・パイロットテスト | 2026 Q3 |
| **Phase 5** | セキュリティ監査 | 2026 Q3 |
| **Phase 6** | メインネットローンチ | 2026 Q4 |

---

## 👥 チーム構成（例）

- **スマートコントラクト開発**: 1-2名 (Solidity)
- **iOS開発**: 1名 (Swift)
- **Android開発**: 1名 (Kotlin)
- **バックエンド/Web3**: 1名 (JavaScript/TypeScript)
- **セキュリティ監査**: 外部監査社

---

## 📚 参考資料

### Ethereum開発

- [Solidity Documentation](https://docs.soliditylang.org/)
- [ethers.js Documentation](https://docs.ethers.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)

### 暗号署名

- [ECDSA署名検証](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
- [P-256 Curve](https://en.wikipedia.org/wiki/Curve25519)

### マイナンバーカード

- [公式: デジタル庁](https://www.digital.go.jp/policies/mynumbercard/)
- [マイナンバーカード利用者向け情報](https://www.cao.go.jp/bangouseido/)

### 日本の年齢確認規制

- [特定商取引法](https://www.caa.go.jp/policies/policy_id_1101/)
- [オンラインサービスと成人確認](https://www.meti.go.jp/)

---

## 📞 サポート・問い合わせ

- **GitHub Issues**: プロジェクト内の問題報告
- **Security**: セキュリティ脆弱性報告先（TBD）
- **Email**: contact@adult-verification.example (TBD)

---

## 📜 ライセンス

本プロジェクトのライセンス: **MIT** (予定)

スマートコントラクト: `SPDX-License-Identifier: MIT`

---

## 🙋 貢献

プルリクエスト、フィードバック、アイデアは大歓迎です。

### 貢献手順

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. コミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

---

## 🎓 開発環境のセットアップ（予定）

```bash
# リポジトリをクローン
git clone https://github.com/your-org/adult-verification.git
cd adult-verification

# 依存関係をインストール
npm install

# コントラクトをコンパイル
npx hardhat compile

# テストを実行
npx hardhat test

# ローカルノードを起動
npx hardhat node
```

---

## 🌟 次のステップ

- [ ] スマートコントラクトの詳細実装
- [ ] iOS/Android アプリの開発
- [ ] マイナンバーカード読取ライブラリの統合
- [ ] SaaS企業向けSDK開発
- [ ] セキュリティ監査
- [ ] テストネットでのパイロット運用

---

## 📝 更新履歴

| 日付 | 変更内容 |
|------|---------|
| 2024-01-01 | 初版作成 |
| 2024-01-05 | API設計詳細化 |
| 2024-01-10 | UIモック追加 |

---

**Made with ❤️ for ETHGlobal 2026 Mumbai**
