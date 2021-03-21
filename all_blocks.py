# ブロックオブジェクト呼び出し用

import block, block_image


# 全ブロックオブジェクトのリスト
def all_blocks_list():
    str_block_list = [
        # #はブロックで埋まっている箇所、.はブロックで埋まっていない箇所
        "3 2 2 Y1 2", # x軸サイズ、y軸サイズ、z軸サイズ、ブロック名称、ブロック個数
        "###", # y=1, z=1
        ".#.", # y=2, z=1
        "#..", # y=1, z=2
        "...", # y=2, z=2
        "3 2 2 Y2 2",
        "###",
        "#..",
        "..#",
        "...",
        "2 2 2 Y3 3",
        "#.",
        "##",
        "#.",
        "..",
        "3 2 1 Y4 2",
        "###",
        "#.#",
        "3 2 2 B1 2",
        "#..",
        "###",
        "#..",
        "...",
        "3 2 2 B2 2",
        "##.",
        "#..",
        ".##",
        "...",
        "3 2 1 B3 3",
        "###",
        "##.",
        "2 2 1 B4 4",
        "##",
        "#.",
        "2 2 2 R1 3",
        "##",
        "##",
        "#.",
        "..",
        "2 2 2 R2 3",
        "##",
        ".#",
        "#.",
        "..",
        "3 2 2 R3 2",
        "###",
        "..#",
        "#..",
        "...",
        "3 2 1 R4 2",
        "##.",
        ".##",
        "3 2 2 G1 2",
        "##.",
        ".##",
        "#..",
        "...",
        "3 2 2 G2 2",
        "###",
        "#..",
        "...",
        "#..",
        "3 2 1 G3 2",
        "###",
        ".#.",
        "3 2 1 G4 4",
        "###",
        "#.."
    ]

    block_area_size = 3  # どのように回転させてもブロックが収まる立方体の1辺の長さ
    all_blocks = []

    i = 0
    while i < len(str_block_list):
        cells = [[[False for _ in range(block_area_size)] for _ in range(block_area_size)] for _ in range(block_area_size)] # Falseは".", ブロックで埋まっていない部分に相当
        x_size, y_size, z_size, name, n = str_block_list[i].split() # x軸サイズ、y軸サイズ、z軸サイズ、ブロック名称、ブロック個数
        i += 1
        for z in range(int(z_size)):
            for y in range(int(y_size)):
                s = str_block_list[i]
                for x in range(int(x_size)):
                    cells[z][y][x] = True if s[x] == '#' else False # True, "#"はブロックで埋まっている箇所
                i += 1
        for _ in range(int(n)):
            all_blocks.append(block.Block(cells, name)) # ブロックオブジェクトを作成してブロックの個数(n)だけリストに格納

    return all_blocks


# 同じ形状のブロックを複数含まない、ブロックオブジェクトのリスト
def all_unique_blocks_list():
    all_unique_blocks_list = []
    block_name_set = set()
    for block in all_blocks_list():
        if block.name in block_name_set:
            pass
        else:
            all_unique_blocks_list.append(block)
            block_name_set.add(block.name)
    return all_unique_blocks_list

# ブロック名を与えると、ブロックオブジェクトを返す辞書
def all_blocks_dict():
    all_blocks_dict = dict()
    for block in all_blocks_list():
        all_blocks_dict[block.name] = block
    return all_blocks_dict

# 半角スペース区切りのブロック名称の入力に対し、全ブロックオブジェクトのリストを返す
def read_block_list():
    blocks = []
    d = all_blocks_dict()
    print("使用ブロックを半角スペース区切りで入力してください ex:R1 B3 B3 G2")
    ip = list(input().split())
    for block_name in ip:
        blocks.append(d[block_name])
    print("ブロックの画像を別ウィンドウに表示しています。ウィンドウを閉じて続行してください")
    block_image.show_2d([ip])
    return blocks

# テスト用。全ブロックの形状を出力
if __name__ == '__main__':
    for x in all_unique_blocks_list():
        x.show()