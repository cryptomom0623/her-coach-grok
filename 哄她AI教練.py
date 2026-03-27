import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="🌸",
    initial_sidebar_state="collapsed"
)

# 優化後的柔和清晰風格
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f4ff 0%, #fff8f0 100%);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.97);
        border-radius: 28px;
        padding: 3rem 2.5rem;
        box-shadow: 0 15px 50px rgba(139, 92, 246, 0.12);
        max-width: 820px;
        margin: 0 auto;
    }
    h1 {
        font-size: 2.9rem !important;
        background: linear-gradient(90deg, #c026d3, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    /* 重要：讓表單標籤文字清晰可見 */
    label, .stMarkdown p, .stSelectbox label, .stTextInput label {
        color: #4c1d95 !important;
        font-weight: 500;
        font-size: 1.05rem;
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
        border-radius: 18px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e879f9, #c084fc);
        color: white;
        border-radius: 9999px;
        height: 3.6rem;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 6px 25px rgba(232, 121, 249, 0.35);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(192, 132, 252, 0.45);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌸 哄她AI教練")
st.markdown("""
<p style='text-align: center; color: #6b21a8; font-size: 1.35rem; margin-bottom: 2.5rem;'>
    讓每一次對話，都帶著溫柔與真心 💕
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
    
    prompt = f"""你是一位溫柔細心的情感陪伴者，幫助男生用真誠自然的方式表達心意。

使用者資訊：
- 性別：{gender}，年紀：{age}歲，職業：{job}
- 關係階段：{relation}
- 她的名字：{her_name}，星座：{zodiac}
- 目前情境：{situation}

請生成以下內容（全部用溫柔自然的中文）：

1. **4句最適合的表達方式**
2. **💕 後續感情升溫建議**（3點具體建議）
3. **⚠️ 這階段要注意的雷區**（3點常見錯誤）

輸出格式請嚴格如下：
---
**表達方式 1**（溫柔描述）
「實際要說的話」

**表達方式 2**（溫柔描述）
「實際要說的話」

**表達方式 3**（溫柔描述）
「實際要說的話」

**表達方式 4**（溫柔描述）
「實際要說的話」

💕 **後續感情升溫建議**
• 第一點
• 第二點
• 第三點

⚠️ **這階段要注意的雷區**
• 第一點
• 第二點
• 第三點
---

語氣要溫柔、真誠、有溫度，像朋友給建議一樣自然。"""

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
