#!/usr/bin/env python3
"""
WordPress自動投稿スクリプト
WordPress REST APIを使用して、生成された記事を自動的に投稿する
"""

import os
import sys
import requests
import base64
from typing import Dict, Optional, List

class WordPressPoster:
    def __init__(
        self,
        site_url: str,
        username: str,
        app_password: str
    ):
        """
        WordPress投稿器の初期化
        
        Args:
            site_url: WordPressサイトのURL（例: https://s360.jp）
            username: WordPress管理者ユーザー名
            app_password: WordPressアプリケーションパスワード
        """
        self.site_url = site_url.rstrip('/')
        self.username = username
        self.app_password = app_password
        # パーマリンク設定によってREST APIのURLが異なる場合があるため、両方試す
        self.api_base = f"{self.site_url}/index.php?rest_route=/wp/v2"
        
        # Basic認証用のヘッダーを作成
        credentials = f"{username}:{app_password}"
        token = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """
        WordPress REST APIへの接続をテストする
        
        Returns:
            接続成功の場合True、失敗の場合False
        """
        try:
            response = requests.get(
                f"{self.api_base}/users/me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"接続成功: {user_data.get('name', 'Unknown')} としてログイン")
                return True
            else:
                print(f"接続失敗: ステータスコード {response.status_code}")
                print(f"レスポンス: {response.text}")
                return False
        
        except Exception as e:
            print(f"接続エラー: {str(e)}")
            return False
    
    def get_or_create_category(self, category_name: str) -> Optional[int]:
        """
        カテゴリーを取得または作成する
        
        Args:
            category_name: カテゴリー名
        
        Returns:
            カテゴリーID、失敗の場合None
        """
        try:
            # 既存のカテゴリーを検索
            response = requests.get(
                f"{self.api_base}/categories",
                params={'search': category_name},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                categories = response.json()
                for cat in categories:
                    if cat['name'] == category_name:
                        print(f"既存のカテゴリーを使用: {category_name} (ID: {cat['id']})")
                        return cat['id']
            
            # カテゴリーが存在しない場合は作成
            response = requests.post(
                f"{self.api_base}/categories",
                headers=self.headers,
                json={'name': category_name},
                timeout=10
            )
            
            if response.status_code == 201:
                category = response.json()
                print(f"新しいカテゴリーを作成: {category_name} (ID: {category['id']})")
                return category['id']
            else:
                print(f"カテゴリー作成失敗: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"カテゴリー処理エラー: {str(e)}")
            return None
    
    def upload_media(self, image_path: str, title: str) -> Optional[int]:
        """
        メディアライブラリに画像をアップロードする
        
        Args:
            image_path: 画像ファイルのパス
            title: 画像のタイトル
        
        Returns:
            メディアID、失敗の場合None
        """
        try:
            if not os.path.exists(image_path):
                print(f"画像ファイルが見つかりません: {image_path}")
                return None
            
            # ファイルを読み込む
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # ファイル名を取得
            filename = os.path.basename(image_path)
            
            # Content-Typeを設定
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif filename.lower().endswith('.png'):
                content_type = 'image/png'
            else:
                content_type = 'application/octet-stream'
            
            # アップロード用のヘッダー
            upload_headers = {
                'Authorization': self.headers['Authorization'],
                'Content-Type': content_type,
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
            
            # メディアをアップロード
            response = requests.post(
                f"{self.api_base}/media",
                headers=upload_headers,
                data=image_data,
                params={'title': title},
                timeout=30
            )
            
            if response.status_code == 201:
                media = response.json()
                print(f"画像をアップロード: {filename} (ID: {media['id']})")
                return media['id']
            else:
                print(f"画像アップロード失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return None
        
        except Exception as e:
            print(f"画像アップロードエラー: {str(e)}")
            return None
    
    def create_post(
        self,
        title: str,
        content: str,
        excerpt: str = "",
        category_name: str = "コラム",
        featured_image_id: Optional[int] = None,
        status: str = "publish"
    ) -> Optional[int]:
        """
        WordPressに記事を投稿する
        
        Args:
            title: 記事タイトル
            content: 記事本文（HTML）
            excerpt: 抜粋
            category_name: カテゴリー名
            featured_image_id: アイキャッチ画像のメディアID
            status: 投稿ステータス（publish, draft, private）
        
        Returns:
            投稿ID、失敗の場合None
        """
        try:
            # カテゴリーIDを取得または作成
            category_id = self.get_or_create_category(category_name)
            
            # 投稿データを作成
            post_data = {
                'title': title,
                'content': content,
                'excerpt': excerpt,
                'status': status,
                'categories': [category_id] if category_id else []
            }
            
            # アイキャッチ画像が指定されている場合
            if featured_image_id:
                post_data['featured_media'] = featured_image_id
            
            # 投稿を作成
            response = requests.post(
                f"{self.api_base}/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post = response.json()
                post_id = post['id']
                post_url = post['link']
                print(f"記事を投稿: {title}")
                print(f"投稿ID: {post_id}")
                print(f"URL: {post_url}")
                return post_id
            else:
                print(f"投稿失敗: ステータスコード {response.status_code}")
                print(f"レスポンス: {response.text}")
                return None
        
        except Exception as e:
            print(f"投稿エラー: {str(e)}")
            return None


def main():
    """
    テスト用のメイン関数
    """
    # 環境変数から認証情報を取得
    site_url = os.getenv('WP_SITE_URL', 'https://s360.jp')
    username = os.getenv('WP_USERNAME', 'admin')
    app_password = os.getenv('WP_APP_PASSWORD')
    
    if not app_password:
        print("エラー: WP_APP_PASSWORD環境変数が設定されていません")
        sys.exit(1)
    
    # WordPressPosterを初期化
    poster = WordPressPoster(site_url, username, app_password)
    
    # 接続テスト
    print("=== WordPress接続テスト ===")
    if not poster.test_connection():
        print("接続に失敗しました")
        sys.exit(1)
    
    print("\n=== テスト投稿 ===")
    
    # テスト記事を読み込む
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_article_path = os.path.join(script_dir, 'test_article.html')
    
    if not os.path.exists(test_article_path):
        print(f"エラー: テスト記事が見つかりません: {test_article_path}")
        print("先に article_generator.py を実行してください")
        sys.exit(1)
    
    with open(test_article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # タイトルを抽出
    import re
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    if title_match:
        title = title_match.group(1)
        content = re.sub(r'<h1>.*?</h1>\n?', '', content)
    else:
        title = "テスト記事"
    
    # 投稿を作成
    post_id = poster.create_post(
        title=title,
        content=content,
        excerpt="これはテスト投稿です。",
        category_name="コラム",
        status="draft"  # テストなのでドラフトとして保存
    )
    
    if post_id:
        print(f"\nテスト投稿が成功しました（ドラフトとして保存）")
    else:
        print("\nテスト投稿に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
