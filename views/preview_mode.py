import streamlit as st

def render_preview_mode():
    state = st.session_state
    basic = state['basic_info']
    platform = state['platform']
    
    # 상단 네비게이션
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅ 편집으로 돌아가기"):
            state['view_mode'] = 'edit'
            st.rerun()
    
    # 스타일링 및 헤더
    platform_colors = {
        'blog': 'green',
        'instagram': 'purple',
        'youtube': 'red'
    }
    color = platform_colors.get(platform, 'gray')
    
    st.markdown(f"""
    <div style="background-color: {color}; padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h1>{basic['brand_name']}</h1>
        <h3>{basic['model_name']} {basic['campaign_round']} | {platform.upper()} 가이드라인</h3>
        <span style="background: rgba(255,255,255,0.3); padding: 5px 10px; border-radius: 15px; font-size: 0.8em;">
            {'📢 오피셜' if basic['campaign_type'] == 'official' else '🔒 히든'}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # 포스팅 기한 (배경 적용)
    st.markdown(f"""
    <div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: #856404; border: 1px solid #ffeeba;">
        📅 <strong>포스팅 기한</strong>: {basic['posting_date']} {basic['posting_time']} 이후
    </div>
    """, unsafe_allow_html=True)

    # 1. 플랫폼별 상세 가이드 (상단)
    if platform == 'blog':
        blog = state['blog_data']
        
        # 키워드 섹션
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
        st.subheader("🏷️ 키워드 설정")
        st.markdown("**필수 제목 키워드**")
        st.markdown(" ".join([f"`{k['text']}`" for k in blog['title_keywords'] if k['text']]))
        st.markdown("**서브 키워드**")
        st.markdown(" ".join([f"`{k['text']}`" for k in blog['sub_keywords'] if k['text']]))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 활용 이미지 섹션
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
        st.subheader("🖼️ 활용 이미지")
        st.markdown(f"- {basic['model_name']} {blog['images']['model_note']} **{blog['images']['model_count']}장** 이상")
        if blog['images']['sns_url']:
            st.markdown(f"- SNS 캡쳐 **{blog['images']['sns_count']}장** 이상")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 스토리라인 섹션
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
        st.subheader("📖 스토리라인")
        st.markdown(f"**타겟**: {blog['story']['target_audience']}")
        if blog['story']['campaign_concept']:
            st.markdown(f"**컨셉**: {blog['story']['campaign_concept']}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif platform == 'instagram':
        insta = state['insta_data']
        
        # 콘텐츠 스펙
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
        st.subheader("📐 콘텐츠 스펙")
        c1, c2 = st.columns(2)
        c1.metric("유형", insta['content_type'])
        c2.metric("사이즈", insta['content_size'])
        st.markdown(f"**멘션**: `{insta['mentions']}`")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 톤앤매너
        if insta['tone_and_manner']:
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
            st.subheader("🎨 톤앤매너")
            st.info(insta['tone_and_manner'])
            st.markdown('</div>', unsafe_allow_html=True)
            
        # 2차 활용
        st.markdown('<div style="background-color: #fff0f3; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #ffccd5;">', unsafe_allow_html=True)
        st.subheader("♻️ 2차 활용")
        st.markdown(f"**{insta['reuse_clause']}**")
        st.markdown('</div>', unsafe_allow_html=True)

    elif platform == 'youtube':
        yt = state['youtube_data']
        
        # 콘텐츠 스펙
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
        st.subheader("🎬 콘텐츠 스펙")
        c1, c2 = st.columns(2)
        c1.metric("유형", yt['content_type'])
        c2.metric("권장 길이", yt['duration'] or "자유")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if yt['key_message']:
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px;">', unsafe_allow_html=True)
            st.subheader("💬 희망 메시지")
            st.info(yt['key_message'])
            st.markdown('</div>', unsafe_allow_html=True)

    # 2. 법적 문구
    final_legal = state['legal_text'].replace('{브랜드명}', basic['brand_name'])
    st.markdown(f"""
    <div style="background-color: #e9ecef; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin-top:0;">⚖️ 필수 기재 문구</h3>
        <code style="display:block; padding:15px; background:white; border-radius:5px;">{final_legal}</code>
    </div>
    """, unsafe_allow_html=True)

    # 3. 제품 정보 (하단)
    st.markdown('<div style="background-color: #f1f3f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.subheader("📦 제품 정보")
    
    valid_products = [p for p in state['products'] if p.get('name') or p.get('productCode')]
    
    if not valid_products:
        st.info("입력된 제품 정보가 없습니다. 편집 탭에서 제품을 추가해주세요.")
    else:
        for p in valid_products:
            with st.container(border=True):
                # 제품 카드 내부는 흰색 유지 (st.container 기본값)
                title_prefix = "★ [메인]" if p.get('isMain') else ""
                
                img_col, text_col = st.columns([1, 3])
                
                with img_col:
                    if p.get('imageUrl'):
                        st.image(p['imageUrl'], use_container_width=True)
                    else:
                        st.markdown("<div style='height:150px; background-color:#f0f2f6; display:flex; align-items:center; justify-content:center; color:#aaa;'>No Image</div>", unsafe_allow_html=True)
                
                with text_col:
                    product_name = p.get('name', '제품명 미입력')
                    st.markdown(f"### {title_prefix} {product_name}")
                    
                    cols = st.columns(3)
                    cols[0].markdown(f"**가격**: {p.get('price', '-')}")
                    cols[1].markdown(f"**컬러**: {p.get('colors', '-')}")
                    cols[2].markdown(f"**사이즈**: {p.get('sizes', '-')}")
                    
                    if p.get('productCode'):
                        st.caption(f"Code: {p['productCode']}")
                    
                    if p.get('features'):
                        st.markdown(f"**특징**:\n{p['features']}")
                    
                    if p.get('productUrl'):
                        st.markdown(f"[제품 상세보기]({p['productUrl']})")
    st.markdown('</div>', unsafe_allow_html=True)
