<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * テーマ用スタイルの読み込み
 */
function lcd_theme_enqueue_styles() {
    wp_enqueue_style( 'lcd-theme-style', get_stylesheet_uri(), array(), '2.0' );
}
add_action( 'wp_enqueue_scripts', 'lcd_theme_enqueue_styles' );

/**
 * ルートドメイン単位のアフィリエイトリンク設定を取得
 *
 * @return array
 */
function lcd_get_affiliate_domain_links() {
    $saved = get_option( 'lcd_affiliate_domain_links', array() );

    if ( ! is_array( $saved ) ) {
        return array();
    }

    $normalized = array();

    foreach ( $saved as $row ) {
        if ( empty( $row['domain'] ) || empty( $row['affiliate'] ) ) {
            continue;
        }

        $domain    = strtolower( trim( $row['domain'] ) );
        $affiliate = esc_url_raw( $row['affiliate'] );

        // 先頭の www. は無視して扱う
        $domain = preg_replace( '/^www\./', '', $domain );

        if ( ! empty( $domain ) && ! empty( $affiliate ) ) {
            $normalized[ $domain ] = $affiliate;
        }
    }

    return $normalized;
}

/**
 * 管理画面: アフィリエイトリンク設定保存
 */
function lcd_handle_affiliate_domain_save() {
    if ( ! isset( $_POST['lcd_affiliate_domain_nonce'] ) ) {
        return;
    }

    if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['lcd_affiliate_domain_nonce'] ) ), 'lcd_affiliate_domain_save' ) ) {
        return;
    }

    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    $domains   = isset( $_POST['lcd_affiliate_domain'] ) ? (array) $_POST['lcd_affiliate_domain'] : array();
    $links     = isset( $_POST['lcd_affiliate_link'] ) ? (array) $_POST['lcd_affiliate_link'] : array();
    $sanitized = array();

    $count = max( count( $domains ), count( $links ) );

    for ( $i = 0; $i < $count; $i++ ) {
        $domain_input = isset( $domains[ $i ] ) ? sanitize_text_field( wp_unslash( $domains[ $i ] ) ) : '';
        $link_input   = isset( $links[ $i ] ) ? esc_url_raw( wp_unslash( $links[ $i ] ) ) : '';

        if ( empty( $domain_input ) || empty( $link_input ) ) {
            continue;
        }

        $sanitized[] = array(
            'domain'    => $domain_input,
            'affiliate' => $link_input,
        );
    }

    update_option( 'lcd_affiliate_domain_links', $sanitized );

    add_settings_error( 'lcd_affiliate_domains', 'lcd_affiliate_domains_updated', 'アフィリエイトリンク設定を保存しました。', 'updated' );
}
add_action( 'admin_init', 'lcd_handle_affiliate_domain_save' );

/**
 * 管理画面: アフィリエイトリンク設定ページ
 */
function lcd_render_affiliate_domain_page() {
    $mappings = lcd_get_affiliate_domain_links();
    settings_errors( 'lcd_affiliate_domains' );
    ?>
    <div class="wrap">
        <h1>アフィリエイトリンク設定</h1>
        <p>ルートドメインごとに置き換えるアフィリエイトリンクを管理します。サイト内のリンクはクリック時に設定したアフィリエイトリンクへ書き換えられます。</p>
        <form method="post">
            <?php wp_nonce_field( 'lcd_affiliate_domain_save', 'lcd_affiliate_domain_nonce' ); ?>
            <table class="widefat striped" style="max-width: 900px;">
                <thead>
                    <tr>
                        <th style="width: 30%;">ルートドメイン（例: example.com）</th>
                        <th>アフィリエイトリンク URL</th>
                    </tr>
                </thead>
                <tbody id="lcd-affiliate-domain-rows">
                    <?php if ( ! empty( $mappings ) ) : ?>
                        <?php foreach ( $mappings as $domain => $affiliate ) : ?>
                            <tr>
                                <td><input type="text" name="lcd_affiliate_domain[]" value="<?php echo esc_attr( $domain ); ?>" class="regular-text" /></td>
                                <td><input type="url" name="lcd_affiliate_link[]" value="<?php echo esc_url( $affiliate ); ?>" class="regular-text" style="width:100%;" /></td>
                            </tr>
                        <?php endforeach; ?>
                    <?php else : ?>
                        <tr>
                            <td><input type="text" name="lcd_affiliate_domain[]" value="" class="regular-text" /></td>
                            <td><input type="url" name="lcd_affiliate_link[]" value="" class="regular-text" style="width:100%;" /></td>
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
            <p>
                <button type="button" class="button" id="lcd-affiliate-add-row">行を追加</button>
                <input type="submit" class="button button-primary" value="保存する" />
            </p>
        </form>
    </div>
    <script>
        (function() {
            const addRowButton = document.getElementById('lcd-affiliate-add-row');
            const container = document.getElementById('lcd-affiliate-domain-rows');

            if (!addRowButton || !container) return;

            addRowButton.addEventListener('click', function() {
                const row = document.createElement('tr');
                row.innerHTML = '<td><input type="text" name="lcd_affiliate_domain[]" class="regular-text" /></td>' +
                    '<td><input type="url" name="lcd_affiliate_link[]" class="regular-text" style="width:100%;" /></td>';
                container.appendChild(row);
            });
        })();
    </script>
    <?php
}

/**
 * 管理画面メニュー登録
 */
function lcd_register_affiliate_domain_menu() {
    add_menu_page(
        'アフィリエイトリンク設定',
        'アフィリエイトリンク',
        'manage_options',
        'lcd-affiliate-domains',
        'lcd_render_affiliate_domain_page',
        'dashicons-admin-links',
        58
    );
}
add_action( 'admin_menu', 'lcd_register_affiliate_domain_menu' );

/**
 * プロフィール一覧を取得してカードHTMLを返す
 *
 * @param int $limit 表示件数
 * @return string HTML
 */
function lcd_get_live_profiles_cards( $limit = 60 ) {
    global $wpdb;

    // プラグイン側で定数が定義されていればそれを優先
    if ( defined( 'LPM_TABLE_NAME' ) ) {
        $table = LPM_TABLE_NAME;
    } else {
        // フォールバック（プレフィックス + live_profiles）
        $table = $wpdb->prefix . 'live_profiles';
    }

    $limit = absint( $limit );
    if ( $limit <= 0 ) {
        $limit = 60;
    }

    // テーブル存在チェック（無ければ何も表示しない）
    $table_exists = $wpdb->get_var( $wpdb->prepare(
        "SHOW TABLES LIKE %s",
        $table
    ) );

    if ( $table_exists !== $table ) {
        return '<p style="text-align:center;color:#999;">プロフィールテーブルが見つかりませんでした。</p>';
    }

    // データ取得
    $rows = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT samune, url, oneword
             FROM {$table}
             ORDER BY created_at DESC
             LIMIT %d",
            $limit
        )
    );

    if ( ! $rows ) {
        return '<p style="text-align:center;color:#999;">現在表示できるプロフィールがありません。</p>';
    }

    ob_start();
    ?>
    <div class="lcd-grid">
        <?php foreach ( $rows as $row ) : 
            $url     = ! empty( $row->url ) ? esc_url( $row->url ) : '#';
            $samune  = ! empty( $row->samune ) ? esc_url( $row->samune ) : '';
            $oneword = ! empty( $row->oneword ) ? esc_html( $row->oneword ) : '';
        ?>
            <a class="lcd-card" href="<?php echo $url; ?>" target="_blank" rel="noopener">
                <?php if ( $samune ) : ?>
                    <img src="<?php echo $samune; ?>" alt="">
                <?php else : ?>
                    <div style="width:100%;height:220px;background:#f1f1f5;"></div>
                <?php endif; ?>
                <div class="lcd-oneword">
                    <?php echo $oneword ? $oneword : '・・・'; ?>
                </div>
            </a>
        <?php endforeach; ?>
    </div>
    <?php
    return ob_get_clean();
}

/**
 * フロントエンド: クリック時にアフィリエイトリンクへ書き換えるスクリプトを追加
 */
function lcd_enqueue_affiliate_rewriter_script() {
    $mappings = lcd_get_affiliate_domain_links();

    if ( empty( $mappings ) ) {
        return;
    }

    wp_register_script( 'lcd-affiliate-rewriter', '', array(), '1.0', true );

    $script = '(function(){'
        . 'const mappings=' . wp_json_encode( $mappings ) . ';'
        . 'const normalizeHost=(host)=>host.replace(/^www\./i,"").toLowerCase();'
        . 'const resolveAffiliate=(href)=>{try{const url=new URL(href,document.baseURI);const host=normalizeHost(url.hostname);return mappings[host]||null;}catch(e){return null;}};'
        . 'document.addEventListener("click",function(event){if(event.defaultPrevented){return;}const link=event.target.closest("a[href]");if(!link){return;}const affiliate=resolveAffiliate(link.getAttribute("href"));if(!affiliate){return;}link.setAttribute("data-lcd-original-href",link.getAttribute("href"));link.setAttribute("href",affiliate);},true);'
        . '})();';

    wp_add_inline_script( 'lcd-affiliate-rewriter', $script );
    wp_enqueue_script( 'lcd-affiliate-rewriter' );
}
add_action( 'wp_enqueue_scripts', 'lcd_enqueue_affiliate_rewriter_script', 20 );
