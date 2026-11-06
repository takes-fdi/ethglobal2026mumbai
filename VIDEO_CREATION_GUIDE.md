# 🎬 大人証明 - 説明ビデオ作成ガイド

## 📺 ビデオ作成完全ガイド

### ✅ 既に作成されているもの

| 資料 | ファイル | 内容 |
|------|---------|------|
| **ビデオスクリプト** | `VIDEO_SCRIPT.txt` | 13シーン、5分30秒分の詳細スクリプト |
| **HTMLプレゼンテーション** | `presentation.html` | ブラウザで再生可能なインタラクティブプレゼンテーション |

---

## 🎯 ビデオ作成方法（3つのオプション）

### 📌 オプション1: HTMLプレゼンテーションをビデオに変換（推奨・最速）

**所要時間**: 5分  
**難度**: ⭐ 簡単

#### ステップ1: プレゼンテーションを開く

```bash
# ファイルをダブルクリック、またはブラウザで開く
open presentation.html

# または

google-chrome presentation.html  # Linux
```

#### ステップ2: スクリーンを録画

**Windows:**
```
1. Windows + G キーを押す
2. 「ゲーム バー」が開く
3. 「キャプチャ開始」をクリック
4. プレゼンを見ながら操作
5. 停止
6. ビデオが保存される
```

**Mac:**
```
1. Command + Shift + 5 を押す
2. スクリーンレコーディングを選択
3. 画面をドラッグして記録範囲選択
4. 赤いボタンをクリック（記録開始）
5. 完了したら停止
```

**Linux:**
```
# OBS Studio をインストール
sudo apt install obs-studio

# OBS で記録開始
obs
```

#### ステップ3: ナレーションを追加（オプション）

```bash
# ffmpegでナレーションを合成
ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac output.mp4
```

---

### 📌 オプション2: Adobe After Effects / Premiere Pro（プロフェッショナル）

**所要時間**: 1-2日  
**難度**: ⭐⭐⭐ 中程度

#### ステップ1: テンプレートをダウンロード

- Motion Bro (プラグイン)
- Video Copilot (エフェクト)
- などの無料テンプレート

#### ステップ2: スクリプトに基づいてシーンを作成

```
各シーン（13個）ごとに：
1. ビジュアル作成
2. テキスト追加
3. アニメーション設定
4. ナレーション同期
```

#### ステップ3: 書き出し

```
- 解像度: 1920×1080
- フレームレート: 30fps
- コーデック: H.264
- ビットレート: 5 Mbps
```

---

### 📌 オプション3: DaVinci Resolve（無料・推奨）

**所要時間**: 1日  
**難度**: ⭐⭐ 簡単～中程度  
**コスト**: 無料

#### ステップ1: インストール

```bash
# Windows/Mac/Linux 対応
https://www.blackmagicdesign.com/products/davinciresolve/

# インストール後、起動
DaVinci Resolve
```

#### ステップ2: 新しいプロジェクトを作成

```
File → New Project
- 解像度: 1920×1080
- フレームレート: 30fps
- フォーマット: H.264
```

#### ステップ3: メディアをインポート

```
File → Import Media
- スクリーンショット（13個）
- BGM / SE
- ナレーション音声
```

#### ステップ4: タイムライン編集

```
1. Mediaタブから画像をドラッグ&ドロップ
2. 各シーンの長さを調整
3. トランジション追加
4. テキスト・タイトル追加
5. エフェクト適用
```

#### ステップ5: オーディオミックス

```
Audio → Mix
- ナレーション: -6dB
- BGM: -12dB
- SE: -9dB
```

#### ステップ6: 書き出し

```
File → Export → Add to Deliver
- Format: MP4
- Codec: H.264
- Resolution: 1920×1080
- Frame rate: 30
- Bit rate: 5000k
```

---

## 🎤 ナレーション作成方法

### 方法1: テキスト音声変換（TTS）

**推奨**: Google Cloud Text-to-Speech / Azure TTS

```bash
# Google Cloud TTS を使用
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
input_text = texttospeech.SynthesisInput(text="大人証明は...")
voice = texttospeech.VoiceSelectionParams(
    language_code="ja-JP",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)
response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config}
)
```

### 方法2: 自分で録音

**必要なもの**:
- マイク
- Audacity（無料）

```
1. Audacity を開く
2. 赤いボタン（記録）をクリック
3. スクリプトを読む
4. 停止
5. File → Export → MP3
```

---

## 🎬 YouTubeアップロード方法

### ステップ1: ビデオをアップロード

```
1. YouTube Studio にアクセス
2. 「コンテンツ」→「動画をアップロード」
3. 「ファイルを選択」で MP4 を選択
4. 待機（アップロード完了まで）
```

### ステップ2: 詳細情報を入力

```
- タイトル: 🎫 大人証明 - Adult Verification | 説明ビデオ
- 説明: 
  ビデオ説明...
  GitHub: https://github.com/...
  デモ: ...

- タグ: adult-verification, ethereum, blockchain, 年齢確認
- サムネイル: カスタムサムネイル設定
- 公開設定: 「公開」または「限定公開」
```

### ステップ3: 字幕を追加

```
1. 動画管理 → 字幕
2. 「新しい字幕を追加」
3. 言語を選択（日本語、英語）
4. 手動で追加または自動生成
```

---

## 📊 ビデオ仕様

```
解像度:       1920×1080 (Full HD)
アスペクト比: 16:9
フレームレート: 30 fps
ビットレート: 5 Mbps
コーデック:   H.264 (MP4)
オーディオ:   AAC 192kbps
総尺:         5分30秒
ファイルサイズ: ~200 MB
```

---

## 📝 スクリプトの詳細

### シーン別タイムコード

| # | シーン | 時間 | ファイル |
|---|--------|------|---------|
| 1 | タイトル | 0:00-0:05 | タイトルシーン |
| 2 | 問題提起 | 0:05-0:15 | 問題の説明 |
| 3 | 解決策 | 0:15-0:30 | 3つのコンポーネント |
| 4 | ユーザーフロー1 | 0:30-1:00 | 初期登録 |
| 5 | ユーザーフロー2 | 1:00-1:45 | 年齢確認 |
| 6 | セキュリティ | 1:45-2:15 | セキュリティ機能 |
| 7 | ビジネスモデル | 2:15-2:45 | 課金・収益 |
| 8 | 特徴 | 2:45-3:15 | 6つの特徴 |
| 9 | ユースケース | 3:15-3:45 | 対応サービス |
| 10 | 技術スタック | 3:45-4:15 | 使用技術 |
| 11 | 実装状況 | 4:15-4:45 | 現在の進捗 |
| 12 | ロードマップ | 4:45-5:15 | 今後の予定 |
| 13 | クロージング | 5:15-5:30 | エンディング |

### 完全スクリプト

詳細は `VIDEO_SCRIPT.txt` を参照

---

## 🎬 クイックスタート（最速ビデオ作成方法）

### 所要時間: 30分

```
1. HTMLプレゼンテーションを開く (1分)
   - presentation.html をブラウザで開く

2. スクリーンを録画 (15分)
   - Windows/Mac のスクリーンレコーダーを使用
   - プレゼンを見ながら操作
   - 各スライドで2-5秒停止

3. ナレーションを添付 (10分)
   - FFmpeg で音声合成
   - または自分で録音

4. MP4 に書き出す (5分)
   - OBS / DaVinci Resolve で出力
   - YouTube にアップロード
```

---

## 🎯 推奨作成フロー

### **最も簡単**: HTMLプレゼンテーション版
```
presentation.html を開く
  ↓ (スクリーンレコード)
  ↓ MP4 ビデオ
  ↓ (ナレーション追加)
  ↓ 完成動画
```

### **バランス型**: DaVinci Resolve 版
```
スクリーンショット 13枚
  ↓ (DaVinci Resolve にインポート)
  ↓ タイムライン編集
  ↓ ナレーション・BGM 追加
  ↓ エフェクト適用
  ↓ MP4 書き出し
```

### **プロ仕様**: Adobe After Effects 版
```
スクリプト
  ↓ (After Effects で制作)
  ↓ 各シーン作成・アニメーション
  ↓ Premiere Pro で編集
  ↓ 音声同期・カラーコレクション
  ↓ 高品質 MP4 出力
```

---

## 📱 SNS 用ショートビデオ

### YouTube Shorts / TikTok 対応版

```
- 解像度: 1080×1920 (縦型)
- フレームレート: 30fps
- 尺: 15-60秒
- フォーマット: MP4

推奨: 5分版から抽出して編集
      - シーン3,5,7を組み合わせ
      - テンポアップ
      - 字幕強調
```

---

## 🎤 ナレーション スクリプト（テキスト）

### 日本語版（要約）

```
「SaaS企業にユーザーの年齢確認を提供する
 ブロックチェーンベースのシステムが登場しました。

 それが『大人証明』です。

 多くのSaaS企業は、ユーザーが18歳以上かどうか
 確認する必要があります。

 しかし、ユーザーの個人情報は
 できるだけ守りたい。

 大人証明は3つの要素で構成されています：

 1. ユーザーのスマートフォンに
    インストールされた『大人証明アプリ』

 2. ユーザーの年齢をNFTで記録する
    『スマートコントラクト』

 3. ユーザーにサービスを提供する
    『SaaS企業』

 ユーザーは、まずアプリをインストール。

 マイナンバーカードをスマートフォンにかざして、
 個人情報を読み取ります。

 アプリは政府の公開鍵を使用して
 データを検証します。

 すべてはスマートフォンの中で完結。
 個人情報は外部には一切送信されません。

 [続きは VIDEO_SCRIPT.txt を参照]
```

---

## 📊 完成チェックリスト

- [ ] HTMLプレゼンテーション表示確認
- [ ] スクリーンレコード完了
- [ ] ナレーション音声作成
- [ ] BGM・SE 選択
- [ ] ビデオ編集完了
- [ ] MP4 書き出し完了
- [ ] YouTubeアップロード準備
- [ ] 字幕作成
- [ ] サムネイル作成
- [ ] メタデータ入力完了
- [ ] YouTubeアップロード完了

---

## 💡 推奨 BGM / SE リソース

### 無料 BGM

- YouTube Audio Library (ログイン不要)
- Pixabay Music (https://pixabay.com/music/)
- Incompetech (https://www.incompetech.com/)

### 無料 効果音

- Freesound (https://freesound.org/)
- Zapsplat (https://www.zapsplat.com/)

### 推奨曲

- **Intro**: 信頼感・穏やか (Tech/Corporate)
- **Main**: 活発・テック (Upbeat/Tech)
- **Outro**: 希望的 (Inspirational)

---

## 🎬 最終チェック

**ビデオ完成後に確認**:

- [ ] 音声が明確に聞こえるか
- [ ] テキストが読みやすいか
- [ ] トランジションがスムーズか
- [ ] ロゴ・ブランドが統一されているか
- [ ] 字幕が正確か
- [ ] 色配置は適切か
- [ ] ファイルサイズは適切か
- [ ] YouTubeフォーマット対応か

---

**Made with ❤️ for ETHGlobal 2026 Mumbai**

🎬 このガイドに従って、プロフェッショナルな説明ビデオを作成できます！
