import os
import re
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIG & AUTHENTIC INSTAGRAM LIGHT MODE CSS
# ==============================================================================
st.set_page_config(
    page_title="Instagram",
    page_icon="📸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Grand+Hotel&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #EFEFEF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Mobile Phone Frame (430px centered) */
.block-container {
    max-width: 430px !important;
    background-color: #FFFFFF;
    border: 1px solid #DBDBDB;
    border-radius: 30px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
    padding: 12px 14px 20px 14px !important;
    margin-top: 16px !important;
    margin-bottom: 24px !important;
}

/* Instagram Top Header */
.ig-logo {
    font-family: 'Grand Hotel', cursive;
    font-size: 32px;
    font-weight: 400;
    color: #000000;
    text-align: center;
    line-height: 1.1;
    margin-top: 2px;
}

/* Stories Row */
.stories-row {
    display: flex;
    gap: 14px;
    overflow-x: auto;
    padding: 8px 2px 12px 2px;
    border-bottom: 1px solid #EFEFEF;
    margin-bottom: 10px;
    scrollbar-width: none;
}
.stories-row::-webkit-scrollbar { display: none; }
.story-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 64px;
}
.story-ring {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    padding: 2.5px;
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}
.story-ring-plain {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    padding: 2px;
    background: #E0E0E0;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}
.story-inner {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: #F4F4F4;
    border: 2.5px solid #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 16px;
    color: #333333;
}
.story-plus-badge {
    position: absolute;
    bottom: 0px;
    right: 0px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #000000;
    color: #FFFFFF;
    border: 2px solid #FFFFFF;
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
}
.story-name {
    font-size: 11px;
    color: #262626;
    margin-top: 5px;
    max-width: 64px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: center;
}

/* Post Header */
.post-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 2px 8px 2px;
}
.post-user-info { display: flex; align-items: center; }
.post-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    padding: 2px;
    background: linear-gradient(45deg, #f09433, #dc2743, #bc1888);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 12px;
    margin-right: 10px;
}
.post-username {
    font-weight: 600;
    font-size: 13.5px;
    color: #000000;
    line-height: 1.2;
}
.post-location { font-size: 11.5px; color: #737373; }

/* Missing Photo Placeholder */
.img-placeholder {
    width: 100%;
    height: 300px;
    background-color: #F7F7F7;
    border: 1.5px dashed #CCCCCC;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #8E8E8E;
    font-size: 13px;
    text-align: center;
    margin-bottom: 6px;
}

/* Caption & Lemmatise Box */
.post-caption {
    font-size: 13.5px;
    line-height: 1.45;
    color: #000000;
    margin: 2px 0 4px 0;
}
.lemma-output {
    background-color: #F8F9FA;
    border-left: 3px solid #262626;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 6px 0 8px 0;
    font-size: 13px;
    line-height: 1.5;
    color: #262626;
}
.lemma-tag {
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    color: #737373;
    letter-spacing: 0.4px;
    margin-bottom: 2px;
}
.post-divider {
    border-bottom: 1px solid #EFEFEF;
    margin: 10px 0 12px 0;
}

/* Make Streamlit buttons look like clean borderless IG icons / text links */
div.stButton > button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #000000 !important;
    padding: 2px 4px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    min-height: 0px !important;
    height: auto !important;
}
div.stButton > button:hover {
    color: #737373 !important;
    background-color: transparent !important;
}

/* Bottom Navigation Bar Divider */
.bottom-nav-line {
    border-top: 1px solid #DBDBDB;
    margin-top: 10px;
    padding-top: 6px;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. BACKEND PLACEHOLDER (Replace with your teammate's real NLP functions later)
# ==============================================================================
MOCK_SLANG_DICT = {
    "xleh": "tidak boleh", "takleh": "tidak boleh", "mcm": "macam",
    "dgn": "dengan", "yg": "yang", "utk": "untuk", "sgt": "sangat",
    "mmg": "memang", "tggu": "tunggu", "smlm": "semalam", "arini": "hari ini",
    "saye": "saya", "nak": "hendak", "tak": "tidak", "dah": "sudah",
    "kat": "dekat", "je": "sahaja", "tapi": "tetapi", "pls": "please",
    "tmr": "tomorrow", "gonna": "going to", "dunno": "do not know",
    "japgi": "sekejap lagi", "skali": "sekali",
}

def lemmatise_word(word: str) -> str:
    w = word.lower().strip()
    w = re.sub(r"([a-z]+)2$", r"\1", w)
    w = re.sub(r"(.)\1{2,}", r"\1", w)
    if w in MOCK_SLANG_DICT:
        return MOCK_SLANG_DICT[w]
    if w.endswith("ing") and len(w) > 4:
        return w[:-3]
    if w.startswith("me") and len(w) > 5:
        return w[2:]
    return w

def lemmatise_sentence(text: str) -> str:
    tokens = re.findall(r"[a-zA-Z0-9]+|[^\w\s]", text)
    lemmas = [lemmatise_word(t) if re.match(r"^[a-zA-Z0-9]+$", t) else t for t in tokens]
    return " ".join(lemmas)


# ==============================================================================
# 3. SESSION STATE
# ==============================================================================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "home"

if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "id": 1,
            "username": "jiemin_eats",
            "avatar": "JM",
            "location": "Setapak, Kuala Lumpur",
            "image": "images/post1.jpg",
            "caption": "Saye xleh nak pergi shopping mall arini sebab tengah makan2 kat rumah, laparrrr gila!",
            "likes": 149,
            "liked": False,
            "reposts": 3,
            "shares": 34,
            "saved": False,
            "show_lemma": False,
            "show_comments": False,
            "time": "5 hours ago",
            "comments": [
                {"user": "weihen_k", "text": "Mmg sedap gila weh, tggu aku datang makan2 skali!", "show_lemma": False},
                {"user": "yoongkeat", "text": "Pls save some for me tmr, dunno why suddenly hungryyyy.", "show_lemma": False},
            ],
        },
        {
            "id": 2,
            "username": "kl_foodie_daily",
            "avatar": "KF",
            "location": "Petaling Jaya, Selangor",
            "image": "images/post2.jpg",
            "caption": "Good morning! Sarapan apa ye arini? Ikut je member nanti. I am super hungryyyy!",
            "likes": 94,
            "liked": False,
            "reposts": 2,
            "shares": 18,
            "saved": False,
            "show_lemma": False,
            "show_comments": False,
            "time": "8 hours ago",
            "comments": [
                {"user": "aisyah_my", "text": "Jom pergi mamak dekat office, roti canai dgn teh tarik!", "show_lemma": False},
            ],
        },
        {
            "id": 3,
            "username": "malaysia_vibes",
            "avatar": "MV",
            "location": "Bukit Bintang, KL",
            "image": "images/post3.jpg",
            "caption": "Everytime lapar je padahal baru makan nasi. Now scrolling food delivery nak order apa japgi.",
            "likes": 215,
            "liked": False,
            "reposts": 5,
            "shares": 41,
            "saved": False,
            "show_lemma": False,
            "show_comments": False,
            "time": "1 day ago",
            "comments": [
                {"user": "daniel_tan", "text": "Same bro, smlm pun order supper pukul 1 pagi haha.", "show_lemma": False},
            ],
        },
    ]


# ==============================================================================
# 4. INSTAGRAM TOP BAR (+   Instagram   ♡)
# ==============================================================================
t1, t2, t3 = st.columns([1, 4, 1])
with t1:
    if st.button("＋", key="top_plus", help="Create Post"):
        st.session_state.active_tab = "create"
        st.rerun()
with t2:
    st.markdown('<div class="ig-logo">Instagram</div>', unsafe_allow_html=True)
with t3:
    st.markdown('<div style="text-align:right; font-size:22px; padding-top:4px; color:#000;">♡</div>', unsafe_allow_html=True)


# ==============================================================================
# 5. TAB 1: HOME FEED
# ==============================================================================
if st.session_state.active_tab == "home":
    # Purely decorative IG Stories bar (no indentation = no code-block bug!)
    stories = [
        ("Your story", "JM", True),
        ("britnchan", "BC", False),
        ("bell_lh", "BL", False),
        ("_yywenc", "YW", False),
        ("kl_food", "KF", False),
        ("tarumt", "TR", False),
    ]
    stories_html = '<div class="stories-row">'
    for name, initials, is_you in stories:
        if is_you:
            stories_html += (
                f'<div class="story-item">'
                f'<div class="story-ring-plain"><div class="story-inner">{initials}</div>'
                f'<div class="story-plus-badge">+</div></div>'
                f'<div class="story-name">{name}</div></div>'
            )
        else:
            stories_html += (
                f'<div class="story-item">'
                f'<div class="story-ring"><div class="story-inner">{initials}</div></div>'
                f'<div class="story-name">{name}</div></div>'
            )
    stories_html += '</div>'
    st.markdown(stories_html, unsafe_allow_html=True)

    # Scrollable Posts Feed
    for post in st.session_state.posts:
        pid = post["id"]

        # Post Header
        header_html = (
            f'<div class="post-header">'
            f'<div class="post-user-info">'
            f'<div class="post-avatar">{post["avatar"]}</div>'
            f'<div><div class="post-username">{post["username"]}</div>'
            f'<div class="post-location">{post["location"]}</div></div></div>'
            f'<div style="color:#000; font-weight:700; font-size:16px;">⋯</div></div>'
        )
        st.markdown(header_html, unsafe_allow_html=True)

        # Post Image
        if os.path.exists(post["image"]):
            st.image(post["image"], use_container_width=True)
        else:
            placeholder_html = (
                f'<div class="img-placeholder">'
                f'<div style="font-size:26px; margin-bottom:4px;">🖼️</div>'
                f'<div><b>Photo Placeholder</b></div>'
                f'<div style="font-size:11px; margin-top:4px;">Put your photo at: <code>{post["image"]}</code></div>'
                f'</div>'
            )
            st.markdown(placeholder_html, unsafe_allow_html=True)

        # Action Bar (Like, Comment, Repost, Share, Bookmark — matching IG layout)
        a1, a2, a3, a4, a5 = st.columns([1.3, 1.1, 1.1, 1.2, 1.0])
        with a1:
            heart_icon = "❤️" if post["liked"] else "♡"
            if st.button(f"{heart_icon} {post['likes']}", key=f"like_{pid}"):
                post["liked"] = not post["liked"]
                post["likes"] += 1 if post["liked"] else -1
                st.rerun()
        with a2:
            if st.button(f"💬 {len(post['comments'])}", key=f"cm_btn_{pid}"):
                post["show_comments"] = not post["show_comments"]
                st.rerun()
        with a3:
            if st.button(f"⇄ {post['reposts']}", key=f"repost_{pid}"):
                post["reposts"] += 1
                st.rerun()
        with a4:
            st.button(f"➤ {post['shares']}", key=f"share_{pid}")
        with a5:
            bm_icon = "🔖" if post["saved"] else "🏷️"
            if st.button(bm_icon, key=f"save_{pid}"):
                post["saved"] = not post["saved"]
                st.rerun()

        # Caption
        st.markdown(
            f'<div class="post-caption"><b>{post["username"]}</b> {post["caption"]}</div>',
            unsafe_allow_html=True,
        )

        # Timestamp + "Lemmatise" button (replacing IG's "See translation")
        meta_c1, meta_c2 = st.columns([1.1, 2.5])
        with meta_c1:
            st.markdown(
                f'<div style="font-size:12px; color:#737373; padding-top:4px;">{post["time"]} ·</div>',
                unsafe_allow_html=True,
            )
        with meta_c2:
            btn_label = "See Original" if post["show_lemma"] else "Lemmatise"
            if st.button(btn_label, key=f"lemma_post_{pid}"):
                post["show_lemma"] = not post["show_lemma"]
                st.rerun()

        # Show Lemmatised Output when clicked
        if post["show_lemma"]:
            lemma_res = lemmatise_sentence(post["caption"])
            st.markdown(
                f'<div class="lemma-output"><div class="lemma-tag">Lemmatised</div>{lemma_res}</div>',
                unsafe_allow_html=True,
            )

        # Comments Section (toggled by clicking the comment icon)
        if post["show_comments"]:
            st.markdown('<div style="font-size:12px; font-weight:600; color:#737373; margin:6px 0;">Comments</div>', unsafe_allow_html=True)
            for idx, cm in enumerate(post["comments"]):
                c_txt, c_btn = st.columns([3.2, 1.2])
                with c_txt:
                    st.markdown(
                        f'<div style="font-size:13px; color:#000; padding-top:3px;"><b>{cm["user"]}</b> {cm["text"]}</div>',
                        unsafe_allow_html=True,
                    )
                with c_btn:
                    cm_label = "Hide" if cm["show_lemma"] else "Lemmatise"
                    if st.button(cm_label, key=f"cm_lem_{pid}_{idx}"):
                        cm["show_lemma"] = not cm["show_lemma"]
                        st.rerun()
                if cm["show_lemma"]:
                    cm_lemma = lemmatise_sentence(cm["text"])
                    st.markdown(
                        f'<div class="lemma-output"><div class="lemma-tag">Lemmatised</div>{cm_lemma}</div>',
                        unsafe_allow_html=True,
                    )

            with st.form(key=f"add_cm_{pid}", clear_on_submit=True):
                new_cm = st.text_input("Comment", placeholder="Add a comment...", label_visibility="collapsed")
                if st.form_submit_button("Post") and new_cm.strip():
                    post["comments"].append({"user": "you_demo", "text": new_cm.strip(), "show_lemma": False})
                    st.rerun()

        st.markdown('<div class="post-divider"></div>', unsafe_allow_html=True)


# ==============================================================================
# 6. TAB 2: WORD LEMMATISER (Search Icon in Bottom Bar)
# ==============================================================================
elif st.session_state.active_tab == "word":
    st.markdown('<div style="font-size:16px; font-weight:700; margin:10px 0 4px 0;">Word Lemmatiser</div>', unsafe_allow_html=True)
    st.caption("Enter any Malay, English, or Bahasa Rojak word to get its root form.")
    word_input = st.text_input("Search word", placeholder="e.g., xleh, laparrrr, makan2, running", label_visibility="collapsed")
    if word_input and word_input.strip():
        root = lemmatise_word(word_input)
        st.markdown(
            f'<div class="lemma-output" style="text-align:center; padding:16px;">'
            f'<span style="font-size:18px; font-weight:700;">{word_input.strip()}</span>'
            f'<span style="font-size:18px; margin:0 10px;">➔</span>'
            f'<span style="font-size:18px; font-weight:700; color:#0095F6;">{root}</span>'
            f'<div style="font-size:11px; color:#737373; margin-top:4px;">Root Form (Lemma)</div></div>',
            unsafe_allow_html=True,
        )


# ==============================================================================
# 7. TAB 3: CREATE POST (+ Icon in Top Left)
# ==============================================================================
elif st.session_state.active_tab == "create":
    st.markdown('<div style="font-size:16px; font-weight:700; margin:10px 0 4px 0;">New Post</div>', unsafe_allow_html=True)
    with st.form("new_post_form"):
        username = st.text_input("Username", value="malaysia_student")
        location = st.text_input("Location", value="Kuala Lumpur, Malaysia")
        caption = st.text_area("Write a caption...", placeholder="Type a Bahasa Rojak caption...")
        uploaded_img = st.file_uploader("Upload Photo (optional)", type=["jpg", "jpeg", "png"])
        if st.form_submit_button("Share") and caption.strip():
            new_id = max(p["id"] for p in st.session_state.posts) + 1
            img_path = "images/post1.jpg"
            if uploaded_img is not None:
                os.makedirs("images", exist_ok=True)
                img_path = f"images/custom_{new_id}.jpg"
                with open(img_path, "wb") as f:
                    f.write(uploaded_img.getbuffer())
            st.session_state.posts.insert(0, {
                "id": new_id,
                "username": username.strip() or "guest",
                "avatar": (username.strip()[:2] or "GU").upper(),
                "location": location.strip() or "Malaysia",
                "image": img_path,
                "caption": caption.strip(),
                "likes": 1,
                "liked": False,
                "reposts": 0,
                "shares": 0,
                "saved": False,
                "show_lemma": False,
                "show_comments": False,
                "time": "Just now",
                "comments": [],
            })
            st.session_state.active_tab = "home"
            st.rerun()


# ==============================================================================
# 8. INSTAGRAM BOTTOM NAVIGATION BAR
# ==============================================================================
st.markdown('<div class="bottom-nav-line"></div>', unsafe_allow_html=True)
b1, b2, b3, b4, b5 = st.columns(5)
with b1:
    if st.button("🏠", key="nav_home", help="Home"):
        st.session_state.active_tab = "home"
        st.rerun()
with b2:
    st.markdown('<div style="text-align:center; font-size:18px; padding-top:2px;">🎬</div>', unsafe_allow_html=True)
with b3:
    st.markdown('<div style="text-align:center; font-size:18px; padding-top:2px;">➤</div>', unsafe_allow_html=True)
with b4:
    if st.button("🔍", key="nav_word", help="Word Lemmatiser"):
        st.session_state.active_tab = "word"
        st.rerun()
with b5:
    st.markdown('<div style="text-align:center; font-size:18px; padding-top:2px;">👤</div>', unsafe_allow_html=True)