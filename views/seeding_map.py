"""
리뷰 블로거 시딩 맵 - 월별 제품 카드 뷰
기존 가이드라인과 독립적으로 운영
"""
import streamlit as st
import json
import base64
from datetime import datetime
from io import BytesIO
from data.product_db import fetch_product_info

def init_seeding_map_state():
    """시딩 맵 전용 상태 초기화"""
    if 'seeding_map_data' not in st.session_state:
        st.session_state['seeding_map_data'] = {
            'season': '26SS',
            'highlight_month': get_current_month_default(),  # 하이라이트 월
            'months': {
                'JAN': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
                'FEB': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
                'MAR': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
                'APR': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
                'MAY': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
                'JUN': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
                'JUL': {'event': '', 'key_cate': '', 'headcount': 0, 'main_items': [], 'sub_items': []},
            }
        }

def get_current_month_default():
    """현재 월 반환 (영문 약어)"""
    month_map = {
        1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
        7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'
    }
    return month_map.get(datetime.now().month, 'JAN')

def compress_base64_image(data_url, max_size_kb=200, max_width=400):
    """base64 이미지를 압축하여 반환"""
    if not data_url or not data_url.startswith('data:image'):
        return data_url
    
    # 이미 작은 이미지는 그대로 반환
    if len(data_url) / 1024 < max_size_kb:
        return data_url
    
    try:
        from PIL import Image
        
        # base64 디코딩
        header, b64_data = data_url.split(',', 1)
        img_bytes = base64.b64decode(b64_data)
        
        # 이미지 열기
        img = Image.open(BytesIO(img_bytes))
        
        # RGBA -> RGB 변환
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if len(img.split()) > 3:
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 리사이즈
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        
        # 압축
        quality = 80
        while quality >= 20:
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            if len(buffer.getvalue()) / 1024 <= max_size_kb:
                break
            quality -= 10
        
        # 새 base64 반환
        b64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{b64}"
    except:
        return data_url

def get_saveable_seeding_data():
    """저장 가능한 시딩 맵 데이터 반환"""
    data = st.session_state.get('seeding_map_data', {})
    return {
        'season': data.get('season', '26SS'),
        'highlight_month': data.get('highlight_month', 'JAN'),
        'months': data.get('months', {}),
        'saved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def load_seeding_data_from_json(json_data, compress_images=False):
    """JSON 데이터로부터 시딩 맵 복원"""
    try:
        data = json.loads(json_data)
        
        # 이미지 압축 옵션
        if compress_images and 'months' in data:
            for month_key, month_data in data['months'].items():
                # main_items 이미지 압축
                for item in month_data.get('main_items', []):
                    if item.get('imageUrl'):
                        item['imageUrl'] = compress_base64_image(item['imageUrl'], max_size_kb=200, max_width=400)
                # sub_items 이미지 압축
                for item in month_data.get('sub_items', []):
                    if item.get('imageUrl'):
                        item['imageUrl'] = compress_base64_image(item['imageUrl'], max_size_kb=200, max_width=400)
        
        st.session_state['seeding_map_data'] = {
            'season': data.get('season', '26SS'),
            'highlight_month': data.get('highlight_month', get_current_month_default()),
            'months': data.get('months', {})
        }
        return True, data.get('saved_at', '알 수 없음')
    except Exception as e:
        return False, str(e)

def render_product_card(product, is_current_month=False):
    """제품 카드 렌더링"""
    # 현재 월이면 강조 스타일 적용
    if is_current_month:
        card_style = """
            border: 3px solid #1976d2;
            box-shadow: 0 8px 16px rgba(25, 118, 210, 0.3);
            background: #fff;
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
        """
    else:
        card_style = """
            border: 1px solid #dee2e6;
            background: #fff;
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
        """
    
    # 가격 포맷팅
    price = product.get('price', '')
    if price:
        try:
            price_num = int(str(price).replace(',', '').replace('원', ''))
            price_display = f"{price_num:,}원"
        except:
            price_display = price
    else:
        price_display = ''
    
    # 입고 지연 표시
    delay_badge = ''
    if product.get('delay'):
        delay_badge = f'<span style="background:#dc3545; color:white; padding:2px 6px; border-radius:3px; font-size:0.7em;">{product.get("delay")}</span>'
    
    html = f"""
    <div style="{card_style}">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="background:#f8f9fa; padding:2px 8px; border-radius:4px; font-size:0.8em;">{product.get('headcount', '')}명</span>
            <span style="color:#dc3545; font-weight:bold;">{price_display}</span>
        </div>
        <div style="font-size:0.75em; color:#6c757d; margin-bottom:3px;">{product.get('code', '')}</div>
        {f'<img src="{product.get("imageUrl", "")}" style="width:100%; height:80px; object-fit:contain; margin:5px 0;">' if product.get('imageUrl') else '<div style="width:100%; height:80px; background:#f8f9fa; display:flex; align-items:center; justify-content:center; color:#adb5bd;">No Image</div>'}
        <div style="font-size:0.8em; font-weight:500; margin-top:5px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{product.get('name', '')}</div>
        {delay_badge}
    </div>
    """
    return html

def render_seeding_map():
    """시딩 맵 메인 렌더링"""
    init_seeding_map_state()
    
    st.title("📊 리뷰 블로거 시딩 맵")
    st.caption("월별 시딩 제품을 한눈에 확인하세요")
    
    data = st.session_state['seeding_map_data']
    months_list = list(data['months'].keys())
    
    # 시즌 및 하이라이트 월 설정
    col_season, col_highlight, col_spacer = st.columns([1, 1, 2])
    with col_season:
        data['season'] = st.text_input("시즌", value=data.get('season', '26SS'))
    with col_highlight:
        # 하이라이트 월 선택
        current_highlight = data.get('highlight_month', get_current_month_default())
        if current_highlight not in months_list:
            current_highlight = months_list[0]
        highlight_idx = months_list.index(current_highlight)
        
        selected_highlight = st.selectbox(
            "🔆 하이라이트 월", 
            months_list, 
            index=highlight_idx,
            help="선택한 월의 카드가 파란색 테두리로 강조됩니다"
        )
        data['highlight_month'] = selected_highlight
    
    st.markdown("---")
    
    # 💾 저장/불러오기 섹션
    with st.expander("💾 저장 / 불러오기", expanded=False):
        save_col1, save_col2 = st.columns(2)
        
        with save_col1:
            st.markdown("**📥 시딩 맵 저장**")
            
            # 저장 데이터 생성
            save_data = get_saveable_seeding_data()
            json_str = json.dumps(save_data, ensure_ascii=False, indent=2)
            
            # 파일 크기 표시
            size_kb = len(json_str.encode('utf-8')) / 1024
            if size_kb < 1024:
                size_text = f"{size_kb:.1f} KB"
            else:
                size_text = f"{size_kb/1024:.2f} MB"
            
            file_name = f"시딩맵_{data['season']}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            st.download_button(
                label="💾 JSON으로 저장",
                data=json_str,
                file_name=file_name,
                mime="application/json",
                use_container_width=True
            )
            
            if size_kb > 5120:  # 5MB 초과
                st.warning(f"⚠️ 현재 크기: {size_text}")
            else:
                st.caption(f"📊 현재 크기: {size_text}")
        
        with save_col2:
            st.markdown("**📤 시딩 맵 불러오기**")
            
            uploaded_json = st.file_uploader(
                "JSON 파일 업로드",
                type=['json'],
                key="seeding_load_json",
                label_visibility="collapsed"
            )
            
            if uploaded_json:
                file_size_mb = uploaded_json.size / 1024 / 1024
                
                if file_size_mb > 5:
                    st.warning(f"⚠️ 파일 크기: {file_size_mb:.1f}MB - 이미지가 자동 압축됩니다")
                    compress = True
                else:
                    st.caption(f"📁 파일 크기: {file_size_mb:.2f}MB")
                    compress = False
                
                if st.button("📂 불러오기 실행", use_container_width=True, key="seeding_load_btn"):
                    json_content = uploaded_json.read().decode('utf-8')
                    success, info = load_seeding_data_from_json(json_content, compress_images=compress)
                    if success:
                        st.success(f"✅ 불러오기 완료! (저장 시간: {info})")
                        st.rerun()
                    else:
                        st.error(f"❌ 불러오기 실패: {info}")
    
    st.markdown("---")
    
    # 제품 추가 섹션
    with st.expander("➕ 제품 추가 (URL로 불러오기)", expanded=False):
        add_col1, add_col2, add_col3 = st.columns([2, 1, 1])
        
        with add_col1:
            product_url = st.text_input("공식몰 제품 URL", placeholder="https://sergiotacchini.co.kr/...", key="seeding_product_url")
        with add_col2:
            target_month = st.selectbox("추가할 월", list(data['months'].keys()), key="seeding_target_month")
        with add_col3:
            item_type = st.selectbox("구분", ["MAIN", "SUB"], key="seeding_item_type")
        
        headcount_col, delay_col, btn_col = st.columns([1, 1, 1])
        with headcount_col:
            item_headcount = st.number_input("인원", value=10, min_value=0, key="seeding_headcount")
        with delay_col:
            item_delay = st.text_input("입고 지연", placeholder="예: 1/22 입고 지연", key="seeding_delay")
        
        if st.button("제품 추가", type="primary", use_container_width=True):
            if product_url:
                with st.spinner("제품 정보 조회 중..."):
                    product_info = fetch_product_info(product_url)
                    if product_info:
                        new_item = {
                            'code': product_info.get('productCode', ''),
                            'name': product_info.get('name', ''),
                            'price': product_info.get('price', ''),
                            'imageUrl': product_info.get('imageUrl', ''),
                            'headcount': item_headcount,
                            'delay': item_delay,
                            'url': product_url
                        }
                        
                        if item_type == "MAIN":
                            data['months'][target_month]['main_items'].append(new_item)
                        else:
                            data['months'][target_month]['sub_items'].append(new_item)
                        
                        st.success(f"✅ {target_month}월 {item_type}에 '{product_info.get('name', '')}' 추가 완료!")
                        st.rerun()
                    else:
                        st.error("❌ 제품 정보를 가져올 수 없습니다.")
            else:
                st.warning("⚠️ URL을 입력해주세요.")
    
    st.markdown("---")
    
    # 월별 헤더 정보 편집
    with st.expander("📝 월별 정보 편집", expanded=False):
        edit_month = st.selectbox("편집할 월", list(data['months'].keys()), key="edit_month_select")
        month_data = data['months'][edit_month]
        
        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            month_data['event'] = st.text_input("EVENT", value=month_data.get('event', ''), key=f"event_{edit_month}")
        with e_col2:
            month_data['key_cate'] = st.text_input("KEY CATE", value=month_data.get('key_cate', ''), key=f"keycate_{edit_month}")
        with e_col3:
            month_data['headcount'] = st.number_input("인원수", value=int(month_data.get('headcount', 0)), key=f"headcount_{edit_month}")
    
    st.markdown("---")
    
    # 월별 카드 그리드 표시
    st.subheader(f"🗓️ {data['season']} 리뷰블로거 시딩 맵")
    
    months = list(data['months'].keys())
    
    # CSS 스타일
    st.markdown("""
    <style>
        .month-header {
            background: linear-gradient(135deg, #343a40 0%, #495057 100%);
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            border-radius: 8px 8px 0 0;
        }
        .month-header.current {
            background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%);
        }
        .month-info {
            background: #f8f9fa;
            padding: 8px;
            font-size: 0.85em;
            border-left: 1px solid #dee2e6;
            border-right: 1px solid #dee2e6;
        }
        .month-content {
            border: 1px solid #dee2e6;
            border-top: none;
            padding: 10px;
            min-height: 200px;
            border-radius: 0 0 8px 8px;
        }
        .section-label {
            background: #e9ecef;
            padding: 5px 10px;
            font-size: 0.75em;
            font-weight: bold;
            margin: 10px 0 5px 0;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 월별 컬럼 생성
    cols = st.columns(len(months))
    highlight_month = data.get('highlight_month', get_current_month_default())
    
    for idx, month in enumerate(months):
        is_highlighted = (month == highlight_month)
        month_data = data['months'][month]
        
        with cols[idx]:
            # 월 헤더
            header_class = "month-header current" if is_highlighted else "month-header"
            st.markdown(f'<div class="{header_class}">{month}</div>', unsafe_allow_html=True)
            
            # 월 정보
            st.markdown(f"""
            <div class="month-info">
                <div><strong>EVENT:</strong> {month_data.get('event', '-')}</div>
                <div><strong>KEY:</strong> {month_data.get('key_cate', '-')}</div>
                <div><strong>인원:</strong> {month_data.get('headcount', 0)}인</div>
            </div>
            """, unsafe_allow_html=True)
            
            # MAIN 아이템
            st.markdown('<div class="section-label">MAIN (ITEM)</div>', unsafe_allow_html=True)
            main_items = month_data.get('main_items', [])
            if main_items:
                for item in main_items:
                    st.markdown(render_product_card(item, is_highlighted), unsafe_allow_html=True)
            else:
                st.caption("등록된 제품 없음")
            
            # SUB 아이템
            st.markdown('<div class="section-label">SUB</div>', unsafe_allow_html=True)
            sub_items = month_data.get('sub_items', [])
            if sub_items:
                for item in sub_items:
                    st.markdown(render_product_card(item, is_highlighted), unsafe_allow_html=True)
            else:
                st.caption("등록된 제품 없음")
            
            # 삭제 버튼
            if main_items or sub_items:
                if st.button("🗑️ 전체 삭제", key=f"clear_{month}", use_container_width=True):
                    data['months'][month]['main_items'] = []
                    data['months'][month]['sub_items'] = []
                    st.rerun()
