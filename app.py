import os
import re
import streamlit as st
from PIL import Image

# Safe import for OCR (won't crash if pytesseract isn't installed yet)
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

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
    padding: 12px 14px 16px 14px !important;
    margin-top: 16px !important;
    margin-bottom: 24px !important;
}

/* Reduce default horizontal gap between Streamlit columns */
div[data-testid="stHorizontalBlock"] {
    gap: 0.25rem !important;
    align-items: center !important;
}

/* Instagram Top Header (加底部间距，彻底解决字母 g 和头像重叠) */
.ig-logo {
    font-family: 'Grand Hotel', cursive;
    font-size: 32px;
    font-weight: 400;
    color: #000000;
    text-align: center;
    line-height: 1.2;
    margin-top: 2px;
    margin-bottom: 14px;
}

/* Clickable Story Circle Buttons */
div[class*="st-key-story_btn_"] {
    display: flex !important;
    justify-content: center !important;
}
div[class*="st-key-story_btn_"] button {
    width: 58px !important;
    height: 58px !important;
    min-width: 58px !important;
    min-height: 58px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #333333 !important;
    background: linear-gradient(#F4F4F4, #F4F4F4) padding-box,
                linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%) border-box !important;
    border: 2.5px solid transparent !important;
    box-shadow: inset 0 0 0 2.5px #FFFFFF !important;
    position: relative !important;
    overflow: visible !important;
}
div[class*="st-key-story_btn_"] button:hover {
    transform: scale(1.04);
    color: #000000 !important;
}

/* First Circle ("Your story"): Grey ring + black '+' badge */
div.st-key-story_btn_0 button {
    background: linear-gradient(#F4F4F4, #F4F4F4) padding-box,
                linear-gradient(#E0E0E0, #E0E0E0) border-box !important;
}
div.st-key-story_btn_0 button::after {
    content: "+";
    position: absolute;
    bottom: -2px;
    right: -2px;
    width: 19px;
    height: 19px;
    border-radius: 50%;
    background-color: #000000;
    color: #FFFFFF;
    border: 2px solid #FFFFFF;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
}

/* Story Name (Plain text below circle) */
.story-name {
    font-size: 11px;
    color: #262626;
    text-align: center;
    margin-top: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.stories-divider {
    border-bottom: 1px solid #EFEFEF;
    margin: 8px 0 10px 0;
}

/* Story Name Clickable Button */
div[class*="st-key-story_btn_"] button {
    font-size: 11px !important;
    font-weight: 400 !important;
    color: #262626 !important;
    padding: 2px 0 !important;
    width: 100% !important;
    justify-content: center !important;
}

/* Story Viewer Top Progress Bar */
.story-progress-bg {
    width: 100%;
    height: 3px;
    background-color: #E0E0E0;
    border-radius: 2px;
    margin: 4px 0 10px 0;
    overflow: hidden;
}
.story-progress-fill {
    width: 65%;
    height: 100%;
    background-color: #262626;
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
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #8E8E8E;
    font-size: 13px;
    text-align: center;
    margin-bottom: 6px;
    padding: 16px;
}

/* Caption & Lemmatise Output Box */
.post-caption {
    font-size: 13.5px;
    line-height: 1.45;
    color: #000000;
    margin: 2px 0 2px 0;
}
.lemma-output {
    background-color: #F8F9FA;
    border-left: 3px solid #262626;
    border-radius: 6px;
    padding: 9px 12px;
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
    margin: 8px 0 12px 0;
}

/* Force ALL Streamlit buttons to be borderless & transparent */
div.stButton > button,
button[data-testid="stBaseButton-secondary"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    color: #000000 !important;
    padding: 2px 2px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    min-height: 0px !important;
    height: auto !important;
    gap: 3px !important;
}
div.stButton > button:hover,
button[data-testid="stBaseButton-secondary"]:hover,
div.stButton > button:focus,
button[data-testid="stBaseButton-secondary"]:focus {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #737373 !important;
}

/* Pill CTA button specifically for Story Scan & Lemmatise */
div[class*="st-key-scan_story_"] button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border-radius: 20px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-top: 8px !important;
}
div[class*="st-key-scan_story_"] button:hover {
    background-color: #333333 !important;
    color: #FFFFFF !important;
}

/* Action Bar Icons Size */
div.stButton > button span[data-testid="stIconMaterial"] {
    font-size: 22px !important;
    font-weight: 300 !important;
}

/* Filled Red Heart when Liked */
div[class*="st-key-liked_"] button span[data-testid="stIconMaterial"] {
    color: #FF3040 !important;
    font-variation-settings: 'FILL' 1 !important;
}

/* Filled Black Bookmark when Saved */
div[class*="st-key-saved_"] button span[data-testid="stIconMaterial"] {
    color: #000000 !important;
    font-variation-settings: 'FILL' 1 !important;
}

/* Timestamp + Lemmatise Inline Link */
div[class*="st-key-lemma_post_"] button {
    font-size: 12px !important;
    font-weight: 400 !important;
    color: #737373 !important;
    padding: 0px !important;
    justify-content: flex-start !important;
}
div[class*="st-key-lemma_post_"] button:hover {
    color: #262626 !important;
}

/* Bottom Navigation Bar */
.bottom-nav-line {
    border-top: 1px solid #DBDBDB;
    margin-top: 8px;
    padding-top: 8px;
}
div[class*="st-key-nav_"] button {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 4px 0 !important;
}
div[class*="st-key-nav_"] button span[data-testid="stIconMaterial"] {
    font-size: 26px !important;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. BACKEND PLACEHOLDER + IMAGE OCR HELPER
# ==============================================================================
MOCK_SLANG_DICT = {
    "xleh": "tidak boleh", "takleh": "tidak boleh", "mcm": "macam",
    "dgn": "dengan", "yg": "yang", "utk": "untuk", "sgt": "sangat",
    "mmg": "memang", "tggu": "tunggu", "smlm": "semalam", "arini": "hari ini",
    "saye": "saya", "nak": "hendak", "tak": "tidak", "dah": "sudah",
    "kat": "dekat", "je": "sahaja", "tapi": "tetapi", "pls": "please",
    "tmr": "tomorrow", "gonna": "going to", "dunno": "do not know",
    "japgi": "sekejap lagi", "skali": "sekali", "sbb": "sebab",
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

def extract_text_from_image(img_source) -> str:
    """Scan text from an uploaded image or local file path using Tesseract OCR."""
    if not OCR_AVAILABLE:
        return ""
    try:
        img = Image.open(img_source)
        raw_text = pytesseract.image_to_string(img)
        cleaned = re.sub(r"\s+", " ", raw_text).strip()
        return cleaned
    except Exception:
        return ""


# ==============================================================================
# 3. SESSION STATE (Stories & Posts)
# ==============================================================================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "home"
if "active_story_id" not in st.session_state:
    st.session_state.active_story_id = None

if "stories" not in st.session_state:
    st.session_state.stories = [
        {
            "id": 0,
            "name": "Your story",
            "initials": "JM",
            "is_you": True,
            "time": "Upload",
            "image": None,
            "fallback_text": "",
        },
        {
            "id": 1,
            "name": "britnchan",
            "initials": "BC",
            "is_you": False,
            "time": "2h",
            "image": "images/story1.jpg",
            "fallback_text": "Promo arini je! Beli 2 kopi dapat free cake, mmg berbaloi gila!",
        },
        {
            "id": 2,
            "name": "bell_lh",
            "initials": "BL",
            "is_you": False,
            "time": "4h",
            "image": "images/story2.jpg",
            "fallback_text": "Saye xleh fokus studying sbb laparrrr nak makan2 kat mamak.",
        },
        {
            "id": 3,
            "name": "kl_food",
            "initials": "KF",
            "is_you": False,
            "time": "6h",
            "image": "images/story3.jpg",
            "fallback_text": "New cafe opening tmr! Coffee sedap dgn vibes mmg nice.",
        },
        {
            "id": 4,
            "name": "tarumt",
            "initials": "TR",
            "is_you": False,
            "time": "9h",
            "image": "images/story4.jpg",
            "fallback_text": "Pls submit assignment before 5pm arini, jgn lupa check format!",
        },
    ]

if "posts" not in st.session_state or "reposts" not in st.session_state.posts[0]:
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
# 4. STORY VIEWER MODE (When a Story circle is clicked)
# ==============================================================================
if st.session_state.active_tab == "story":
    story = next(
        (s for s in st.session_state.stories if s["id"] == st.session_state.active_story_id),
        st.session_state.stories[0],
    )

    # IG Story Progress Bar
    st.markdown('<div class="story-progress-bg"><div class="story-progress-fill"></div></div>', unsafe_allow_html=True)

    # Story Header (Avatar + Name + Close Button)
    sh1, sh2 = st.columns([5, 1])
    with sh1:
        st.markdown(
            f'<div class="post-user-info" style="padding:2px 0 8px 0;">'
            f'<div class="post-avatar">{story["initials"]}</div>'
            f'<div><div class="post-username">{story["name"]} '
            f'<span style="font-weight:400; color:#737373; font-size:12px;">· {story["time"]}</span></div>'
            f'<div class="post-location">Story Image Scanner (OCR)</div></div></div>',
            unsafe_allow_html=True,
        )
    with sh2:
        if st.button("", icon=":material/close:", key="close_story", use_container_width=True):
            st.session_state.active_tab = "home"
            st.session_state.active_story_id = None
            st.rerun()

    # Case A: "Your story" -> Upload any photo with text to scan live
    if story["is_you"]:
        uploaded = st.file_uploader("Upload a Story photo containing text", type=["jpg", "jpeg", "png"])
        if uploaded is not None:
            st.image(uploaded, use_container_width=True)
            if st.button("Scan & Lemmatise Text", key="scan_story_upload", use_container_width=True):
                scanned = extract_text_from_image(uploaded)
                if scanned:
                    lemma_res = lemmatise_sentence(scanned)
                    st.markdown(
                        f'<div class="lemma-output">'
                        f'<div class="lemma-tag">Scanned Text (OCR)</div><div>{scanned}</div><br>'
                        f'<div class="lemma-tag">Lemmatised</div><div>{lemma_res}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("No readable text detected in this photo. Try a clearer image with printed text.")
        else:
            st.markdown(
                '<div class="img-placeholder">'
                '<div style="font-size:14px; font-weight:600; color:#555;">Live Story OCR Scanner</div>'
                '<div style="font-size:12px; margin-top:6px;">Upload any screenshot or photo with Malay-English text above to scan and lemmatise it.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

    # Case B: Friend's Story -> Display local .jpg and scan its text
    else:
        has_img = story["image"] and os.path.exists(story["image"])
        if has_img:
            st.image(story["image"], use_container_width=True)
        else:
            st.markdown(
                f'<div class="img-placeholder">'
                f'<div style="font-size:14px; font-weight:600; color:#555;">Story Photo Placeholder</div>'
                f'<div style="font-size:11.5px; margin-top:4px;">Put your photo with text at: <code>{story["image"]}</code></div>'
                f'<div style="font-size:12px; color:#262626; margin-top:12px; font-style:italic;">"{story["fallback_text"]}"</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if st.button("Scan & Lemmatise Text", key=f"scan_story_{story['id']}", use_container_width=True):
            scanned = extract_text_from_image(story["image"]) if has_img else ""
            used_fallback = False
            if not scanned:
                scanned = story["fallback_text"]
                used_fallback = True

            lemma_res = lemmatise_sentence(scanned)
            note = " (Demo Preview)" if used_fallback else " (OCR)"
            st.markdown(
                f'<div class="lemma-output">'
                f'<div class="lemma-tag">Scanned Text{note}</div><div>{scanned}</div><br>'
                f'<div class="lemma-tag">Lemmatised</div><div>{lemma_res}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ==============================================================================
# 5. MAIN APP VIEW (Top Bar + Home / Word / Create + Bottom Bar)
# ==============================================================================
else:
    # --- INSTAGRAM TOP BAR (+   Instagram   ♡) ---
    t1, t2, t3 = st.columns([1, 4, 1])
    with t1:
        if st.button("", icon=":material/add:", key="top_plus", help="Create Post"):
            st.session_state.active_tab = "create"
            st.rerun()
    with t2:
        st.markdown('<div class="ig-logo">Instagram</div>', unsafe_allow_html=True)
    with t3:
        heart_svg = (
            '<div style="display:flex; justify-content:flex-end; padding-top:4px;">'
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>'
            '</svg></div>'
        )
        st.markdown(heart_svg, unsafe_allow_html=True)


        # --- TAB 1: HOME FEED ---
    if st.session_state.active_tab == "home":
        # Clickable IG Stories Row (Click the avatar circle itself!)
        s_cols = st.columns(5, gap="small")
        for idx, s in enumerate(st.session_state.stories):
            with s_cols[idx]:
                if st.button(s["initials"], key=f"story_btn_{s['id']}"):
                    st.session_state.active_story_id = s["id"]
                    st.session_state.active_tab = "story"
                    st.rerun()
                st.markdown(f'<div class="story-name">{s["name"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="stories-divider"></div>', unsafe_allow_html=True)

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
                    f'<div style="font-size:14px; font-weight:600; color:#555;">Photo Placeholder</div>'
                    f'<div style="font-size:11px; margin-top:4px;">Put your photo at: <code>{post["image"]}</code></div>'
                    f'</div>'
                )
                st.markdown(placeholder_html, unsafe_allow_html=True)

            # Action Bar
            a1, a2, a3, a4, spacer, a5 = st.columns([0.95, 0.72, 0.72, 0.85, 2.0, 0.45], gap="small")
            with a1:
                like_key = f"liked_{pid}" if post["liked"] else f"unliked_{pid}"
                if st.button(f"{post['likes']}", icon=":material/favorite:", key=like_key):
                    post["liked"] = not post["liked"]
                    post["likes"] += 1 if post["liked"] else -1
                    st.rerun()
            with a2:
                if st.button(f"{len(post['comments'])}", icon=":material/chat_bubble:", key=f"cm_btn_{pid}"):
                    post["show_comments"] = not post["show_comments"]
                    st.rerun()
            with a3:
                if st.button(f"{post['reposts']}", icon=":material/repeat:", key=f"repost_{pid}"):
                    post["reposts"] += 1
                    st.rerun()
            with a4:
                st.button(f"{post['shares']}", icon=":material/send:", key=f"share_{pid}")
            with a5:
                save_key = f"saved_{pid}" if post["saved"] else f"unsaved_{pid}"
                if st.button("", icon=":material/bookmark:", key=save_key):
                    post["saved"] = not post["saved"]
                    st.rerun()

            # Caption
            st.markdown(
                f'<div class="post-caption"><b>{post["username"]}</b> {post["caption"]}</div>',
                unsafe_allow_html=True,
            )

            # Combined "5 hours ago · Lemmatise"
            action_word = "See Original" if post["show_lemma"] else "Lemmatise"
            if st.button(f"{post['time']} · {action_word}", key=f"lemma_post_{pid}"):
                post["show_lemma"] = not post["show_lemma"]
                st.rerun()

            # Lemmatised Output
            if post["show_lemma"]:
                lemma_res = lemmatise_sentence(post["caption"])
                st.markdown(
                    f'<div class="lemma-output"><div class="lemma-tag">Lemmatised</div>{lemma_res}</div>',
                    unsafe_allow_html=True,
                )

            # Comments Section
            if post["show_comments"]:
                st.markdown('<div style="font-size:12px; font-weight:600; color:#737373; margin:6px 0;">Comments</div>', unsafe_allow_html=True)
                for idx, cm in enumerate(post["comments"]):
                    c_txt, c_btn = st.columns([3.4, 1.1], gap="small")
                    with c_txt:
                        st.markdown(
                            f'<div style="font-size:13px; color:#000; padding-top:2px;"><b>{cm["user"]}</b> {cm["text"]}</div>',
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

    # --- TAB 2: WORD LEMMATISER ---
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

    # --- TAB 3: CREATE POST ---
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

    # --- INSTAGRAM BOTTOM NAVIGATION BAR ---
    st.markdown('<div class="bottom-nav-line"></div>', unsafe_allow_html=True)
    b1, b2, b3, b4, b5 = st.columns(5, gap="small")
    with b1:
        if st.button("", icon=":material/home:", key="nav_home", help="Home", use_container_width=True):
            st.session_state.active_tab = "home"
            st.rerun()
    with b2:
        st.button("", icon=":material/smart_display:", key="nav_reels", help="Reels", use_container_width=True)
    with b3:
        st.button("", icon=":material/send:", key="nav_dm", help="Messages", use_container_width=True)
    with b4:
        if st.button("", icon=":material/search:", key="nav_word", help="Word Lemmatiser", use_container_width=True):
            st.session_state.active_tab = "word"
            st.rerun()
    with b5:
        st.button("", icon=":material/person:", key="nav_profile", help="Profile", use_container_width=True)