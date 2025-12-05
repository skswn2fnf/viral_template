import re
import time
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64

# ═══════════════════════════════════════════════════════════════
# 📦 Sergio Tacchini 제품 데이터베이스 (v6 스키마 반영)
# ═══════════════════════════════════════════════════════════════
PRODUCT_DATABASE = {
    # 다운점퍼 - 클라시코 코듀로이
    'TWDJ20656': {
        'name': 'W 클라시코 코듀로이 다운점퍼',
        'price': '359,000',
        'colors': ['NAVY', 'BROWN', 'IVORY'],
        'sizes': 'S, M',
        'features': '- 클래식하고 고급스러운 코듀로이 소재의 여성 클래식 윈터 다운\n- 크롭한 기장감에 소매 시보리와 밑단 스트링 적용으로 바람 유입 차단\n- 2WAY 지퍼 적용\n- 소프트 코듀로이 소재로 은은한 광택과 부드러운 터치\n- 덕다운 충전재로 가벼운 착용감과 우수한 보온력\n- RELAX FIT'
    },
    # 다운점퍼 - 쿠쉬웜
    'TWDJ20156': {
        'name': 'W 쿠쉬웜 다운점퍼',
        'price': '299,000',
        'colors': ['BROWN', 'BLACK', 'IVORY'],
        'sizes': 'S, M',
        'features': '- 세르지오 타키니의 시그니처 액티브 클래식 패딩\n- 가볍고 스포티한 절개라인이 특징\n- 실루엣 조절이 가능한 스트링으로 볼륨감있는 핏 연출 가능\n- 하이넥 디자인으로 겨울철 바람 차단\n- 내구성이 뛰어난 고밀도 나일론 소재로 생활 방수 가능\n- RELAX FIT'
    },
    # 플리스 - 쿠쉬웜 하프집
    'TWMT19056': {
        'name': 'W 쿠쉬웜 플리스 하프집',
        'price': '179,000',
        'colors': ['KHAKI', 'BROWN', 'IVORY'],
        'sizes': 'S, M',
        'features': '- 부드럽고 포근한 플리스 소재의 하프집업\n- 소매에 Thumb Hole 적용으로 활동성과 보온성 향상\n- 도톰한 두께감과 여유있는 실루엣으로 아우터로도 활용 가능\n- OVER FIT'
    },
    # 플리스 - MC 하프집업
    'TWMT64556': {
        'name': 'W MC 하프집업 플리스 풀오버',
        'price': '179,000',
        'colors': ['NAVY'],
        'sizes': 'S, M',
        'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 하프집업 풀오버\n- 등판에 그라데이션 자수기법을 사용한 로고 아트웍 포인트\n- RELAX FIT'
    },
    'TWMT64546': {
        'name': 'W MC 하프집업 플리스 풀오버',
        'price': '179,000',
        'colors': ['BROWN'],
        'sizes': 'S, M',
        'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 하프집업 풀오버\n- 등판에 그라데이션 자수기법을 사용한 로고 아트웍 포인트\n- RELAX FIT'
    },
    # 플리스 후드집업
    'TWTR19156': {
        'name': 'W 쿠쉬웜 플리스 후드집업',
        'price': '179,000',
        'colors': ['IVORY', 'KHAKI'],
        'sizes': 'S, M',
        'features': '- 세르지오 타키니의 시그니처 쿠쉬웜 소재의 플리스 버전\n- 밑단에 스트링을 적용하여 볼륨감 있는 실루엣 연출 가능\n- 플리스 소재가 가벼운 공기층을 형성하여 경량하지만 따뜻하며 놀라운 신축성\n- RELAX FIT'
    },
    # 스커트
    'TWSK60156': {
        'name': 'W MC 마이크로플리스 스커트',
        'price': '159,000',
        'colors': ['NAVY'],
        'sizes': 'S, M',
        'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 A라인 스커트\n- 허리에 E-밴드가 내장되어 편안한 착용\n- 볼 수납이 가능한 기능성 포켓 이너팬츠 내장'
    },
    'TWSK60146': {
        'name': 'W MC 마이크로플리스 스커트',
        'price': '159,000',
        'colors': ['BROWN'],
        'sizes': 'S, M',
        'features': '- 소프트한 터치감과 보온력이 우수하고 가벼운 중량감이 특징인 마이크로 플리스 A라인 스커트\n- 허리에 E-밴드가 내장되어 편안한 착용\n- 볼 수납이 가능한 기능성 포켓 이너팬츠 내장'
    },
    # 팬츠
    'TWPT19156': {
        'name': 'W 쿠쉬웜 플리스 루즈 조거 팬츠',
        'price': '149,000',
        'colors': ['IVORY', 'KHAKI'],
        'sizes': 'S, M',
        'features': '- 부드럽고 포근한 플리스 소재의 조거 팬츠\n- 넉넉한 루즈핏으로 편안한 착용감\n- 밑단 시보리로 핏 조절 가능'
    },
    'TWPT10844': {
        'name': 'W 에센셜 부츠컷 레깅스 팬츠',
        'price': '129,000',
        'colors': ['BLACK', 'NAVY', 'BROWN'],
        'sizes': 'S, M',
        'features': '- 겨울 시즌에 가장 활용도 높게 즐길 수 있는 코트 레깅스 팬츠\n- 부츠컷 실루엣으로 다리 라인을 길어보이게 연출'
    },
    'TWPT11046': {
        'name': 'W 에센셜 기모 부츠컷 레깅스 팬츠',
        'price': '129,000',
        'colors': ['BLACK', 'BROWN'],
        'sizes': 'S, M',
        'features': '- 따뜻한 기모 안감이 적용된 부츠컷 레깅스 팬츠\n- 겨울철 보온성과 스타일을 동시에'
    },
    # 맨투맨/스웨터
    'TXMT16054': {
        'name': 'U 쿠쉬라이트 프렌치 클래식 맨투맨',
        'price': '119,000',
        'colors': ['NAVY', 'IVORY', 'BLACK'],
        'sizes': 'S, M, L',
        'features': '- 프렌치 테리 소재의 클래식 맨투맨\n- 가볍고 부드러운 착용감\n- 세르지오 타키니 시그니처 로고 자수'
    },
    'TXMT14054': {
        'name': 'U 쿠쉬라이트 베이직 맨투맨',
        'price': '119,000',
        'colors': ['IVORY', 'BLACK', 'NAVY'],
        'sizes': 'S, M, L',
        'features': '- 베이직한 디자인의 데일리 맨투맨\n- 가볍고 부드러운 쿠쉬라이트 소재'
    },
    'TXMT14154': {
        'name': 'U 쿠쉬라이트 하프집',
        'price': '129,000',
        'colors': ['BLACK', 'IVORY'],
        'sizes': 'S, M, L',
        'features': '- 베이직한 디자인의 하프집업\n- 가볍고 부드러운 쿠쉬라이트 소재'
    },
    'TMMT15056': {
        'name': 'M 클래식 기모 하프집 풀오버',
        'price': '139,000',
        'colors': ['BLACK', 'NAVY', 'IVORY'],
        'sizes': 'M, L, XL',
        'features': '- 따뜻한 기모 안감이 적용된 하프집 풀오버\n- 클래식한 디자인과 편안한 착용감'
    },
    # 악세서리
    'TXSO4105N': {
        'name': 'U 3-PACK 크루 삭스',
        'price': '19,900',
        'colors': ['WHITE', 'BLACK', 'MIXED'],
        'sizes': 'FREE',
        'features': '- 데일리로 활용하기 좋은 크루 삭스 3팩 세트\n- 세르지오 타키니 로고 포인트'
    },
    'TWSO9044N': {
        'name': 'W 셔링 오버 니삭스',
        'price': '35,000',
        'colors': ['BLACK', 'WHITE'],
        'sizes': 'FREE',
        'features': '- 셔링 디테일이 포인트인 오버 니삭스\n- 테니스 스커트와 매치하기 좋은 아이템'
    },
    'TXSO4015N': {
        'name': 'U 에센셜 크루 삭스',
        'price': '15,000',
        'colors': ['WHITE', 'BLACK'],
        'sizes': 'FREE',
        'features': '- 에센셜 라인의 베이직 크루 삭스\n- 데일리로 활용하기 좋은 아이템'
    }
}

def extract_product_code(input_url):
    """
    URL 또는 텍스트에서 상품 코드를 추출합니다.
    """
    patterns = [
        r'sergiotacchini\.co\.kr\/product-detail\/([A-Z0-9]+)-[A-Z]{2,3}',
        r'product-detail\/([A-Z0-9]+)-[A-Z]{2,3}',
        r'([A-Z]{2,4}\d{5})-[A-Z]{2,3}',
        r'([A-Z]{4}\d{5}[A-Z]?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_url, re.IGNORECASE)
        if match:
            return match.group(1).upper()
            
    # 전체 코드에서 컬러 부분 제거
    full_code_match = re.search(r'([A-Z]{4}\d{5}[A-Z]?)-[A-Z]{2,3}', input_url, re.IGNORECASE)
    if full_code_match:
        return full_code_match.group(1).upper()
        
    # 직접 입력된 경우
    direct_match = re.match(r'^([A-Z]{4}\d{5}[A-Z]?)(?:-[A-Z]{2,3})?$', input_url.strip().upper())
    if direct_match:
        return direct_match.group(1)
        
    return None

def get_processed_thumbnail(product_url):
    """
    제품 상세 페이지에서 og:image를 찾고, 
    이를 다운로드하여 작은 사이즈(썸네일)로 리사이징한 뒤 Base64 문자열로 반환합니다.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 1. 페이지 접속 및 메타태그 추출
        response = requests.get(product_url, headers=headers, timeout=3)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        
        if not og_image or not og_image.get('content'):
            return None
            
        image_url = og_image['content']
        
        # 2. 이미지 다운로드
        img_response = requests.get(image_url, headers=headers, timeout=5)
        if img_response.status_code != 200:
            return None
            
        # 3. 이미지 리사이징 (PIL)
        img = Image.open(BytesIO(img_response.content))
        
        # RGB 변환 (PNG 등 투명도가 있는 경우 호환성 위해)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # 썸네일 생성 (가로세로 최대 300px, 비율 유지)
        img.thumbnail((300, 300))
        
        # 4. Base64 인코딩
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=80) # 압축 품질 80%
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{img_str}"

    except Exception as e:
        print(f"Thumbnail processing failed: {e}")
        return None

def fetch_product_info(url_input):
    """
    제품 정보를 조회하고 썸네일 이미지를 생성합니다.
    """
    if not url_input:
        return None
        
    product_code = extract_product_code(url_input)
    
    if product_code and product_code in PRODUCT_DATABASE:
        info = PRODUCT_DATABASE[product_code]
        
        if "http" in url_input:
            target_url = url_input
        else:
            first_color_suffix = f"{info['colors'][0][:2]}S" if info['colors'] else "BKS"
            target_url = f"https://www.sergiotacchini.co.kr/product-detail/{product_code}-{first_color_suffix}"
        
        # 이미지 처리 (리사이징 및 Base64 변환)
        thumbnail_data = get_processed_thumbnail(target_url)
        
        # 실패 시 Placeholder
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
    
    return None
