import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_review(api_key, text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Sam의 초기 분석
    sam_prompt = f"""
    당신은 AI PhD 졸업생 Sam입니다. 다음 연구 논문을 분석하고 주요 내용을 간단히 설명해주세요:
    {text}
    
    다음 항목들을 포함해주세요:
    - 주요 포인트
    - 연구 방법론
    - 주요 발견사항
    """
    sam_analysis = model.generate_content(sam_prompt).text
    
    # Jenny의 검토 및 개선
    jenny_prompt = f"""
    당신은 AI와 교육 분야의 PhD를 가진 Jenny입니다. Sam의 분석을 검토하고 더 이해하기 쉽게 개선해주세요:
    {sam_analysis}
    
    다음 사항들을 고려해주세요:
    - 더 쉬운 언어로 설명
    - 실제 적용 사례 추가
    - 추가 설명이 필요한 부분 보완
    """
    jenny_review = model.generate_content(jenny_prompt).text
    
    # Will의 최종 검토
    will_prompt = f"""
    당신은 팀 리더 Will입니다. Jenny의 검토를 바탕으로 최종 보고서를 작성해주세요:
    {jenny_review}
    
    다음 구조로 작성해주세요:
    1. 핵심 요약
    2. 연구 주제 소개
    3. 주요 발견 및 방법론
    4. 복잡한 개념의 간단한 설명
    5. 실제 응용 및 시사점
    6. 결론 및 향후 연구 방향
    """
    final_report = model.generate_content(will_prompt).text
    
    return final_report

def main():
    st.title("📚 AI 연구 논문 리뷰 시스템")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요", type="password")
    
    # PDF 파일 업로드
    uploaded_file = st.file_uploader("AI 연구 논문 PDF를 업로드하세요", type=['pdf'])
    
    if uploaded_file and api_key:
        try:
            # PDF에서 텍스트 추출
            text = extract_text_from_pdf(uploaded_file)
            
            if st.button("논문 분석하기"):
                with st.spinner("AI 팀이 논문을 분석 중입니다..."):
                    final_report = generate_review(api_key, text)
                    
                    st.subheader("📋 최종 리뷰 보고서")
                    st.write(final_report)
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
    
    elif not api_key:
        st.warning("API 키를 입력해주세요.")
    
    elif not uploaded_file:
        st.warning("PDF 파일을 업로드해주세요.")

if __name__ == "__main__":
    main() 