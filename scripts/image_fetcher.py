#!/usr/bin/env python3
"""
アイキャッチ画像自動取得スクリプト
Unsplash APIまたはPexels APIを使用して、記事に適した画像を自動取得する
"""

import os
import sys
import requests
from typing import Optional, Dict
import tempfile

class ImageFetcher:
    def __init__(self, api_key: Optional[str] = None, service: str = "unsplash"):
        """
        画像取得器の初期化
        
        Args:
            api_key: API キー（指定しない場合は環境変数から取得）
            service: 使用するサービス（unsplash または pexels）
        """
        self.service = service.lower()
        
        if self.service == "unsplash":
            self.api_key = api_key or os.getenv('UNSPLASH_API_KEY')
            self.api_base = "https://api.unsplash.com"
        elif self.service == "pexels":
            self.api_key = api_key or os.getenv('PEXELS_API_KEY')
            self.api_base = "https://api.pexels.com/v1"
        else:
            raise ValueError(f"サポートされていないサービス: {service}")
        
        # APIキーが不要な場合はフリー画像を使用
        self.use_free_images = not self.api_key
        
        if self.use_free_images:
            print(f"警告: {service.upper()} APIキーが設定されていません。フリー画像を使用します。")
    
    def search_image(self, keyword: str, orientation: str = "landscape") -> Optional[Dict]:
        """
        キーワードに基づいて画像を検索する
        
        Args:
            keyword: 検索キーワード
            orientation: 画像の向き（landscape, portrait, squarish）
        
        Returns:
            画像情報の辞書、失敗の場合None
        """
        if self.use_free_images:
            return self._get_free_image(keyword)
        
        if self.service == "unsplash":
            return self._search_unsplash(keyword, orientation)
        elif self.service == "pexels":
            return self._search_pexels(keyword, orientation)
    
    def _search_unsplash(self, keyword: str, orientation: str) -> Optional[Dict]:
        """
        Unsplash APIで画像を検索する
        
        Args:
            keyword: 検索キーワード
            orientation: 画像の向き
        
        Returns:
            画像情報の辞書
        """
        try:
            headers = {'Authorization': f'Client-ID {self.api_key}'}
            params = {
                'query': keyword,
                'orientation': orientation,
                'per_page': 1
            }
            
            response = requests.get(
                f"{self.api_base}/search/photos",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    photo = data['results'][0]
                    return {
                        'url': photo['urls']['regular'],
                        'download_url': photo['urls']['full'],
                        'author': photo['user']['name'],
                        'author_url': photo['user']['links']['html'],
                        'source': 'Unsplash'
                    }
            
            print(f"Unsplash検索失敗: {response.status_code}")
            return None
        
        except Exception as e:
            print(f"Unsplash検索エラー: {str(e)}")
            return None
    
    def _search_pexels(self, keyword: str, orientation: str) -> Optional[Dict]:
        """
        Pexels APIで画像を検索する
        
        Args:
            keyword: 検索キーワード
            orientation: 画像の向き
        
        Returns:
            画像情報の辞書
        """
        try:
            headers = {'Authorization': self.api_key}
            params = {
                'query': keyword,
                'orientation': orientation,
                'per_page': 1
            }
            
            response = requests.get(
                f"{self.api_base}/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    photo = data['photos'][0]
                    return {
                        'url': photo['src']['large'],
                        'download_url': photo['src']['original'],
                        'author': photo['photographer'],
                        'author_url': photo['photographer_url'],
                        'source': 'Pexels'
                    }
            
            print(f"Pexels検索失敗: {response.status_code}")
            return None
        
        except Exception as e:
            print(f"Pexels検索エラー: {str(e)}")
            return None
    
    def _get_free_image(self, keyword: str) -> Dict:
        """
        フリー画像サービス（Picsum Photos）から画像を取得する
        APIキーが不要な代替手段
        
        Args:
            keyword: 検索キーワード（実際には使用されない）
        
        Returns:
            画像情報の辞書
        """
        # Picsum Photosはランダムな画像を提供
        # キーワード検索はできないが、APIキー不要
        return {
            'url': 'https://picsum.photos/1200/800',
            'download_url': 'https://picsum.photos/1200/800',
            'author': 'Lorem Picsum',
            'author_url': 'https://picsum.photos',
            'source': 'Picsum Photos'
        }
    
    def download_image(self, image_info: Dict, save_path: Optional[str] = None) -> Optional[str]:
        """
        画像をダウンロードする
        
        Args:
            image_info: search_imageで取得した画像情報
            save_path: 保存先パス（指定しない場合は一時ファイル）
        
        Returns:
            保存されたファイルパス、失敗の場合None
        """
        try:
            # 画像をダウンロード
            response = requests.get(image_info['download_url'], timeout=30)
            
            if response.status_code == 200:
                # 保存先を決定
                if not save_path:
                    # 一時ファイルを作成
                    temp_file = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix='.jpg',
                        prefix='featured_'
                    )
                    save_path = temp_file.name
                    temp_file.close()
                
                # ファイルに保存
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"画像をダウンロード: {save_path}")
                print(f"提供元: {image_info['source']} - {image_info['author']}")
                
                return save_path
            else:
                print(f"画像ダウンロード失敗: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"画像ダウンロードエラー: {str(e)}")
            return None
    
    def get_featured_image(
        self,
        keyword: str,
        save_path: Optional[str] = None,
        orientation: str = "landscape"
    ) -> Optional[str]:
        """
        キーワードに基づいてアイキャッチ画像を取得してダウンロードする
        
        Args:
            keyword: 検索キーワード
            save_path: 保存先パス
            orientation: 画像の向き
        
        Returns:
            保存されたファイルパス、失敗の場合None
        """
        # 画像を検索
        image_info = self.search_image(keyword, orientation)
        
        if not image_info:
            print(f"キーワード '{keyword}' で画像が見つかりませんでした")
            return None
        
        # 画像をダウンロード
        return self.download_image(image_info, save_path)


def main():
    """
    テスト用のメイン関数
    """
    # スクリプトのディレクトリに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=== アイキャッチ画像取得テスト ===")
    
    # ImageFetcherを初期化（APIキーなしでフリー画像を使用）
    fetcher = ImageFetcher()
    
    # テスト用のキーワード
    keyword = "ライブチャット"
    
    # 画像を取得
    image_path = fetcher.get_featured_image(
        keyword=keyword,
        save_path="test_featured_image.jpg"
    )
    
    if image_path:
        print(f"\n✓ 画像取得成功: {image_path}")
        
        # ファイルサイズを確認
        file_size = os.path.getsize(image_path)
        print(f"ファイルサイズ: {file_size / 1024:.2f} KB")
    else:
        print("\n✗ 画像取得失敗")
        sys.exit(1)


if __name__ == "__main__":
    main()
