import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="❤️"
)

st.title("🤖 哄她AI教練")
st.subheader("不知道怎麼跟她說話？讓我幫你生成溫柔自然的表達方式")
st.markdown("---")

# ====================== 表單 ======================
with st.form("coach_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("你的年紀", 18, 60, 28)
        job = st.text_input("你的職業", "工程師")
    with col2:
        gender = st.selectbox("你的性別", ["男性", "女性", "同志1（攻）", "同志0（受）"])
  
    relation = st.selectbox("與她的關係",
        ["追求中", "互有好感", "曖昧", "情侶", "已婚", "離婚"])
    zodiac = st.selectbox("她的星座",
        ["白羊座","金牛座","雙子座","巨蟹座","獅子座","處女座",
         "天秤座","天蠍座","射手座","摩羯座","水瓶座","雙魚座"])
  
    her_name = st.text_input("她的名字 / 暱稱", "小薇")
    situation = st.text_area("目前情境（越詳細越好）",
        placeholder="例如：她今天突然對我有點冷淡、她送我一個小禮物、她說今天工作很累...",
        height=120)
  
    submitted = st.form_submit_button("🚀 生成溫柔自然的表達方式", type="primary")

# ====================== Gemini API 呼叫 ======================
if submitted:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ 請先在 Streamlit Settings → Secrets 中設定 GEMINI_API_KEY")
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

1. 用溫柔的拒絕姿態表達喜歡（例如：你不要這樣…不然我會…）
2. 讓她感受到自己很特別（例如：這是我第一次…）
3. 用驚喜的方式肯定她（例如：沒想到你這麼…）
4. 給她溫暖的正面肯定（例如：我發現你其實很…）
5. 柔軟地表達想念或需要她（例如：要是有你在就好了…）
6. 用關心的語氣展現重視（例如：你不準再…不然我會擔心…）

輸出格式請嚴格如下（用溫柔自然的中文）：
---
**表達方式 1**（溫柔描述）
「實際要說的話」

**為什麼有效**：簡短說明
**可能帶給她的感覺**：她可能會有的正面感受

（請依序輸出 4 句）
---

請讓每一句話都聽起來真誠、有溫度、自然，像日常真心說出的話。避免油膩、刻意或技巧感。根據關係階段和目前情境，選擇最適合她的表達方式。"""

    with st.spinner("正在為你生成溫柔自然的表達方式..."):
        try:
            response = model.generate_content(prompt)
            result = response.text
            
            st.success("✅ 已生成溫柔自然的表達方式！")
            st.markdown(result)
            
            if st.button("📋 複製全部內容"):
                st.code(result, language=None)
                st.toast("✅ 已複製到剪貼簿！", icon="✅")
                
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
            st.info("請確認 Secrets 中的 GEMINI_API_KEY 是否正確。")

# ====================== 側邊欄 ======================
st.sidebar.title("📢 如何讓別人使用？")
st.sidebar.markdown("### 1. 本地測試")
st.sidebar.code("""
pip install -r requirements.txt
streamlit run 哄她AI教練.py
""", language="bash")

st.sidebar.markdown("### 2. 免費公開部署")
st.sidebar.markdown("""
1. 把程式碼推到 GitHub  
2. 前往 https://share.streamlit.io/  
3. 點「New app」→ 選擇你的 GitHub 倉庫  
4. 部署完成後會給你一個公開連結
""")

st.sidebar.markdown("**重要**：請在 Streamlit Cloud 的 Settings → Secrets 中設定：")
st.sidebar.code("""
GEMINI_API_KEY = "你的 Gemini API Key"
""", language="toml")

st.sidebar.info("💡 這是完全免費的版本，適合個人使用與分享給朋友。")
