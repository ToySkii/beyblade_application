# -*- coding: utf-8 -*-
import yaml
import csv

# コンフィグファイル読み込み
with open('config.yml', 'r', encoding="utf-8") as yml:
    config = yaml.load(yml)
INPUT_FILE = config["input_file"]
DIV_LIST = config["div_list"]
TYPE_LIST = config["type_list"]
CORE_LIST = config["core_list"]

# パーツリストの読み込み
text = open(INPUT_FILE, "r", encoding="utf-8")

line_cnt = 0
division = ""
fight_type = ""
retention_list = ["区分", "タイプ", "名称", "攻撃力", "防御力", "持久力", "重量", "機動力", "バースト力"]
output_list = []
for line in text:
    line = line.replace("\n", "")
    if len(DIV_LIST) > 0 and line == DIV_LIST[0]:
        division = DIV_LIST[0]
        DIV_LIST.pop(0)
        if division == "ガチンコチップ" or division == "ウエイト" or division == "ディスク" or division == "フレーム":
            line_cnt = 0
            fight_type = ""
            output_list.append("\t".join(retention_list))
            retention_list = []           

    for tmp_type in TYPE_LIST:
        if line == "{0}タイプ".format(tmp_type):
            line_cnt = 0
            fight_type = tmp_type
            output_list.append("\t".join(retention_list))
            retention_list = []
    
    if line_cnt == 1:
        if division == "ディスク":
            for core in CORE_LIST:
                division = "コアディスク" if line == core else division
        retention_list.append(division)
        retention_list.append(fight_type)
        retention_list.append(line)

    if line_cnt == 4 or line_cnt == 5 or line_cnt == 6 or line_cnt == 7 or line_cnt == 8:
        retention_list.append(line)

    if line_cnt == 9:
        for num in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            append_flg = True if num == line else False
        retention_list.append(line if append_flg else "0")
        
    line_cnt += 1

output_list.append("\t".join(retention_list))
text.close()

# 変換後ファイル出力
with open('beyblade_parts.tsv', 'w', encoding="utf-8") as f:
    for index in range(len(output_list)):
        if index != 0:
            f.write("\n")
        f.write(output_list[index])