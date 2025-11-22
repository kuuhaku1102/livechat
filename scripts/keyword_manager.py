#!/usr/bin/env python3
"""
キーワード管理システム
記事の重複を防ぎ、多様なコンテンツを生成するためのキーワード選択・管理スクリプト
"""

import json
import random
import os
from typing import Dict, List, Tuple, Optional

class KeywordManager:
    def __init__(self, keywords_file: str = "keywords.json"):
        """
        キーワードマネージャーの初期化
        
        Args:
            keywords_file: キーワードデータファイルのパス
        """
        self.keywords_file = keywords_file
        self.data = self._load_keywords()
    
    def _load_keywords(self) -> Dict:
        """
        キーワードデータをJSONファイルから読み込む
        
        Returns:
            キーワードデータの辞書
        """
        if not os.path.exists(self.keywords_file):
            raise FileNotFoundError(f"キーワードファイルが見つかりません: {self.keywords_file}")
        
        with open(self.keywords_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_keywords(self) -> None:
        """
        キーワードデータをJSONファイルに保存する
        """
        with open(self.keywords_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_unused_combination(self) -> Optional[Dict]:
        """
        未使用のキーワード組み合わせを取得する
        
        Returns:
            キーワード組み合わせの辞書、または None（すべて使用済みの場合）
        """
        main_keywords = self.data['main_keywords']
        sub_keywords = self.data['sub_keywords']
        article_types = self.data['article_types']
        used_combinations = self.data['used_combinations']
        
        # すべての可能な組み合わせを生成
        all_combinations = []
        for main_kw in main_keywords:
            for sub_kw in sub_keywords:
                for article_type in article_types:
                    combination = {
                        'main_keyword': main_kw,
                        'sub_keyword': sub_kw,
                        'article_type': article_type['type'],
                        'title_pattern': article_type['title_pattern'],
                        'prompt_template': article_type['prompt_template']
                    }
                    
                    # 使用済みかチェック
                    combination_key = f"{main_kw}|{sub_kw}|{article_type['type']}"
                    if combination_key not in used_combinations:
                        all_combinations.append((combination_key, combination))
        
        if not all_combinations:
            print("警告: すべてのキーワード組み合わせが使用済みです")
            return None
        
        # ランダムに1つ選択
        selected_key, selected_combination = random.choice(all_combinations)
        
        # 使用済みとしてマーク
        self.data['used_combinations'].append(selected_key)
        self._save_keywords()
        
        return selected_combination
    
    def generate_title(self, combination: Dict) -> str:
        """
        キーワード組み合わせからタイトルを生成する
        
        Args:
            combination: キーワード組み合わせの辞書
        
        Returns:
            生成されたタイトル
        """
        title_pattern = combination['title_pattern']
        title = title_pattern.format(
            main_keyword=combination['main_keyword'],
            sub_keyword=combination['sub_keyword']
        )
        return title
    
    def generate_prompt(self, combination: Dict) -> str:
        """
        キーワード組み合わせからAI用プロンプトを生成する
        
        Args:
            combination: キーワード組み合わせの辞書
        
        Returns:
            生成されたプロンプト
        """
        prompt_template = combination['prompt_template']
        prompt = prompt_template.format(
            main_keyword=combination['main_keyword'],
            sub_keyword=combination['sub_keyword']
        )
        return prompt
    
    def get_stats(self) -> Dict:
        """
        キーワード使用状況の統計を取得する
        
        Returns:
            統計情報の辞書
        """
        total_combinations = (
            len(self.data['main_keywords']) *
            len(self.data['sub_keywords']) *
            len(self.data['article_types'])
        )
        used_combinations = len(self.data['used_combinations'])
        remaining_combinations = total_combinations - used_combinations
        
        return {
            'total_combinations': total_combinations,
            'used_combinations': used_combinations,
            'remaining_combinations': remaining_combinations,
            'usage_percentage': (used_combinations / total_combinations * 100) if total_combinations > 0 else 0
        }
    
    def reset_used_combinations(self) -> None:
        """
        使用済みキーワード組み合わせをリセットする
        注意: この操作は慎重に行ってください
        """
        self.data['used_combinations'] = []
        self._save_keywords()
        print("使用済みキーワード組み合わせをリセットしました")


def main():
    """
    テスト用のメイン関数
    """
    # スクリプトのディレクトリに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # キーワードマネージャーを初期化
    manager = KeywordManager()
    
    # 統計情報を表示
    stats = manager.get_stats()
    print("=== キーワード管理システム ===")
    print(f"総組み合わせ数: {stats['total_combinations']}")
    print(f"使用済み: {stats['used_combinations']}")
    print(f"残り: {stats['remaining_combinations']}")
    print(f"使用率: {stats['usage_percentage']:.2f}%")
    print()
    
    # 未使用の組み合わせを取得
    combination = manager.get_unused_combination()
    
    if combination:
        print("=== 選択されたキーワード組み合わせ ===")
        print(f"メインキーワード: {combination['main_keyword']}")
        print(f"サブキーワード: {combination['sub_keyword']}")
        print(f"記事タイプ: {combination['article_type']}")
        print()
        
        # タイトルとプロンプトを生成
        title = manager.generate_title(combination)
        prompt = manager.generate_prompt(combination)
        
        print(f"生成されたタイトル:\n{title}")
        print()
        print(f"生成されたプロンプト:\n{prompt}")
    else:
        print("すべてのキーワード組み合わせが使用済みです")


if __name__ == "__main__":
    main()
