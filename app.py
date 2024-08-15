from flask import Flask, request, render_template, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "ファイルが選択されていません"

    file = request.files['file']

    if file.filename == '':
        return "ファイルが選択されていません"

    if file and file.filename.endswith('.csv'):
        # CSVファイルを適切なエンコーディングで読み込み
        df = pd.read_csv(file, encoding='shift_jis')

        # 明示的に転置処理
        df_transposed = df.T

        # インデックスを列に変換し、1行目に追加
        df_transposed.reset_index(inplace=True)
        df_transposed.columns = df_transposed.iloc[0]  # 1行目をヘッダーとして設定
        df_transposed = df_transposed[1:]  # 1行目を削除

        # 新しいCSVファイルをメモリ上にバイナリモードで保存
        output = BytesIO()
        df_transposed.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)

        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='transposed.csv')

    return "CSVファイルをアップロードしてください"

if __name__ == '__main__':
    app.run(debug=True)
