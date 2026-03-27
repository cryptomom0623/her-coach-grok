import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="哄她AI教練 🤖❤️", layout="centered", page_icon="❤️")

st.title("🤖 哄她AI教練")
st.subheader("不知道怎麼哄女生？讓 Grok 即時幫你生成海王級話術")
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
    
    submitted = st.form_submit_button("🚀 讓 Grok 生成專屬哄她話術", type="primary")

# ====================== Grok API 呼叫 ======================
if submitted:
    if not os.getenv("XAI_API_KEY"):
        st.error("⚠️ 請先在程式碼上方設定你的 Grok API Key（環境變數 XAI_API_KEY）")
        st.stop()
    
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1"
    )
    
    prompt = f"""你是最頂尖的情感教練，專門教男生如何用「海王六大句型公式」哄女生。
以下是使用者資訊：
- 性別：{gender}，年紀：{age}歲，職業：{job}
- 關係階段：{relation}
- 她的名字：{her_name}，星座：{zodiac}
- 目前情境：{situation}

請嚴格依照以下六大海王句型公式，為他生成**4句最合適、最自然的客製化話術**：
1. 你不要這樣…不然我會怎麼樣…（拒絕式邀請投入）
2. 這是我第一次…（讓她覺得自己最特別）
3. 沒想到妳怎麼樣…其他人都做不到（反向驚喜誇獎）
4. 我發現妳怎麼樣…（貼正面標籤）
5. 要是有你在就好了…（柔性表達需求）
6. 妳不準怎麼樣…不然我就會…（霸道關心建立主導權）

輸出格式必須完全如下（用中文）：
---
**推薦話術 1**（句型名稱）
「實際要說的話，直接替換成她的名字和情境」

**底層邏輯**：xxx
**預期反應**：xxx

（依序輸出 4 句）
---

記得要自然、真誠、不要太油。根據當前關係階段和情境選擇最適合的句型。"""

    with st.spinner("Grok 正在為你深度分析情境並生成話術..."):
        response = client.chat.completions.create(
            model="grok-4",           # 或改成 "grok-4.1-fast" 更便宜
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.75
        )
        result = response.choices[0].message.content

    st.success("✅ Grok 已生成專屬話術！")
    st.markdown(result)
    
    # 複製按鈕
    st.button("📋 複製全部話術", on_click=lambda: st.session_state.update({"copy": result}))
    if st.session_state.get("copy"):
        st.code(result, language=None)
        st.toast("已複製到剪貼簿！", icon="✅")

# ====================== 側邊欄部署教學 ======================
st.sidebar.title("📢 如何讓別人使用？")

st.sidebar.markdown("""
### 1. 本地測試
```bash
pip install -r requirements.txt
streamlit run 哄她AI教練.py
