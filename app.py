from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Flask 환경에서 GUI 백엔드 사용 방지
import matplotlib.pyplot as plt
# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def save_as_image(gu_data):
    plt.figure(figsize=(10, 5))
    plt.bar(gu_data['label'], gu_data['value'])
    plt.xlabel('구')
    plt.ylabel('대여소 수')
    plt.title('구별 대여소 분포')
    plt.xticks(rotation=60, fontsize=8)
    plt.savefig('seoul_bike_station.png')
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_csv(file, encoding='utf-8-sig')
    
    # 필수 칼럼명 인증
    required_columns = ['대여소_ID', '주소1', '주소2', '위도', '경도']
    
    if list(df.columns) != required_columns:
        flash('필수 칼럼명이 일치하지 않습니다.')
        return redirect(url_for('index'))
    
    df = df['주소1']
    
    # 결측치 제거
    df = df.dropna(axis=0).reset_index(drop=True)
    
    gu_list = df.str.split().str[1]
    
    # ~구로 끝나는 주소만 필터링
    gu_list = gu_list[gu_list.str.endswith('구', na=False)]
    
    value_counts = gu_list.value_counts()
    gu_data = {
        "label": value_counts.index.tolist(),
        "value": value_counts.values.tolist()
    }
    
    save_as_image(gu_data)
    
    flash('대여소 분포 분석이 완료되었습니다.')
    return render_template('index.html', gu_data=gu_data)

if __name__ == '__main__':
    app.run(debug=True)