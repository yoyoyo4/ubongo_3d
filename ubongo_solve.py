# 問題と使用ブロックを与えると、問題の解答パターン数と解答一覧文字列を返す

import dancinglinks, block, all_blocks

# 問題、使用ブロック、使用ブロックを回転させたもの(、全解答を返すフラグ)を渡すと、解答パターン数と解答一覧文字列を返す
def solve(question, blocks, variations, return_all_ans=True):
    whole_size = question.z_size * question.y_size * question.x_size
    subsets = [] # ブロック配置候補
    # 全ブロックの全回転後バージョンについて、全座標に対してそれぞれブロックを置けるか判定し、置けるならば配置候補に加える
    for block_id, variation in enumerate(variations):
        for vs in variation:
            for shift_z in range(question.z_size):
                for shift_y in range(question.y_size):
                    for shift_x in range(question.x_size):
                        if question.can_add_block(vs, shift_z, shift_y, shift_x):
                            subsets.append([whole_size + block_id] + [(question.x_size * question.y_size) * (vz + shift_z) + question.x_size * (vy + shift_y) + shift_x + vx
                                            for vz in range(vs.z_size)
                                            for vy in range(vs.y_size)
                                            for vx in range(vs.x_size)
                                            if vs.form[vz][vy][vx]])
    question_blocked_area = [(question.x_size * question.y_size) * vz + question.x_size * vy + vx  # 問題で指定されている、ブロックを置けない箇所
                            for vz in range(question.z_size)
                            for vy in range(question.y_size)
                            for vx in range(question.x_size)
                            if question.form[vz][vy][vx]]
    if question_blocked_area: # 問題で指定されているブロックを置けない箇所を最後のブロックとして扱う
        subsets.append([whole_size + len(blocks)] + question_blocked_area)

    dl = dancinglinks.DancingLinks(whole_size + len(blocks) + (1 if question_blocked_area else 0), subsets) # アイテムリストをDancingLinksオブジェクトに与える
    res = dl.algorithm_x(return_all_ans) # 解答インデックスのリスト
    if not res: # 解無し
        return 0, None

    result = []
    for ans_id, r in enumerate(sorted(res)):
        ans = [subsets[x] for x in r]
        result.append(["answer", ans_id + 1])
        cells = [[['.' for x in range(question.x_size)] for y in range(question.y_size)] for z in range(question.z_size)]
        for a in ans:
            try:
                block_name = blocks[a[0] - whole_size].name # a[0]にあるidに従ってブロック名を取得
            except IndexError:
                block_name = "##" # ブロックが入らない箇所は##で表現
            for p in a[1:]: # ブロックが入る箇所にブロック名を入れる
                cells[p // (question.x_size * question.y_size)][(p % (question.x_size * question.y_size)) // question.x_size][(p % (question.x_size * question.y_size)) % question.x_size] = block_name
        for floor in cells:
            for row in floor:
                result.append(row)
            result.append("=" * (2*question.x_size -1)) # 階層ごとに区切りを入れる
        result.append("")
    return ans_id + 1, result

if __name__ == '__main__':
    question = block.read_question() # 問題読み込み
    blocks = all_blocks.read_block_list() # 使用ブロック読み込み
    variations = [block.generate_variations(b) for b in blocks] # 使用ブロックの全回転verを取得
    _, test = solve(question, blocks, variations)
    print("")
    if test:
        for x in test:
            print(*x)
    else:
        print("no answer")