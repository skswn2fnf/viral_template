import streamlit as st
from datetime import datetime

def generate_shareable_html(state):
    """
    외부 공유용 완전한 HTML 파일을 생성합니다.
    모든 스타일이 인라인으로 포함되어 독립적으로 볼 수 있습니다.
    """
    basic = state['basic_info']
    platform = state['platform']
    
    platform_colors = {
        'blog': '#28a745',
        'instagram': '#833ab4',
        'youtube': '#ff0000'
    }
    color = platform_colors.get(platform, '#6c757d')
    
    platform_names = {
        'blog': '블로그',
        'instagram': '인스타그램',
        'youtube': '유튜브'
    }
    
    # 플랫폼별 섹션 HTML 생성
    platform_section = ""
    
    if platform == 'blog':
        blog = state['blog_data']
        title_keywords = " ".join([f'<span class="keyword">{k["text"]}</span>' for k in blog['title_keywords'] if k['text']])
        sub_keywords = " ".join([f'<span class="keyword sub">{k["text"]}</span>' for k in blog['sub_keywords'] if k['text']])
        
        platform_section = f"""
        <div class="section">
            <h2>🏷️ 키워드 설정</h2>
            <div class="keyword-group">
                <strong>필수 제목 키워드</strong>
                <div class="keywords">{title_keywords}</div>
            </div>
            <div class="keyword-group">
                <strong>서브 키워드</strong>
                <div class="keywords">{sub_keywords}</div>
            </div>
        </div>
        <div class="section">
            <h2>🖼️ 활용 이미지</h2>
            <ul>
                <li>{basic['model_name']} {blog['images']['model_note']} <strong>{blog['images']['model_count']}장</strong> 이상</li>
                {'<li>SNS 캡쳐 <strong>' + str(blog['images']['sns_count']) + '장</strong> 이상</li>' if blog['images']['sns_url'] else ''}
            </ul>
        </div>
        <div class="section">
            <h2>📖 스토리라인</h2>
            <p><strong>타겟</strong>: {blog['story']['target_audience']}</p>
            {'<p><strong>컨셉</strong>: ' + blog['story']['campaign_concept'] + '</p>' if blog['story']['campaign_concept'] else ''}
        </div>
        """
    
    elif platform == 'instagram':
        insta = state['insta_data']
        platform_section = f"""
        <div class="section">
            <h2>📐 콘텐츠 스펙</h2>
            <div class="metrics">
                <div class="metric">
                    <span class="label">유형</span>
                    <span class="value">{insta['content_type']}</span>
                </div>
                <div class="metric">
                    <span class="label">사이즈</span>
                    <span class="value">{insta['content_size']}</span>
                </div>
            </div>
            <p><strong>멘션</strong>: <code>{insta['mentions']}</code></p>
        </div>
        {'<div class="section"><h2>🎨 톤앤매너</h2><div class="info-box">' + insta['tone_and_manner'] + '</div></div>' if insta['tone_and_manner'] else ''}
        <div class="section highlight-pink">
            <h2>♻️ 2차 활용</h2>
            <p><strong>{insta['reuse_clause']}</strong></p>
        </div>
        """
    
    elif platform == 'youtube':
        yt = state['youtube_data']
        platform_section = f"""
        <div class="section">
            <h2>🎬 콘텐츠 스펙</h2>
            <div class="metrics">
                <div class="metric">
                    <span class="label">유형</span>
                    <span class="value">{yt['content_type']}</span>
                </div>
                <div class="metric">
                    <span class="label">권장 길이</span>
                    <span class="value">{yt['duration'] or '자유'}</span>
                </div>
            </div>
        </div>
        {'<div class="section"><h2>💬 희망 메시지</h2><div class="info-box">' + yt['key_message'] + '</div></div>' if yt['key_message'] else ''}
        """
    
    # 제품 정보 HTML 생성
    products_html = ""
    valid_products = [p for p in state['products'] if p.get('name') or p.get('productCode')]
    
    if valid_products:
        for p in valid_products:
            main_badge = '<span class="main-badge">★ 메인</span>' if p.get('isMain') else ''
            img_html = f'<img src="{p["imageUrl"]}" alt="제품 이미지">' if p.get('imageUrl') else '<div class="no-image">No Image</div>'
            
            products_html += f"""
            <div class="product-card">
                <div class="product-image">{img_html}</div>
                <div class="product-info">
                    <h3>{main_badge} {p.get('name', '제품명 미입력')}</h3>
                    <div class="product-details">
                        <span><strong>가격</strong>: {p.get('price', '-')}</span>
                        <span><strong>컬러</strong>: {p.get('colors', '-')}</span>
                        <span><strong>사이즈</strong>: {p.get('sizes', '-')}</span>
                    </div>
                    {'<p class="product-code">Code: ' + p['productCode'] + '</p>' if p.get('productCode') else ''}
                    {'<p><strong>특징</strong>: ' + p['features'] + '</p>' if p.get('features') else ''}
                    {'<a href="' + p['productUrl'] + '" target="_blank" class="product-link">제품 상세보기 →</a>' if p.get('productUrl') else ''}
                </div>
            </div>
            """
    else:
        products_html = '<p class="no-products">입력된 제품 정보가 없습니다.</p>'
    
    # 법적 문구
    final_legal = state['legal_text'].replace('{브랜드명}', basic['brand_name'])
    
    # 생성 날짜
    generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{basic['brand_name']} - {basic['model_name']} {platform_names.get(platform, platform)} 가이드라인</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, {color}, {color}dd);
            color: white;
            padding: 40px 30px;
        }}
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        .header h3 {{
            font-weight: 400;
            opacity: 0.95;
            margin-bottom: 15px;
        }}
        .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.25);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        .content {{
            padding: 30px;
        }}
        .deadline {{
            background: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            font-weight: 500;
        }}
        .section {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .section.highlight-pink {{
            background: #fff0f3;
            border: 1px solid #ffccd5;
        }}
        .section h2 {{
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #333;
        }}
        .keyword-group {{
            margin-bottom: 15px;
        }}
        .keywords {{
            margin-top: 8px;
        }}
        .keyword {{
            display: inline-block;
            background: {color};
            color: white;
            padding: 5px 12px;
            border-radius: 6px;
            margin: 3px;
            font-size: 0.9em;
        }}
        .keyword.sub {{
            background: #6c757d;
        }}
        .metrics {{
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
        }}
        .metric {{
            background: white;
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
            flex: 1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .metric .label {{
            display: block;
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }}
        .metric .value {{
            font-size: 1.3em;
            font-weight: 700;
            color: {color};
        }}
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            border-radius: 0 8px 8px 0;
        }}
        .legal-section {{
            background: #e9ecef;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .legal-section h3 {{
            margin-bottom: 15px;
        }}
        .legal-section code {{
            display: block;
            background: white;
            padding: 15px;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.95em;
        }}
        .products-section {{
            background: #f1f3f5;
            padding: 25px;
            border-radius: 12px;
        }}
        .products-section h2 {{
            margin-bottom: 20px;
        }}
        .product-card {{
            display: flex;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .product-image {{
            width: 180px;
            min-height: 180px;
            background: #f0f2f6;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .product-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .no-image {{
            color: #aaa;
            font-size: 0.9em;
        }}
        .product-info {{
            flex: 1;
            padding: 20px;
        }}
        .product-info h3 {{
            margin-bottom: 12px;
            font-size: 1.1em;
        }}
        .main-badge {{
            background: #ffc107;
            color: #333;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            margin-right: 5px;
        }}
        .product-details {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 10px;
            font-size: 0.95em;
        }}
        .product-code {{
            color: #666;
            font-size: 0.85em;
        }}
        .product-link {{
            display: inline-block;
            margin-top: 10px;
            color: {color};
            text-decoration: none;
            font-weight: 500;
        }}
        .product-link:hover {{
            text-decoration: underline;
        }}
        .no-products {{
            text-align: center;
            color: #666;
            padding: 30px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 0.85em;
            border-top: 1px solid #eee;
        }}
        .nav-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 30px;
            background: white;
            border-bottom: 1px solid #eee;
        }}
        .back-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            color: #495057;
            text-decoration: none;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .back-btn:hover {{
            background: #e9ecef;
            color: #333;
        }}
        .print-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: {color};
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .print-btn:hover {{
            opacity: 0.9;
        }}
        @media print {{
            .nav-bar {{
                display: none;
            }}
        }}
        code {{
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Noto Sans KR', sans-serif;
        }}
        ul {{
            margin-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        @media (max-width: 600px) {{
            .product-card {{
                flex-direction: column;
            }}
            .product-image {{
                width: 100%;
                height: 200px;
            }}
            .metrics {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav-bar">
            <a href="javascript:history.back()" class="back-btn" onclick="if(history.length <= 1) window.close();">
                ⬅ 이전으로 돌아가기
            </a>
            <button class="print-btn" onclick="window.print()">
                🖨️ 인쇄하기
            </button>
        </div>
        <div class="header">
            <h1>{basic['brand_name']}</h1>
            <h3>{basic['model_name']} {basic['campaign_round']} | {platform_names.get(platform, platform).upper()} 가이드라인</h3>
            <span class="badge">{'📢 오피셜' if basic['campaign_type'] == 'official' else '🔒 히든'}</span>
        </div>
        
        <div class="content">
            <div class="deadline">
                📅 <strong>포스팅 기한</strong>: {basic['posting_date']} {basic['posting_time']} 이후
            </div>
            
            {platform_section}
            
            <div class="legal-section">
                <h3>⚖️ 필수 기재 문구</h3>
                <code>{final_legal}</code>
            </div>
            
            <div class="products-section">
                <h2>📦 제품 정보</h2>
                {products_html}
            </div>
        </div>
        
        <div class="footer">
            Generated by Viral Guideline Template | {generated_date}
        </div>
    </div>
</body>
</html>"""
    
    return html_template


def render_preview_mode():
    state = st.session_state
    basic = state['basic_info']
    platform = state['platform']
    
    # 상단 네비게이션
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ 편집으로 돌아가기"):
            state['view_mode'] = 'edit'
            st.rerun()
    
    with col3:
        # HTML 다운로드 버튼
        html_content = generate_shareable_html(state)
        file_name = f"{basic['brand_name']}_{basic['model_name']}_{platform}_가이드라인.html"
        file_name = file_name.replace(" ", "_")
        
        st.download_button(
            label="📥 HTML 다운로드",
            data=html_content,
            file_name=file_name,
            mime="text/html",
            help="외부 공유용 HTML 파일을 다운로드합니다"
        )
    
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
