from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    
    flash('대여소 분포 분석이 완료되었습니다.')
    return render_template('index.html', gu_data=gu_data)

if __name__ == '__main__':
    app.run(debug=True)