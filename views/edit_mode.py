import streamlit as st
import time
import base64
import json
from datetime import datetime
from data.product_db import fetch_product_info

def get_saveable_state():
    """저장 가능한 상태 데이터를 딕셔너리로 반환"""
    return {
        'basic_info': st.session_state.get('basic_info', {}),
        'platform': st.session_state.get('platform', 'blog'),
        'blog_data': st.session_state.get('blog_data', {}),
        'insta_data': st.session_state.get('insta_data', {}),
        'youtube_data': st.session_state.get('youtube_data', {}),
        'products': st.session_state.get('products', []),
        'legal_text': st.session_state.get('legal_text', ''),
        'saved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def ensure_blog_data_structure(blog):
    """블로그 데이터 구조 보장"""
    if 'title_keywords' not in blog:
        blog['title_keywords'] = [{'id': 1, 'text': ''}]
    if 'sub_keywords' not in blog:
        blog['sub_keywords'] = [{'id': 1, 'text': ''}]
    if 'images' not in blog:
        blog['images'] = {}
    if 'story' not in blog:
        blog['story'] = {}
    
    # images 하위 구조
    img = blog['images']
    img.setdefault('model_count', 8)
    img.setdefault('model_note', '')
    img.setdefault('sns_count', 2)
    img.setdefault('sns_url', '')
    img.setdefault('coupon_capture', True)
    img.setdefault('mall_link', '')
    
    # story 하위 구조
    story = blog['story']
    story.setdefault('target_audience', '')
    story.setdefault('trend', '')
    story.setdefault('product_strength', '')
    story.setdefault('campaign_concept', '')
    
    return blog

def ensure_insta_data_structure(insta):
    """인스타그램 데이터 구조 보장"""
    insta.setdefault('content_type', 'feed')
    insta.setdefault('content_size', '1:1')
    insta.setdefault('tone_and_manner', '')
    insta.setdefault('hashtags', '')
    insta.setdefault('brand_mention', '')
    insta.setdefault('celeb_mention', '')
    return insta

def ensure_youtube_data_structure(yt):
    """유튜브 데이터 구조 보장"""
    yt.setdefault('content_type', 'shorts')
    yt.setdefault('duration', '')
    yt.setdefault('key_message', '')
    yt.setdefault('required_mentions', '')
    return yt

def ensure_product_structure(p, idx=0):
    """제품 데이터 구조 보장"""
    p.setdefault('id', int(time.time() * 1000) + idx)
    p.setdefault('name', '')
    p.setdefault('price', '')
    p.setdefault('colors', '')
    p.setdefault('sizes', '')
    p.setdefault('features', '')
    p.setdefault('productCode', '')
    p.setdefault('productUrl', '')
    p.setdefault('imageUrl', '')
    p.setdefault('isMain', False)
    return p

def load_state_from_json(json_data):
    """JSON 데이터로부터 상태 복원"""
    try:
        data = json.loads(json_data)
        if 'basic_info' in data:
            st.session_state['basic_info'] = data['basic_info']
        if 'platform' in data:
            st.session_state['platform'] = data['platform']
        if 'blog_data' in data:
            st.session_state['blog_data'] = ensure_blog_data_structure(data['blog_data'])
        if 'insta_data' in data:
            st.session_state['insta_data'] = ensure_insta_data_structure(data['insta_data'])
        if 'youtube_data' in data:
            st.session_state['youtube_data'] = ensure_youtube_data_structure(data['youtube_data'])
        if 'products' in data:
            # 제품 데이터 구조 보장
            products = data['products']
            for idx, p in enumerate(products):
                ensure_product_structure(p, idx)
            st.session_state['products'] = products
        if 'legal_text' in data:
            st.session_state['legal_text'] = data['legal_text']
        return True, data.get('saved_at', '알 수 없음')
    except Exception as e:
        return False, str(e)

def image_to_data_url(uploaded_file):
    """업로드된 이미지를 base64 data URL로 변환 (원본 유지, 메인 화보용)"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        b64 = base64.b64encode(bytes_data).decode()
        file_type = uploaded_file.type
        return f"data:{file_type};base64,{b64}"
    return None

def compress_image_to_data_url(uploaded_file, max_size_kb=300, max_width=800):
    """
    제품 이미지를 압축하여 base64 data URL로 변환
    - max_size_kb: 목표 최대 파일 크기 (KB)
    - max_width: 최대 가로 픽셀
    """
    if uploaded_file is None:
        return None
    
    try:
        from PIL import Image
        from io import BytesIO
        
        # 이미지 열기
        img = Image.open(uploaded_file)
        
        # RGBA -> RGB 변환 (PNG 투명 배경 처리)
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 리사이즈 (가로 기준)
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        
        # 압축 (JPEG 품질 조정)
        quality = 85
        while quality >= 20:
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            size_kb = len(buffer.getvalue()) / 1024
            
            if size_kb <= max_size_kb:
                break
            quality -= 10
        
        # base64 인코딩
        b64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{b64}"
    
    except Exception as e:
        # 압축 실패 시 원본 반환
        uploaded_file.seek(0)
        bytes_data = uploaded_file.getvalue()
        b64 = base64.b64encode(bytes_data).decode()
        return f"data:{uploaded_file.type};base64,{b64}"

def section_header(icon, title):
    """진회색 배경 + 화이트 텍스트 섹션 헤더"""
    st.markdown(f"""
    <div style="background-color: #343a40; color: white; padding: 12px 16px; border-radius: 8px; margin: 20px 0 10px 0; font-weight: 600; font-size: 1.1em;">
        {icon} {title}
    </div>
    """, unsafe_allow_html=True)

def render_edit_mode():
    st.title("✨ 바이럴 가이드라인 템플릿")
    st.caption("플랫폼별 맞춤 가이드라인을 빠르게 작성하세요")

    # 저장/불러오기 섹션
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 10px;">
        <strong>💾 중간 저장은 여기에서 하세요!</strong>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💾 저장 / 불러오기 사용방법", expanded=False):
        st.markdown("""
        **📌 사용 방법 안내**
        
        1. 작성 중인 내용은 **JSON 파일로 필수 저장**해주세요.  
           그렇지 않으면 작성 중인 내용이 **모두 날아갑니다.**
        
        2. 다시 작성하실 때, 저장한 **JSON 파일을 오른쪽 공간에 업로드**해주세요.
        """)
        st.markdown("---")
        
        save_col1, save_col2 = st.columns(2)
        
        with save_col1:
            st.markdown("**📥 작업 내용 저장**")
            st.caption("현재 작성 중인 내용을 JSON 파일로 저장합니다")
            
            # 저장 데이터 생성
            save_data = get_saveable_state()
            json_str = json.dumps(save_data, ensure_ascii=False, indent=2)
            
            # 파일명 생성
            brand_name = st.session_state.get('basic_info', {}).get('brand_name', 'template')
            file_name = f"{brand_name}_가이드라인_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            file_name = file_name.replace(" ", "_")
            
            st.download_button(
                label="💾 JSON으로 저장",
                data=json_str,
                file_name=file_name,
                mime="application/json",
                use_container_width=True
            )
            
            # 현재 파일 크기 표시
            current_size_kb = len(json_str.encode('utf-8')) / 1024
            if current_size_kb < 1024:
                size_text = f"{current_size_kb:.1f} KB"
            else:
                size_text = f"{current_size_kb/1024:.2f} MB"
            
            if current_size_kb > 5120:  # 5MB 초과 시 경고
                st.warning(f"⚠️ 현재 크기: {size_text} (권장: 5MB 이하)")
            else:
                st.caption(f"📊 현재 크기: {size_text} / 권장 최대: 5MB")
        
        with save_col2:
            st.markdown("**📤 저장된 작업 불러오기**")
            st.caption("이전에 저장한 JSON 파일을 불러옵니다")
            
            uploaded_json = st.file_uploader(
                "JSON 파일 업로드",
                type=['json'],
                key="load_json_file",
                label_visibility="collapsed"
            )
            
            if uploaded_json:
                # 파일 크기 확인
                file_size_mb = uploaded_json.size / 1024 / 1024
                if file_size_mb > 10:
                    st.error(f"❌ 파일이 너무 큽니다 ({file_size_mb:.1f}MB). 10MB 이하 파일만 불러올 수 있습니다.")
                elif file_size_mb > 5:
                    st.warning(f"⚠️ 파일 크기: {file_size_mb:.1f}MB - 로딩이 느릴 수 있습니다.")
                    if st.button("📂 불러오기 실행", use_container_width=True):
                        with st.spinner("불러오는 중... (파일이 커서 시간이 걸릴 수 있습니다)"):
                            json_content = uploaded_json.read().decode('utf-8')
                            success, info = load_state_from_json(json_content)
                            if success:
                                st.success(f"✅ 불러오기 완료! (저장 시간: {info})")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"❌ 불러오기 실패: {info}")
                else:
                    if st.button("📂 불러오기 실행", use_container_width=True):
                        json_content = uploaded_json.read().decode('utf-8')
                        success, info = load_state_from_json(json_content)
                        if success:
                            st.success(f"✅ 불러오기 완료! (저장 시간: {info})")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ 불러오기 실패: {info}")
    
    st.markdown("---")

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
        section_header("📄", "기본 정보")
        with st.expander("상세 설정", expanded=True):
            basic = st.session_state['basic_info']
            
            # main_image 키가 없으면 추가 (기존 데이터 호환)
            if 'main_image' not in basic:
                basic['main_image'] = ''
            
            # 캠페인 타입 토글
            c_type = st.radio("캠페인 타입", ["official", "hidden"], 
                            format_func=lambda x: "📢 오피셜" if x == "official" else "🔒 히든",
                            index=0 if basic['campaign_type'] == 'official' else 1,
                            horizontal=True)
            basic['campaign_type'] = c_type

            b_col1, b_col2 = st.columns(2)
            basic['brand_name'] = b_col1.text_input("브랜드명", value=basic['brand_name'])
            basic['model_name'] = b_col2.text_input("모델/인플루언서", value=basic['model_name'], placeholder="예: 박지현")
            
            # 메인 화보 이미지 업로드
            st.markdown("---")
            st.markdown("**🖼️ 메인 화보 이미지** (썸네일 / 컨텐츠 상단 노출)")
            
            main_img_col1, main_img_col2 = st.columns([1, 2])
            
            with main_img_col1:
                if basic.get('main_image'):
                    st.image(basic['main_image'], use_container_width=True)
                    if st.button("🗑️ 이미지 삭제", key="del_main_img", use_container_width=True):
                        basic['main_image'] = ''
                        st.rerun()
                else:
                    main_img_upload = st.file_uploader(
                        "메인 화보 업로드",
                        type=['png', 'jpg', 'jpeg', 'webp'],
                        key="main_image_upload",
                        label_visibility="collapsed"
                    )
                    if main_img_upload:
                        data_url = image_to_data_url(main_img_upload)
                        if data_url:
                            basic['main_image'] = data_url
                            st.rerun()
                    st.caption("PNG, JPG, WEBP")
            
            with main_img_col2:
                st.info("💡 이 이미지가 가이드라인 상단에 메인컷으로 표시됩니다.\n\n인플루언서가 썸네일로 사용할 대표 화보를 업로드해주세요.")
            
            st.markdown("---")
            
            b_col3, b_col4, b_col5 = st.columns(3)
            basic['campaign_round'] = b_col3.text_input("캠페인 회차", value=basic['campaign_round'])
            basic['posting_date'] = b_col4.text_input("포스팅 날짜", value=basic['posting_date'], placeholder="YYYY-MM-DD")
            basic['posting_time'] = b_col5.text_input("포스팅 시간", value=basic['posting_time'], placeholder="13:00")

        # 2. 제품 정보 섹션
        section_header("📦", "제품 정보")
        with st.expander("제품 목록", expanded=True):
            st.info("🔗 공식몰 제품 URL을 입력하면 정보가 자동 채워집니다.")
            
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
                        st.success(f"제품 추가 완료! (총 {len(st.session_state['products'])}개)")
                        time.sleep(1) # 성공 메시지 보여주기
                        st.rerun()
                    else:
                        st.error("제품을 찾을 수 없습니다.")

            # 제품 리스트 렌더링 (최신순 or 등록순)
            products = st.session_state['products']
            
            if len(products) > 0:
                st.markdown(f"**등록된 제품: {len(products)}개**")
                
            for idx, p in enumerate(products):
                # 제품 데이터 구조 보장 (누락된 필드 기본값 설정)
                if 'id' not in p:
                    p['id'] = int(time.time() * 1000) + idx
                if 'name' not in p:
                    p['name'] = ''
                if 'price' not in p:
                    p['price'] = ''
                if 'colors' not in p:
                    p['colors'] = ''
                if 'sizes' not in p:
                    p['sizes'] = ''
                if 'features' not in p:
                    p['features'] = ''
                if 'productCode' not in p:
                    p['productCode'] = ''
                if 'productUrl' not in p:
                    p['productUrl'] = ''
                if 'imageUrl' not in p:
                    p['imageUrl'] = ''
                if 'isMain' not in p:
                    p['isMain'] = False
                
                # 제품명으로 아코디언 제목 설정 (없으면 Product N)
                title = p.get('name', '') if p.get('name') else f"Product {idx + 1}"
                title_prefix = "★ " if p.get('isMain', False) else ""
                
                # 아코디언으로 감싸서 공간 절약 (마지막에 추가된 것은 열어두기)
                is_expanded = (idx == len(products) - 1)
                
                with st.expander(f"{title_prefix}{title}", expanded=is_expanded):
                    # 이미지와 내용을 나누기 위한 컬럼 (1:4 비율)
                    img_col, content_col = st.columns([1, 4])
                    
                    with img_col:
                        if p.get('imageUrl'):
                            st.image(p.get('imageUrl', ''), use_container_width=True)
                            # 이미지 삭제 버튼
                            if st.button("🗑️ 이미지 삭제", key=f"del_img_{p['id']}", use_container_width=True):
                                p['imageUrl'] = ''
                                st.rerun()
                        else:
                            # 이미지 업로드 (자동 압축 적용)
                            uploaded_file = st.file_uploader(
                                "이미지 업로드",
                                type=['png', 'jpg', 'jpeg', 'webp'],
                                key=f"upload_{p['id']}",
                                label_visibility="collapsed"
                            )
                            if uploaded_file:
                                # 제품 이미지는 자동 압축 적용 (최대 300KB, 가로 800px)
                                data_url = compress_image_to_data_url(uploaded_file, max_size_kb=300, max_width=800)
                                if data_url:
                                    p['imageUrl'] = data_url
                                    st.rerun()
                            st.caption("자동 압축됨")

                    with content_col:
                        # 메인 제품 체크 및 삭제 버튼
                        h_col1, h_col2 = st.columns([4, 1])
                        p['isMain'] = h_col1.checkbox("★ 메인 제품으로 설정", value=p.get('isMain', False), key=f"main_{p['id']}")
                        
                        # 삭제 버튼 로직 개선
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
                        p['name'] = p_col1.text_input("제품명", value=p.get('name', ''), key=f"name_{p['id']}")
                        p['productCode'] = p_col2.text_input("상품코드", value=p.get('productCode', ''), key=f"code_{p['id']}")
                        
                        p_col3, p_col4, p_col5 = st.columns(3)
                        p['price'] = p_col3.text_input("가격", value=p.get('price', ''), key=f"price_{p['id']}")
                        p['colors'] = p_col4.text_input("컬러", value=p.get('colors', ''), key=f"colors_{p['id']}")
                        p['sizes'] = p_col5.text_input("사이즈", value=p.get('sizes', ''), key=f"sizes_{p['id']}")
                    
                    # 특징은 아래에 넓게 배치
                    p['features'] = st.text_area("특징", value=p.get('features', ''), key=f"feat_{p['id']}", height=150)

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
            section_header("📖", "블로그 설정")
            blog = st.session_state.get('blog_data', {})
            
            # 블로그 데이터 구조 보장
            if 'title_keywords' not in blog:
                blog['title_keywords'] = [{'id': 1, 'text': ''}]
            if 'sub_keywords' not in blog:
                blog['sub_keywords'] = [{'id': 1, 'text': ''}]
            if 'images' not in blog:
                blog['images'] = {}
            if 'story' not in blog:
                blog['story'] = {}
            
            # images 하위 구조 보장
            blog_images = blog['images']
            if 'model_count' not in blog_images:
                blog_images['model_count'] = 8
            if 'model_note' not in blog_images:
                blog_images['model_note'] = ''
            if 'sns_count' not in blog_images:
                blog_images['sns_count'] = 2
            if 'sns_url' not in blog_images:
                blog_images['sns_url'] = ''
            if 'coupon_capture' not in blog_images:
                blog_images['coupon_capture'] = True
            if 'mall_link' not in blog_images:
                blog_images['mall_link'] = ''
            
            # story 하위 구조 보장
            blog_story = blog['story']
            if 'target_audience' not in blog_story:
                blog_story['target_audience'] = ''
            if 'trend' not in blog_story:
                blog_story['trend'] = ''
            if 'product_strength' not in blog_story:
                blog_story['product_strength'] = ''
            if 'campaign_concept' not in blog_story:
                blog_story['campaign_concept'] = ''
            
            st.session_state['blog_data'] = blog
            
            with st.expander("🏷️ 키워드 설정", expanded=True):
                st.caption("필수 제목 키워드 (콤마로 구분)")
                # 단순화를 위해 리스트 UI 대신 텍스트 입력 후 분리 방식으로 변경
                title_kw_str = ", ".join([k.get('text', '') for k in blog.get('title_keywords', []) if k.get('text')])
                new_title_kw = st.text_input("필수 키워드", value=title_kw_str, placeholder="예: 여성패딩, 숏패딩")
                # 저장 로직
                blog['title_keywords'] = [{'id': i, 'text': t.strip()} for i, t in enumerate(new_title_kw.split(','))]

                st.caption("서브 키워드 (콤마로 구분)")
                sub_kw_str = ", ".join([k.get('text', '') for k in blog.get('sub_keywords', []) if k.get('text')])
                new_sub_kw = st.text_input("서브 키워드", value=sub_kw_str)
                blog['sub_keywords'] = [{'id': i, 'text': t.strip()} for i, t in enumerate(new_sub_kw.split(','))]

            with st.expander("🖼️ 활용 이미지", expanded=True):
                i_col1, i_col2 = st.columns(2)
                blog_images['model_count'] = i_col1.number_input("모델 이미지 장수", value=int(blog_images.get('model_count', 8)))
                blog_images['model_note'] = i_col2.text_input("이미지 구분", value=blog_images.get('model_note', ''))
                
                blog_images['sns_url'] = st.text_input("SNS 캡쳐 URL", value=blog_images.get('sns_url', ''))
                blog_images['mall_link'] = st.text_input("자사몰 링크", value=blog_images.get('mall_link', ''))

            with st.expander("✨ 스토리라인", expanded=True):
                blog_story['target_audience'] = st.text_input("타겟 오디언스", value=blog_story.get('target_audience', ''))
                blog_story['trend'] = st.text_area("트렌드 배경", value=blog_story.get('trend', ''))
                blog_story['product_strength'] = st.text_area("제품 특장점", value=blog_story.get('product_strength', ''))
                blog_story['campaign_concept'] = st.text_input("캠페인 컨셉", value=blog_story.get('campaign_concept', ''))

        elif platform == 'instagram':
            section_header("📷", "인스타그램 설정")
            insta = st.session_state['insta_data']
            
            # 기존 데이터 호환성 처리
            if 'mentions' in insta and 'brand_mention' not in insta:
                insta['brand_mention'] = insta.get('mentions', '')
            if 'brand_mention' not in insta:
                insta['brand_mention'] = ''
            if 'celeb_mention' not in insta:
                insta['celeb_mention'] = ''
            if 'tone_and_manner' not in insta:
                insta['tone_and_manner'] = ''
            if 'hashtags' not in insta:
                insta['hashtags'] = ''
            if 'content_type' not in insta:
                insta['content_type'] = 'feed'
            if 'content_size' not in insta:
                insta['content_size'] = '1:1'
            
            # content_type이 유효한 값인지 확인
            content_types = ['feed', 'reels', 'story', 'carousel']
            if insta['content_type'] not in content_types:
                insta['content_type'] = 'feed'
            
            content_sizes = ['1:1', '4:5', '9:16', '1.91:1']
            if insta['content_size'] not in content_sizes:
                insta['content_size'] = '1:1'
            
            with st.expander("📐 콘텐츠 스펙", expanded=True):
                i_col1, i_col2 = st.columns(2)
                insta['content_type'] = i_col1.selectbox("콘텐츠 유형", content_types, 
                                                         index=content_types.index(insta['content_type']))
                insta['content_size'] = i_col2.selectbox("사이즈", content_sizes, 
                                                         index=content_sizes.index(insta['content_size']))
                
                st.markdown("**📍 멘션 계정**")
                m_col1, m_col2 = st.columns(2)
                insta['brand_mention'] = m_col1.text_input("브랜드 계정", value=insta['brand_mention'], placeholder="@brand_official")
                insta['celeb_mention'] = m_col2.text_input("셀럽/모델 계정", value=insta['celeb_mention'], placeholder="@celeb_official")
            
            with st.expander("🎨 톤앤매너", expanded=True):
                insta['tone_and_manner'] = st.text_area("톤앤매너 가이드", value=insta['tone_and_manner'])
                insta['hashtags'] = st.text_area("해시태그", value=insta['hashtags'])

        elif platform == 'youtube':
            section_header("🎬", "유튜브 설정")
            yt = st.session_state.get('youtube_data', {})
            
            # 유튜브 데이터 구조 보장
            if 'content_type' not in yt:
                yt['content_type'] = 'shorts'
            if 'duration' not in yt:
                yt['duration'] = ''
            if 'key_message' not in yt:
                yt['key_message'] = ''
            if 'required_mentions' not in yt:
                yt['required_mentions'] = ''
            
            content_types = ['shorts', 'review', 'vlog', 'integration']
            if yt['content_type'] not in content_types:
                yt['content_type'] = 'shorts'
            
            st.session_state['youtube_data'] = yt
            
            with st.expander("🎬 콘텐츠 스펙", expanded=True):
                y_col1, y_col2 = st.columns(2)
                yt['content_type'] = y_col1.selectbox("콘텐츠 유형", content_types,
                                                      index=content_types.index(yt['content_type']))
                yt['duration'] = y_col2.text_input("권장 영상 길이", value=yt.get('duration', ''))
            
            with st.expander("💬 희망 메시지", expanded=True):
                yt['key_message'] = st.text_area("대표 메시지", value=yt.get('key_message', ''))
                yt['required_mentions'] = st.text_area("필수 멘트", value=yt.get('required_mentions', ''))

        # 4. 공통 법적 문구
        section_header("⚖️", "필수 기재 문구")
        with st.expander("문구 설정", expanded=True):
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
