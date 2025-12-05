import streamlit as st
from utils.state_manager import init_session_state
from views.edit_mode import render_edit_mode
from views.preview_mode import render_preview_mode

# 페이지 설정 (가장 먼저 실행되어야 함)
st.set_page_config(
    page_title="Viral Guideline Template",
    page_icon="✨",
    layout="wide"
)

# 세션 상태 초기화
init_session_state()

# CSS 스타일링 (폰트 등)
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: 'Noto Sans KR', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 뷰 모드에 따른 렌더링
if st.session_state['view_mode'] == 'edit':
    render_edit_mode()
else:
    render_preview_mode()

