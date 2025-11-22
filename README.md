# livechat

## 概要
ライブチャットサイト向けのテーマです。スクレイピング対象となるルートドメインや、アフィリエイトリンク置換、ドメイン別のプロフィールフィルタなどをサポートしています。

## 現在のスクレイピングルートドメイン
- angel-live.com
- madamlive.tv
- j-live.tv
- chatpia.jp

## ルートドメイン単位のアフィリエイトリンク置換
- 管理画面の「アフィリエイトリンク」メニューで、`ルートドメイン` と `アフィリエイトリンク` の組み合わせを複数登録できます。
- サイト全体でリンクがクリックされた際に、登録済みのドメインに一致すればアフィリエイトリンクへ差し替えます（プラグインが出力するリンクも対象）。

### 使い方
1. WordPress 管理画面にログインし、左メニューの **アフィリエイトリンク** を開く。
2. 「ルートドメイン」に `example.com` などのドメインを入力し、「アフィリエイトリンク URL」に差し替え先を入力する。
3. 複数登録したい場合は「行を追加」で行を増やし、保存する。

## ドメインで女性プロフィールをフィルタリングするショートコード
ライブプロフィールを、特定のルートドメインを含む URL のデータだけに絞り込んで表示するショートコードを提供しています。

```php
[angel_sort domain="angel-live.com" limit="100"]
```

- `domain`（必須）: 抽出したいルートドメイン。`http(s)://` や `www.` を付けても自動で正規化されます。
- `limit`（任意）: 取得件数の上限。未指定時は 100 件。

プロフィールテーブル（`{$wpdb->prefix}live_profiles` または定数 `LPM_TABLE_NAME` で指定されたテーブル）が存在する場合のみ動作します。データが見つからない場合はメッセージを表示します。


## AI記事自動投稿システム

### 概要

AIによる記事の自動生成・投稿機能を備えたシステムです。GitHub Actionsで毎日定時実行され、完全自動で高品質なコンテンツを生成します。

### 主要機能

- **キーワード管理システム**: 3,456パターンのキーワード組み合わせ
- **AI記事生成**: GPT-4.1-miniでSEO最適化記事を生成（2,500文字以上）
- **アイキャッチ画像自動取得**: Unsplash/Pexels/Picsum対応
- **WordPress自動投稿**: REST API経由で自動公開
- **GitHub Actions定時実行**: 毎日午前10時（日本時間）

### ファイル構成

```
scripts/
├── keywords.json           # キーワードデータベース
├── keyword_manager.py      # キーワード管理
├── article_generator.py    # AI記事生成
├── image_fetcher.py        # 画像取得
├── wordpress_poster.py     # WordPress投稿
└── auto_post.py            # 統合メインスクリプト
```

### 使用方法

#### 手動実行

```bash
cd scripts
export OPENAI_API_KEY="your-api-key"
export WP_APP_PASSWORD="your-app-password"
python3 auto_post.py
```

#### GitHub Actionsで自動実行

1. GitHub Secretsを設定（詳細は `github_secrets_setup.md` 参照）
2. 毎日午前10時に自動実行
3. 手動実行も可能（Actionsタブから）

### 詳細ドキュメント

- **最終報告書**: `AI_AUTO_POST_FINAL_REPORT.md`
- **GitHub Secrets設定**: `github_secrets_setup.md`

---

## 更新履歴

### 2025-11-21

#### v2.3 - ライブチャットサイト別プロフィール表示追加
- 各ライブチャットサイト別にプロフィールカードを表示
  - エンジェルライブ（angel-live.com）
  - マダムライブ（madamlive.tv）
  - Jライブ（j-live.tv）
  - チャットピア（chatpia.jp）
- ドメイン別フィルタリングショートコード `[angel_sort]` を使用
- 各サイトごとに12件のプロフィールを表示

#### v2.2 - WordPress標準テーマ構造へリファクタリング
- index.phpをheader.php、footer.php、index.phpに分割
- WordPressテンプレート階層に準拠
- get_header()、get_footer()を使用
- Matomoトラッキングコードをheader.phpに統合

#### v2.1 - 詳細なSEOコンテンツ追加
- 6つの主要SEOセクションを追加
  1. ライブチャットとは？（概要）
  2. ライブチャットの料金体系
  3. 安全性とリスク
  4. よくある質問（FAQ）
  5. 主要ライブチャット比較表
  6. 初心者ガイド
- 可愛い装飾とアニメーション効果
- レスポンシブ対応の比較表
- FAQ形式のQ&A

#### v2.0 - デザインリニューアル
- プロフィールカードを一番上に配置
- ピンクグラデーション背景
- 絵文字アイコン追加
- バウンスアニメーション効果
- ホバーエフェクト

#### v1.2 - 画像ぼかし処理実装
- プロフィール画像にガウスぼかし（blur(8px)）を適用
- クロスブラウザ対応（-webkit-filter）

#### v1.1 - 初期SEOコンテンツ追加
- ライブチャットの遊び方
- ライブチャットの楽しみ方
- ライブチャットの魅力とは
- 安全にライブチャットを利用するために

#### v1.0 - 初期リリース
- プロフィールカード一覧表示機能
- 基本的なスタイリング

## ファイル構成

```
livechat/
├── header.php          # ヘッダーテンプレート
├── footer.php          # フッターテンプレート
├── index.php           # メインテンプレート
├── functions.php       # テーマ関数
├── style.css           # スタイルシート
└── README.md           # このファイル
```

## カスタマイズ

### プロフィール表示件数の変更

index.phpの各セクションで`[angel_sort]`ショートコードの`limit`属性を変更：

```php
<?php echo do_shortcode('[angel_sort domain="angel-live.com" limit="12"]'); ?>
```

### ぼかし効果の調整

style.cssの`.lcd-card img`セクションで調整：

```css
filter: blur(8px); /* 8pxを変更 */
```

### カラースキームの変更

style.cssの以下の変数を変更：

- メインカラー: `#ff6b9d`
- アクセントカラー: `#ffc0e0`
- 背景グラデーション: `linear-gradient(135deg, #ffeef8 0%, #fff5f7 50%, #f0f4ff 100%)`

## デプロイ

GitHub Actionsによる自動デプロイを使用しています。

- mainブランチへのpushで自動的にs360.jpサーバーにデプロイ
- デプロイ先: `public_html/s360.jp/wp-content/themes/live-chat-directory-theme-v2/`

## ライセンス

Proprietary

## 作者

InfinityDesign
