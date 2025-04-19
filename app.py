import streamlit as st
from utils.seo_analyzer import analyze_seo, extract_meta_tags
from utils.ai_helper import generate_ai_suggestions, improve_content
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# إعداد واجهة المستخدم
st.set_page_config(page_title="SEO AI Assistant", layout="wide")
st.markdown("""
<style>
    .reportview-container {background: #f0f2f6}
    .sidebar .sidebar-content {background: #ffffff}
</style>
""", unsafe_allow_html=True)

# --- الوظائف الرئيسية ---
def main():
    st.sidebar.title("الإعدادات ⚙️")
    analysis_type = st.sidebar.radio("اختر نوع التحليل:", ["مقالة نصية", "رابط URL", "تحميل ملف"])

    st.title("🛠️ مساعد SEO الذكي مع الذكاء الاصطناعي")
    st.markdown("---")

    if analysis_type == "مقالة نصية":
        content = st.text_area("الصق محتوى المقالة هنا 📝", height=300)
        if st.button("بدء التحليل 🚀"):
            with st.spinner('جارِ التحليل...'):
                process_content(content)

    elif analysis_type == "رابط URL":
        url = st.text_input("أدخل رابط URL 🌐")
        if st.button("تحليل الموقع 🔍"):
            with st.spinner('جارِ سحب البيانات...'):
                # أضف هنا كود سحب البيانات من الويب
                pass

    elif analysis_type == "تحميل ملف":
        uploaded_file = st.file_uploader("رفع ملف (DOCX/PDF) 📂", type=["docx", "pdf"])
        if uploaded_file:
            with st.spinner('جارِ معالجة الملف...'):
                # أضف هنا كود قراءة الملفات
                pass

def process_content(content):
    # تحليل SEO
    with st.container():
        st.subheader("📈 تحليل SEO الأساسي")
        col1, col2 = st.columns(2)
        
        with col1:
            keywords = analyze_seo(content)
            st.write("### الكلمات المفتاحية الرئيسية")
            st.dataframe(pd.DataFrame(keywords, columns=["الكلمة", "التكرار"]))
            
        with col2:
            readability = calculate_readability(content)
            st.write("### قابلية القراءة")
            st.metric("درجة الوضوح", f"{readability}/100")

    # تحليل الذكاء الاصطناعي
    with st.container():
        st.subheader("🧠 تحليل الذكاء الاصطناعي المتقدم")
        suggestions = generate_ai_suggestions(content)
        
        tab1, tab2, tab3 = st.tabs(["تحسين المحتوى", "الاقتراحات الإبداعية", "تحليل المنافسين"])
        
        with tab1:
            st.write("### مقترحات التحسين")
            improved_text = improve_content(content)
            st.write(improved_text)
            
        with tab2:
            st.write("### أفكار إبداعية")
            st.write(suggestions.get('ideas', ''))
            
        with tab3:
            st.write("### مقارنة مع المعايير القياسية")
            st.dataframe(pd.DataFrame(suggestions['benchmarks']))

def calculate_readability(text):
    # احسب درجة قابلية القراءة (مثال مبسط)
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?')
    return min(100, int((words / max(sentences, 1)) * 10))

if __name__ == "__main__":
    main()
