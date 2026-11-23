import os
import re
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIG & MOBILE PHONE FRAME CSS (INSTAGRAM LIGHT MODE)
# ==============================================================================
st.set_page_config(
    page_title="RojakGram",
    page_icon="📸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* Hide Streamlit default header, menu, and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Outer desktop background */
    .stApp {
        background-color: #EFEFEF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Phone Screen Container (430px width, centered) */
    .block-container {
        max-width: 430px !important;
        background-color: #FFFFFF;
        border: 1px solid #DBDBDB;
        border-radius: 30px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
        padding: 16px 16px 28px 16px !important;
        margin-top: 18px !important;
        margin-bottom: 24px !important;
    }

    /* IG Top Header */
    .ig-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 4px 10px 4px;
        border-bottom: 1px solid #EFEFEF;
        margin-bottom: 10px;
    }
    .ig-logo {
        font-family: 'Brush Script MT', 'Segoe Script', cursive;
        font-size: 28px;
        font-weight: 700;
        color: #262626;
        letter-spacing: 0.5px;
    }
    .ig-top-icons {
        font-size: 20px;
        letter-spacing: 10px;
        color: #262626;
    }

    /* Decorative Stories Bar */
    .stories-row {
        display: flex;
        gap: 14px;
        overflow-x: auto;
        padding: 6px 2px 12px 2px;
        border-bottom: 1px solid #EFEFEF;
        margin-bottom: 14px;
        scrollbar-width: none;
    }
    .stories-row::-webkit-scrollbar {
        display: none;
    }
    .story-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 62px;
    }
    .story-ring {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        padding: 2.5px;
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .story-inner {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: #FAFAFA;
        border: 2px solid #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 15px;
        color: #444444;
    }
    .story-name {
        font-size: 11px;
        color: #262626;
        margin-top: 5px;
        max-width: 62px;
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
        padding: 8px 2px;
    }
    .post-user-info {
        display: flex;
        align-items: center;
    }
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
        color: #262626;
        line-height: 1.2;
    }
    .post-location {
        font-size: 11px;
        color: #737373;
    }

    /* Missing Image Placeholder */
    .img-placeholder {
        width: 100%;
        height: 290px;
        background-color: #F5F5F5;
        border: 1.5px dashed #CCCCCC;
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #8E8E8E;
        font-size: 13px;
        text-align: center;
        margin-bottom: 8px;
    }

    /* Caption & Meta */
    .post-caption {
        font-size: 13.5px;
        line-height: 1.45;
        color: #262626;
        margin: 4px 0 6px 0;
    }
    .post-time {
        font-size: 10.5px;
        color: #8E8E8E;
        text-transform: uppercase;
        margin-top: 6px;
        margin-bottom: 14px;
        padding-bottom: 14px;
        border-bottom: 1px solid #EFEFEF;
    }

    /* Lemmatise & Translation Box */
    .trans-box {
        background-color: #F8F9FA;
        border-left: 3px solid #0095F6;
        border-radius: 6px;
        padding: 9px 12px;
        margin: 6px 0 10px 0;
        font-size: 12.5px;
        line-height: 1.5;
        color: #262626;
    }
    .trans-label {
        font-weight: 700;
        font-size: 10.5px;
        text-transform: uppercase;
        color: #0095F6;
        letter-spacing: 0.4px;
    }

    /* Compact Buttons */
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #DBDBDB;
        background-color: #FFFFFF;
        color: #262626;
        font-size: 12.5px;
        font-weight: 600;
        padding: 4px 10px;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #0095F6;
        color: #0095F6;
        background-color: #F0F8FF;
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
}

def lemmatise_word(word: str) -> str:
    w = word.lower().strip()
    w = re.sub(r"([a-z]+)2$", r"\1", w)       # makan2 -> makan
    w = re.sub(r"(.)\1{2,}", r"\1", w)        # laparrrr -> lapar
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

def translate_rojak(text: str) -> dict:
    preset = {
        "Saye xleh nak pergi shopping mall arini sebab tengah makan2 kat rumah, laparrrr gila!": {
            "formal_ms": "Saya tidak dapat pergi ke pusat beli-belah hari ini kerana sedang makan di rumah, sangat lapar!",
            "formal_en": "I cannot go to the shopping mall today because I am eating at home, I am extremely hungry!",
        },
        "Good morning! Sarapan apa ye arini? Ikut je member nanti. I am super hungryyyy!": {
            "formal_ms": "Selamat pagi! Apakah sarapan hari ini? Saya hanya akan mengikut rakan nanti. Saya sangat lapar!",
            "formal_en": "Good morning! What is for breakfast today? I will just follow my friend later. I am super hungry!",
        },
        "Everytime lapar je padahal baru makan nasi. Now scrolling food delivery nak order apa japgi.": {
            "formal_ms": "Setiap masa berasa lapar walaupun baru sahaja makan nasi. Sekarang sedang melihat aplikasi penghantaran makanan untuk memesan makanan sebentar lagi.",
            "formal_en": "Always feeling hungry even though I just ate rice. Now scrolling through food delivery to decide what to order shortly.",
        },
    }
    if text in preset:
        return preset[text]
    lemma_ver = lemmatise_sentence(text)
    return {
        "formal_ms": f"[Formal Malay] {lemma_ver}",
        "formal_en": f"[Formal English] {lemma_ver}",
    }


# ==============================================================================
# 3. SESSION STATE (Navigation & Sample Posts pointing to local .jpg files)
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
            "likes": 128,
            "liked": False,
            "time": "2 HOURS AGO",
            "comments": [
                {"user": "weihen_k", "text": "Mmg sedap gila weh, tggu aku datang makan2 skali!"},
                {"user": "yoongkeat", "text": "Pls save some for me tmr, dunno why suddenly hungryyyy."},
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
            "time": "5 HOURS AGO",
            "comments": [
                {"user": "aisyah_my", "text": "Jom pergi mamak dekat office, roti canai dgn teh tarik!"},
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
            "time": "1 DAY AGO",
            "comments": [
                {"user": "daniel_tan", "text": "Same bro, smlm pun order supper pukul 1 pagi haha."},
            ],
        },
    ]


# ==============================================================================
# 4. TOP IG HEADER & COMPACT MOBILE NAV
# ==============================================================================
st.markdown("""
<div class="ig-top-bar">
    <div class="ig-logo">RojakGram</div>
    <div class="ig-top-icons">♡ ✉</div>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.active_tab = "home"
with nav2:
    if st.button("🔍 Word", use_container_width=True):
        st.session_state.active_tab = "word"
with nav3:
    if st.button("➕ Post", use_container_width=True):
        st.session_state.active_tab = "create"


# ==============================================================================
# 5. TAB 1: HOME FEED (Stories + Scrollable Posts + Comments)
# ==============================================================================
if st.session_state.active_tab == "home":
    # Purely decorative IG Stories bar
    stories = [
        ("Your story", "＋"),
        ("jiemin", "JM"),
        ("weihen", "WH"),
        ("kl_food", "KF"),
        ("aisyah", "AY"),
        ("tarumt", "TR"),
    ]
    stories_html = '<div class="stories-row">'
    for name, initials in stories:
        stories_html += f"""
        <div class="story-item">
            <div class="story-ring"><div class="story-inner">{initials}</div></div>
            <div class="story-name">{name}</div>
        </div>
        """
    stories_html += "</div>"
    st.markdown(stories_html, unsafe_allow_html=True)

    # Scrollable Posts Feed
    for post in st.session_state.posts:
        pid = post["id"]

        # Post Header
        st.markdown(f"""
        <div class="post-header">
            <div class="post-user-info">
                <div class="post-avatar">{post['avatar']}</div>
                <div>
                    <div class="post-username">{post['username']}</div>
                    <div class="post-location">{post['location']}</div>
                </div>
            </div>
            <div style="color:#262626; font-weight:700;">⋯</div>
        </div>
        """, unsafe_allow_html=True)

        # Post Image (reads local .jpg; shows clean placeholder if file not added yet)
        if os.path.exists(post["image"]):
            st.image(post["image"], use_container_width=True)
        else:
            st.markdown(f"""
            <div class="img-placeholder">
                <div style="font-size:28px; margin-bottom:6px;">🖼️</div>
                <div><b>Photo Placeholder</b></div>
                <div style="font-size:11.5px; margin-top:4px;">Put your photo at: <code>{post['image']}</code></div>
            </div>
            """, unsafe_allow_html=True)

        # Action Bar (Like + See Translation)
        c1, c2 = st.columns([1, 1.8])
        with c1:
            heart = "❤️" if post["liked"] else "🤍"
            if st.button(f"{heart} {post['likes']}", key=f"like_{pid}"):
                post["liked"] = not post["liked"]
                post["likes"] += 1 if post["liked"] else -1
                st.rerun()
        with c2:
            show_trans = st.toggle("See Translation", key=f"trans_post_{pid}")

        # Caption
        st.markdown(
            f'<div class="post-caption"><b>{post["username"]}</b> {post["caption"]}</div>',
            unsafe_allow_html=True,
        )

        # Caption Lemmatise & Translation Output
        if show_trans:
            lemma_text = lemmatise_sentence(post["caption"])
            trans = translate_rojak(post["caption"])
            st.markdown(f"""
            <div class="trans-box">
                <div class="trans-label">Lemmatised (Root Forms)</div>
                <div>{lemma_text}</div><br>
                <div class="trans-label">Formal Malay</div>
                <div>{trans['formal_ms']}</div><br>
                <div class="trans-label">Formal English</div>
                <div>{trans['formal_en']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Click to open Comments
        with st.expander(f"View all {len(post['comments'])} comments"):
            for idx, cm in enumerate(post["comments"]):
                st.markdown(
                    f'<div style="font-size:13px; margin-bottom:4px;"><b>{cm["user"]}</b> {cm["text"]}</div>',
                    unsafe_allow_html=True,
                )
                if st.toggle("Translate comment", key=f"cm_{pid}_{idx}"):
                    cm_lemma = lemmatise_sentence(cm["text"])
                    cm_trans = translate_rojak(cm["text"])
                    st.markdown(f"""
                    <div class="trans-box">
                        <div class="trans-label">Lemmatised</div> {cm_lemma}<br>
                        <div class="trans-label">Formal Malay</div> {cm_trans['formal_ms']}<br>
                        <div class="trans-label">Formal English</div> {cm_trans['formal_en']}
                    </div>
                    """, unsafe_allow_html=True)

            # Add new comment
            with st.form(key=f"add_cm_{pid}", clear_on_submit=True):
                new_cm = st.text_input("Comment", placeholder="Add a Bahasa Rojak comment...", label_visibility="collapsed")
                if st.form_submit_button("Post Comment") and new_cm.strip():
                    post["comments"].append({"user": "you_demo", "text": new_cm.strip()})
                    st.rerun()

        st.markdown(f'<div class="post-time">{post["time"]}</div>', unsafe_allow_html=True)


# ==============================================================================
# 6. TAB 2: SINGLE-WORD LEMMATISER
# ==============================================================================
elif st.session_state.active_tab == "word":
    st.markdown("### Single-Word Lemmatiser")
    st.caption("Test any Malay, English, or Bahasa Rojak word to see its base root form.")

    word_input = st.text_input("Enter a word:", placeholder="e.g., xleh, laparrrr, makan2, running")
    if word_input and word_input.strip():
        root = lemmatise_word(word_input)
        st.markdown(f"""
        <div class="trans-box" style="text-align:center; padding:18px;">
            <span style="font-size:20px; font-weight:700;">{word_input.strip()}</span>
            <span style="font-size:20px; color:#0095F6; margin:0 10px;">➔</span>
            <span style="font-size:20px; font-weight:700; color:#0095F6;">{root}</span>
            <div style="font-size:11px; color:#8E8E8E; margin-top:6px;">Normalized Root Form (Lemma)</div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 7. TAB 3: CREATE POST
# ==============================================================================
elif st.session_state.active_tab == "create":
    st.markdown("### Create New Post")
    with st.form("new_post_form"):
        username = st.text_input("Username", value="malaysia_student")
        location = st.text_input("Location", value="Kuala Lumpur, Malaysia")
        caption = st.text_area("Caption (Bahasa Rojak)", placeholder="Type a Bahasa Rojak caption...")
        uploaded_img = st.file_uploader("Upload Photo (optional)", type=["jpg", "jpeg", "png"])
        if st.form_submit_button("Share to Feed") and caption.strip():
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
                "time": "JUST NOW",
                "comments": [],
            })
            st.session_state.active_tab = "home"
            st.rerun()