def generate_plain_text(state):
    """
    현재 상태(Session State)를 기반으로 클립보드 복사용 텍스트를 생성합니다.
    """
    basic_info = state.get('basic_info', {})
    platform = state.get('platform', 'blog')
    blog_data = state.get('blog_data', {})
    insta_data = state.get('insta_data', {})
    youtube_data = state.get('youtube_data', {})
    products = state.get('products', [])
    legal_text = state.get('legal_text', '')

    campaign_label = '🔒 히든' if basic_info.get('campaign_type') == 'hidden' else '📢 오피셜'
    platform_label_map = {'blog': '블로그', 'instagram': '인스타그램', 'youtube': '유튜브'}
    platform_label = platform_label_map.get(platform, '블로그')

    output = []
    output.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append(f"{basic_info.get('brand_name', '')} [{platform_label}] {basic_info.get('model_name', '')} {basic_info.get('campaign_round', '')}")
    output.append(f"{campaign_label} 캠페인")
    output.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 인스타그램은 '이후' 제외
    deadline_suffix = "" if platform == 'instagram' else " 이후"
    output.append(f"📅 포스팅 기한: {basic_info.get('posting_date', '')} {basic_info.get('posting_time', '')}{deadline_suffix}\n")

    if platform == 'blog':
        blog_images = blog_data.get('images', {})
        blog_story = blog_data.get('story', {})
        title_keywords = blog_data.get('title_keywords', [])
        sub_keywords = blog_data.get('sub_keywords', [])
        
        title_kw = " / ".join([k.get('text', '') for k in title_keywords if k.get('text')])
        sub_kw = " / ".join([k.get('text', '') for k in sub_keywords if k.get('text')])
        
        output.append("🏷️ 키워드 설정")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ 필수 제목 키워드: {title_kw or '(미입력)'}")
        output.append(f"▸ 본문 서브 키워드: {sub_kw or '(미입력)'}\n")
        
        output.append("🖼️ 활용 이미지 (필수★)")
        output.append("─────────────────────────────────────────")
        output.append(f"□ {basic_info.get('model_name', '')} {blog_images.get('model_note', '')} {blog_images.get('model_count', 0)}장 이상")
        if blog_images.get('sns_url'):
            output.append(f"□ SNS 캡쳐 {blog_images.get('sns_count', 0)}장 이상 ({blog_images.get('sns_url', '')})")
        if blog_images.get('coupon_capture'):
            output.append("□ 자사몰 쿠폰팩 캡쳐이미지")
        output.append(f"□ 자사몰 링크: {blog_images.get('mall_link', '')}\n")
        
        output.append("📖 스토리라인")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ 타겟: {blog_story.get('target_audience', '')}")
        if blog_story.get('trend'):
            output.append(f"[트렌드] {blog_story.get('trend', '')}")
        if blog_story.get('product_strength'):
            output.append(f"[특장점] {blog_story.get('product_strength', '')}")
        if blog_story.get('campaign_concept'):
            output.append(f"[컨셉] {blog_story.get('campaign_concept', '')}")

    elif platform == 'instagram':
        type_map = {'feed': '피드', 'reels': '릴스', 'story': '스토리', 'carousel': '캐러셀'}
        content_type = type_map.get(insta_data.get('content_type', 'feed'), '피드')
        
        output.append("📐 콘텐츠 스펙")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ 유형: {content_type} | 사이즈: {insta_data.get('content_size', '1:1')}")
        
        # 멘션 (브랜드/셀럽 분리)
        brand_mention = insta_data.get('brand_mention', '')
        celeb_mention = insta_data.get('celeb_mention', '')
        if brand_mention:
            output.append(f"▸ 브랜드 멘션: {brand_mention}")
        if celeb_mention:
            output.append(f"▸ 셀럽/모델 멘션: {celeb_mention}")
        output.append("")
        
        output.append(f"🎨 톤앤매너: {insta_data.get('tone_and_manner', '') or '(자유롭게 작성)'}")
        output.append(f"#️⃣ 해시태그: {insta_data.get('hashtags', '') or '(미입력)'}")

    elif platform == 'youtube':
        type_map = {'shorts': '쇼츠', 'review': '리뷰', 'vlog': '브이로그', 'integration': 'PPL'}
        content_type = type_map.get(youtube_data.get('content_type', 'shorts'), '쇼츠')
        
        output.append(f"🎬 콘텐츠 스펙: {content_type} | 길이: {youtube_data.get('duration', '') or '자유'}")
        output.append(f"💬 희망 메시지: {youtube_data.get('key_message', '') or '(자유)'}")
        output.append(f"📢 필수 멘트: {youtube_data.get('required_mentions', '') or '(없음)'}")

    elif platform == 'review_blog':
        rb = state.get('review_blog_data', {})
        
        output.append(f"📷 이미지 분량: {rb.get('min_images', 10)}장 이상\n")
        
        # 필수 키워드
        output.append("🏷️ 필수 키워드")
        output.append("─────────────────────────────────────────")
        title_kw = rb.get('title_keywords', {})
        req_kw = ", ".join([k.get('text', '') for k in title_kw.get('required', []) if k.get('text')])
        opt_kw = ", ".join([k.get('text', '') for k in title_kw.get('optional', []) if k.get('text')])
        output.append(f"▸ 필수 제목: {req_kw or '(미입력)'}")
        output.append(f"▸ 선택 제목: {opt_kw or '(미입력)'}")
        
        body_kw = rb.get('body_keywords', {})
        output.append(f"▸ BRAND: {body_kw.get('brand', '') or '(미입력)'}")
        output.append(f"▸ ITEM: {body_kw.get('item', '') or '(미입력)'}")
        output.append(f"▸ STYLE: {body_kw.get('style', '') or '(미입력)'}\n")
        
        # 브랜드 소개
        if rb.get('brand_intro'):
            output.append("🏢 브랜드 소개")
            output.append("─────────────────────────────────────────")
            output.append(rb.get('brand_intro', ''))
            output.append("")
        
        # 스타일링 가이드
        styling = rb.get('styling', {})
        if styling.get('concept') or styling.get('matching_items') or styling.get('other_notes'):
            output.append("👗 스타일링 가이드")
            output.append("─────────────────────────────────────────")
            if styling.get('concept'):
                output.append(f"▸ 컨셉: {styling.get('concept', '')}")
            if styling.get('matching_items'):
                output.append(f"▸ 매칭 아이템: {styling.get('matching_items', '')}")
            if styling.get('other_notes'):
                output.append(f"▸ 기타: {styling.get('other_notes', '')}")
            output.append("")
        
        # 필수 촬영 앵글
        angles = rb.get('required_angles', {})
        angle_list = []
        if angles.get('full_body'):
            angle_list.append("전신샷")
        if angles.get('upper_body'):
            angle_list.append("상반신샷")
        if angles.get('mirror'):
            angle_list.append("거울샷")
        if angles.get('detail'):
            angle_list.append("디테일샷")
        
        output.append("📸 필수 촬영 앵글")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ {', '.join(angle_list) if angle_list else '(미선택)'}")
        if angles.get('custom'):
            output.append(f"▸ {angles.get('custom', '')}")
        output.append("")
        
        # 톤앤매너
        if rb.get('tone_and_manner'):
            output.append(f"🎨 톤앤매너: {rb.get('tone_and_manner', '')}\n")
        
        # 포스팅 가이드
        if rb.get('posting_guide'):
            output.append(f"✍️ 포스팅 가이드: {rb.get('posting_guide', '')}\n")

    output.append("\n📦 제품 정보")
    output.append("─────────────────────────────────────────")
    
    for p in products:
        if p.get('name'):
            mark = "★ [메인]" if p.get('isMain', False) else "•"
            output.append(f"\n{mark} {p.get('name', '')}")
            if p.get('colors'):
                output.append(f"   컬러: {p.get('colors', '')}")
            if p.get('price'):
                output.append(f"   가격: ₩{p.get('price', '')}")
            if p.get('sizes'):
                output.append(f" | 사이즈: {p.get('sizes', '')}")
            if p.get('features'):
                output.append(f"   특징: {p.get('features', '')}")
            if p.get('productUrl'):
                output.append(f"   🔗 {p.get('productUrl', '')}")

    # 인스타그램은 필수 기재 문구 제외
    if platform != 'instagram':
        output.append("\n⚖️ 필수 기재 문구")
        output.append("─────────────────────────────────────────")
        brand_name = basic_info.get('brand_name', '')
        final_legal = legal_text.replace('{브랜드명}', brand_name)
        output.append(f'"{final_legal}"')

    return "\n".join(output)

