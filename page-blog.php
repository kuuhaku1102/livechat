<?php
/**
 * Template Name: ブログ記事一覧
 * Description: コラム記事の一覧ページ
 */

get_header();
?>

<main class="lcd-main lcd-blog-page">
    <div class="lcd-blog-header">
        <h1>コラム</h1>
        <p>ライブチャットに関する役立つ情報をお届けします</p>
    </div>

    <div class="lcd-blog-list">
        <?php
        // コラムカテゴリーの記事を取得
        $paged = (get_query_var('paged')) ? get_query_var('paged') : 1;
        
        // 「コラム」カテゴリーを取得（存在しない場合は全記事を表示）
        $column_category = get_category_by_slug('column');
        if (!$column_category) {
            // スラッグがない場合、名前で検索
            $column_category = get_term_by('name', 'コラム', 'category');
        }
        
        $args = array(
            'post_type' => 'post',
            'posts_per_page' => 12,
            'paged' => $paged,
            'orderby' => 'date',
            'order' => 'DESC'
        );
        
        // カテゴリーが存在する場合のみフィルタリング
        if ($column_category) {
            $args['cat'] = $column_category->term_id;
        }
        
        $blog_query = new WP_Query($args);
        
        if ($blog_query->have_posts()) :
            while ($blog_query->have_posts()) : $blog_query->the_post();
        ?>
            <article class="lcd-blog-item">
                <?php if (has_post_thumbnail()) : ?>
                    <div class="lcd-blog-thumbnail">
                        <a href="<?php the_permalink(); ?>">
                            <?php the_post_thumbnail('medium'); ?>
                        </a>
                    </div>
                <?php endif; ?>
                
                <div class="lcd-blog-content">
                    <h2 class="lcd-blog-title">
                        <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                    </h2>
                    
                    <div class="lcd-blog-meta">
                        <time datetime="<?php echo get_the_date('c'); ?>">
                            <?php echo get_the_date(); ?>
                        </time>
                        <?php
                        $categories = get_the_category();
                        if ($categories) :
                            foreach ($categories as $category) :
                        ?>
                            <span class="lcd-blog-category"><?php echo esc_html($category->name); ?></span>
                        <?php
                            endforeach;
                        endif;
                        ?>
                    </div>
                    
                    <div class="lcd-blog-excerpt">
                        <?php
                        if (has_excerpt()) {
                            the_excerpt();
                        } else {
                            echo wp_trim_words(get_the_content(), 100, '...');
                        }
                        ?>
                    </div>
                    
                    <a href="<?php the_permalink(); ?>" class="lcd-blog-readmore">続きを読む →</a>
                </div>
            </article>
        <?php
            endwhile;
            
            // ページネーション
            if ($blog_query->max_num_pages > 1) :
        ?>
            <div class="lcd-pagination">
                <?php
                echo paginate_links(array(
                    'total' => $blog_query->max_num_pages,
                    'current' => $paged,
                    'prev_text' => '← 前へ',
                    'next_text' => '次へ →',
                ));
                ?>
            </div>
        <?php
            endif;
            
            wp_reset_postdata();
        else :
        ?>
            <p class="lcd-no-posts">まだ記事がありません。</p>
        <?php
        endif;
        ?>
    </div>
</main>

<?php get_footer(); ?>
