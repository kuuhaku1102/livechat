<?php
/**
 * Single Post Template
 * 個別記事ページ
 */

get_header();
?>

<main class="lcd-main lcd-single-post">
    <?php
    while (have_posts()) : the_post();
    ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class('lcd-article-single'); ?>>
            <header class="lcd-article-header">
                <h1 class="lcd-article-title"><?php the_title(); ?></h1>
                
                <div class="lcd-article-meta">
                    <time datetime="<?php echo get_the_date('c'); ?>">
                        <?php echo get_the_date(); ?>
                    </time>
                    <?php
                    $categories = get_the_category();
                    if ($categories) :
                        foreach ($categories as $category) :
                    ?>
                        <span class="lcd-article-category"><?php echo esc_html($category->name); ?></span>
                    <?php
                        endforeach;
                    endif;
                    ?>
                </div>
            </header>
            
            <?php if (has_post_thumbnail()) : ?>
                <div class="lcd-article-featured-image">
                    <?php the_post_thumbnail('large'); ?>
                </div>
            <?php endif; ?>
            
            <div class="lcd-article-content-wrapper">
                <?php the_content(); ?>
            </div>
            
            <footer class="lcd-article-footer">
                <?php
                // タグを表示
                $tags = get_the_tags();
                if ($tags) :
                ?>
                    <div class="lcd-article-tags">
                        <strong>タグ:</strong>
                        <?php
                        foreach ($tags as $tag) :
                        ?>
                            <a href="<?php echo get_tag_link($tag->term_id); ?>" class="lcd-tag">
                                <?php echo esc_html($tag->name); ?>
                            </a>
                        <?php
                        endforeach;
                        ?>
                    </div>
                <?php endif; ?>
                
                <div class="lcd-article-nav">
                    <?php
                    $prev_post = get_previous_post();
                    $next_post = get_next_post();
                    
                    if ($prev_post) :
                    ?>
                        <div class="lcd-prev-post">
                            <a href="<?php echo get_permalink($prev_post->ID); ?>">
                                ← <?php echo esc_html($prev_post->post_title); ?>
                            </a>
                        </div>
                    <?php endif; ?>
                    
                    <?php if ($next_post) : ?>
                        <div class="lcd-next-post">
                            <a href="<?php echo get_permalink($next_post->ID); ?>">
                                <?php echo esc_html($next_post->post_title); ?> →
                            </a>
                        </div>
                    <?php endif; ?>
                </div>
                
                <div class="lcd-back-to-blog">
                    <a href="<?php echo home_url('/blog/'); ?>">← コラム一覧に戻る</a>
                </div>
            </footer>
        </article>
    <?php
    endwhile;
    ?>
</main>

<?php get_footer(); ?>
