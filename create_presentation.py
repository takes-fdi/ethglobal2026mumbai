#!/usr/bin/env python3
"""
大人証明 - プレゼンテーション資料生成スクリプト
PowerPoint形式で全12スライドを自動生成
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation():
    """PowerPoint プレゼンテーションを作成"""
    
    # プレゼンテーション初期化
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # スライドマスター設定
    blank_slide_layout = prs.slide_layouts[6]  # 空白スライド
    
    # スライド1: タイトル
    slide = prs.slides.add_slide(blank_slide_layout)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(102, 126, 234)  # 青紫
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = "🎫 大人証明"
    title_frame.paragraphs[0].font.size = Pt(72)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(9), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Adult Verification"
    subtitle_frame.paragraphs[0].font.size = Pt(48)
    subtitle_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    desc_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.8), Inches(9), Inches(2))
    desc_frame = desc_box.text_frame
    desc_frame.word_wrap = True
    desc_frame.text = "プライバシーを守りながら\n安全に年齢確認する\nブロックチェーンベースのシステム"
    for paragraph in desc_frame.paragraphs:
        paragraph.font.size = Pt(28)
        paragraph.font.color.rgb = RGBColor(255, 255, 255)
        paragraph.alignment = PP_ALIGN.CENTER
    
    # スライド2: 問題提起
    slide = prs.slides.add_slide(blank_slide_layout)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🤔 なぜ必要か？"
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)
    
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    items = [
        "📺 ストリーミングサービス (Netflix, Hulu, Amazon Prime)",
        "🎮 オンラインゲーム (18禁コンテンツ)",
        "🍷 酒・タバコ通販",
        "🔞 アダルトサイト",
    ]
    
    for i, item in enumerate(items):
        if i == 0:
            content_frame.text = item
            content_frame.paragraphs[0].font.size = Pt(24)
            content_frame.paragraphs[0].level = 0
        else:
            p = content_frame.add_paragraph()
            p.text = item
            p.font.size = Pt(24)
            p.level = 0
    
    # 課題
    challenge_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(9), Inches(1.5))
    challenge_frame = challenge_box.text_frame
    challenge_frame.word_wrap = True
    challenge_frame.text = "➜ ユーザーの年齢確認が必要だが、個人情報は最小限にしたい"
    challenge_frame.paragraphs[0].font.size = Pt(26)
    challenge_frame.paragraphs[0].font.bold = True
    challenge_frame.paragraphs[0].font.color.rgb = RGBColor(242, 113, 28)
    challenge_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # スライド3: 解決策
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "✨ 3つのコンポーネント"
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    # 3つのボックス
    components = [
        ("📱 大人証明アプリ", "スマートフォンにインストール\nマイナンバーカード読取", 0.8),
        ("🔐 スマートコントラクト", "Ethereum上に実装\n年齢確認済みNFT発行", 3.7),
        ("💼 SaaS企業", "NFT保有を確認\nサービス提供開始", 6.6)
    ]
    
    for title, desc, x_pos in components:
        # ボックス背景
        shape = slide.shapes.add_shape(1, Inches(x_pos), Inches(1.8), Inches(2.5), Inches(4.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(245, 247, 250)
        shape.line.color.rgb = RGBColor(102, 126, 234)
        shape.line.width = Pt(2)
        
        # タイトル
        title_box = slide.shapes.add_textbox(Inches(x_pos+0.2), Inches(2.1), Inches(2.1), Inches(0.8))
        title_frame = title_box.text_frame
        title_frame.word_wrap = True
        title_frame.text = title
        title_frame.paragraphs[0].font.size = Pt(18)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
        
        # 説明
        desc_box = slide.shapes.add_textbox(Inches(x_pos+0.2), Inches(3.2), Inches(2.1), Inches(3))
        desc_frame = desc_box.text_frame
        desc_frame.word_wrap = True
        desc_frame.text = desc
        desc_frame.paragraphs[0].font.size = Pt(14)
        desc_frame.paragraphs[0].line_spacing = 1.3
    
    # スライド4: ユーザーフロー1
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🚀 ユーザーフロー1 - 初期登録"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    steps = [
        "1️⃣ アプリインストール",
        "2️⃣ ウォレット自動生成",
        "3️⃣ マイナンバーカード読取",
        "4️⃣ 署名検証",
        "5️⃣ 年齢判定 (18歳以上/未満)",
        "6️⃣ マイナンバー情報は削除 ✓"
    ]
    
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    for i, step in enumerate(steps):
        if i == 0:
            content_frame.text = step
            content_frame.paragraphs[0].font.size = Pt(20)
        else:
            p = content_frame.add_paragraph()
            p.text = step
            p.font.size = Pt(20)
            p.level = 0
    
    # スライド5: ユーザーフロー2
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🔗 ユーザーフロー2 - 年齢確認"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    steps2 = [
        "1️⃣ SaaS企業へアクセス",
        "2️⃣ 年齢確認リクエスト受け取る",
        "3️⃣ アプリで確認 (ワンタップ)",
        "4️⃣ NFT発行リクエスト送信",
        "5️⃣ Etherを送金 (約10円)",
        "6️⃣ SaaS企業がNFT検証",
        "7️⃣ ✅ サービス提供開始"
    ]
    
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    for i, step in enumerate(steps2):
        if i == 0:
            content_frame.text = step
            content_frame.paragraphs[0].font.size = Pt(20)
        else:
            p = content_frame.add_paragraph()
            p.text = step
            p.font.size = Pt(20)
            p.level = 0
    
    # スライド6: セキュリティ
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🔒 セキュリティ - 4層防御"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    security_items = [
        ("🔐 層1: ローカル保管", "個人情報はスマートフォンのみ"),
        ("🔑 層2: 秘密鍵保護", "iOS Keychain / Android KeyStore"),
        ("✓ 層3: 公開鍵検証", "政府公開鍵による検証"),
        ("⛓️ 層4: ブロックチェーン", "改ざん不可能な永続記録")
    ]
    
    y_pos = 1.8
    for title, desc in security_items:
        title_box = slide.shapes.add_textbox(Inches(1), Inches(y_pos), Inches(8), Inches(0.35))
        title_frame = title_box.text_frame
        title_frame.text = title
        title_frame.paragraphs[0].font.size = Pt(18)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
        
        desc_box = slide.shapes.add_textbox(Inches(1.5), Inches(y_pos+0.45), Inches(7.5), Inches(0.5))
        desc_frame = desc_box.text_frame
        desc_frame.text = desc
        desc_frame.paragraphs[0].font.size = Pt(16)
        
        y_pos += 1.2
    
    # スライド7: ビジネスモデル
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "💰 ビジネスモデル"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    # 3つのボックス
    business = [
        ("👤 ユーザー", "1回 = 10円", 1),
        ("💼 SaaS企業", "追加コスト = 0円", 3.8),
        ("🏢 システム", "手数料獲得", 6.5)
    ]
    
    for label, value, x_pos in business:
        shape = slide.shapes.add_shape(1, Inches(x_pos), Inches(2), Inches(2.5), Inches(3.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(245, 247, 250)
        shape.line.color.rgb = RGBColor(102, 126, 234)
        shape.line.width = Pt(2)
        
        label_box = slide.shapes.add_textbox(Inches(x_pos+0.3), Inches(2.5), Inches(1.9), Inches(0.6))
        label_frame = label_box.text_frame
        label_frame.text = label
        label_frame.paragraphs[0].font.size = Pt(20)
        label_frame.paragraphs[0].font.bold = True
        label_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
        label_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        value_box = slide.shapes.add_textbox(Inches(x_pos+0.3), Inches(4), Inches(1.9), Inches(1))
        value_frame = value_box.text_frame
        value_frame.word_wrap = True
        value_frame.text = value
        value_frame.paragraphs[0].font.size = Pt(18)
        value_frame.paragraphs[0].font.bold = True
        value_frame.paragraphs[0].font.color.rgb = RGBColor(242, 113, 28)
        value_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # スライド8: 6つの特徴
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "⭐ 6つの特徴"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    features = [
        "🔐 プライバシー - 個人情報はスマートフォンのみ",
        "✅ セキュリティ - 政府公開鍵による検証",
        "📈 スケーラビリティ - 複数SaaS企業対応",
        "💸 低コスト - 1回わずか10円",
        "⚡ 高速 - ブロックチェーン処理",
        "👤 シンプル - ワンタップで完了"
    ]
    
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    for i, feature in enumerate(features):
        if i == 0:
            content_frame.text = feature
            content_frame.paragraphs[0].font.size = Pt(22)
        else:
            p = content_frame.add_paragraph()
            p.text = feature
            p.font.size = Pt(22)
    
    # スライド9: ユースケース
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🎯 ユースケース"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    usecases = [
        "📺 ストリーミング: Netflix, Hulu, Amazon Prime, Disney+",
        "🎮 ゲーム: Call of Duty, PUBG, Fortnite",
        "📱 ソーシャル: X (Twitter), Mastodon",
        "🎰 その他: オンラインカジノ, 酒・タバコ通販"
    ]
    
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    for i, usecase in enumerate(usecases):
        if i == 0:
            content_frame.text = usecase
            content_frame.paragraphs[0].font.size = Pt(20)
            content_frame.paragraphs[0].level = 0
        else:
            p = content_frame.add_paragraph()
            p.text = usecase
            p.font.size = Pt(20)
            p.level = 0
    
    # スライド10: 技術スタック
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🛠️ 技術スタック"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    tech_items = [
        ("📱 フロントエンド", "React Native / Flutter"),
        ("🔐 スマートコントラクト", "Solidity (Ethereum)"),
        ("🔌 API", "REST / GraphQL"),
        ("💾 データストア", "Ethereum Blockchain")
    ]
    
    y_pos = 1.8
    for label, tech in tech_items:
        label_box = slide.shapes.add_textbox(Inches(1), Inches(y_pos), Inches(3), Inches(0.5))
        label_frame = label_box.text_frame
        label_frame.text = label
        label_frame.paragraphs[0].font.size = Pt(20)
        label_frame.paragraphs[0].font.bold = True
        label_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
        
        tech_box = slide.shapes.add_textbox(Inches(4.5), Inches(y_pos), Inches(4.5), Inches(0.5))
        tech_frame = tech_box.text_frame
        tech_frame.text = tech
        tech_frame.paragraphs[0].font.size = Pt(20)
        
        y_pos += 1.2
    
    # スライド11: 実装状況
    slide = prs.slides.add_slide(blank_slide_layout)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "✅ 実装状況"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(102, 126, 234)
    
    completed = [
        "✅ 仕様書・設計ドキュメント",
        "✅ スマートコントラクト (Solidity)",
        "✅ デモアプリ (Streamlit)",
        "✅ UI モック (12個の画面)",
        "✅ テストスクリプト (100% 合格)"
    ]
    
    upcoming = [
        "⏳ iOS・Android アプリ開発",
        "⏳ バックエンド API 実装",
        "⏳ Ethereum Sepolia テストネット",
        "⏳ メインネット ローンチ"
    ]
    
    # 完了
    y_pos = 1.8
    for item in completed:
        item_box = slide.shapes.add_textbox(Inches(1), Inches(y_pos), Inches(8), Inches(0.4))
        item_frame = item_box.text_frame
        item_frame.text = item
        item_frame.paragraphs[0].font.size = Pt(18)
        item_frame.paragraphs[0].font.color.rgb = RGBColor(52, 199, 89)
        y_pos += 0.6
    
    # 予定中
    y_pos += 0.5
    for item in upcoming:
        item_box = slide.shapes.add_textbox(Inches(1), Inches(y_pos), Inches(8), Inches(0.4))
        item_frame = item_box.text_frame
        item_frame.text = item
        item_frame.paragraphs[0].font.size = Pt(18)
        item_frame.paragraphs[0].font.color.rgb = RGBColor(255, 149, 0)
        y_pos += 0.6
    
    # スライド12: ロードマップ & クロージング
    slide = prs.slides.add_slide(blank_slide_layout)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(102, 126, 234)
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.8), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🗓️ ロードマップ"
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    roadmap_items = [
        ("2024 Q4", "Ethereum Sepolia テストネット検証"),
        ("2025 Q1", "ベータ版リリース・SaaS企業テスト"),
        ("2025 Q2", "正式版・メインネット展開"),
        ("2025 Q3", "L2拡張 (Polygon等)")
    ]
    
    y_pos = 2.0
    for quarter, desc in roadmap_items:
        quarter_box = slide.shapes.add_textbox(Inches(1), Inches(y_pos), Inches(2), Inches(0.5))
        quarter_frame = quarter_box.text_frame
        quarter_frame.text = quarter
        quarter_frame.paragraphs[0].font.size = Pt(18)
        quarter_frame.paragraphs[0].font.bold = True
        quarter_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        
        desc_box = slide.shapes.add_textbox(Inches(3.5), Inches(y_pos), Inches(5.5), Inches(0.5))
        desc_frame = desc_box.text_frame
        desc_frame.text = desc
        desc_frame.paragraphs[0].font.size = Pt(16)
        desc_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        
        y_pos += 0.9
    
    closing_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.2), Inches(9), Inches(1))
    closing_frame = closing_box.text_frame
    closing_frame.word_wrap = True
    closing_frame.text = "Made with ❤️ for ETHGlobal 2026 Mumbai"
    closing_frame.paragraphs[0].font.size = Pt(24)
    closing_frame.paragraphs[0].font.bold = True
    closing_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    closing_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # プレゼンテーション保存
    prs.save('presentation.pptx')
    print("✅ PowerPoint プレゼンテーション作成完了: presentation.pptx")
    
    return prs

if __name__ == "__main__":
    try:
        from pptx import Presentation
        create_presentation()
    except ImportError:
        print("❌ エラー: python-pptx がインストールされていません")
        print("インストール: pip install python-pptx")
