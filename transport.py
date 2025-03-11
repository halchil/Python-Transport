import os
import pandas as pd
import math

# info.csv から情報を読み込む
info_path = "info.csv"
info_df = pd.read_csv(info_path, header=None, index_col=0)

# 入力・出力ディレクトリとカラム名を取得
input_dir = info_df.loc["B1", 1]
column_name = info_df.loc["B2", 1]
output_dir = info_df.loc["B3", 1]

# 出力ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# 入力ディレクトリ内のCSVファイルを取得
csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]

for file in csv_files:
    input_path = os.path.join(input_dir, file)
    output_path = os.path.join(output_dir, file)

    try:
        # CSVを読み込む（エンコーディングの自動判定）
        try:
            df = pd.read_csv(input_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(input_path, encoding="shift_jis")  # 文字化けしたらShift-JISで再試行

        # 指定カラムの小数点を切り捨て
        if column_name in df.columns:
            df[column_name] = pd.to_numeric(df[column_name], errors="coerce")  # 数値変換（エラー時 NaN）
            df[column_name] = df[column_name].apply(lambda x: math.floor(x) if pd.notna(x) else x)

        # 新しいCSVを出力（Excel用にutf-8-sigを推奨）
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

        print(f"処理完了: {file}")

    except Exception as e:
        print(f"エラー発生（{file}）: {e}")

print("全ての処理が完了しました。")