<?php
/**
 * Live Chat Directory Theme v2
 * Footer Template
 */
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>
    <div class="lcd-footer">
        &copy; <?php echo esc_html( date_i18n( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?>
    </div>
</div><!-- .lcd-container -->

<script>
// ハンバーガーメニューのトグル
(function() {
    const hamburger = document.getElementById('hamburger-menu');
    const navMenu = document.getElementById('nav-menu');
    
    if (!hamburger || !navMenu) return;
    
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // メニュー項目をクリックしたら閉じる
    const menuLinks = navMenu.querySelectorAll('a');
    menuLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
})();
</script>

<?php wp_footer(); ?>
</body>
</html>
