import streamlit as st
from tiktok_updater import update_username # استيراد الدالة التي كتبناها سابقاً

# إعداد عنوان الصفحة وتوصيل الأداة
st.set_page_config(page_title="TikTok Username Changer", layout="wide")

st.title("⚙️ أداة تغيير اسم مستخدم تيك توك")
st.write("استخدم هذه الأداة لتحديث الـ @Handle الخاص بحسابك على TikTok عبر واجهة برمجة التطبيقات (API).")

# ------------------- المدخلات من المستخدم -------------------
with st.form("username_update_form"):
    old_user = st.text_input("1. اسم المستخدم الحالي (Username):", placeholder="أدخل @اسمك القديم")
    new_user = st.text_input("2. الاسم الجديد المراد تعيينه:", placeholder="أدخل الاسم الذي تريده جديداً")
    submit_button = st.form_submit_button(label='🚀 بدء عملية التغيير')

# ------------------- منطق التنفيذ -------------------
if submit_button:
    if not old_user or not new_user:
        st.error("🛑 الرجاء ملء كلا الحقلين (القديم والجديد) للمتابعة.")
    else:
        st.info(f"⏳ جاري محاولة تغيير الاسم من **{old_user}** إلى **{new_user}**...")
       # استدعاء دالة التوكن من ملف get_tiktok_token
        from get_tiktok_token import get_tiktok_token
        
        # حط معلوماتك الخاصة بـ TikTok API هنا
        client_id = "awt2ygdl113f74a6"
        client_secret = "zIbDi4KAg4O6k4Wdth3tBWe4fqskh0cc"
        
        # الحصول على التوكن
        token_response = get_tiktok_token(client_id, client_secret)
        token = token_response.get("access_token", "")
        
        # الـ Endpoint المطلوب
        endpoint = "https://open.tiktokapis.com/v2/user/info/get/"
        
        # استدعاء الدالة الرئيسية
        result = update_username(old_user, new_user, token, endpoint)
        # استدعاء الدالة الرئيسية من الملف السابق
        
        
    st.subheader("✅ حالة العملية:")
    if result:
            st.balloons()
            st.success("🎉 نجاح! تم تحديث اسم المستخدم بنجاح.")
    else:
            st.error("❌ فشل التحديث! تحقق من البيانات أو التوكن.")
# ------------------- نصائح إضافية -------------------
st.sidebar.header("💡 ملاحظات هامة")
st.sidebar.markdown("""
*   **أهم خطوة:** يجب عليك الحصول على **Access Token** صالح من TikTok أولاً ووضعه في ملف `tiktok_updater.py`.
*   **التوثيق (API):** هذا الكود يعتمد على نقطة نهاية محددة؛ قد تحتاج إلى مراجعة التوثيق الرسمي لتيك توك إذا فشل الاتصال.
""")