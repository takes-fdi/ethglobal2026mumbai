# 大人証明アプリ - ユーザーフロー & API設計

## 1. 完全なシーケンスダイアグラム

```
┌─────────┐      ┌──────────┐      ┌─────────────────┐      ┌──────────────────┐
│  ユーザー │      │大人証明   │      │ Ethereum Smart  │      │  SaaS企業        │
│(スマート  │      │アプリ     │      │ Contract        │      │  サーバー         │
│フォン)   │      │          │      │                 │      │                  │
└────┬────┘      └─────┬────┘      └────────┬────────┘      └────────┬─────────┘
     │                 │                    │                        │
     │ 1. アプリ起動    │                    │                        │
     │────────────────→│                    │                        │
     │                 │ 2. ウォレット生成  │                        │
     │                 │  (初回のみ)        │                        │
     │                 │                    │                        │
     │ 3. マイナンバー  │                    │                        │
     │    カード読取    │                    │                        │
     │────────────────→│                    │                        │
     │                 │ 4. 生年月日+署名抽出
     │                 │                    │                        │
     │                 │ 5. 公開鍵取得      │                        │
     │                 │────────────────────→ getGovernmentPublicKey()
     │                 │                    │                        │
     │                 │                    │ 6. 公開鍵返却          │
     │                 │←────────────────────                        │
     │                 │                    │                        │
     │                 │ 7. 署名検証 (オフライン)                     │
     │                 │                    │                        │
     │                 │ 8. 18歳判定 & 状態保存                     │
     │                 │                    │                        │
     │                 │ 9. マイナンバー削除 │                        │
     │                 │                    │                        │
     │                 │ ============ SaaS企業利用 ============      │
     │                 │                    │                        │
     │ 10. SaaS企業に接続                     │                        │
     │─────────────────────────────────────────────────→            │
     │                 │                    │  11. 年齢確認リクエスト  │
     │                 │←─────────────────────────────────────       │
     │                 │                    │                        │
     │ 12. 確認ダイアログ表示
     │                 │                    │                        │
     │ 13. ユーザー承認 │                    │                        │
     │────────────────→│                    │                        │
     │                 │                    │                        │
     │                 │ 14. ローカル状態確認(18歳以上?)           │
     │                 │     → true の場合                           │
     │                 │                    │                        │
     │                 │ 15. issueAgeVerificationNFT()              │
     │                 │     (Ether送金)                             │
     │                 │────────────────────→ NFTを発行             │
     │                 │                    │                        │
     │                 │                    │ 16. イベント発火       │
     │                 │                    │    (AgeVerificationIssued)
     │                 │                    │                        │
     │                 │ 17. トランザック確認                        │
     │                 │                    │                        │
     │                 │ 18. ウォレットアドレス返送                 │
     │                 │─────────────────────────────────────→      │
     │                 │                    │                        │
     │                 │                    │ 19. verifyAgeVerification()
     │                 │                    │←────────────────────────
     │                 │                    │                        │
     │                 │                    │ 20. NFT所有確認        │
     │                 │                    │  (true/false)          │
     │                 │                    │────────────────────→   │
     │                 │                    │                        │
     │                 │                    │ 21. サービス提供開始   │
     │                 │                    │     (またはアクセス拒否)
```

---

## 2. 状態遷移図（ユーザー）

```
        ┌─────────────────────┐
        │   未インストール      │
        └──────────┬──────────┘
                   │ アプリインストール
                   ▼
        ┌─────────────────────┐
        │  ウォレット未生成    │
        └──────────┬──────────┘
                   │ 初回起動
                   ▼
        ┌─────────────────────┐
        │ ウォレット生成済    │
        └──────────┬──────────┘
                   │ マイナンバーカード読取
                   ▼
        ┌─────────────────────┐        ┌─────────────────────┐
        │  署名検証中         │───No───→│    18歳未満状態      │
        └──────────┬──────────┘        └─────────────────────┘
                   │ Yes
                   ▼
        ┌─────────────────────┐
        │    18歳以上状態     │
        │  (SaaS利用可)       │
        └─────────────────────┘
```

---

## 3. スマートコントラクト API仕様

### 関数: `getGovernmentPublicKey()`

```solidity
function getGovernmentPublicKey() public view returns (bytes memory)
```

**説明**: 
- 政府公開鍵を取得（アプリ側で署名検証に使用）

**パラメータ**: なし

**戻り値**:
- `bytes`: 政府公開鍵（ECDSA P-256推定、HEX形式）

**ガス消費**: 読み取り専用 (ガス代なし)

**例**:
```javascript
const publicKey = await contract.getGovernmentPublicKey();
console.log("Government Public Key:", publicKey);
```

---

### 関数: `issueAgeVerificationNFT()`

```solidity
function issueAgeVerificationNFT() public payable returns (bool)
```

**説明**: 
- 18歳以上ユーザーに対して年齢確認NFTを発行
- Ether送金により課金

**パラメータ**: 
- （なし）`msg.sender` で呼び出し元ウォレットを特定

**送信Ether**: 
- 最小値: `verificationFee` (初期値: 0.001 ETH ≈ 10円)

**戻り値**:
- `bool`: 発行成功時 `true`, 失敗時 `false`

**発火イベント**:
```solidity
AgeVerificationIssued(address indexed user, uint256 timestamp)
```

**エラーハンドリング**:
```solidity
require(msg.value >= verificationFee, "Insufficient payment");
require(!ageVerifiedNFT[msg.sender], "Already verified");
```

**例**:
```javascript
const tx = await contract.issueAgeVerificationNFT({
  value: ethers.utils.parseEther("0.001")
});
const receipt = await tx.wait();
console.log("NFT issued:", receipt.transactionHash);
```

---

### 関数: `verifyAgeVerification(address userAddress)`

```solidity
function verifyAgeVerification(address userAddress) public view returns (bool)
```

**説明**: 
- SaaS企業が呼び出し、ユーザーがNFTを保有しているか確認

**パラメータ**: 
- `userAddress` (address): 確認対象ユーザーのEthereumウォレットアドレス

**戻り値**:
- `bool`: NFT保有時 `true`, 非保有時 `false`

**ガス消費**: 読み取り専用 (ガス代なし)

**例**:
```javascript
const isVerified = await contract.verifyAgeVerification(userWalletAddress);
if (isVerified) {
  console.log("User is 18+ and verified");
} else {
  console.log("User is not verified");
}
```

---

### 関数: `setGovernmentPublicKey(bytes memory newPublicKey)`

```solidity
function setGovernmentPublicKey(bytes memory newPublicKey) public onlyAdmin
```

**説明**: 
- 政府公開鍵を登録・更新（管理者のみ）

**パラメータ**: 
- `newPublicKey` (bytes): 新しい政府公開鍵

**戻り値**: なし

**発火イベント**:
```solidity
GovernmentPublicKeyUpdated(bytes newKey, uint256 timestamp)
```

**アクセス制御**:
```solidity
require(msg.sender == admin, "Only admin can update");
```

**例**:
```javascript
const newKey = "0x..."; // 新しい公開鍵
await contract.setGovernmentPublicKey(newKey);
```

---

## 4. アプリ⇔SaaS企業間の API設計

### リクエスト: 年齢確認要求

**方向**: SaaS企業 → アプリ

**通信方法**: Deep Link / URL Scheme

```
adult-verification://verify?
  serviceId=saas_company_123&
  callbackUrl=https://saas.example.com/verify/callback&
  timestamp=1704067200
```

**パラメータ**:
- `serviceId` (string): SaaS企業のID
- `callbackUrl` (string): レスポンス返送先（HTTPS必須）
- `timestamp` (integer): リクエスト発行タイムスタンプ

**例**:
```javascript
// SaaS企業側が開く
window.location.href = "adult-verification://verify?" + 
  "serviceId=netflix&" +
  "callbackUrl=" + encodeURIComponent("https://netflix.com/verify/callback") +
  "&timestamp=" + Date.now();
```

---

### レスポンス: 年齢確認結果

**方向**: アプリ → SaaS企業

**通信方法**: HTTPS POST to `callbackUrl`

```json
{
  "status": "success",
  "walletAddress": "0x1234567890abcdef1234567890abcdef12345678",
  "contractAddress": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
  "transactionHash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
  "timestamp": 1704067200,
  "signature": "0x..." // アプリのウォレットで署名
}
```

**パラメータ**:
- `status` (string): `success` / `failure`
- `walletAddress` (string): ユーザーのEthereumウォレットアドレス
- `contractAddress` (string): スマートコントラクトのアドレス
- `transactionHash` (string): NFT発行トランザクションHash（成功時）
- `timestamp` (integer): レスポンス発行タイムスタンプ
- `signature` (string): アプリのウォレットで署名（検証用）

**失敗時レスポンス例**:
```json
{
  "status": "failure",
  "reason": "user_under_18",
  "timestamp": 1704067200
}
```

---

## 5. エラーハンドリング

### アプリ側

| エラーコード | 原因 | 対応 |
|-----------|------|------|
| `card_read_error` | マイナンバーカード読取失敗 | 再度読取を要求 |
| `signature_verification_failed` | 署名検証失敗 | エラーメッセージ表示 |
| `user_under_18` | 18歳未満判定 | アクセス拒否 |
| `contract_call_error` | スマートコントラクト呼び出し失敗 | リトライ |
| `insufficient_balance` | Ether残高不足 | チャージ要求 |
| `network_error` | ネットワーク接続失敗 | リトライ |

### SaaS企業側

| エラーコード | 原因 | 対応 |
|-----------|------|------|
| `invalid_wallet_address` | ウォレットアドレス形式エラー | ユーザーに再度実施要求 |
| `verification_failed` | NFT検証失敗 | ユーザーに再度実施要求 |
| `contract_unreachable` | スマートコントラクト呼び出し失敗 | リトライ |

---

## 6. テスト用データ

### テスト用ウォレットアドレス
```
0x1234567890abcdef1234567890abcdef12345678 (18歳以上・検証済)
0xabcdefabcdefabcdefabcdefabcdefabcdefabcd (18歳未満)
0xffffffffffffffffffffffffffffffffffffffff (検証未実施)
```

### テスト用トランザクション例
```json
{
  "from": "0x1234567890abcdef1234567890abcdef12345678",
  "to": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
  "value": "1000000000000000",
  "gasLimit": "21000",
  "gasPrice": "20000000000"
}
```

---

## 7. 今後の検討項目

- [ ] テストネット (Sepolia / Mumbai) でのデプロイ・検証
- [ ] マイナンバーカード読取SDKの具体的な実装方法
- [ ] iOS/Androidでのウォレット秘密鍵の安全保管実装
- [ ] NFT発行後の有効期限設定（例：1年有効）
- [ ] 多言語対応（日本語/英語/中国語）
- [ ] アナリティクス・ロギングの仕様
