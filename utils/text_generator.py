def generate_plain_text(state):
    """
    현재 상태(Session State)를 기반으로 클립보드 복사용 텍스트를 생성합니다.
    """
    basic_info = state['basic_info']
    platform = state['platform']
    blog_data = state['blog_data']
    insta_data = state['insta_data']
    youtube_data = state['youtube_data']
    products = state['products']
    legal_text = state['legal_text']

    campaign_label = '🔒 히든' if basic_info['campaign_type'] == 'hidden' else '📢 오피셜'
    platform_label_map = {'blog': '블로그', 'instagram': '인스타그램', 'youtube': '유튜브'}
    platform_label = platform_label_map.get(platform, '블로그')

    output = []
    output.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append(f"{basic_info['brand_name']} [{platform_label}] {basic_info['model_name']} {basic_info['campaign_round']}")
    output.append(f"{campaign_label} 캠페인")
    output.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    output.append(f"📅 포스팅 기한: {basic_info['posting_date']} {basic_info['posting_time']} 이후\n")

    if platform == 'blog':
        title_kw = " / ".join([k['text'] for k in blog_data['title_keywords'] if k['text']])
        sub_kw = " / ".join([k['text'] for k in blog_data['sub_keywords'] if k['text']])
        
        output.append("🏷️ 키워드 설정")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ 필수 제목 키워드: {title_kw or '(미입력)'}")
        output.append(f"▸ 본문 서브 키워드: {sub_kw or '(미입력)'}\n")
        
        output.append("🖼️ 활용 이미지 (필수★)")
        output.append("─────────────────────────────────────────")
        output.append(f"□ {basic_info['model_name']} {blog_data['images']['model_note']} {blog_data['images']['model_count']}장 이상")
        if blog_data['images']['sns_url']:
            output.append(f"□ SNS 캡쳐 {blog_data['images']['sns_count']}장 이상 ({blog_data['images']['sns_url']})")
        if blog_data['images']['coupon_capture']:
            output.append("□ 자사몰 쿠폰팩 캡쳐이미지")
        output.append(f"□ 자사몰 링크: {blog_data['images']['mall_link']}\n")
        
        output.append("📖 스토리라인")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ 타겟: {blog_data['story']['target_audience']}")
        if blog_data['story']['trend']:
            output.append(f"[트렌드] {blog_data['story']['trend']}")
        if blog_data['story']['product_strength']:
            output.append(f"[특장점] {blog_data['story']['product_strength']}")
        if blog_data['story']['campaign_concept']:
            output.append(f"[컨셉] {blog_data['story']['campaign_concept']}")

    elif platform == 'instagram':
        type_map = {'feed': '피드', 'reels': '릴스', 'story': '스토리', 'carousel': '캐러셀'}
        content_type = type_map.get(insta_data['content_type'], '피드')
        
        output.append("📐 콘텐츠 스펙")
        output.append("─────────────────────────────────────────")
        output.append(f"▸ 유형: {content_type} | 사이즈: {insta_data['content_size']}")
        output.append(f"▸ 멘션: {insta_data['mentions']}\n")
        
        output.append(f"🎨 톤앤매너: {insta_data['tone_and_manner'] or '(자유롭게 작성)'}")
        output.append(f"#️⃣ 해시태그: {insta_data['hashtags'] or '(미입력)'}")
        output.append(f"♻️ 2차 활용: {insta_data['reuse_clause']}")

    elif platform == 'youtube':
        type_map = {'shorts': '쇼츠', 'review': '리뷰', 'vlog': '브이로그', 'integration': 'PPL'}
        content_type = type_map.get(youtube_data['content_type'], '쇼츠')
        
        output.append(f"🎬 콘텐츠 스펙: {content_type} | 길이: {youtube_data['duration'] or '자유'}")
        output.append(f"💬 희망 메시지: {youtube_data['key_message'] or '(자유)'}")
        output.append(f"📢 필수 멘트: {youtube_data['required_mentions'] or '(없음)'}")

    output.append("\n📦 제품 정보")
    output.append("─────────────────────────────────────────")
    
    for p in products:
        if p['name']:
            mark = "★ [메인]" if p.get('isMain', False) else "•"
            output.append(f"\n{mark} {p['name']}")
            if p['colors']:
                output.append(f"   컬러: {p['colors']}")
            if p['price']:
                output.append(f"   가격: ₩{p['price']}")
            if p['sizes']:
                output.append(f" | 사이즈: {p['sizes']}")
            if p['features']:
                output.append(f"   특징: {p['features']}")
            if p['productUrl']:
                output.append(f"   🔗 {p['productUrl']}")

    output.append("\n⚖️ 필수 기재 문구")
    output.append("─────────────────────────────────────────")
    brand_name = basic_info.get('brand_name', '')
    final_legal = legal_text.replace('{브랜드명}', brand_name)
    output.append(f'"{final_legal}"')

    return "\n".join(output)

