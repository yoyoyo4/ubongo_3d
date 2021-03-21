# ブロックオブジェクト定義用

import copy, json

class Block:
    # self.form[z][y][x] == Trueなら、そこはブロックで埋まっているか、ブロックが置けないスペース
    def __init__(self, form:list, name='#'):
        self.name = name
        self.form = copy.deepcopy(form)
        self.z_size = len(self.form)
        self.y_size = len(self.form[0])
        self.x_size = len(self.form[0][0])

    # ブロック形状の出力
    def show(self):
        print(self.name)
        for z in range(self.z_size):
            for y in range(self.y_size):
                print(*["#" if self.form[z][y][x] else "." for x in range(self.x_size)])
            print("=" * (self.x_size * 2 -1))
        print()

    # ブロックの体積
    def volume(self):
        v = 0
        for z in range(self.z_size):
            for y in range(self.y_size):
                for x in range(self.x_size):
                    if self.form[z][y][x]:
                        v += 1
        return v

    # x軸周りにブロックを90度回転させ、y座標が負にならないようy軸に沿ってスライドする
    def x_roll(self):
        tmp_form = copy.deepcopy(self.form)
        for z in range(self.z_size):
            for y in range(self.y_size):
                for x in range(self.x_size):
                    self.form[y][-z + (self.z_size-1)][x] = tmp_form[z][y][x]

    # y軸周りにブロックを90度回転させ、z座標が負にならないようz軸に沿ってスライドする
    def y_roll(self, posi_flg = True):
        tmp_form = copy.deepcopy(self.form)
        for z in range(self.z_size):
            for y in range(self.y_size):
                for x in range(self.x_size):
                    self.form[-x + (self.x_size-1)][y][z] = tmp_form[z][y][x]

    # z軸周りにブロックを90度回転させ、x座標が負にならないようx軸に沿ってスライドする
    def z_roll(self):
        tmp_form = copy.deepcopy(self.form)
        for z in range(self.z_size):
            for y in range(self.y_size):
                for x in range(self.x_size):
                    self.form[z][x][-y + (self.y_size-1)] = tmp_form[z][y][x]

    # 原点とブロックの間の無駄なスペースを詰める
    def slide_to_origin(self):
        z_min = float("inf")
        y_min = float("inf")
        x_min = float("inf")
        for z in range(self.z_size):
            for y in range(self.y_size):
                for x in range(self.x_size):
                    if self.form[z][y][x]:
                        z_min = min(z_min, z)
                        y_min = min(y_min, y)
                        x_min = min(x_min, x)
        tmp_form = copy.deepcopy(self.form)
        for z in range(self.z_size):
            for y in range(self.y_size):
                for x in range(self.x_size):
                    try:
                        self.form[z][y][x] = tmp_form[z + z_min][y + y_min][x + x_min]
                    except IndexError:
                        self.form[z][y][x] = False

    # ブロックと座標を与えると、与えた座標にブロックを置けるかどうか判定して結果を返す
    def can_add_block(self, block, offset_z, offset_y, offset_x):
        for z in range(block.z_size):
            for y in range(block.y_size):
                for x in range(block.x_size):
                    if block.form[z][y][x]: # ブロックが存在する座標それぞれについて
                        try:
                            if self.form[z + offset_z][y + offset_y][x + offset_x]: # 既に埋まっている場合
                                return False
                        except IndexError: # 範囲外になってしまう場合
                            return False
        return True

# ブロックを与えると、全ての回転バージョンのブロックオブジェクトのリストを返す
# x,y,z軸周りにそれぞれ90度、180度、270度、360度回転させたパターンを導き、重複を除く。ブロックの対称性もカバーできる
def generate_variations(block):
    variations = set()
    for x in range(4):
        for y in range(4):
            for z in range(4):
                p1 = copy.deepcopy(block)
                for _ in range(x):
                    p1.x_roll()
                for _ in range(y):
                    p1.y_roll()
                for _ in range(z):
                    p1.z_roll()
                p1.slide_to_origin()
                variations.add(json.dumps(p1.form)) # 座標リストを文字列に変換してからsetに格納することで重複を除く
    return list(map(lambda f: Block(f, p1.name), [json.loads(f) for f in variations])) # 文字列をブロックオブジェクトに戻してリストに格納


# 問題を読み込んで、ブロックオブジェクトとして返す
# 問題で指定されているブロックが置けない箇所に、既にブロックが置かれていると考える
def read_question():
    msg = """
    下記の例に従って問題を入力してください
    問題の横、縦、高さの範囲(半角スペース区切り)
    問題の底面(.は空きスペース、#はブロックを置けないスペース)
    ↓↓↓ex↓↓↓
    4 3 2
    ....
    ...#
    .#.#
    ↑↑↑ex↑↑↑
    """
    print(msg)
    x_size, y_size, z_size = map(int, input().split())
    cells = []
    for _y in range(y_size):
        s = input()
        row = [s[x] == '#' for x in range(x_size)]
        cells.append(row)
    cells = [cells for _z in range(z_size)]
    return Block(cells, 'question')

# テスト用。どの軸に対しても非対称なブロックR1を回転させ、24パターンあることをチェック
if __name__ == '__main__':
    import all_blocks
    d = all_blocks.all_blocks_dict()
    x = generate_variations(d["R1"])
    print("generate_pattern:", len(x))
    for p in x: 
        p.show()