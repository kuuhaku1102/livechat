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
<?php wp_footer(); ?>
</body>
</html>
