import streamlit as st
import PyPDF2

def main():
    st.title("CV Matcher")

    st.header("Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="For example: Looking for a Python developer with 3+ years of experience..."
    )
    
    st.header("CV Upload")
    uploaded_file = st.file_uploader("Upload your CV in PDF format", type=['pdf'])
    if uploaded_file is not None:
        with st.expander("View Uploaded CV"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            cv_text = ""
            for page in pdf_reader.pages:
                cv_text += page.extract_text()
            st.text_area("CV Content", cv_text, height=300)

    if st.button("🎯 Compare", type="primary"):
        if not job_description:
            st.error("Please enter the job description")
            return
        if not uploaded_file:
            st.error("Please upload your CV")
            return
            
        with st.spinner("Analyzing match..."):
            st.success("Analysis complete!")
            
            st.header("Comparison Results")
            col1, _, _ = st.columns(3)
            with col1:
                st.metric("Overall Match", "75%")
            
            st.subheader("Detailed Analysis")
            with st.expander("View Details"):
                st.write("🔹 Technical Skills")
                st.progress(0.8, text="Python (80%)")
                st.progress(0.6, text="SQL (60%)")
                st.progress(0.9, text="Git (90%)")
                
                st.write("🔹 Soft Skills")
                st.progress(0.7, text="Teamwork (70%)")
                st.progress(0.8, text="Communication (80%)")

if __name__ == "__main__":
    st.set_page_config(
        page_title="CV Matcher",
        page_icon="📄",
        layout="wide"
    )
    main() 