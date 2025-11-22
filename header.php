<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="ライブチャットの遊び方、楽しみ方、安全な使い方など、初心者から上級者まで役立つ情報を提供。人気ライブチャットサイトの比較や、おすすめの女性プロフィールも掲載中。">
    <?php wp_head(); ?>
    
    <!-- Matomo -->
    <script>
      var _paq = window._paq = window._paq || [];
      /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="//matomo.s360.jp/";
        _paq.push(['setTrackerUrl', u+'matomo.php']);
        _paq.push(['setSiteId', '2']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <!-- End Matomo Code -->
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div class="lcd-container">
    <nav class="lcd-nav-top">
        <div class="lcd-nav-container">
            <div class="lcd-nav-logo">
                <a href="<?php echo home_url('/'); ?>"><?php bloginfo( 'name' ); ?></a>
            </div>
            
            <!-- ハンバーガーメニューボタン -->
            <button class="lcd-hamburger" id="hamburger-menu" aria-label="メニュー">
                <span></span>
                <span></span>
                <span></span>
            </button>
            
            <!-- メニュー -->
            <ul class="lcd-nav-menu" id="nav-menu">
                <li><a href="<?php echo home_url('/'); ?>"><span class="nav-icon">🏠</span>ホーム</a></li>
                <li><a href="<?php echo home_url('/blog/'); ?>"><span class="nav-icon">📝</span>コラム</a></li>
            </ul>
        </div>
    </nav>
    <header class="lcd-header">
        <h1><?php bloginfo( 'name' ); ?></h1>
        <p>ライブチャットプロフィールの最新一覧</p>
    </header>
