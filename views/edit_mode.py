import streamlit as st
import time
from data.product_db import fetch_product_info

def render_edit_mode():
    st.title("✨ 바이럴 가이드라인 템플릿")
    st.caption("플랫폼별 맞춤 가이드라인을 빠르게 작성하세요")

    # 플랫폼 선택 (Tabs)
    platforms = ["blog", "instagram", "youtube"]
    labels = ["📖 블로그", "📷 인스타그램", "🎬 유튜브"]
    
    # 현재 선택된 플랫폼의 인덱스 찾기
    current_index = platforms.index(st.session_state['platform'])
    selected_tab = st.radio("플랫폼 선택", labels, index=current_index, horizontal=True, label_visibility="collapsed")
    
    # 선택에 따라 상태 업데이트
    if selected_tab == "📖 블로그":
        st.session_state['platform'] = 'blog'
    elif selected_tab == "📷 인스타그램":
        st.session_state['platform'] = 'instagram'
    else:
        st.session_state['platform'] = 'youtube'

    st.markdown("---")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        # 1. 기본 정보 섹션
        with st.expander("📄 기본 정보", expanded=True):
            basic = st.session_state['basic_info']
            
            # 캠페인 타입 토글
            c_type = st.radio("캠페인 타입", ["official", "hidden"], 
                            format_func=lambda x: "📢 오피셜" if x == "official" else "🔒 히든",
                            index=0 if basic['campaign_type'] == 'official' else 1,
                            horizontal=True)
            basic['campaign_type'] = c_type

            b_col1, b_col2 = st.columns(2)
            basic['brand_name'] = b_col1.text_input("브랜드명", value=basic['brand_name'])
            basic['model_name'] = b_col2.text_input("모델/인플루언서", value=basic['model_name'], placeholder="예: 박지현")
            
            b_col3, b_col4, b_col5 = st.columns(3)
            basic['campaign_round'] = b_col3.text_input("캠페인 회차", value=basic['campaign_round'])
            basic['posting_date'] = b_col4.text_input("포스팅 날짜", value=basic['posting_date'], placeholder="YYYY-MM-DD")
            basic['posting_time'] = b_col5.text_input("포스팅 시간", value=basic['posting_time'], placeholder="13:00")

        # 2. 제품 정보 섹션
        with st.expander("📦 제품 정보", expanded=True):
            st.info("🔗 Sergio Tacchini 공식몰 제품 URL을 입력하면 정보가 자동 채워집니다.")
            
            url_col1, url_col2 = st.columns([3, 1])
            url_input = url_col1.text_input("제품 URL 입력", key="url_input_field")
            
            if url_col2.button("가져오기"):
                with st.spinner("제품 정보 조회 중..."):
                    new_product = fetch_product_info(url_input)
                    if new_product:
                        # 첫 번째 빈 제품이 있으면 덮어쓰기, 아니면 추가
                        products = st.session_state['products']
                        if len(products) == 1 and not products[0]['name']:
                            st.session_state['products'] = [new_product]
                        else:
                            st.session_state['products'].append(new_product)
                        st.success("제품 추가 완료!")
                        time.sleep(1) # 성공 메시지 보여주기
                        st.rerun()
                    else:
                        st.error("제품을 찾을 수 없습니다.")

            # 제품 리스트 렌더링
            products = st.session_state['products']
            for idx, p in enumerate(products):
                st.markdown(f"**Product {idx + 1}**")
                with st.container(border=True):
                    # 이미지와 내용을 나누기 위한 컬럼 (1:4 비율)
                    img_col, content_col = st.columns([1, 4])
                    
                    with img_col:
                        if p.get('imageUrl'):
                            st.image(p['imageUrl'], use_container_width=True)
                        else:
                            st.container(height=100, border=True).markdown("<div style='text-align:center; padding-top:30px; color:#ccc;'>No Image</div>", unsafe_allow_html=True)

                    with content_col:
                        # 메인 제품 체크 및 삭제 버튼
                        h_col1, h_col2 = st.columns([4, 1])
                        p['isMain'] = h_col1.checkbox("★ 메인 제품으로 설정", value=p.get('isMain', False), key=f"main_{p['id']}")
                        if h_col2.button("삭제", key=f"del_{p['id']}"):
                            if len(products) > 1:
                                products.pop(idx)
                                st.rerun()
                            else:
                                # 다 지워도 빈 폼 하나는 남김
                                products[idx] = {
                                    'id': int(time.time() * 1000), 'name': '', 'price': '', 
                                    'colors': '', 'sizes': '', 'features': '', 
                                    'productCode': '', 'productUrl': '', 'imageUrl': '', 'isMain': False
                                }
                                st.rerun()

                        p_col1, p_col2 = st.columns(2)
                        p['name'] = p_col1.text_input("제품명", value=p['name'], key=f"name_{p['id']}")
                        p['productCode'] = p_col2.text_input("상품코드", value=p['productCode'], key=f"code_{p['id']}")
                        
                        p_col3, p_col4, p_col5 = st.columns(3)
                        p['price'] = p_col3.text_input("가격", value=p['price'], key=f"price_{p['id']}")
                        p['colors'] = p_col4.text_input("컬러", value=p['colors'], key=f"colors_{p['id']}")
                        p['sizes'] = p_col5.text_input("사이즈", value=p['sizes'], key=f"sizes_{p['id']}")
                    
                    # 특징은 아래에 넓게 배치
                    p['features'] = st.text_area("특징", value=p['features'], key=f"feat_{p['id']}", height=150)

            if st.button("➕ 제품 직접 추가"):
                st.session_state['products'].append({
                    'id': int(time.time() * 1000), 'name': '', 'price': '', 
                    'colors': '', 'sizes': '', 'features': '', 
                    'productCode': '', 'productUrl': '', 'imageUrl': '', 'isMain': False
                })
                st.rerun()

        # 3. 플랫폼별 섹션
        platform = st.session_state['platform']
        
        if platform == 'blog':
            blog = st.session_state['blog_data']
            with st.expander("🏷️ 키워드 설정", expanded=True):
                st.caption("필수 제목 키워드 (콤마로 구분)")
                # 단순화를 위해 리스트 UI 대신 텍스트 입력 후 분리 방식으로 변경
                title_kw_str = ", ".join([k['text'] for k in blog['title_keywords'] if k['text']])
                new_title_kw = st.text_input("필수 키워드", value=title_kw_str, placeholder="예: 여성패딩, 숏패딩")
                # 저장 로직
                blog['title_keywords'] = [{'id': i, 'text': t.strip()} for i, t in enumerate(new_title_kw.split(','))]

                st.caption("서브 키워드 (콤마로 구분)")
                sub_kw_str = ", ".join([k['text'] for k in blog['sub_keywords'] if k['text']])
                new_sub_kw = st.text_input("서브 키워드", value=sub_kw_str)
                blog['sub_keywords'] = [{'id': i, 'text': t.strip()} for i, t in enumerate(new_sub_kw.split(','))]

            with st.expander("🖼️ 활용 이미지", expanded=True):
                i_col1, i_col2 = st.columns(2)
                blog['images']['model_count'] = i_col1.number_input("모델 이미지 장수", value=int(blog['images']['model_count']))
                blog['images']['model_note'] = i_col2.text_input("이미지 구분", value=blog['images']['model_note'])
                
                blog['images']['sns_url'] = st.text_input("SNS 캡쳐 URL", value=blog['images']['sns_url'])
                blog['images']['mall_link'] = st.text_input("자사몰 링크", value=blog['images']['mall_link'])

            with st.expander("✨ 스토리라인", expanded=True):
                blog['story']['target_audience'] = st.text_input("타겟 오디언스", value=blog['story']['target_audience'])
                blog['story']['trend'] = st.text_area("트렌드 배경", value=blog['story']['trend'])
                blog['story']['product_strength'] = st.text_area("제품 특장점", value=blog['story']['product_strength'])
                blog['story']['campaign_concept'] = st.text_input("캠페인 컨셉", value=blog['story']['campaign_concept'])

        elif platform == 'instagram':
            insta = st.session_state['insta_data']
            with st.expander("📐 콘텐츠 스펙", expanded=True):
                i_col1, i_col2 = st.columns(2)
                insta['content_type'] = i_col1.selectbox("콘텐츠 유형", ['feed', 'reels', 'story', 'carousel'], 
                                                         index=['feed', 'reels', 'story', 'carousel'].index(insta['content_type']))
                insta['content_size'] = i_col2.selectbox("사이즈", ['1:1', '4:5', '9:16', '1.91:1'], 
                                                         index=['1:1', '4:5', '9:16', '1.91:1'].index(insta['content_size']))
                insta['mentions'] = st.text_input("멘션 계정", value=insta['mentions'])
            
            with st.expander("🎨 톤앤매너", expanded=True):
                insta['tone_and_manner'] = st.text_area("톤앤매너 가이드", value=insta['tone_and_manner'])
                insta['hashtags'] = st.text_area("해시태그", value=insta['hashtags'])
            
            with st.expander("♻️ 2차 활용", expanded=True):
                insta['reuse_clause'] = st.text_area("2차 활용 문구", value=insta['reuse_clause'])

        elif platform == 'youtube':
            yt = st.session_state['youtube_data']
            with st.expander("🎬 콘텐츠 스펙", expanded=True):
                y_col1, y_col2 = st.columns(2)
                yt['content_type'] = y_col1.selectbox("콘텐츠 유형", ['shorts', 'review', 'vlog', 'integration'],
                                                      index=['shorts', 'review', 'vlog', 'integration'].index(yt['content_type']))
                yt['duration'] = y_col2.text_input("권장 영상 길이", value=yt['duration'])
            
            with st.expander("💬 희망 메시지", expanded=True):
                yt['key_message'] = st.text_area("대표 메시지", value=yt['key_message'])
                yt['required_mentions'] = st.text_area("필수 멘트", value=yt['required_mentions'])

        # 4. 공통 법적 문구
        with st.expander("⚖️ 필수 기재 문구", expanded=True):
            st.session_state['legal_text'] = st.text_area("법적 문구", value=st.session_state['legal_text'])
            st.caption("💡 '{브랜드명}'은 자동으로 치환됩니다")

    # 우측 미리보기 패널 (Sticky 느낌으로 구현 어려우므로 그냥 컬럼에 배치)
    with col2:
        st.subheader("👁️ 텍스트 미리보기")
        from utils.text_generator import generate_plain_text
        
        generated_text = generate_plain_text(st.session_state)
        
        st.text_area("결과물", value=generated_text, height=600, label_visibility="collapsed")
        
        if st.button("공유용 미리보기 페이지 열기", type="primary", use_container_width=True):
            st.session_state['view_mode'] = 'preview'
            st.rerun()
