#!/bin/bash
# 大人証明 デモアプリ 起動スクリプト

echo "🎫 大人証明 - Adult Verification デモ"
echo "=========================================="
echo ""

# Python バージョン確認
echo "✓ Python バージョン確認..."
python_version=$(python --version 2>&1)
echo "  使用: $python_version"
echo ""

# 依存パッケージのインストール
echo "✓ 依存パッケージをインストール中..."
python -m pip install -q streamlit 2>&1 | tail -1 || echo "  Streamlit をインストール中..."

echo ""
echo "✓ セットアップ完了"
echo ""
echo "=========================================="
echo "デモアプリを起動します..."
echo "=========================================="
echo ""
echo "📱 ブラウザで自動で開きます:"
echo "   http://localhost:8501"
echo ""
echo "✓ 起動中..."
echo ""

# Streamlit アプリを起動
python -m streamlit run app.py --logger.level=error
