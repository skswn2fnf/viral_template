import streamlit as st
import time

def init_session_state():
    """
    앱의 초기 상태(Session State)를 설정합니다.
    새로고침해도 데이터가 유지되도록 합니다.
    """
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        
        # UI State
        if 'platform' not in st.session_state:
            st.session_state['platform'] = 'blog'
        if 'view_mode' not in st.session_state:
            st.session_state['view_mode'] = 'edit'
        
        # Basic Info
        if 'basic_info' not in st.session_state:
            st.session_state['basic_info'] = {
                'brand_name': '세르지오 타키니',
                'model_name': '',
                'campaign_round': '2차화보',
                'posting_date': '',
                'posting_time': '13:00',
                'campaign_type': 'official'
            }
            
        # Blog Data
        if 'blog_data' not in st.session_state:
            st.session_state['blog_data'] = {
                'title_keywords': [{'id': 1, 'text': ''}],
                'sub_keywords': [{'id': 1, 'text': ''}],
                'images': {
                    'model_count': 8,
                    'model_note': '3차 이미지',
                    'sns_count': 2,
                    'sns_url': '',
                    'coupon_capture': True,
                    'mall_link': 'https://sergiotacchini.co.kr/'
                },
                'story': {
                    'target_audience': '트렌디한 2030 여성',
                    'trend': '',
                    'product_strength': '',
                    'campaign_concept': '',
                    'campaign_sub_copy': ''
                }
            }
            
        # Instagram Data
        if 'insta_data' not in st.session_state:
            st.session_state['insta_data'] = {
                'content_type': 'feed',
                'content_size': '1:1',
                'tone_and_manner': '',
                'hashtags': '',
                'reuse_clause': '본 콘텐츠는 브랜드 공식 채널에서 2차 활용될 수 있습니다.',
                'mentions': '@sergiotacchini_kr'
            }
            
        # Youtube Data
        if 'youtube_data' not in st.session_state:
            st.session_state['youtube_data'] = {
                'content_type': 'shorts',
                'key_message': '',
                'required_mentions': '',
                'duration': '',
                'provided_content': {}
            }
            
        # Products
        if 'products' not in st.session_state:
            st.session_state['products'] = [
                {
                    'id': int(time.time() * 1000),
                    'name': '',
                    'price': '',
                    'colors': '',
                    'sizes': '',
                    'features': '',
                    'productCode': '',
                    'productUrl': '',
                    'imageUrl': '',
                    'isMain': True
                }
            ]
            
        # Legal
        if 'legal_text' not in st.session_state:
            st.session_state['legal_text'] = '본 포스팅은 {브랜드명}(으)로부터 원고료 및 제품을 지원받아 작성되었습니다.'

