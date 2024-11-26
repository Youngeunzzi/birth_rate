import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium

# 제목 및 설명
st.title("시군구별 합계출산율 Choropleth 지도")
st.markdown("👼🏻아래의 지도는 대한민국의 시군구별 합계출산율 데이터를 시각화한 Choropleth 지도입니다🍼")
st.markdown("색상이 진할수록 합계출산율이 높은 지역입니다:)")


# 엑셀파일 불러오기
excel_file_path = "C:/Users/lynn9/데이터시각화(실습)/data/연령별_출산율_및_합계출산율_행정구역별.xlsx"
df = pd.read_excel(excel_file_path)

# 시군구별 합계출산율 데이터 준비하기
df = df[['행정구역별', '합계출산율 (가임여성 1명당 명)']]
df.columns = ['시군구', '합계출산율']
df['시군구'] = df['시군구'].str.strip()
df['시군구'] = df['시군구'].str.replace('서울특별시', '서울')

# 시군구 -> 지역 매핑
district_mapping = {
    '권선구': '수원시 권선구',
    '기흥구': '용인시기흥구',
    '단원구': '안산시단원구',
    '덕양구': '고양시덕양구',
    '덕진구': '전주시덕진구',
    '동남구': '천안시동남구',
    '마산합포구': '창원시 마산합포구',
    '마산회원구': '창원시 마산회원구',
    '분당구': '성남시 분당구',
    '상당구': '청주시 상당구',
    '상록구': '안산시상록구',
    '서북구': '천안시서북구',
    '서원구': '청주시 서원구',
    '성산구': '창원시 성산구',
    '세종시': '세종특별자치시',
    '수정구': '성남시 수정구',
    '수지구': '용인시수지구',
    '영통구': '수원시 영통구',
    '완산구': '전주시완산구',
    '의창구': '창원시 의창구',
    '일산동구': '고양시일산동구',
    '일산서구': '고양시일산서구',
    '장안구': '수원시 장안구',
    '중원구': '성남시 중원구',
    '진해구': '창원시 진해구',
    '처인구': '용인시처인구',
    '청원구': '청주시 청원구',
    '팔달구': '수원시 팔달구',
    '포항-남구': '포항시 남구',
    '포항-북구': '포항시 북구',
    '흥덕구': '청주시 흥덕구',
    '천안시': '천안시동남구, 천안시서북구',
    '전주시': '전주시덕진구, 전주시완산구',
    '용인시': '용인시기흥구, 용인시수지구, 용인시처인구',
    '안산시': '안산시단원구, 안산시상록구',
    '안양시': '안양시',
    '만안구': '안양시만안구',
    '동안구': '안양시동안구',
    '성남시': '성남시 분당구, 성남시 수정구, 성남시 중원구',
    '수원시': '수원시 권선구, 수원시 영통구, 수원시 장안구, 수원시 팔달구'
}
df['시군구'] = df['시군구'].map(district_mapping).fillna(df['시군구'])

# GeoJSON 파일 불러오기
geojson_file_path = "C:/Users/lynn9/데이터시각화(실습)/data/TL_SCCO_SIG.json"
with open(geojson_file_path, 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)

# GeoJSON 시군구 이름 공백 제거 및 형식 통일하기
for feature in geojson_data['features']:
    feature['properties']['SIG_KOR_NM'] = feature['properties']['SIG_KOR_NM'].strip()
    feature['properties']['SIG_KOR_NM'] = feature['properties']['SIG_KOR_NM'].replace('서울특별시', '서울')

# Choropleth 지도 생성하기
m = folium.Map(location=[37.5665, 126.978], zoom_start=7)
folium.Choropleth(
    geo_data=geojson_data,
    data=df,
    columns=['시군구', '합계출산율'],
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='합계출산율'
).add_to(m)


# Streamlit에서 지도 표시
st_folium(m, width=800, height=600)
