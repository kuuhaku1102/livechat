#!/usr/bin/env python3
"""
AI記事自動投稿メインスクリプト
キーワード選択、記事生成、画像取得、WordPress投稿を統合実行する
"""

import os
import sys
from keyword_manager import KeywordManager
from article_generator import ArticleGenerator
from image_fetcher import ImageFetcher
from wordpress_poster import WordPressPoster

def main():
    """
    メイン処理
    """
    print("=" * 60)
    print("AI記事自動投稿システム")
    print("=" * 60)
    
    # 環境変数を確認
    openai_api_key = os.getenv('OPENAI_API_KEY')
    wp_site_url = os.getenv('WP_SITE_URL', 'https://s360.jp')
    wp_username = os.getenv('WP_USERNAME', 'admin')
    wp_app_password = os.getenv('WP_APP_PASSWORD')
    
    if not openai_api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        sys.exit(1)
    
    if not wp_app_password:
        print("エラー: WP_APP_PASSWORD環境変数が設定されていません")
        sys.exit(1)
    
    try:
        # Step 1: キーワード組み合わせを選択
        print("\n[Step 1] キーワード組み合わせを選択中...")
        keyword_manager = KeywordManager()
        
        # 統計情報を表示
        stats = keyword_manager.get_stats()
        print(f"  総組み合わせ数: {stats['total_combinations']}")
        print(f"  使用済み: {stats['used_combinations']}")
        print(f"  残り: {stats['remaining_combinations']}")
        print(f"  使用率: {stats['usage_percentage']:.2f}%")
        
        combination = keyword_manager.get_unused_combination()
        
        if not combination:
            print("エラー: すべてのキーワード組み合わせが使用済みです")
            sys.exit(1)
        
        print(f"  選択されたキーワード:")
        print(f"    メイン: {combination['main_keyword']}")
        print(f"    サブ: {combination['sub_keyword']}")
        print(f"    記事タイプ: {combination['article_type']}")
        
        # タイトルとプロンプトを生成
        title = keyword_manager.generate_title(combination)
        prompt = keyword_manager.generate_prompt(combination)
        
        print(f"  タイトル: {title}")
        
        # Step 2: AI記事を生成
        print("\n[Step 2] AI記事を生成中...")
        article_generator = ArticleGenerator(openai_api_key)
        article = article_generator.generate_article(prompt, title)
        
        print(f"  記事生成完了: {article['char_count']}文字")
        
        # Step 3: アイキャッチ画像を取得
        print("\n[Step 3] アイキャッチ画像を取得中...")
        image_fetcher = ImageFetcher()
        
        # メインキーワードで画像を検索
        image_keyword = combination['main_keyword']
        image_path = image_fetcher.get_featured_image(
            keyword=image_keyword,
            orientation="landscape"
        )
        
        if image_path:
            print(f"  画像取得成功: {image_path}")
        else:
            print("  警告: 画像取得に失敗しました。画像なしで投稿します。")
        
        # Step 4: WordPressに投稿
        print("\n[Step 4] WordPressに投稿中...")
        wordpress_poster = WordPressPoster(wp_site_url, wp_username, wp_app_password)
        
        # 接続テスト
        if not wordpress_poster.test_connection():
            print("エラー: WordPressへの接続に失敗しました")
            sys.exit(1)
        
        # 画像をアップロード
        featured_image_id = None
        if image_path:
            featured_image_id = wordpress_poster.upload_media(image_path, title)
            if featured_image_id:
                print(f"  画像アップロード成功: メディアID {featured_image_id}")
        
        # 記事を投稿
        post_id = wordpress_poster.create_post(
            title=article['title'],
            content=article['content'],
            excerpt=article['excerpt'],
            category_name="コラム",
            featured_image_id=featured_image_id,
            status="publish"  # 公開
        )
        
        if post_id:
            print(f"\n{'=' * 60}")
            print("✓ 投稿成功！")
            print(f"{'=' * 60}")
            print(f"投稿ID: {post_id}")
            print(f"タイトル: {article['title']}")
            print(f"URL: {wp_site_url}/?p={post_id}")
            print(f"文字数: {article['char_count']}")
            print(f"カテゴリー: コラム")
            if featured_image_id:
                print(f"アイキャッチ画像: あり（メディアID: {featured_image_id}）")
            print(f"{'=' * 60}")
            
            # 一時ファイルをクリーンアップ
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
                print(f"一時ファイルを削除: {image_path}")
            
            return 0
        else:
            print("\nエラー: 投稿に失敗しました")
            return 1
    
    except Exception as e:
        print(f"\nエラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
