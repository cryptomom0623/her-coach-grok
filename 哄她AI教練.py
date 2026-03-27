import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="哄她AI教練 🤖❤️",
    layout="centered",
    page_icon="❤️"
)

st.title("🤖 哄她AI教練")
st.subheader("不知道怎麼哄女生？讓 Gemini 即時幫你生成自然話術")
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
        placeholder="例如：她今天突然對我很冷淡、她送我一個小禮物、她說今天工作很累...",
        height=120)
  
    submitted = st.form_submit_button("🚀 生成專屬哄她話術", type="primary")

# ====================== Gemini API 呼叫 ======================
if submitted:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ 請先在 Streamlit Settings → Secrets 中設定 GEMINI_API_KEY")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')   # 免費額度較多的模型
    
    prompt = f"""你是最頂尖的情感教練，專門教男生如何自然、真誠地哄女生。
以下是使用者資訊：
- 性別：{gender}，年紀：{age}歲，職業：{job}
- 關係階段：{relation}
- 她的名字：{her_name}，星座：{zodiac}
- 目前情境：{situation}

請根據「海王六大句型公式」為他生成 **4 句最適合、最自然的客製化話術**：
1. 你不要這樣…不然我會怎麼樣…
2. 這是我第一次…
3. 沒想到妳怎麼樣…其他人都做不到
4. 我發現妳怎麼樣…
5. 要是有你在就好了…
6. 妳不準怎麼樣…不然我就會…

輸出格式必須嚴格如下（用中文）：
---
**推薦話術 1**（句型名稱）
「實際要說的話」

**底層邏輯**：簡短說明
**預期反應**：女生可能有的感覺

（請依序輸出 4 句）
---

語氣要自然、真誠、溫柔，避免太油或太刻意。根據關係階段和情境選擇最適合的句型。"""

    with st.spinner("正在為你生成專屬話術..."):
        try:
            response = model.generate_content(prompt)
            result = response.text
            
            st.success("✅ 已生成專屬話術！")
            st.markdown(result)
            
            if st.button("📋 複製全部話術"):
                st.code(result, language=None)
                st.toast("✅ 已複製到剪貼簿！", icon="✅")
                
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
            st.info("請確認 Secrets 中的 GEMINI_API_KEY 是否正確。")

# ====================== 側邊欄 ======================
st.sidebar.title("📢 如何讓別人使用？")
st.sidebar.markdown("### 本地測試")
st.sidebar.code("""
pip install -r requirements.txt
streamlit run 哄她AI教練.py
""", language="bash")

st.sidebar.markdown("**重要**：請在 Streamlit Settings → Secrets 中設定：")
st.sidebar.code("""
GEMINI_API_KEY = "你的 Gemini API Key"
""", language="toml")

st.sidebar.info("💡 這是完全免費方案，適合個人使用與分享！")
