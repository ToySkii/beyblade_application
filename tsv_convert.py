# -*- coding: utf-8 -*-
import yaml
import csv
from tqdm import tqdm

# コンフィグファイル読み込み
with open('config.yaml', 'r', encoding="utf-8") as yml:
    config = yaml.load(yml)
INPUT_FILE = config["input_file"] # 対象ファイル名
DIV_LIST = config["div_list"]     # 区分
ID_INITIAL = config["id_initial"] # IDの頭文字
TYPE_LIST = config["type_list"]   # タイプ
CORE_LIST = config["core_list"]   # コアディスク

# パーツリストの読み込み
text = open(INPUT_FILE, "r", encoding="utf-8")

line_cnt = 0        # パーツごとの行番号
id_num = 0          # ID番号
division = ""       # 区分（持ち回り用）
notype_flg = False  # タイプが無いパーツフラグ
fight_type = ""     # タイプ（持ち回り用）
retention_list = [] # 行保持リスト
# 出力リスト
output_list = ["ID\t区分\tタイプ\t名称\t攻撃力\t防御力\t持久力\t重量\t機動力\tバースト力\t説明"]

tmp_list = []
# 進捗バーを出すための一時リストを作成
for value in text:
    tmp_list.append(value)

# データ取得処理開始
for idx in tqdm(range(len(tmp_list))):
    line = tmp_list[idx]

    # 改行削除
    line = line.replace("\n", "")

    # 例外行除去
    if line == "GTレイヤー" or line == "ガチンコチップ ウエイト ベース":
        continue

    # 区分の取得
    if len(DIV_LIST) > 0 and line == DIV_LIST[0]:
        division = DIV_LIST[0]
        DIV_LIST.pop(0)
        if division == "ガチンコチップ" or division == "ウエイト" or division == "フレーム" or division == "ディスク":
            notype_flg = True
            fight_type = ""
            line_cnt = 1
            id_num = 0
        else:
            notype_flg = False
            line_cnt = 0
            id_num = 0
        continue

    # タイプが空文字なら次の行へ
    if line_cnt == 0 and line == "":
        continue

    # タイプの取得
    if line_cnt == 0 and notype_flg == False:
        # 無限ドライバのみ例外判定
        if division == "ドライバー" and "無限" in line:
            fight_type = ""
            line_cnt = 1

        for tmp_type in TYPE_LIST:
            if line == "{0}タイプ".format(tmp_type) or line == tmp_type:
                fight_type = tmp_type
                line_cnt = 0

    # パーツ名が空文字なら次の行へ
    if line_cnt == 1 and line == "":
        continue

    # パーツ名の取得
    if line_cnt == 1:
        if division == "ディスク":
            for core in CORE_LIST:
                division = "コアディスク" if line == core else division

        id_num += 1
        str_num = "{:04}".format(id_num)
        retention_list.append("{0}{1}".format(ID_INITIAL[division], str_num))
        retention_list.append(division)
        retention_list.append(fight_type)
        retention_list.append(line)

    # 攻撃力、防御力、持久力、重量、機動力の取得
    if 4 <= line_cnt and line_cnt <= 8:
        retention_list.append(line)

    # バースト力の取得
    if line_cnt == 9:
        for num in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if num == line:
                append_flg = True
        if append_flg:
            retention_list.append(line)
            append_flg = False
        else:
            retention_list.append("0")
            line_cnt += 1

    # 説明の取得
    if line_cnt == 10:
        retention_list.append(line)

    # 現在の取得状況に合わせて、カウンターを調整
    # パーツの最終行なら出力リストに登録し、行保持リストを初期化する。
    if len(retention_list) < 10:
        line_cnt += 1
    elif line == "":
        output_list.append("\t".join(retention_list))
        retention_list = []
        line_cnt = 1 if notype_flg else 0
    else:
        line_cnt += 1

output_list.append("\t".join(retention_list))
text.close()

# 変換後ファイル出力
with open('beyblade_parts.tsv', 'w', encoding="utf-8") as f:
    for index in range(len(output_list)):
        if index != 0:
            f.write("\n")
        f.write(output_list[index])