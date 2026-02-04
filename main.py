import streamlit as st
from utils.state_manager import init_session_state
from views.edit_mode import render_edit_mode
from views.preview_mode import render_preview_mode
from views.seeding_map import render_seeding_map

# 페이지 설정 (가장 먼저 실행되어야 함)
st.set_page_config(
    page_title="Viral Guideline Template",
    page_icon="✨",
    layout="wide"
)

# 세션 상태 초기화
init_session_state()

# 앱 모드 초기화
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = 'guideline'

# CSS 스타일링 (폰트 등)
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: 'Noto Sans KR', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 사이드바 메뉴
with st.sidebar:
    st.markdown("### 🔧 메뉴")
    app_mode = st.radio(
        "기능 선택",
        ["✨ 가이드라인 템플릿", "📊 시딩 맵"],
        index=0 if st.session_state['app_mode'] == 'guideline' else 1,
        label_visibility="collapsed"
    )
    
    if app_mode == "✨ 가이드라인 템플릿":
        st.session_state['app_mode'] = 'guideline'
    else:
        st.session_state['app_mode'] = 'seeding_map'
    
    st.markdown("---")
    st.caption("© 2026 Viral Template")

# 앱 모드에 따른 렌더링
if st.session_state['app_mode'] == 'seeding_map':
    render_seeding_map()
else:
    # 기존 가이드라인 모드
    if st.session_state['view_mode'] == 'edit':
        render_edit_mode()
    else:
        render_preview_mode()

