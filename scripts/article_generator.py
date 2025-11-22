#!/usr/bin/env python3
"""
AI記事生成スクリプト
OpenAI APIを使用して、SEO最適化されたHTML記事を自動生成する
"""

import os
import sys
from openai import OpenAI
from typing import Dict, Optional

class ArticleGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        記事生成器の初期化
        
        Args:
            api_key: OpenAI APIキー（指定しない場合は環境変数から取得）
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI APIキーが設定されていません")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4.1-mini"  # 指定されたモデル
    
    def generate_article(self, prompt: str, title: str) -> Dict[str, str]:
        """
        AIを使用して記事を生成する
        
        Args:
            prompt: AI用プロンプト
            title: 記事タイトル
        
        Returns:
            生成された記事の辞書（title, content, excerpt）
        """
        # システムプロンプト（記事の品質を向上させる）
        system_prompt = """あなたはプロのWebライターです。以下の要件を満たす記事を作成してください：

1. **文字数**: 2500文字以上
2. **形式**: SEOに最適化されたHTML形式
3. **文体**: 人間味のある自然で親しみやすい文章
4. **構成**: 
   - 導入部分（問題提起・読者の興味を引く）
   - 本文（見出しを使った構造化された内容）
   - まとめ（要点の整理と行動喚起）
5. **SEO対策**:
   - 適切な見出しタグ（h2, h3）の使用
   - キーワードの自然な配置
   - 読みやすい段落構成
6. **HTML要素**:
   - <h2>、<h3>で見出しを構造化
   - <p>で段落を分ける
   - <ul>、<ol>でリストを使用
   - <strong>で重要箇所を強調
7. **禁止事項**:
   - <!DOCTYPE>、<html>、<head>、<body>タグは不要
   - 記事本文のHTMLのみを出力
   - タイトルは含めない（別途指定）

実用的で、読者に価値を提供する内容にしてください。"""

        try:
            print(f"記事を生成中: {title}")
            print(f"モデル: {self.model}")
            
            # OpenAI APIを呼び出し
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # 創造性を高める
                max_tokens=4000,  # 十分な長さを確保
            )
            
            # 生成されたコンテンツを取得
            content = response.choices[0].message.content.strip()
            
            # 文字数をカウント（HTMLタグを除く）
            import re
            text_only = re.sub(r'<[^>]+>', '', content)
            char_count = len(text_only)
            
            print(f"記事生成完了: {char_count}文字")
            
            # 抜粋を生成（最初の段落から200文字程度）
            first_paragraph = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
            excerpt = ""
            if first_paragraph:
                excerpt_text = re.sub(r'<[^>]+>', '', first_paragraph.group(1))
                excerpt = excerpt_text[:200] + "..." if len(excerpt_text) > 200 else excerpt_text
            
            return {
                'title': title,
                'content': content,
                'excerpt': excerpt,
                'char_count': char_count
            }
        
        except Exception as e:
            print(f"エラー: 記事生成に失敗しました - {str(e)}")
            raise
    
    def generate_from_combination(self, combination: Dict) -> Dict[str, str]:
        """
        キーワード組み合わせから記事を生成する
        
        Args:
            combination: keyword_manager.pyから取得したキーワード組み合わせ
        
        Returns:
            生成された記事の辞書
        """
        from keyword_manager import KeywordManager
        
        manager = KeywordManager()
        title = manager.generate_title(combination)
        prompt = manager.generate_prompt(combination)
        
        return self.generate_article(prompt, title)


def main():
    """
    テスト用のメイン関数
    """
    # スクリプトのディレクトリに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # APIキーを確認
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        sys.exit(1)
    
    # キーワード組み合わせを取得
    from keyword_manager import KeywordManager
    manager = KeywordManager()
    combination = manager.get_unused_combination()
    
    if not combination:
        print("エラー: 未使用のキーワード組み合わせがありません")
        sys.exit(1)
    
    # 記事を生成
    generator = ArticleGenerator(api_key)
    article = generator.generate_from_combination(combination)
    
    print("\n=== 生成された記事 ===")
    print(f"タイトル: {article['title']}")
    print(f"文字数: {article['char_count']}")
    print(f"抜粋: {article['excerpt']}")
    print("\n--- コンテンツ（最初の500文字） ---")
    print(article['content'][:500] + "...")
    
    # テスト用にファイルに保存
    output_file = "test_article.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"<h1>{article['title']}</h1>\n")
        f.write(article['content'])
    
    print(f"\n記事を {output_file} に保存しました")


if __name__ == "__main__":
    main()
