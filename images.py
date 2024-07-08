class home:
    logo = "./data/insta_logo.png"
    logo_full = "./data/insta_logo_full.png"
    like = "./data/home_like.png"
    liked = "./data/home_liked.png"
    comment = "./data/home_comment_btn.png"
    mute = "./data/home_mute.png"
    un_mute = "./data/home_unmute.png"
    home_btn = "./data/home_button.png"
    on_home_btn = "./data/on_home_button.png"
    reload = "./data/reload.png"
    reload_close = "./data/refresh_close.png"
    reload_error = "./data/reload_error.png"


class reels:
    like = "./data/reels_like.png"
    liked = "./data/reels_liked.png"
    reels_btn = "./data/reels_button.png"
    on_reels_btn = "./data/on_reels_button.png"
    direct_btn = "./data/reels_direct_btn.png"
    suggest_lbl = "./data/reels_suggest_label.png"
    send_btn = "./data/reel_send_btn.png"
    write_msg_lbl =  "./data/reels_write_msg_label.png"

    #comments
    comment_btn =  "./data/reels_comment_btn.png"
    comment_label =  "./data/reel_comment_label.png"
    comment_like =  "./data/reel_comment_like.png"
    comment_close_btn =  "./data/reels_comment_close_btn.png"
    

class explore:
    explore_btn = "./data/explore_button.png"
    on_explore_btn = "./data/on_explore_button.png"
    next = "./data/explore_next.png"
    prev = "./data/explore_prev.png"
    comment_add = "./data/explore_comment_add.png"
    comment_like = "./data/explore_comment_like.png"
    comment_emoji = "./data/explore_comment_emoji.png"
    slider_close_btn =  "./data/slider_close_btn.png"

class carousel:
    next = "./data/carousel_next.png"
    prev = "./data/carousel_prev.png"
    comment_add = "./data/carousel_comment_add.png"
    comment_like = "./data/carousel_comment_like.png"
    comment_emoji = "./data/carousel_comment_emoji.png"
    close_btn =  "./data/carousel_close_btn.png"
    emoji_most_popular_lbl =  "./data/carousel_emoji_most_popular_lbl.png"
    three_dot =  "./data/carousel_three_dot.png"
    save_btn =  "./data/carousel_save_btn.png"
    follow = "./data/carousel_follow.png"

class comments_read:
    heart = "./data/comm/read_heart.png"
    fire  = "./data/comm/read_fire.png"
    laugh = "./data/comm/read_laugh.png"
    heart_eye = "./data/comm/read_heart_eye_face.png"

class comments_emoji:
    heart = "./data/comm/heart.png"
    fire = "./data/comm/fire.png"
    laugh = "./data/comm/laugh.png"
    heart_eye = "./data/comm/heart_eye_face.png"


class search:
    search_btn = "./data/search_btn.png"
    search_on_btn = "./data/search_on_btn.png"
    recent_label = "./data/search_recent_label.png"
    close_btn = "./data/search_close_btn.png"
    top_post_label = "./data/search_top_post_label.png"
    posts_label = "./data/search_posts_label.png"
    no_post_yet_label = "./data/search_no_post_yet_label.png"




READ_EMOJI = { "heart" : comments_read.heart, "fire" : comments_read.fire, "laugh" : comments_read.laugh,
    "heart_eye" : comments_read.heart_eye}

EMOJI_BTN = { "heart" : comments_emoji.heart, "fire" : comments_emoji.fire, "laugh" : comments_emoji.laugh,
            "heart_eye" : comments_emoji.heart_eye}

def get_read_emoji( except_emoji = list):
    find = {}
    for emoji in READ_EMOJI:
        if not emoji in except_emoji:
            find[emoji] = READ_EMOJI[emoji]
        
    return find