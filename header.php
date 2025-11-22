<?php
/**
 * Live Chat Directory Theme v2
 * Header Template
 */
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="ライブチャットの遊び方、料金体系、安全性、主要サイト比較まで徹底解説。初心者にもわかりやすく、人気のライブチャット女性プロフィール一覧も掲載中。">
    <!-- Matomo -->
<script>
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="//matomo.sakura.ne.jp/matomo/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '7']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<!-- End Matomo Code -->

    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div class="lcd-container">
    <nav class="lcd-nav-top">
        <div class="lcd-nav-container">
            <div class="lcd-nav-logo">
                <a href="<?php echo home_url('/'); ?>"><?php bloginfo( 'name' ); ?></a>
            </div>
            <ul class="lcd-nav-menu">
                <li><a href="<?php echo home_url('/'); ?>"><span class="nav-icon">🏠</span>ホーム</a></li>
                <li><a href="<?php echo home_url('/blog/'); ?>"><span class="nav-icon">📝</span>コラム</a></li>
            </ul>
        </div>
    </nav>
    <header class="lcd-header">
        <h1><?php bloginfo( 'name' ); ?></h1>
        <p>ライブチャットプロフィールの最新一覧</p>
    </header>
