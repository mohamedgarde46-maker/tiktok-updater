import streamlit as st
from get_tiktok_token import get_tiktok_token
import requests

# إعدادات الواجهة
st.set_page_config(page_title="مستعرض بيانات تيك توك", page_icon="🎵")

st.title("🎵 عرض بيانات حساب تيك توك")
st.write("استخدم هذه الأداة لجلب معلومات الحساب عبر API الرسمي.")

# نموذج إدخال البيانات
with st.form("user_info_form"):
    client_id = st.text_input("Client Key:", type="password")
    client_secret = st.text_input("Client Secret:", type="password")
    submit_button = st.form_submit_button("🔍 جلب البيانات")

if submit_button:
    if not client_id or not client_secret:
        st.error("❌ الرجاء إدخال الـ Client Key والـ Client Secret!")
    else:
        st.info("⏳ جاري الاتصال بـ TikTok API...")
        
        # 1. الحصول على Access Token
        token_data = get_tiktok_token(client_id, client_secret)
        access_token = token_data.get("access_token")
        
        if access_token:
            # 2. طلب بيانات المستخدم
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            # الـ Endpoint الرسمي لقراءة البيانات
            url = "https://open.tiktokapis.com/v2/user/info/get/?fields=open_id,union_id,avatar_url,display_name"
            
            response = requests.get(url, headers=headers)
            res_json = response.json()
            
            if response.status_code == 200 and "data" in res_json:
                user_info = res_json["data"]["user"]
                st.success("✅ تم جلب البيانات بنجاح!")
                
                # عرض البيانات بالواجهة
                st.image(user_info.get("avatar_url"), width=150)
                st.subheader(f"الاسم: {user_info.get('display_name')}")
                st.json(res_json)
            else:
                st.error("❌ فشل في جلب البيانات من تيك توك.")
                st.write("استجابة السيرفر:", res_json)
        else:
            st.error("❌ فشل الحصول على Access Token! تحقق من المفاتيح.")
