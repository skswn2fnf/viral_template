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
                'campaign_type': 'official',
                'main_image': ''  # 메인 화보 이미지 (썸네일)
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
                'brand_mention': '',
                'celeb_mention': ''
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
        
        # Review Blog Data (리뷰 블로그)
        if 'review_blog_data' not in st.session_state:
            st.session_state['review_blog_data'] = {
                # 필수 키워드
                'title_keywords': {
                    'required': [{'id': 1, 'text': ''}],  # 필수 제목 키워드
                    'optional': [{'id': 1, 'text': ''}]   # 선택 제목 키워드
                },
                'body_keywords': {
                    'brand': '',    # BRAND 키워드
                    'item': '',     # ITEM 키워드
                    'style': ''     # STYLE 키워드
                },
                # 브랜드 소개
                'brand_intro': '',
                # 제품 소개 가이드
                'product_guide': '제품 정보 참고하여 상세히 리뷰 부탁드립니다.',
                # 스타일링 가이드
                'styling': {
                    'concept': '',           # 스타일링 컨셉
                    'matching_items': '',    # 매칭 아이템
                    'other_notes': ''        # 기타 안내 (브라탑 착용 등)
                },
                # 필수 촬영 앵글
                'required_angles': {
                    'full_body': True,       # 전신샷
                    'upper_body': True,      # 상반신샷
                    'mirror': False,         # 거울샷
                    'detail': False,         # 디테일샷
                    'custom': ''             # 기타 앵글
                },
                # 톤앤매너
                'tone_and_manner': '',
                # 이미지 분량
                'min_images': 10,
                # 포스팅 가이드
                'posting_guide': '본인의 말투로 친근하게 워싱해서 작성 필수'
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

