import streamlit as st
# import pypdf

def main():
    st.title("CV Matcher")

    # Секция для ввода описания вакансии
    st.header("Описание вакансии")
    job_description = st.text_area(
        "Вставьте описание вакансии",
        height=200,
        placeholder="Например: Ищем Python разработчика с опытом работы от 3 лет..."
    )
    
    # Секция для загрузки резюме
    st.header("Загрузка резюме")
    uploaded_file = st.file_uploader("Загрузите ваше резюме в формате PDF", type=['pdf'])
    
    # Кнопка для запуска сравнения
    if st.button("🎯 Сравнить", type="primary"):
        if not job_description:
            st.error("Пожалуйста, введите описание вакансии")
            return
        if not uploaded_file:
            st.error("Пожалуйста, загрузите резюме")
            return
            
        # Здесь будет логика сравнения
        with st.spinner("Анализируем соответствие..."):
            # Заглушка для демонстрации
            st.success("Анализ завершен!")
            
            # Общий результат
            st.header("Результаты сравнения")
            col1, _, _ = st.columns(3)
            with col1:
                st.metric("Общее соответствие", "75%")
            
            # Детальный анализ
            st.subheader("Детальный анализ")
            with st.expander("Посмотреть детали"):
                st.write("🔹 Технические навыки")
                st.progress(0.8, text="Python (80%)")
                st.progress(0.6, text="SQL (60%)")
                st.progress(0.9, text="Git (90%)")
                
                st.write("🔹 Soft skills")
                st.progress(0.7, text="Командная работа (70%)")
                st.progress(0.8, text="Коммуникация (80%)")

if __name__ == "__main__":
    st.set_page_config(
        page_title="CV Matcher",
        page_icon="📄",
        layout="wide"
    )
    main() 