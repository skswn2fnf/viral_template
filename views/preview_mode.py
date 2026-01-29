import streamlit as st
from datetime import datetime

def generate_shareable_html(state):
    """
    외부 공유용 완전한 HTML 파일을 생성합니다.
    모든 스타일이 인라인으로 포함되어 독립적으로 볼 수 있습니다.
    """
    basic = state['basic_info']
    platform = state['platform']
    
    # 모노톤 색상 (진회색)
    color = '#343a40'
    accent_color = '#1976d2'  # 파란색 하이라이트
    
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
        
        # 자사몰 링크 섹션
        mall_link_section = ""
        if blog['images'].get('mall_link'):
            mall_link_section = f"""
            <div class="section-wrapper">
                <div class="section-header">🔗 자사몰 링크</div>
                <div class="section-body">
                    <a href="{blog['images']['mall_link']}" target="_blank" style="color: {accent_color}; text-decoration: none; font-weight: 500;">{blog['images']['mall_link']} →</a>
                </div>
            </div>
            """
        
        # 트렌드/브랜드 설명 섹션
        trend_section = ""
        if blog['story'].get('trend'):
            trend_html = blog['story']['trend'].replace('\n', '<br>')
            trend_section = f"""
            <div class="section-wrapper">
                <div class="section-header">💡 트렌드 / 브랜드 설명</div>
                <div class="section-body">
                    <p>{trend_html}</p>
                </div>
            </div>
            """
        
        # 제품 특장점 섹션
        strength_section = ""
        if blog['story'].get('product_strength'):
            strength_html = blog['story']['product_strength'].replace('\n', '<br>')
            strength_section = f"""
            <div class="section-wrapper">
                <div class="section-header">✨ 제품 특장점</div>
                <div class="section-body">
                    <p>{strength_html}</p>
                </div>
            </div>
            """
        
        platform_section = f"""
        <div class="section-wrapper">
            <div class="section-header">🏷️ 키워드 설정</div>
            <div class="section-body">
                <div class="keyword-group">
                    <strong>필수 제목 키워드</strong>
                    <div class="keywords">{title_keywords}</div>
                </div>
                <div class="keyword-group">
                    <strong>서브 키워드</strong>
                    <div class="keywords">{sub_keywords}</div>
                </div>
            </div>
        </div>
        <div class="section-wrapper">
            <div class="section-header">🖼️ 활용 이미지</div>
            <div class="section-body">
                <ul>
                    <li>{basic['model_name']} {blog['images']['model_note']} <strong>{blog['images']['model_count']}장</strong> 이상</li>
                    {'<li>SNS 캡쳐 <strong>' + str(blog['images']['sns_count']) + '장</strong> 이상</li>' if blog['images']['sns_url'] else ''}
                </ul>
            </div>
        </div>
        {mall_link_section}
        <div class="section-wrapper">
            <div class="section-header">📖 스토리라인</div>
            <div class="section-body">
                <p><strong>타겟</strong>: {blog['story']['target_audience']}</p>
                {'<p><strong>컨셉</strong>: ' + blog['story']['campaign_concept'] + '</p>' if blog['story']['campaign_concept'] else ''}
            </div>
        </div>
        {trend_section}
        {strength_section}
        """
    
    elif platform == 'instagram':
        insta = state['insta_data']
        platform_section = f"""
        <div class="section-wrapper">
            <div class="section-header">📐 콘텐츠 스펙</div>
            <div class="section-body">
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
        </div>
        {'<div class="section-wrapper"><div class="section-header">🎨 톤앤매너</div><div class="section-body"><div class="info-box">' + insta['tone_and_manner'] + '</div></div></div>' if insta['tone_and_manner'] else ''}
        {'<div class="section-wrapper"><div class="section-header">#️⃣ 해시태그</div><div class="section-body"><code style="display:block; background:#e9ecef; padding:15px; border-radius:8px; white-space:pre-wrap;">' + insta['hashtags'] + '</code></div></div>' if insta.get('hashtags') else ''}
        <div class="section-wrapper highlight-blue">
            <div class="section-header accent">♻️ 2차 활용</div>
            <div class="section-body accent">
                <p><strong>{insta['reuse_clause']}</strong></p>
            </div>
        </div>
        """
    
    elif platform == 'youtube':
        yt = state['youtube_data']
        platform_section = f"""
        <div class="section-wrapper">
            <div class="section-header">🎬 콘텐츠 스펙</div>
            <div class="section-body">
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
        </div>
        {'<div class="section-wrapper"><div class="section-header">💬 희망 메시지</div><div class="section-body"><div class="info-box">' + yt['key_message'] + '</div></div></div>' if yt['key_message'] else ''}
        {'<div class="section-wrapper"><div class="section-header accent">📢 필수 멘트</div><div class="section-body accent"><p><strong>' + yt['required_mentions'] + '</strong></p></div></div>' if yt.get('required_mentions') else ''}
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
            background: #e3f2fd;
            border-left: 4px solid {accent_color};
            color: #1565c0;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            font-weight: 500;
        }}
        .section-wrapper {{
            margin-bottom: 20px;
        }}
        .section-header {{
            background: #495057;
            color: white;
            padding: 12px 20px;
            border-radius: 8px 8px 0 0;
            font-weight: 600;
            font-size: 1.05em;
        }}
        .section-header.accent {{
            background: {accent_color};
        }}
        .section-body {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            border: 1px solid #dee2e6;
            border-top: none;
        }}
        .section-body.accent {{
            background: #e3f2fd;
            border-color: #90caf9;
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
            color: #343a40;
        }}
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            border-radius: 0 8px 8px 0;
        }}
        .legal-section {{
            margin-bottom: 20px;
        }}
        .legal-header {{
            background: {accent_color};
            color: white;
            padding: 12px 20px;
            border-radius: 8px 8px 0 0;
            font-weight: 600;
            font-size: 1.05em;
        }}
        .legal-body {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            border: 1px solid #90caf9;
            border-top: none;
        }}
        .legal-body code {{
            display: block;
            background: white;
            padding: 15px;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.95em;
            color: #1565c0;
            font-weight: 500;
        }}
        .products-section {{
            margin-bottom: 20px;
        }}
        .products-header {{
            background: #495057;
            color: white;
            padding: 12px 20px;
            border-radius: 8px 8px 0 0;
            font-weight: 600;
            font-size: 1.05em;
        }}
        .products-body {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            border: 1px solid #dee2e6;
            border-top: none;
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
            color: {accent_color};
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
            
            {f'''<div class="section-wrapper">
                <div class="section-header">🖼️ 메인 화보 (썸네일 지정)</div>
                <div class="section-body" style="text-align: center;">
                    <img src="{basic.get('main_image', '')}" alt="메인 화보" style="max-width: 100%; border-radius: 8px;">
                    <p style="margin-top: 10px; color: #666; font-size: 0.9em;">⬆️ 이 이미지를 썸네일로 사용해주세요</p>
                </div>
            </div>''' if basic.get('main_image') else ''}
            
            {platform_section}
            
            <div class="legal-section">
                <div class="legal-header">⚖️ 필수 기재 문구</div>
                <div class="legal-body">
                    <code>{final_legal}</code>
                </div>
            </div>
            
            <div class="products-section">
                <div class="products-header">📦 제품 정보</div>
                <div class="products-body">
                    {products_html}
                </div>
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
    
    # 스타일링 및 헤더 (모노톤)
    platform_labels = {
        'blog': '블로그',
        'instagram': '인스타그램',
        'youtube': '유튜브'
    }
    
    st.markdown(f"""
    <div style="background-color: #343a40; padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h1 style="margin:0 0 8px 0;">{basic['brand_name']}</h1>
        <h3 style="margin:0 0 12px 0; font-weight: 400; opacity: 0.9;">{basic['model_name']} {basic['campaign_round']} | {platform_labels.get(platform, platform).upper()} 가이드라인</h3>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">
            {'📢 오피셜' if basic['campaign_type'] == 'official' else '🔒 히든'}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # 포스팅 기한 (파란색 하이라이트)
    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: #1565c0; border-left: 4px solid #1976d2;">
        📅 <strong>포스팅 기한</strong>: {basic['posting_date']} {basic['posting_time']} 이후
    </div>
    """, unsafe_allow_html=True)

    # 메인 화보 이미지 (썸네일)
    if basic.get('main_image'):
        st.markdown("""
        <div style="background-color: #495057; color: white; padding: 10px 15px; border-radius: 6px 6px 0 0; margin-top: 15px; font-weight: 600;">
            🖼️ 메인 화보 (썸네일 지정)
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 20px; border: 1px solid #dee2e6; border-top: none; text-align: center;">', unsafe_allow_html=True)
        st.image(basic['main_image'], use_container_width=True)
        st.caption("⬆️ 이 이미지를 썸네일로 사용해주세요")
        st.markdown('</div>', unsafe_allow_html=True)

    # 섹션 헤더 스타일 함수
    def section_title(icon, title):
        st.markdown(f"""
        <div style="background-color: #495057; color: white; padding: 10px 15px; border-radius: 6px 6px 0 0; margin-top: 15px; font-weight: 600;">
            {icon} {title}
        </div>
        """, unsafe_allow_html=True)
    
    # 1. 플랫폼별 상세 가이드 (상단)
    if platform == 'blog':
        blog = state['blog_data']
        
        # 키워드 섹션
        section_title("🏷️", "키워드 설정")
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
        st.markdown("**필수 제목 키워드**")
        st.markdown(" ".join([f"`{k['text']}`" for k in blog['title_keywords'] if k['text']]))
        st.markdown("**서브 키워드**")
        st.markdown(" ".join([f"`{k['text']}`" for k in blog['sub_keywords'] if k['text']]))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 활용 이미지 섹션
        section_title("🖼️", "활용 이미지")
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
        st.markdown(f"- {basic['model_name']} {blog['images']['model_note']} **{blog['images']['model_count']}장** 이상")
        if blog['images']['sns_url']:
            st.markdown(f"- SNS 캡쳐 **{blog['images']['sns_count']}장** 이상")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 활용 이미지 섹션 - 자사몰 링크
        if blog['images'].get('mall_link'):
            section_title("🔗", "자사몰 링크")
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
            st.markdown(f"[{blog['images']['mall_link']}]({blog['images']['mall_link']})")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 스토리라인 섹션
        section_title("📖", "스토리라인")
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
        st.markdown(f"**타겟**: {blog['story']['target_audience']}")
        if blog['story']['campaign_concept']:
            st.markdown(f"**컨셉**: {blog['story']['campaign_concept']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 트렌드/브랜드 설명 섹션
        if blog['story'].get('trend'):
            section_title("💡", "트렌드 / 브랜드 설명")
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
            st.markdown(blog['story']['trend'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 제품 특장점 섹션
        if blog['story'].get('product_strength'):
            section_title("✨", "제품 특장점")
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
            st.markdown(blog['story']['product_strength'])
            st.markdown('</div>', unsafe_allow_html=True)

    elif platform == 'instagram':
        insta = state['insta_data']
        
        # 콘텐츠 스펙
        section_title("📐", "콘텐츠 스펙")
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("유형", insta['content_type'])
        c2.metric("사이즈", insta['content_size'])
        st.markdown(f"**멘션**: `{insta['mentions']}`")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 톤앤매너
        if insta['tone_and_manner']:
            section_title("🎨", "톤앤매너")
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
            st.info(insta['tone_and_manner'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 해시태그
        if insta.get('hashtags'):
            section_title("#️⃣", "해시태그")
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
            st.code(insta['hashtags'], language=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # 2차 활용 (파란색 하이라이트)
        section_title("♻️", "2차 활용")
        st.markdown('<div style="background-color: #e3f2fd; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #90caf9; border-top: none;">', unsafe_allow_html=True)
        st.markdown(f"**{insta['reuse_clause']}**")
        st.markdown('</div>', unsafe_allow_html=True)

    elif platform == 'youtube':
        yt = state['youtube_data']
        
        # 콘텐츠 스펙
        section_title("🎬", "콘텐츠 스펙")
        st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("유형", yt['content_type'])
        c2.metric("권장 길이", yt['duration'] or "자유")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if yt['key_message']:
            section_title("💬", "희망 메시지")
            st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
            st.info(yt['key_message'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 필수 멘트
        if yt.get('required_mentions'):
            section_title("📢", "필수 멘트")
            st.markdown('<div style="background-color: #e3f2fd; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 15px; border: 1px solid #90caf9; border-top: none;">', unsafe_allow_html=True)
            st.markdown(f"**{yt['required_mentions']}**")
            st.markdown('</div>', unsafe_allow_html=True)

    # 2. 법적 문구 (파란색 하이라이트 - 중요!)
    final_legal = state['legal_text'].replace('{브랜드명}', basic['brand_name'])
    st.markdown(f"""
    <div style="background-color: #1976d2; color: white; padding: 10px 15px; border-radius: 6px 6px 0 0; margin-top: 15px; font-weight: 600;">
        ⚖️ 필수 기재 문구
    </div>
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 20px; border: 1px solid #90caf9; border-top: none;">
        <code style="display:block; padding:15px; background:white; border-radius:5px; color: #1565c0; font-weight: 500;">{final_legal}</code>
    </div>
    """, unsafe_allow_html=True)

    # 3. 제품 정보 (하단)
    section_title("📦", "제품 정보")
    st.markdown('<div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 6px 6px; margin-bottom: 20px; border: 1px solid #dee2e6; border-top: none;">', unsafe_allow_html=True)
    
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
