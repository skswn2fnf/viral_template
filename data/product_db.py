import re
import time
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64
import urllib3

# SSL 경고 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ═══════════════════════════════════════════════════════════════
# 📦 Sergio Tacchini 제품 데이터베이스 (v6 스키마 반영)
# ═══════════════════════════════════════════════════════════════
PRODUCT_DATABASE = {
    # 기존 데이터 유지
    'TWDJ20656': {
        'name': 'W 클라시코 코듀로이 다운점퍼',
        'price': '359,000',
        'colors': ['NAVY', 'BROWN', 'IVORY'],
        'sizes': 'S, M',
        'features': '- 클래식하고 고급스러운 코듀로이 소재의 여성 클래식 윈터 다운\n- 크롭한 기장감에 소매 시보리와 밑단 스트링 적용으로 바람 유입 차단\n- 2WAY 지퍼 적용\n- 소프트 코듀로이 소재로 은은한 광택과 부드러운 터치\n- 덕다운 충전재로 가벼운 착용감과 우수한 보온력\n- RELAX FIT'
    },
    'TWDJ20156': { 'name': 'W 쿠쉬웜 다운점퍼', 'price': '299,000', 'colors': ['BROWN', 'BLACK', 'IVORY'], 'sizes': 'S, M', 'features': '- 세르지오 타키니의 시그니처 액티브 클래식 패딩\n- 가볍고 스포티한 절개라인이 특징\n- 실루엣 조절이 가능한 스트링으로 볼륨감있는 핏 연출 가능\n- 하이넥 디자인으로 겨울철 바람 차단\n- 내구성이 뛰어난 고밀도 나일론 소재로 생활 방수 가능\n- RELAX FIT' },
    'TWMT19056': { 'name': 'W 쿠쉬웜 플리스 하프집', 'price': '179,000', 'colors': ['KHAKI', 'BROWN', 'IVORY'], 'sizes': 'S, M', 'features': '- 부드럽고 포근한 플리스 소재의 하프집업\n- 소매에 Thumb Hole 적용으로 활동성과 보온성 향상\n- 도톰한 두께감과 여유있는 실루엣으로 아우터로도 활용 가능\n- OVER FIT' },
    'TWMT64556': { 'name': 'W MC 하프집업 플리스 풀오버', 'price': '179,000', 'colors': ['NAVY'], 'sizes': 'S, M', 'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 하프집업 풀오버\n- 등판에 그라데이션 자수기법을 사용한 로고 아트웍 포인트\n- RELAX FIT' },
    'TWMT64546': { 'name': 'W MC 하프집업 플리스 풀오버', 'price': '179,000', 'colors': ['BROWN'], 'sizes': 'S, M', 'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 하프집업 풀오버\n- 등판에 그라데이션 자수기법을 사용한 로고 아트웍 포인트\n- RELAX FIT' },
    'TWTR19156': { 'name': 'W 쿠쉬웜 플리스 후드집업', 'price': '179,000', 'colors': ['IVORY', 'KHAKI'], 'sizes': 'S, M', 'features': '- 세르지오 타키니의 시그니처 쿠쉬웜 소재의 플리스 버전\n- 밑단에 스트링을 적용하여 볼륨감 있는 실루엣 연출 가능\n- 플리스 소재가 가벼운 공기층을 형성하여 경량하지만 따뜻하며 놀라운 신축성\n- RELAX FIT' },
    'TWSK60156': { 'name': 'W MC 마이크로플리스 스커트', 'price': '159,000', 'colors': ['NAVY'], 'sizes': 'S, M', 'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 A라인 스커트\n- 허리에 E-밴드가 내장되어 편안한 착용\n- 볼 수납이 가능한 기능성 포켓 이너팬츠 내장' },
    'TWSK60146': { 'name': 'W MC 마이크로플리스 스커트', 'price': '159,000', 'colors': ['BROWN'], 'sizes': 'S, M', 'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 A라인 스커트\n- 허리에 E-밴드가 내장되어 편안한 착용\n- 볼 수납이 가능한 기능성 포켓 이너팬츠 내장' },
    'TWPT19156': { 'name': 'W 쿠쉬웜 플리스 루즈 조거 팬츠', 'price': '149,000', 'colors': ['IVORY', 'KHAKI'], 'sizes': 'S, M', 'features': '- 부드럽고 포근한 플리스 소재의 조거 팬츠\n- 넉넉한 루즈핏으로 편안한 착용감\n- 밑단 시보리로 핏 조절 가능' },
    'TWPT10844': { 'name': 'W 에센셜 부츠컷 레깅스 팬츠', 'price': '129,000', 'colors': ['BLACK', 'NAVY', 'BROWN'], 'sizes': 'S, M', 'features': '- 겨울 시즌에 가장 활용도 높게 즐길 수 있는 코트 레깅스 팬츠\n- 부츠컷 실루엣으로 다리 라인을 길어보이게 연출' },
    'TWPT11046': { 'name': 'W 에센셜 기모 부츠컷 레깅스 팬츠', 'price': '129,000', 'colors': ['BLACK', 'BROWN'], 'sizes': 'S, M', 'features': '- 따뜻한 기모 안감이 적용된 부츠컷 레깅스 팬츠\n- 겨울철 보온성과 스타일을 동시에' },
    'TXMT16054': { 'name': 'U 쿠쉬라이트 프렌치 클래식 맨투맨', 'price': '119,000', 'colors': ['NAVY', 'IVORY', 'BLACK'], 'sizes': 'S, M, L', 'features': '- 프렌치 테리 소재의 클래식 맨투맨\n- 가볍고 부드러운 착용감\n- 세르지오 타키니 시그니처 로고 자수' },
    'TXMT14054': { 'name': 'U 쿠쉬라이트 베이직 맨투맨', 'price': '119,000', 'colors': ['IVORY', 'BLACK', 'NAVY'], 'sizes': 'S, M, L', 'features': '- 베이직한 디자인의 데일리 맨투맨\n- 가볍고 부드러운 쿠쉬라이트 소재' },
    'TXMT14154': { 'name': 'U 쿠쉬라이트 하프집', 'price': '129,000', 'colors': ['BLACK', 'IVORY'], 'sizes': 'S, M, L', 'features': '- 베이직한 디자인의 하프집업\n- 가볍고 부드러운 쿠쉬라이트 소재' },
    'TMMT15056': { 'name': 'M 클래식 기모 하프집 풀오버', 'price': '139,000', 'colors': ['BLACK', 'NAVY', 'IVORY'], 'sizes': 'M, L, XL', 'features': '- 따뜻한 기모 안감이 적용된 하프집 풀오버\n- 클래식한 디자인과 편안한 착용감' },
    'TXSO4105N': { 'name': 'U 3-PACK 크루 삭스', 'price': '19,900', 'colors': ['WHITE', 'BLACK', 'MIXED'], 'sizes': 'FREE', 'features': '- 데일리로 활용하기 좋은 크루 삭스 3팩 세트\n- 세르지오 타키니 로고 포인트' },
    'TWSO9044N': { 'name': 'W 셔링 오버 니삭스', 'price': '35,000', 'colors': ['BLACK', 'WHITE'], 'sizes': 'FREE', 'features': '- 셔링 디테일이 포인트인 오버 니삭스\n- 테니스 스커트와 매치하기 좋은 아이템' },
    'TXSO4015N': { 'name': 'U 에센셜 크루 삭스', 'price': '15,000', 'colors': ['WHITE', 'BLACK'], 'sizes': 'FREE', 'features': '- 에센셜 라인의 베이직 크루 삭스\n- 데일리로 활용하기 좋은 아이템' }
}

def extract_product_code(input_url):
    # URL 정제 (파라미터 제거)
    clean_url = input_url.split('?')[0]
    
    # 세르지오 타키니 패턴
    sergio_patterns = [
        r'sergiotacchini\.co\.kr\/product-detail\/([A-Z0-9]+)-[A-Z]{2,3}',
        r'product-detail\/([A-Z0-9]+)-[A-Z]{2,3}',
        r'([A-Z]{2,4}\d{5})-[A-Z]{2,3}',
        r'([A-Z]{4}\d{5}[A-Z]?)'
    ]
    
    # 듀베티카 패턴 (세르지오 타키니와 동일한 URL 구조)
    duvetica_patterns = [
        r'duvetica\.co\.kr\/product-detail\/([A-Z0-9]+)-[A-Z]{2,3}',
        r'duvetica\.co\.kr\/product\/([^\/\?]+)',
        r'duvetica\.co\.kr\/goods\/([^\/\?]+)',
        r'\/product\/([A-Z0-9\-]+)',
        r'\/goods\/view\?no=(\d+)',
        r'goodsNo=(\d+)'
    ]
    
    # 1차 시도: 세르지오 타키니 패턴
    for pattern in sergio_patterns:
        match = re.search(pattern, clean_url, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    
    # 2차 시도: 듀베티카 패턴
    for pattern in duvetica_patterns:
        match = re.search(pattern, clean_url, re.IGNORECASE)
        if match:
            return match.group(1)
            
    # 3차 시도: 원본 URL로 확인 (혹시 파라미터 쪽에 코드가 있을 경우 대비)
    for pattern in sergio_patterns + duvetica_patterns:
        match = re.search(pattern, input_url, re.IGNORECASE)
        if match:
            return match.group(1)
            
    # 직접 입력 패턴
    direct_match = re.match(r'^([A-Z]{4}\d{5}[A-Z]?)(?:-[A-Z]{2,3})?$', input_url.strip().upper())
    if direct_match:
        return direct_match.group(1)
        
    return None

def get_referer_from_url(url):
    """URL에서 Referer 추출"""
    if 'duvetica' in url.lower():
        return 'https://www.duvetica.co.kr/'
    elif 'sergiotacchini' in url.lower():
        return 'https://www.sergiotacchini.co.kr/'
    else:
        # URL에서 도메인 추출
        match = re.search(r'https?://([^/]+)', url)
        if match:
            return f"https://{match.group(1)}/"
        return ''

def process_image_from_url(img_url, referer=None):
    """이미지 URL에서 썸네일 생성"""
    try:
        if not referer:
            referer = get_referer_from_url(img_url)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': referer
        }
        # verify=False로 SSL 에러 방지
        img_response = requests.get(img_url, headers=headers, timeout=10, verify=False)
        if img_response.status_code != 200:
            return None
        img = Image.open(BytesIO(img_response.content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.thumbnail((300, 300))
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=80)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"Image process failed: {e}")
        return None

def crawl_product_page(url, product_code):
    """
    DB에 없는 제품일 경우, 실제 웹페이지를 크롤링하여 정보를 추출합니다.
    세르지오 타키니, 듀베티카 등 다양한 쇼핑몰을 지원합니다.
    """
    try:
        referer = get_referer_from_url(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': referer
        }
        # verify=False 옵션 추가
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code != 200:
            print(f"Failed to connect: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. 제품명 추출 (다양한 방법 시도)
        name = ""
        # og:title 시도
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            name = og_title['content']
        
        # h1 태그 시도
        if not name:
            h1 = soup.find('h1')
            if h1:
                name = h1.get_text().strip()
        
        # 상품명 클래스 시도 (다양한 쇼핑몰 대응)
        if not name:
            for selector in ['.goods_name', '.product-name', '.prd_name', '.item_name', '[class*="product"][class*="name"]']:
                elem = soup.select_one(selector)
                if elem:
                    name = elem.get_text().strip()
                    break
        
        if name:
            name = name.split(' - ')[0].split(' | ')[0].strip()
        
        # 2. 가격 추출 (다양한 방법 시도)
        price = ""
        # og:description에서 가격 찾기
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            price_match = re.search(r'(\d{1,3}(?:,\d{3})+)원?', og_desc['content'])
            if price_match:
                price = price_match.group(1)
        
        # 가격 클래스에서 찾기
        if not price:
            for selector in ['.price', '.goods_price', '.prd_price', '.sell_price', '[class*="price"]']:
                elem = soup.select_one(selector)
                if elem:
                    price_match = re.search(r'(\d{1,3}(?:,\d{3})+)', elem.get_text())
                    if price_match:
                        price = price_match.group(1)
                        break
        
        # 전체 텍스트에서 가격 찾기
        if not price:
            text_content = soup.get_text()
            price_matches = re.findall(r'(\d{1,3}(?:,\d{3})+)', text_content)
            for p in price_matches:
                val = int(p.replace(',', ''))
                if 10000 < val < 5000000: 
                    price = p
                    break
                    
        # 3. 특징 추출 (다양한 방법 시도)
        features = ""
        
        # DESCRIPTION 영역 찾기
        desc_markers = soup.find_all(string=re.compile("DESCRIPTION|상품설명|제품설명|상세정보", re.IGNORECASE))
        for marker in desc_markers:
            parent_section = marker.find_parent('div') or marker.find_parent('section')
            if parent_section:
                text = parent_section.get_text(separator='\n')
                for keyword in ["DESCRIPTION", "상품설명", "제품설명", "상세정보"]:
                    if keyword in text:
                        parts = text.split(keyword)
                        target_text = parts[1] if len(parts) > 1 else text
                        for stopper in ["상품코드", "소재", "제조년월", "SIZE", "SHIPPING", "배송", "교환", "반품"]:
                            if stopper in target_text:
                                target_text = target_text.split(stopper)[0]
                        lines = [line.strip() for line in target_text.split('\n') if line.strip()]
                        clean_lines = []
                        for line in lines:
                            if len(line) > 2 and len(line) < 200:
                                if not line.startswith('-') and not line.startswith('*'):
                                    clean_lines.append(f"- {line}")
                                else:
                                    clean_lines.append(line)
                        features = "\n".join(clean_lines[:6])
                        if features:
                            break
                if features:
                    break

        # 4. 이미지 추출
        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image and og_image.get('content') else None
        
        # og:image가 없으면 다른 방법 시도
        if not image_url:
            for selector in ['.goods_image img', '.product-image img', '.prd_img img', '[class*="product"] img']:
                elem = soup.select_one(selector)
                if elem and elem.get('src'):
                    image_url = elem['src']
                    break
        
        # 상대 경로를 절대 경로로 변환
        if image_url and not image_url.startswith('http'):
            # URL에서 도메인 추출
            domain_match = re.search(r'(https?://[^/]+)', url)
            if domain_match:
                image_url = f"{domain_match.group(1)}{image_url}"
            
        processed_image = process_image_from_url(image_url, referer) if image_url else None
        if not processed_image:
            processed_image = f"https://placehold.co/300x300/png?text={product_code}"

        return {
            "id": int(time.time() * 1000),
            "name": name,
            "price": price,
            "colors": "", 
            "sizes": "", 
            "features": features,
            "productCode": product_code,
            "productUrl": url,
            "imageUrl": processed_image,
            "isMain": False
        }

    except Exception as e:
        print(f"Crawling failed: {e}")
        return None

def fetch_product_info(url_input):
    if not url_input:
        return None
        
    product_code = extract_product_code(url_input)
    if not product_code:
        product_code = "UNKNOWN"
    
    target_url = url_input.split('?')[0] if "http" in url_input else ""
    
    # 1. DB 조회
    if product_code in PRODUCT_DATABASE:
        info = PRODUCT_DATABASE[product_code]
        if not target_url:
            first_color_suffix = f"{info['colors'][0][:2]}S" if info['colors'] else "BKS"
            target_url = f"https://www.sergiotacchini.co.kr/product-detail/{product_code}-{first_color_suffix}"
            
        thumbnail_data = None
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(target_url, headers=headers, timeout=5, verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                og_image = soup.find('meta', property='og:image')
                if og_image:
                    thumbnail_data = process_image_from_url(og_image['content'])
        except:
            pass
            
        if not thumbnail_data:
            thumbnail_data = f"https://placehold.co/300x300/png?text={product_code}"
        
        return {
            "id": int(time.time() * 1000),
            "name": info['name'],
            "price": info['price'],
            "colors": ", ".join(info['colors']),
            "sizes": info['sizes'],
            "features": info['features'],
            "productCode": product_code,
            "productUrl": target_url,
            "imageUrl": thumbnail_data,
            "isMain": False
        }
    
    # 2. 크롤링 시도
    if target_url:
        crawled_data = crawl_product_page(target_url, product_code)
        if crawled_data:
            return crawled_data
            
    # 3. 실패 시 빈 폼이라도 반환 (에러 방지)
    return {
        "id": int(time.time() * 1000),
        "name": "",
        "price": "",
        "colors": "",
        "sizes": "",
        "features": "",
        "productCode": product_code,
        "productUrl": target_url or url_input,
        "imageUrl": f"https://placehold.co/300x300/png?text={product_code}",
        "isMain": False
    }
