import streamlit as st
import google.generativeai as genai

# ====================== UI 優化設定 ======================
st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="🌸",
    initial_sidebar_state="expanded"
)

# 自訂柔和風格
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fff7f0 0%, #f5f0ff 100%);
    }
    .main > div {
        padding-top: 2rem;
    }
    h1 {
        font-size: 2.8rem !important;
        background: linear-gradient(90deg, #e879f9, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
        border-radius: 16px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e879f9, #c084fc);
        color: white;
        border-radius: 9999px;
        height: 3.2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(232, 121, 249, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(192, 132, 252, 0.4);
    }
    .sidebar .css-1d391kg {
        background-color: rgba(255,255,255,0.85);
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 主標題 ======================
st.title("🌸 哄她AI教練")
st.markdown("<p style='text-align: center; color: #9f7aea; font-size: 1.25rem; margin-bottom: 2rem;'>讓每一次對話，都帶著溫柔與真心</p>", unsafe_allow_html=True)

# ====================== 表單 ======================
with st.form("coach_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("你的年紀", 18, 60, 28, help="這有助於調整語氣")
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

# ====================== 側邊欄 ======================
st.sidebar.title("💡 使用說明")
st.sidebar.info("這是一個溫柔的陪伴工具\n希望每一次對話都能讓你們更靠近💕")

st.sidebar.markdown("### 本地測試")
st.sidebar.code("""
pip install -r requirements.txt
streamlit run 哄她AI教練.py
""", language="bash")

st.sidebar.markdown("**重要**：請在 Settings → Secrets 中設定：")
st.sidebar.code("""
GEMINI_API_KEY = "你的 Gemini API Key"
""", language="toml")
