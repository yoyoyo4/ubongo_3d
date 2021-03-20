# ブロック画像処理
import cv2, os

# 画像のリストを与えると、リサイズして縦の長さを統一した上で横に連結した画像を返す
def hconcat_resize_min(im_list):
    h_min = max(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1]*h_min/im.shape[0]), h_min), cv2.INTER_LINEAR) for im in im_list]
    return cv2.hconcat(im_list_resize)

# ブロック名のリストと末尾のダミー画像数を与えると、ブロック画像とダミー画像を横に連結して返す
def hconcat_with_dummy(block_name_list, n_dummy=0):
    im_list = []
    path = os.path.join(os.getcwd(), "ubongo_3d", "piece")
    for x in block_name_list:
        im_list.append(cv2.imread(os.path.join(path, x+".png"))) # ubongo_3dフォルダ内の画像ファイルのパスを指定
        im_list.append(cv2.imread(os.path.join(path, "white_v_long.jpeg"))) # 普通にブロック画像だけ繋げると間隔が詰まりすぎるので、縦長ダミーを間に挟む
    im_list.pop() # 最後のダミー画像を除く
    for _ in range(n_dummy):
        im_list.append(cv2.imread(os.path.join(path, "white.jpeg"))) # 末尾にダミー画像追加。上下とブロック数が合わない場合用
    return hconcat_resize_min(im_list)

# 画像のリストを与えると、リサイズして横の長さを統一した上で縦に連結した画像を返す
def vconcat_resize_min(im_list):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0]*w_min/im.shape[1])), cv2.INTER_LINEAR) for im in im_list]
    return cv2.vconcat(im_list_resize)

# 画像の2次元リストを与えると、ダミーを補完しつつ画像を並べて返す
def concat_tile_resize(im_list_2d):
    max_n_block = max(len(x) for x in im_list_2d)
    im_list_v = [hconcat_with_dummy(im_list_h, max_n_block-len(im_list_h)) for im_list_h in im_list_2d]
    im_list_v_with_dummy = []
    for x in im_list_v:
        im_list_v_with_dummy.append(x)
        im_list_v_with_dummy.append(cv2.imread(os.path.join(os.getcwd(), "ubongo_3d", "piece", "white_h_long.jpeg")))
    im_list_v_with_dummy.pop()
    return vconcat_resize_min(im_list_v_with_dummy)

# ブロック名の2次元リストを与えると、リスト内の全ブロックの画像を表示する
def show_2d(block_name_list_2d):
    im_name = "__".join(["_".join(block_name_list) for block_name_list in block_name_list_2d])
    x = concat_tile_resize(block_name_list_2d)
    cv2.imshow(im_name, x)
    print("ブロックの画像を別ウィンドウに表示しています")
    cv2.waitKey(0) # キーを押すとウィンドウを閉じる

# テスト用
if __name__ == '__main__':
    show_2d([["R1", "B2", "Y3", "Y3"], ["R4", "G1", "G2"], ["R3", "B4"], ["R2", "B3", "Y1", "Y2"]])