import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
#from drawnow import drawnow, figure

def m_slice(original_video, start, end, files, p, out_dir, step, ex):
    movie = cv2.VideoCapture(p + original_video)
    Fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT)) # フレーム数カウント
    r_pixels = np.zeros((files, int((end - start) / step + 1)), int) # 調整が必要
    g_pixels = np.zeros((files, int((end - start) / step + 1)), int) # 調整が必要
    b_pixels = np.zeros((files, int((end - start) / step + 1)), int) # 調整が必要
    print(Fs)

    for a in range(0,files): # ここも調整する
        path2 = p + 'received_' + str((20 - 2*a) * 100) + 'kbps_025.mp4'
        movie2 = cv2.VideoCapture(path2)

        path_head = original_video[:-4] + '_' # str型の名前をpath_headに代入してるだけ
        ext_index = np.arange(0, Fs, step) # 変数stepの間隔で値をext_indexに代入している
        f_time = np.array([])
        r_pixel = np.array([])
        g_pixel = np.array([])
        b_pixel = np.array([])

        for i in range(start, end):
            flag, frame = movie.read()
            flag2, frame2 = movie2.read()

            check = i == ext_index # iとext_indexが一致していればcheckがTrue

            if flag == True:
                if True in check: # ここら辺は出力するフレームの数字が綺麗になるように処理しているだけ
                    if i < 10:
                        path_out = path_head + '0000' + str(i) + ex
                    elif i < 100:
                        path_out = path_head + '000' + str(i) + ex
                    elif i < 1000:
                        path_out = path_head + '00' + str(i) + ex
                    elif i < 10000:
                        path_out = path_head + '0' + str(i) + ex
                    else:
                        path_out = path_head + str(i) + ex

                    cv2.imwrite(os.path.join(p + out_dir, path_out), frame) # 指定のパスにフレームを出力(Original)
                    re_path_out = 'received_' + str((20 - 2*a) * 100) + 'kbps_0.25%' + path_out[8:]
                    cv2.imwrite(os.path.join(p + out_dir, re_path_out), frame2) # 指定のパスにフレームを出力(Received)
                    f_time = np.append(f_time, i)
                    print(a,i)
                    r_pixel = np.append(r_pixel, r_diff(p, path_out, re_path_out, out_dir)) # ノイズピクセルを時間軸で数える
                    g_pixel = np.append(g_pixel, g_diff(p, path_out, re_path_out, out_dir)) # ノイズピク>    セルを時間軸で数える
                    b_pixel = np.append(b_pixel, b_diff(p, path_out, re_path_out, out_dir)) # ノイズピク>    セルを時間軸で数える
                    print(r_pixel[-1])
                    print(g_pixel[-1])
                    print(b_pixel[-1])
                else:
                    pass
            else:
                pass

        r_pixels[a] = r_pixel
        g_pixels[a] = g_pixel
        b_pixels[a] = b_pixel

    graph_pixel(f_time, r_pixels, g_pixels, b_pixels) # グラフ絵画
    return

def r_diff(path, o_path, r_path, out_dir): # ノイズピクセルを時間軸で数える

    # ここら辺で画像を読み込んでnumpy配列と化している
    o_path = path + out_dir + o_path
    r_path = path + out_dir + r_path
    o_img = cv2.imread(o_path)
    r_img = cv2.imread(r_path)
    o_array = np.asarray(o_img)
    r_array = np.asarray(r_img)

    # hとwにはフレームの縦横ピクセル数をnp.shapeで代入
    h, w = o_array.shape[0], o_array.shape[1]

    #d = np.zeros((h, w)) 使ってない

    count = 0
    for i in range(h):
        for j in range(w):
            count += r_array[i][j][2] - o_array[i][j][2]
    return count

def g_diff(path, o_path, r_path, out_dir): # ノイズピクセルを時間軸で数える

    # ここら辺で画像を読み込んでnumpy配列と化している
    o_path = path + out_dir + o_path
    r_path = path + out_dir + r_path
    o_img = cv2.imread(o_path)
    r_img = cv2.imread(r_path)
    o_array = np.asarray(o_img)
    r_array = np.asarray(r_img)

    # hとwにはフレームの縦横ピクセル数をnp.shapeで代入
    h, w = o_array.shape[0], o_array.shape[1]

    #d = np.zeros((h, w)) 使ってない

    count = 0
    for i in range(h):
        for j in range(w):
           count += r_array[i][j][1] - o_array[i][j][1]
    return count

def b_diff(path, o_path, r_path, out_dir): # ノイズピクセルを時間軸で数える

    # ここら辺で画像を読み込んでnumpy配列と化している
    o_path = path + out_dir + o_path
    r_path = path + out_dir + r_path
    o_img = cv2.imread(o_path)
    r_img = cv2.imread(r_path)
    o_array = np.asarray(o_img)
    r_array = np.asarray(r_img)

    # hとwにはフレームの縦横ピクセル数をnp.shapeで代入
    h, w = o_array.shape[0], o_array.shape[1]

    #d = np.zeros((h, w)) 使ってない

    count = 0
    for i in range(h):
        for j in range(w):
           count += r_array[i][j][0] - o_array[i][j][0]
    return count

def graph_pixel(f_time, r_pixels, g_pixels, b_pixels):
    fig, ax = plt.subplots()
    c1 = "blue"
    c2 = "forestgreen"
    c3 = "gold"
    c4 = "red"
    #c5 = "purple"
    #c6 = "deepskyblue"
    #c7 = "blue"
    #c8 = "blue"
    #c9 = "magenta"
    #c10 = "deeppink"

    l1 = "2000-1800kbps"
    l2 = "2000-1600kbps"
    l3 = "2000-1400kbps"
    l4 = "2000-1200kbps"
    #l5 = "1200kbps"
    #l6 = "2000kbps blue"
    #l7 = "1700kbps"
    #l8 = "2000kbps"
    #l9 = "1900kbps"
    #l10 = "2000kbps"

    ax.set_xlabel('number of frames')
    ax.set_ylabel('noise value')
    ax.set_title('noise pixels graph')
    ax.grid()

    ave20 = (r_pixels[0,:] + g_pixels[0,:] + b_pixels[0,:]) / 3
    ave18 = (r_pixels[1,:] + g_pixels[1,:] + b_pixels[1,:]) / 3
    ave16 = (r_pixels[2,:] + g_pixels[2,:] + b_pixels[2,:]) / 3
    ave14 = (r_pixels[3,:] + g_pixels[3,:] + b_pixels[3,:]) / 3
    ave12 = (r_pixels[4,:] + g_pixels[4,:] + b_pixels[4,:]) / 3
    
    v18 = 0.0
    v16 = 0.0
    v14 = 0.0
    v12 = 0.0
    for i in range(len(r_pixels[0])):
        v18 += abs(ave20[i] - ave18[i]) / 300.0
        v16 += abs(ave20[i] - ave16[i]) / 300.0
        v14 += abs(ave20[i] - ave14[i]) / 300.0
        v12 += abs(ave20[i] - ave12[i]) / 300.0
    print(v18,v16,v14,v12)

    ax.plot(f_time, abs(ave20 - ave18), color=c1, label=l1)
    ax.plot(f_time, abs(ave20 - ave16), color=c2, label=l2)
    ax.plot(f_time, abs(ave20 - ave14), color=c3, label=l3)
    ax.plot(f_time, abs(ave20 - ave12), color=c4, label=l4)
    #ax.plot(f_time, ave12, color=c5, label=l5)
    #ax.plot(f_time, b_pixels[1,:], color=c6, label=l6)
    #ax.plot(f_time, w_pixels[6,:], color=c7, label=l7)
    #ax.plot(f_time, w_pixels[1,:], color=c8, label=l8)
    #ax.plot(f_time, w_pixels[8,:], color=c9, label=l9)
    #ax.plot(f_time, w_pixels[9,:], color=c10, label=l10)

    ax.legend(loc=0)
    fig.tight_layout()
    plt.savefig('Data_differences.png')
    plt.show()


m_slice('original.mp4', 100, 5001, 5, '/home/ryuma/Desktop/ITU_ISIE/codes/', 'Analyse_noise_time/', 500, '.png') # プログラムの実行
