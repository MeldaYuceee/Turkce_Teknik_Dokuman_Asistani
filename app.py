import streamlit as st

from text_processing import clean_text, split_sentences
from summarizer import create_summary
from keyword_extractor import find_keywords


st.set_page_config(
    page_title="Teknik Metin Özetleyici",
    page_icon="📝",
    layout="centered"
)


def main():
    st.title("Teknik Metin Özetleyici")
    st.write(
        "Türkçe teknik metinleri kısaltın, öne çıkan bilgileri "
        "ve anahtar kelimeleri görün."
    )

    text = st.text_area(
        "Metin",
        height=280,
        placeholder=(
            "Teknik bir makale, rapor veya proje açıklamasını "
            "buraya yapıştırın..."
        )
    )

    summary_count = st.slider(
        "Özet uzunluğu",
        min_value=2,
        max_value=6,
        value=3
    )

    if st.button("Metni Analiz Et"):
        if not text.strip():
            st.warning("Önce analiz edilecek bir metin girin.")
            return

        cleaned_text = clean_text(text)
        sentences = split_sentences(cleaned_text)

        if len(sentences) < 2:
            st.warning("Analiz için en az iki cümle girin.")
            return

        summary = create_summary(
            cleaned_text,
            summary_count
        )

        keywords = find_keywords(
            cleaned_text,
            8
        )

        word_count = len(cleaned_text.split())

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Kelime", word_count)

        with col2:
            st.metric("Cümle", len(sentences))

        st.divider()

        st.subheader("Özet")
        st.write(summary)

        st.subheader("Anahtar Kelimeler")

        if keywords:
            keyword_text = "  •  ".join(keywords)
            st.info(keyword_text)
        else:
            st.write("Uygun anahtar kelime bulunamadı.")

        with st.expander("İşlenen metni göster"):
            st.write(cleaned_text)


if __name__ == "__main__":
    main()
