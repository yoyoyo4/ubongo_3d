# 作問用プログラム

import block, all_blocks, ubongo3d_solve, block_image
import itertools, random
from tqdm import tqdm

# 問題を与えると、解ける可能性のある(体積一致)ブロックの組み合わせ全てを返す
# unique_blockがTrueなら全て別々のブロックを使用する。Falseならウボンゴ3Dに同梱されている数だけブロックの重複を許す
# n_blocks 使用ブロック数。無入力や負入力の場合、指定なしとなる
def choose_blocks(question, unique_block_flg=True, n_blocks=-1):
    if unique_block_flg:
        abl = all_blocks.all_unique_blocks_list()
    else:
        abl = all_blocks.all_blocks_list()
    n_all_blocks = len(abl)
    question_space = question.z_size * question.y_size * question.x_size - question.volume()
    block_and_size = [[abl[i], abl[i].volume()] for i in range(n_all_blocks)]

    output = []
    # 部分集合全列挙。dpでやると全列挙の部分が面倒
    for n in range(1, n_all_blocks):
        if n_blocks > 0 and n != n_blocks: # ブロック数の指定がある場合、その数にnを合わせる
            continue
        tmp_min_vol = float("inf") # 現在のブロック数におけるブロックの合計体積の最小値
        for block_list in list(itertools.combinations(block_and_size, n)):
            if sum([b[1] for b in block_list]) == question_space:
                output.append([b[0] for b in block_list])
            else:
                tmp_min_vol = min(tmp_min_vol, sum([b[1] for b in block_list]))
        if tmp_min_vol > question_space:
            break

    if output:
        return output
    else:
        print("解なし")
        exit()

# 問題の底面(とユニークブロックフラグ、使用ブロック数)を与えると、使用ブロックと解答の全パターンを返す
# 非常に長い出力になるので使い所は少ないかも
def choose_blocks_and_show_ans(unique_block_flg=True, n_blocks=-1):
    question = block.read_question()
    list_of_block_list = choose_blocks(question, unique_block_flg, n_blocks)
    question_id = 1
    for blocks in list_of_block_list:
        variations = [block.generate_variations(b) for b in blocks]
        _, ans = ubongo_solve.solve(question, blocks, variations)
        if ans:
            print("question", question_id)
            print(*[b.name for b in blocks])
            print()
            for a in ans:
                print(*a)
            question_id += 1


# 問題の底面(と作問数、ユニークブロックフラグ、使用ブロック数、解答数を返すフラグ、ランダム抽出フラグ)を与えると、解答数と使用ブロックの組合せを作問数の数だけ返す
# 実行時間長め。短くしたい場合はreturn_all_ansをFalseにする。この場合少なくとも1つ解答が存在する組合せを作問数の数だけ返す
def show_blocks(n_question=-1, unique_block_flg=True, n_blocks=-1, return_n_ans_flg=True, random_flg=True):
    question = block.read_question()

    list_of_block_list = choose_blocks(question, unique_block_flg, n_blocks)
    indices = list(range(len(list_of_block_list)))
    if random_flg:
        random.shuffle(indices) # 同じようなブロックを使う問題が固まることを防ぐためにランダム抽出する
    question_and_n_ans = []

    # tqdmによるプログレスバー設定
    bar = tqdm(total = n_question)

    for i in range(len(list_of_block_list)):
        blocks = list_of_block_list[indices[i]]
        variations = [block.generate_variations(b) for b in blocks]
        n_ans, ans = ubongo3d_solve.solve(question, blocks, variations, return_n_ans_flg)
        if n_ans:
            if return_n_ans_flg:
                question_and_n_ans.append(["解答数:"+str(n_ans), [b.name for b in blocks]])
            else:
                question_and_n_ans.append([b.name for b in blocks])
            bar.update(1) # プログレスバーを1進める
        if len(question_and_n_ans) == n_question:
            break
    
    if return_n_ans_flg:
        for a in question_and_n_ans:
            print(a[0], *a[1])
        block_image.show_2d([a[1] for a in question_and_n_ans])
    else:
        for a in question_and_n_ans:
            print(*a)
        block_image.show_2d(question_and_n_ans)

if __name__ == '__main__':
    show_blocks(n_question=5, unique_block_flg=True, n_blocks=-1, return_n_ans_flg=True, random_flg=True)