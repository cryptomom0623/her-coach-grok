import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="🌸",
    initial_sidebar_state="collapsed"
)

# 徹底解決白色字體問題 + 柔和風格
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f4ff 0%, #fff8f0 100%);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 28px;
        padding: 3rem 2.5rem;
        box-shadow: 0 15px 50px rgba(139, 92, 246, 0.12);
        max-width: 860px;
        margin: 0 auto;
    }
    h1, h2, h3, p, label, span, div, li {
        color: #4c1d95 !important;   /* 深紫色，確保清晰 */
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
        border-radius: 18px !important;
    }
    /* 單獨框框樣式 */
    .talk-box {
        background-color: #ffffff;
        border: 2px solid #e0bbff;
        border-radius: 20px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(192, 132, 252, 0.15);
    }
    .talk-box:hover {
        border-color: #c026d3;
        box-shadow: 0 6px 20px rgba(192, 132, 252, 0.25);
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
        height=140)

    submitted = st.form_submit_button("🌸 生成溫柔自然的表達方式")

# ====================== 生成 ======================
if submitted:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ 請先在 Settings → Secrets 中設定 GEMINI_API_KEY")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 可愛等待動畫
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

請只輸出以下格式，不要加入其他說明：
---
**表達方式 1**（溫柔描述）
「實際要說的話」

**表達方式 2**（溫柔描述）
「實際要說的話」

**表達方式 3**（溫柔描述）
「實際要說的話」

**表達方式 4**（溫柔描述）
「實際要說的話」
---"""

    try:
        response = model.generate_content(prompt)
        full_result = response.text
        my_bar.empty()
        
        st.success("🌸 已為你生成溫柔自然的表達方式")
        
        # 提取4句純文字
        import re
        talk_matches = re.findall(r'「(.*?)」', full_result)
        talks = [talk.strip() for talk in talk_matches[:4]] if len(talk_matches) >= 4 else ["（請稍後再試）"] * 4

        # ====================== 獨立框框顯示 ======================
        st.markdown("### 📝 以下是為你準備的溫柔表達方式")
        
        for i in range(4):
            st.markdown(f"""
            <div class="talk-box">
                <strong>第 {i+1} 句</strong><br>
                {talks[i]}
            </div>
            """, unsafe_allow_html=True)

        # 完整詳細建議
        st.markdown("---")
        st.markdown("### 💡 完整建議（後續升溫與注意事項）")
        st.markdown(full_result)
        
    except Exception as e:
        my_bar.empty()
        st.error(f"發生錯誤：{str(e)}")
