# coding:utf-8
# coding=gbk
import argparse
import os
import cv2
import subprocess
import datetime
import moviepy.editor as mp
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
from PIL import Image, ImageFont, ImageDraw

# 是否保留cache文件（视频每帧图）（注释为保存）
# aparser = argparse.ArgumentParser()
# aparser.add_argument('file')
# aparser.add_argument('-o','--output')
# aparser.add_argument('-f','--fps',type = float, default = 24)#?
# aparser.add_argument('-s','--save',type = bool, nargs='?', default = False, const = True)

#获取参数
#args = parser.parse_args()
#INPUT = args.file
#OUTPUT = args.output
#SAVE = args.save
#FPS = args.fps


#记录时间
start = datetime.datetime.now()

ascii_char = list("MNHQ$OC67)oa+>!:+. ")
#ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+. ")

def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


def txt2image(file_name):
    im = Image.open(file_name).convert('RGB')


    raw_width = im.width
    raw_height = im.height
    width = int(raw_width / 6)
    height = int(raw_height / 15)
    im = im.resize((width, height), Image.NEAREST)
    txt = ""
    colors = []
    for i in range(height):
        for j in range(width):
            pixel = im.getpixel((j, i))
            colors.append((pixel[0], pixel[1], pixel[2]))
            if (len(pixel) == 4):
                txt += get_char(pixel[0], pixel[1], pixel[2], pixel[3])
            else:
                txt += get_char(pixel[0], pixel[1], pixel[2])
        txt += '\n'
        colors.append((255, 255, 255))
    im_txt = Image.new("RGB", (raw_width, raw_height), (255, 255, 255))
    dr = ImageDraw.Draw(im_txt)
    font = ImageFont.load_default().font
    x = y = 0

    font_w, font_h = font.getsize(txt[1])
    font_h *= 1.37

    for i in range(len(txt)):
        if (txt[i] == '\n'):
            x += font_h
            y = -font_w
        dr.text((y, x), txt[i], fill=colors[i])
        y += font_w
    name = file_name
    im_txt.save(name)

#将视频拆分成图片
def video2txt_jpg(file_name):
    vc = cv2.VideoCapture(file_name)
    c = 1
    if vc.isOpened():
        r, frame = vc.read()
        if not os.path.exists('./Cache'):
            os.mkdir('./Cache')
        os.chdir('./Cache')
    else:
        r = False
    while r:
        cv2.imwrite(str(c) + '.jpg', frame)
        txt2image(str(c) + '.jpg')  #同时转换为ascii图
        r, frame = vc.read()
        c += 1
    os.chdir('..')
    return vc

#将图片合成视频
def jpg2video(outfile_name, fps):
    fourcc = VideoWriter_fourcc(*"MJPG")
    images = os.listdir('./Cache')
    im = Image.open('./Cache/' + images[0])
    vw = cv2.VideoWriter(os.path.join(outfile_name, 'convert.avi'), fourcc, fps, im.size)
    os.chdir('./Cache')

    for image in range(len(images)):
        frame = cv2.imread(str(image + 1) + '.jpg')
        vw.write(frame)
    os.chdir('..')
    vw.release()


def remove_dir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            dirs = os.listdir(path)
            for d in dirs:
                if os.path.isdir(path + '/' + d):
                    remove_dir(path + '/' + d)
                elif os.path.isfile(path + '/' + d):
                    os.remove(path + '/' + d)
            os.rmdir(path)
            return
        elif os.path.isfile(path):
            os.remove(path)
        return

#调用ffmpeg获取mp3音频文件
def video2mp3(file_name):
    outfile_name = file_name.split('.')[0] + '.mp3'
    subprocess.call('E:/ffmpeg/ffmpeg/bin/ffmpeg -i ' + file_name + ' -f mp3 ' + outfile_name, shell=True)   #需要将全路径写上否则会出现乱码及报错，下同

#合成音频和视频文件
def video_add_mp3(file_name, mp3_file):
    outfile_name = file_name.split('.')[0] + '-tmp.mp4'
    subprocess.call('E:/ffmpeg/ffmpeg/bin/ffmpeg -i ' + file_name + ' -i ' + mp3_file + ' -strict -2 -f mp4 ' + outfile_name, shell=True)


if __name__ == '__main__':
    INPUT = r"./tmp.mp4"
    OUTPUT = r"C:\Users\Mr.Chow\Desktop\tmp"
    SAVE = r"C:\Users\Mr.Chow\Desktop\tmp"
    FPS = "24"
    vc = video2txt_jpg(INPUT)
    FPS = vc.get(cv2.CAP_PROP_FPS)
    print(FPS)
    vc.release()
    jpg2video(OUTPUT, FPS)
    print(INPUT, INPUT.split('.')[0] + '.mp3')
    video2mp3(INPUT)
    video_add_mp3(INPUT.split('.')[0] + '.avi', INPUT.split('.')[0] + '.mp3')

    if (not SAVE):
        remove_dir("Cache")
        os.remove(INPUT.split('.')[0] + '.mp3')
        os.remove(INPUT.split('.')[0] + '.avi')
#
# #视频加水印
# video = mp.VideoFileClip(r'./tmp.mp4')
# logo = (mp.ImageClip(r'./water.jpg')
#           .set_duration(video.duration)  # 水印持续时间
#           .resize(height=55)  # 水印的高度，会等比缩放
#           .margin(right=1, top=1, opacity=1)  # 水印边距和透明度
#           .set_pos(("right","top")))  # 水印的位置
#
# final = mp.CompositeVideoClip([video, logo])
# # mp4文件默认用libx264编码， 比特率单位bps
# final.write_videofile(r'.mp4', codec="libx264", bitrate="10000000")


#输出文件大小
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)

# if __name__ == '__main__':
#     size = get_FileSize(r"")
#     print("文件大小：%.2f MB"%(size))
#     pass

#输出运行时间
end = datetime.datetime.now()
print("运行时长:", (end-start))
