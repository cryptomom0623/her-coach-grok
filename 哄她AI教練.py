import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="🌸",
    initial_sidebar_state="collapsed"
)

# 溫柔明亮柔和風格（解決黑框問題）
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fdf4ff 0%, #fff7f0 100%);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 28px;
        padding: 3rem 2.8rem;
        box-shadow: 0 20px 60px rgba(192, 132, 252, 0.18);
        max-width: 860px;
        margin: 2rem auto;
    }
    h1 {
        font-size: 3rem !important;
        background: linear-gradient(90deg, #db2777, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
    }
    /* 表單輸入框優化 - 解決黑框問題 */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 2px solid #e0bbff !important;
        border-radius: 16px !important;
        color: #4c1d95 !important;
        font-size: 1.05rem;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c026d3 !important;
        box-shadow: 0 0 0 3px rgba(192, 132, 252, 0.2);
    }
    label {
        color: #6b21a8 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e879f9, #c084fc);
        color: white;
        border-radius: 9999px;
        height: 3.6rem;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(232, 121, 249, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(192, 132, 252, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌸 哄她AI教練")

st.markdown("""
<p style='text-align: center; color: #7e57c2; font-size: 1.4rem; margin-bottom: 3rem;'>
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
        height=140)

    submitted = st.form_submit_button("🌸 生成溫柔自然的表達方式")

# ====================== 生成部分（保持不變） ======================
if submitted:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ 請先在 Settings → Secrets 中設定 GEMINI_API_KEY")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    progress_text = "正在用心為你準備溫柔的表達方式..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent in range(100):
        time.sleep(0.03)
        my_bar.progress(percent + 1, text=progress_text)

    prompt = f"""你是一位溫柔細心的情感陪伴者。

使用者資訊：
- 性別：{gender}，年紀：{age}歲，職業：{job}
- 關係階段：{relation}
- 她的名字：{her_name}，星座：{zodiac}
- 目前情境：{situation}

請生成 4 句最適合、最自然的溫柔表達方式。

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
---

語氣要真誠、自然、有溫度，像日常真心說出的話。"""

    try:
        response = model.generate_content(prompt)
        full_result = response.text
        my_bar.empty()
        
        st.success("🌸 已為你生成溫柔自然的表達方式")
        st.markdown(full_result)
        
        # 提取4句話
        import re
        talk_matches = re.findall(r'「(.*?)」', full_result)
        talks = [talk.strip() for talk in talk_matches[:4]] if len(talk_matches) >= 4 else ["（請稍後再試）"] * 4

        st.markdown("### 📋 選擇你要複製的表達方式")
        cols = st.columns(4)
        
        for i in range(4):
            with cols[i]:
                if st.button(f"複製第 {i+1} 句", key=f"copy_{i}"):
                    st.code(talks[i], language=None)
                    st.toast(f"✅ 已複製第 {i+1} 句！可以直接發給她了～", icon="🌸")
        
        st.markdown("---")
        st.markdown("### 💡 完整建議")
        st.markdown(full_result)
        
    except Exception as e:
        my_bar.empty()
        st.error(f"發生錯誤：{str(e)}")
