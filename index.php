<?php
/**
 * Live Chat Directory Theme v2
 * フロントページ：ライブプロフィールカード一覧
 */
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<div class="lcd-container">
    <header class="lcd-header">
        <h1><?php bloginfo( 'name' ); ?></h1>
        <p>ライブチャットプロフィールの最新一覧</p>
    </header>

    <?php
    // カード一覧を出力
    echo lcd_get_live_profiles_cards( 60 );
    ?>

    <div class="lcd-footer">
        &copy; <?php echo esc_html( date_i18n( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?>
    </div>
</div>
<?php wp_footer(); ?>
</body>
</html>
