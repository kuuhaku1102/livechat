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
