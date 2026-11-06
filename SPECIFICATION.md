# 大人証明アプリ - 仕様書

## 1. プロジェクト概要

### 目的
SaaS企業に対して、ユーザーが18歳以上であることを証明するサービスを提供する。個人情報はユーザーのスマートフォンに留め、Ethereumスマートコントラクトを活用した分散型の年齢確認ソリューション。

### 特徴
- **プライバシーファースト**: マイナンバー情報は一切クラウドに保存しない
- **ブロックチェーンベース**: Ethereumスマートコントラクトで公開鍵を管理
- **NFTベース認証**: 年齢確認済みをNFTで表現
- **軽量なアプリ**: 18歳以上/未満の判定状態のみ保持

---

## 2. システムアーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                      大人証明アプリ（スマートフォン）              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • マイナンバーカード読取（初回のみ）                      │  │
│  │ • Ethereumウォレット生成・管理                           │  │
│  │ • 公開鍵検証（スマートコントラクト内の政府公開鍵を使用）  │  │
│  │ • 18歳以上/未満の状態保持（バイナリ）                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────┬────────────────────┘
                  │                          │
         ┌────────▼──────────┐    ┌─────────▼──────────────┐
         │ Ethereumスマート    │    │   SaaS企業サーバー      │
         │ コントラクト       │    │                       │
         │                   │    │ • ユーザー認証          │
         │ • 政府公開鍵保管   │    │ • ユーザーサービス提供  │
         │ • NFT発行         │    │                       │
         │ • 課金処理        │    │                       │
         └─────────────────────┘    └───────────────────────┘
```

---

## 3. ユーザージャーニー

### フェーズ1: 初期登録（初回のみ）

1. ユーザーが「大人証明」アプリをインストール
2. アプリがEthereumウォレットを生成（秘密鍵はアプリに保管）
3. ユーザーがマイナンバーカードを読取
4. アプリが読取データから以下を抽出：
   - 生年月日
   - 署名（マイナンバーカード内の電子署名）
5. アプリが以下を実施：
   - 生年月日から18歳判定を計算
   - スマートコントラクト内の政府公開鍵を用いて署名を検証
   - 検証成功時：`18歳以上フラグ = true` をローカル保存
   - 検証失敗時：`18歳以上フラグ = false` をローカル保存
6. マイナンバー情報は検証後、アプリから削除
7. ユーザー状態をアプリ内に保持

### フェーズ2: SaaS企業でのサービス利用

1. ユーザーがSaaS企業に接続
2. SaaS企業が「年齢確認」をリクエスト
3. 「大人証明」アプリが以下の手順を実行：
   - ローカルの `18歳以上フラグ` を確認
   - フラグが `true` の場合：
     - 年齢確認済NFTの発行をスマートコントラクトにリクエスト
     - ユーザーのEthereumウォレットアドレスからトランザクション送信
     - Ether を送金（課金：約10円相当）
     - スマートコントラクトがNFTを発行
     - SaaS企業にNFT所有確認をレスポンス（ウォレットアドレス）
   - フラグが `false` の場合：
     - 失敗レスポンスを返す
4. SaaS企業がNFT所有確認：
   - スマートコントラクト上でウォレットアドレスが対象NFTを保有しているか確認
   - 確認成功：ユーザーにサービス提供開始
   - 確認失敗：アクセス拒否

### フェーズ3: 以降の利用

- 同じEthereumウォレットアドレスを使用する限り、再度マイナンバーカード読取は不要
- 新しいウォレットアドレスを作成した場合は、再度初期登録が必要
- 複数のSaaS企業利用時に同じウォレットアドレスを使用すれば、一度のNFT発行で複数企業で利用可能

---

## 4. スマートコントラクト仕様

### 4.1 状態変数

```solidity
// 政府公開鍵（NTTなどから事前取得）
bytes public governmentPublicKey;

// 発行済みNFT
mapping(address => bool) public ageVerifiedNFT;

// 管理者
address public admin;

// 取引手数料（wei）
uint256 public verificationFee = 0.001 ether; // 約10円（参考値）
```

### 4.2 主要関数

#### `issueAgeVerificationNFT()`
- **説明**: 18歳以上であることが確認されたユーザーに対してNFTを発行
- **呼び出し**: 「大人証明」アプリから
- **パラメータ**: なし（msg.senderで判定）
- **処理**:
  1. `msg.value >= verificationFee` を検証
  2. ユーザーアドレスに `ageVerifiedNFT[msg.sender] = true` を設定
  3. トランザクション手数料を回収
- **戻り値**: 成功フラグ
- **イベント**: `AgeVerificationIssued(address indexed user, uint256 timestamp)`

#### `verifyAgeVerification(address userAddress)`
- **説明**: SaaS企業が呼び出し、ユーザーが18歳以上であるか確認
- **呼び出し**: SaaS企業のサーバーまたはクライアント
- **パラメータ**: 
  - `userAddress`: 確認対象ユーザーのEthereumウォレットアドレス
- **処理**:
  1. `ageVerifiedNFT[userAddress]` を確認
  2. 結果を返す
- **戻り値**: `true` / `false`
- **費用**: ガス代のみ（読み取り専用）

#### `setGovernmentPublicKey(bytes memory newPublicKey)`
- **説明**: 政府公開鍵を登録・更新
- **呼び出し**: 管理者のみ
- **パラメータ**: 
  - `newPublicKey`: 政府公開鍵（ECDSA P-256推定）
- **処理**:
  1. 呼び出し元が管理者であることを確認
  2. `governmentPublicKey` を更新
- **イベント**: `GovernmentPublicKeyUpdated(bytes newKey, uint256 timestamp)`

### 4.3 イベント

```solidity
event AgeVerificationIssued(address indexed user, uint256 timestamp);
event GovernmentPublicKeyUpdated(bytes newKey, uint256 timestamp);
event VerificationFeeUpdated(uint256 newFee, uint256 timestamp);
```

---

## 5. アプリケーション仕様

### 5.1 技術スタック

- **対応OS**: iOS, Android
- **開発フレームワーク**: React Native / Flutter（検討）
- **Web3ライブラリ**: ethers.js / web3.js
- **マイナンバーカード読取**: 公式SDK（e-Japan等）
- **暗号化処理**: 標準ライブラリ

### 5.2 ローカルストレージ設計

```javascript
{
  "walletAddress": "0x...",
  "privateKey": "encrypted_key_in_secure_enclave",
  "ageVerificationStatus": true, // true: 18歳以上, false: 18歳未満
  "verificationDate": 1704067200, // Unix timestamp
  "contractAddress": "0x..."
}
```

**注**: 秘密鍵はセキュアエンクレーブ（iOS）またはKeyStore（Android）に保管

### 5.3 アプリの主要機能

#### ① ウォレット生成・管理
- ユーザーが初回起動時にウォレット自動生成
- 秘密鍵をセキュアなローカルストレージに保管
- バックアップ機能（シードフレーズ表示）

#### ② マイナンバーカード読取・検証
- NFC/IC card読取でマイナンバーカード情報取得
- 以下のみ抽出：
  - 生年月日
  - 電子署名
- 18歳判定ロジック：`現在年 - 生年 >= 18` または `(現在年 - 生年 == 18 かつ 誕生月日 <= 現在月日)`

#### ③ 公開鍵検証
- スマートコントラクトから政府公開鍵を取得
- ECDSA署名検証をアプリ内で実行
- 検証結果を `ageVerificationStatus` に保存

#### ④ 年齢確認リクエスト処理
- SaaS企業からのリクエスト受信
- `ageVerificationStatus` を確認
- `true` の場合：
  1. スマートコントラクトの `issueAgeVerificationNFT()` を呼び出し
  2. 手数料を支払い
  3. NFT発行を待機
  4. SaaS企業にウォレットアドレスを返送
- `false` の場合：
  1. エラー応答を返送

### 5.4 UI/UX フロー

```
[アプリ起動]
    ↓
[ウォレット有無確認]
    ├─ 有：[メイン画面]
    └─ 無：[新規ウォレット生成] → [シードフレーズ表示] → [バックアップ確認]
        ↓
    [マイナンバーカード読取画面]
        ↓
    [カード読取実行]
        ↓
    [署名検証処理（バックグラウンド）]
        ↓
    [検証結果表示]
        ├─ 成功：[18歳以上確認] → [メイン画面]
        └─ 失敗：[18歳未満]
        ↓
    [SaaS企業からリクエスト受信時]
        ↓
    [確認ダイアログ表示]
        ↓
    [ユーザー承認]
        ↓
    [NFT発行トランザクション送信]
        ↓
    [ウォレットアドレス返送完了]
```

---

## 6. SaaS企業連携仕様

### 6.1 SaaS企業の実装負担（最小限）

SaaS企業が実装すべき処理：

```javascript
// 1. ユーザーから年齢確認要求受信時
const userWalletAddress = await requestAgeVerificationFromApp();

// 2. スマートコントラクト上で確認
const isAdult = await ageVerificationContract.verifyAgeVerification(userWalletAddress);

// 3. 結果に応じて処理
if (isAdult) {
  // サービス提供開始
  provideService(user);
} else {
  // アクセス拒否
  denyAccess(user);
}
```

### 6.2 通信プロトコル

**アプリ ← SaaS企業**
```json
{
  "action": "requestAgeVerification",
  "timestamp": 1704067200,
  "serviceId": "saas_company_id"
}
```

**アプリ → SaaS企業**
```json
{
  "status": "success" or "failure",
  "walletAddress": "0x...",
  "timestamp": 1704067200,
  "transactionHash": "0x..."
}
```

### 6.3 SaaS企業への保証

- **一度の確認で以降は不要**: 同じウォレットアドレスは1回のNFT発行で複数回利用可能
- **個人情報なし**: マイナンバーやPII情報は一切渡されない
- **公開ブロックチェーン**: スマートコントラクト上で検証可能

---

## 7. セキュリティ考慮

### 7.1 暗号化・鍵管理

- **秘密鍵保管**: iOS Keychain / Android KeyStore
- **マイナンバー情報**: 検証直後に削除（メモリ上から消去）
- **通信**: HTTPS/TLS 1.3 以上

### 7.2 スマートコントラクトセキュリティ

- **リエントランシー対策**: 状態変更を先行実行
- **アクセス制御**: `onlyAdmin` 修飾子
- **タイムロック**: 大型アップデートの遅延実行（検討）

### 7.3 ユーザー識別子の課題と対応

**課題**: ウォレットアドレスはいくらでも生成可能

**対応案**:
1. **複数利用禁止**: SaaS企業が同一ウォレットアドレスからの複数アカウント作成を禁止
2. **ハイレート制限**: 1つのウォレットアドレスに対して、24時間以内に複数回のNFT発行を制限

---

## 8. マイルストーン

| フェーズ | 内容 | 期限 |
|---------|------|------|
| Phase 1 | スマートコントラクト開発・テスト | - |
| Phase 2 | 大人証明アプリ開発（iOS/Android） | - |
| Phase 3 | SaaS企業向けSDK/API提供 | - |
| Phase 4 | パイロットテスト・運用 | - |
| Phase 5 | 本格ローンチ | - |

---

## 9. 開発リソース・体制

- **スマートコントラクト開発**: Solidity エンジニア
- **iOS開発**: Swift エンジニア
- **Android開発**: Kotlin エンジニア
- **Web3インテグレーション**: フロントエンド/バックエンド エンジニア
- **セキュリティレビュー**: セキュリティ監査チーム

---

## 10. 参考資料

- [Ethereum Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [マイナンバーカード利用者向け情報](https://www.cao.go.jp/bangouseido/)
- [Web3.js / ethers.js ドキュメント](https://docs.ethers.org/)
