import streamlit as st
import google.generativeai as genai

# ====================== 頁面設定 ======================
st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="🌸",
    initial_sidebar_state="collapsed"   # ← 隱藏左側邊欄
)

# 自訂柔和明亮的樣式（解決白色文字問題）
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fffaf0 0%, #f8f1ff 100%);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        box-shadow: 0 10px 40px rgba(192, 132, 252, 0.12);
        max-width: 800px;
        margin: 0 auto;
    }
    h1 {
        font-size: 2.8rem !important;
        background: linear-gradient(90deg, #e879f9, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
        border-radius: 16px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e879f9, #c084fc);
        color: white;
        border-radius: 9999px;
        height: 3.4rem;
        font-size: 1.15rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 20px rgba(232, 121, 249, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(192, 132, 252, 0.4);
    }
    /* 讓所有文字清晰可見 */
    .stMarkdown, p, label, .stSelectbox label {
        color: #4c1d95 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 主內容 ======================
st.title("🌸 哄她AI教練")

st.markdown("""
<p style='text-align: center; color: #7e57c2; font-size: 1.3rem; margin-bottom: 2rem;'>
    不知道怎麼溫柔地跟她說話？<br>
    讓我幫你想出自然又有溫度的表達方式 💕
</p>
""", unsafe_allow_html=True)

# ====================== 表單 ======================
with st.form("coach_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("你的年紀", 18, 60, 28)
        job = st.text_input("你的職業", "工程師")
    with col2:
        gender = st.selectbox("你的性別", ["男性", "女性", "同志1（攻）", "同志0（受）"])
  
    relation = st.selectbox("與她的關係階段", 
        ["追求中", "互有好感", "曖昧", "情侶", "已婚", "離婚"])
    
    zodiac = st.selectbox("她的星座", 
        ["白羊座","金牛座","雙子座","巨蟹座","獅子座","處女座",
         "天秤座","天蠍座","射手座","摩羯座","水瓶座","雙魚座"])
  
    her_name = st.text_input("她的名字 / 暱稱", "小薇")
    
    situation = st.text_area("目前的情境或她的近況", 
        placeholder="例如：她今天突然對我有點冷淡、她送了我一個小禮物、她說最近工作很累...",
        height=130)

    submitted = st.form_submit_button("🌸 生成溫柔自然的表達方式")

# ====================== Gemini API 呼叫 ======================
if submitted:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ 請先在 Settings → Secrets 中設定 GEMINI_API_KEY")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""你是一位溫柔細心的情感陪伴者，專門幫助男生用真誠、自然的方式表達心意，讓女生感受到被珍惜與重視。

以下是使用者資訊：
- 性別：{gender}，年紀：{age}歲，職業：{job}
- 目前關係階段：{relation}
- 她的名字：{her_name}，星座：{zodiac}
- 目前情境：{situation}

請根據以下 6 種溫柔的表達方式，為他生成 **4 句最適合、最自然的客製化話術**：

1. 用溫柔的拒絕姿態表達喜歡
2. 讓她感受到自己很特別
3. 用驚喜的方式肯定她
4. 給她溫暖的正面肯定
5. 柔軟地表達想念或需要她
6. 用關心的語氣展現重視

輸出格式請嚴格如下（用溫柔自然的中文）：
---
**表達方式 1**（溫柔描述）
「實際要說的話」

**為什麼有效**：簡短說明
**可能帶給她的感覺**：她可能會有的正面感受

（請依序輸出 4 句）
---

請讓每一句話都聽起來真誠、有溫度、自然，像日常真心說出的話。避免油膩或刻意。根據關係階段和目前情境，選擇最適合她的表達方式。"""

    with st.spinner("正在用心為你思考最適合的表達方式... 💭"):
        try:
            response = model.generate_content(prompt)
            result = response.text
            
            st.success("🌸 已為你生成溫柔自然的表達方式")
            st.markdown(result)
            
            if st.button("📋 複製全部內容"):
                st.code(result, language=None)
                st.toast("✅ 已複製到剪貼簿！", icon="🌸")
                
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
            st.info("請確認 Secrets 中的 GEMINI_API_KEY 是否正確。")
