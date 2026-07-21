import requests
import json
from typing import Optional, Dict

# ==============================================================
# 🎯 الخطوة 1: الإعدادات الأساسية (The Prerequisites)
# وين تحطها؟ في أعلى الملف، أو الأفضل وضعها كـ Environment Variables.
# وش تسوي؟ تضع فيها البيانات التي حصلت عليها من TikTok Developer Portal.
# ==============================================================

TIKTOK_CLIENT_ID = "YOUR_CLIENT_ID"        # <--- ضع معرف التطبيق هنا
TIKTOK_CLIENT_SECRET = "YOUR_CLIENT_SECRET" # <--- ضع السر السري للتطبيق هنا
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"  # نقطة نهاية الحصول على التوكن (مثال)
PROFILE_UPDATE_ENDPOINT = "YOUR_USER_PROFILE_ENDPOINT" # المسار الخاص بتحديث الملف الشخصي

# معلومات الحساب التي نريد تحديثها
TARGET_USER_ID = "1234567890"  # المعرف الفريد للحساب المستهدف على TikTok
NEW_USERNAME = "MyNewCyberNeurovaName" # الاسم الجديد الذي تريد وضعه

# ==============================================================
# 🛠️ الخطوة 2: المكتبات (تم التثبيت مسبقاً عبر pip install requests)
# وش تسوي؟ هذه هي الأداة التي سنتعامل بها مع طلبات الويب.
# ==============================================================

def get_tiktok_token(client_id: str, client_secret: str, token_url: str) -> Optional[str]:
    """
    🎯 الخطوة 3: تطبيق منطق المصادقة (Token Generator)
    يحصل هذا الجزء على المفتاح المؤقت اللازم للوصول إلى الـ API.
    """
    print("--- [المرحلة 1/4] محاولة الحصول على Access Token ---")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        # قد تحتاج أيضاً إلى grant_type (مثل 'authorization_code') حسب آلية المصادقة التي تتبعها TikTok API.
        'grant_type': 'client_credentials'
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()  # يثير استثناء إذا كان هناك خطأ HTTP (4xx أو 5xx)

        token_data = response.json()
        access_token = token_data.get('access_token')

        if access_token:
            print(f"✅ نجاح في الحصول على التوكن. صالح لمدة {token_data.get('expires_in', 'غير محدد')} ثانية.")
            return access_token
        else:
            print("❌ فشل: لم يتم العثور على Access Token في الردود.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 خطأ أثناء الاتصال بـ TikTok API للحصول على التوكن: {e}")
        return None


def update_username(user_id: str, new_name: str, token: str, endpoint: str) -> bool:
    """
    🎯 الخطوة 4: تطبيق منطق التحديث الفعلي (The Business Logic)
    يرسل هذا الجزء طلب PUT لتنفيذ تغيير اسم المستخدم.
    """
    print("\n--- [المرحلة 2/4] بدء عملية تحديث الاسم ---")

    # هيكل البيانات المراد إرسالها في الطلب (حسب متطلبات API TikTok)
    payload = {
        "username": new_name, # افتراضياً، هذا هو المفتاح المطلوب لتحديث الاسم
        # قد تحتاج إلى حقول أخرى مثل bio أو display_name حسب الـ Endpoint المحدد.
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" # وضع التوكن في الرأس هو مفتاح المصادقة الفعالة
    }

    try:
        # يتم إرسال الطلب إلى المسار الذي حددناه لـ تحديث الملف الشخصي
        response = requests.put(endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # التحقق من نجاح الطلب (200 OK)

        # تحليل الاستجابة لتحديد النجاح أو الفشل بدقة
        result = response.json()
        if result and result.get('success'):
            print(f"✅ تم التحديث بنجاح! الاسم الجديد هو: {new_name}")
            return True
        else:
            # هذا يعني أن الطلب وصل لـ API لكنه رفض التنفيذ منطقياً (مثل اسم مكرر)
            error = result.get('message', 'غير محدد')
            print(f"⚠️ فشل التحديث من ناحية المنطق الداخلي للـ API. الرسالة: {error}")
            return False

    except requests.exceptions.HTTPError as http_err:
        # هذا يعني أن الرد كان خطأ HTTP (مثل 401 Unauthorized, 404 Not Found)
        print(f"❌ فشل التحديث بسبب الخطأ HTTP: {http_err}")
        try:
            # محاولة طباعة تفاصيل الخطأ من جسم الاستجابة نفسها إن وجدت
            error_details = response.json()
            print(f"   تفاصيل خطأ TikTok API: {error_details}")
        except json.JSONDecodeError:
             print("   لم نستطع قراءة تفاصيل الخطأ لأن الرد لم يكن بصيغة JSON.")
        return False

    except requests.exceptions.RequestException as e:
        # فشل الاتصال بالإنترنت أو مشاكل أخرى في الشبكة
        print(f"🚨 خطأ عام أثناء محاولة التحديث: {e}")
        return False


# ==============================================================
# 🚀 الخطوة 5: تشغيل النظام (The Execution) - الدالة الرئيسية
# وين تحطها؟ هذا هو مدخل البرنامج الذي يبدأ كل شيء.
# وش تسوي؟ تضع هنا سلسلة التنفيذ بالترتيب الصحيح للعمليات المتسلسلة.
# ==============================================================

if __name__ == "__main__":
    print("==============================================")
    print("🤖 نظام تحديث TikTok الآلي جاهز للتشغيل!")
    print("==============================================")

    # 1. جلب التوكن (الخطوة 3)
    token = get_tiktok_token(TIKTOK_CLIENT_ID, TIKTOK_CLIENT_SECRET, TOKEN_URL)

    if token:
        # 2. إذا نجح الحصول على التوكن، قم بتنفيذ عملية التحديث (الخطوة 4)
        success = update_username(TARGET_USER_ID, NEW_USERNAME, token, PROFILE_UPDATE_ENDPOINT)

        # 3. طباعة النتيجة النهائية للنظام كله (الخطوة 5)
        print("\n==============================================")
        if success:
            print("🎉 العملية الكلية تمت بنجاح.")
        else:
            print("❌ فشلت العملية الكلية في إتمام التحديث المطلوب.")
        print("==============================================")

    else:
        print("\n🚫 لا يمكن المتابعة: لم يتم الحصول على توكن صالح. يجب مراجعة الإعدادات (الخطوة 1).")