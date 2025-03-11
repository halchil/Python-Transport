import os
import pandas as pd
import math

# info.csv から情報を読み込む
info_path = "info.csv"
print(f"デバッグ: info.csv のパス {info_path}")
info_df = pd.read_csv(info_path, header=None)
print("デバッグ: info.csv の内容\n", info_df)

# インデックスを明示的に設定
info_df.set_index(0, inplace=True)

# 入力・出力ディレクトリとカラム名を取得
try:
    input_dir = info_df.loc["Input Dir", 1]
    column_name = info_df.loc["対象カラム名", 1]
    output_dir = info_df.loc["Output Dir", 1]
except KeyError as e:
    print(f"エラー: info.csv に必要なキー {e} が見つかりません")
    exit(1)

print(f"デバッグ: 入力ディレクトリ {input_dir}")
print(f"デバッグ: カラム名 {column_name}")
print(f"デバッグ: 出力ディレクトリ {output_dir}")

# 出力ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# 入力ディレクトリ内のCSVファイルを取得
try:
    csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    print(f"デバッグ: 発見されたCSVファイル {csv_files}")
except FileNotFoundError:
    print(f"エラー: 指定された入力ディレクトリ {input_dir} が見つかりません")
    exit(1)

for file in csv_files:
    input_path = os.path.join(input_dir, file)
    output_path = os.path.join(output_dir, file)
    print(f"デバッグ: 現在処理中のファイル {file}")
    
    try:
        # CSVを読み込む（エンコーディングの自動判定）
        try:
            df = pd.read_csv(input_path, encoding="utf-8")
            print(f"デバッグ: {file} を utf-8 で読み込み成功")
        except UnicodeDecodeError:
            df = pd.read_csv(input_path, encoding="shift_jis")  # 文字化けしたらShift-JISで再試行
            print(f"デバッグ: {file} を shift_jis で読み込み成功")

        print(f"デバッグ: {file} のデータプレビュー\n", df.head())
        
        # 指定カラムの小数点を切り捨て
        if column_name in df.columns:
            print(f"デバッグ: {file} に {column_name} カラムあり、処理開始")
            df[column_name] = pd.to_numeric(df[column_name], errors="coerce")  # 数値変換（エラー時 NaN）
            df[column_name] = df[column_name].apply(lambda x: math.floor(x) if pd.notna(x) else x)
        else:
            print(f"警告: {file} に {column_name} カラムが見つかりません")
        
        # 新しいCSVを出力（Excel用にutf-8-sigを推奨）
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"処理完了: {file}")

    except Exception as e:
        print(f"エラー発生（{file}）: {e}")

print("全ての処理が完了しました。")
