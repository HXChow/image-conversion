import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
import datetime
import sys
import ori
import cv2

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.appName = '视频转换'
        self.setAutoFillBackground(True)
        self.open_file = "./"
        self.output_path = None
        # 面板颜色
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)
        self.setPalette(palette)

        self.setFixedSize(800, 400)
        self.center()
        self.status = self.statusBar()
        self.setWindowTitle(self.appName)
        self.setWindowIcon(QIcon('img**'))
        # 设置字体显示颜色和大小
        font_color = "Black"
        font_size = (270, 150)

        choose_movie = QLabel(self)
        choose_movie.setAutoFillBackground(True)
        choose_movie.setPalette(palette)
        font_family = "Arial"
        # 显示选择源文件的字体样式
        font = QFont()
        font.setFamily(font_family)
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)

        choose_movie.setFont(font)
        choose_movie.setFixedSize(font_size[0], font_size[1])
        choose_movie.setText("<font color="+font_color+">选择视频</font>")
        choose_movie.setAlignment(Qt.AlignRight)
        choose_movie.move(0, 50)
        choose_save_path = QLabel(self)
        choose_save_path.setAutoFillBackground(True)

        self.show_font = QFont()
        self.show_font.setFamily(font_family)
        self.show_font.setPointSize(20)
        self.show_font.setBold(True)
        self.show_font.setWeight(75)

        gray_palette = QPalette()
        gray_palette.setColor(QPalette.Window, Qt.lightGray)
        self.ori_movie_path = QLabel(self)
        self.ori_movie_path.setAutoFillBackground(True)
        self.ori_movie_path.setPalette(gray_palette)
        self.ori_movie_path.setFixedSize(300, 50)
        self.ori_movie_path.move(280, 50)
        self.ori_movie_path.setFont(self.show_font)
        self.ori_movie_path.setAlignment(Qt.AlignCenter)
        self.ori_movie_path.setText("未选择视频")

        ori_movie_bt = QPushButton(self)
        ori_movie_bt.setText("选择视频")
        ori_movie_bt.setFixedSize(150, 50)
        ori_movie_bt.move(600, 50)
        ori_movie_bt.clicked.connect(self.load_ori_movie)

        choose_save_path.setPalette(palette)
        choose_save_path.setFont(font)
        choose_save_path.setFixedSize(font_size[0], font_size[1])
        choose_save_path.setText("<font color="+font_color+">保存位置</font>")
        choose_save_path.setAlignment(Qt.AlignRight)
        choose_save_path.move(0, 130)

        # 显示选择目标文件的字体样式
        self.show_font1 = QFont()
        self.show_font1.setFamily(font_family)
        self.show_font1.setPointSize(20)
        self.show_font1.setBold(True)
        self.show_font1.setWeight(75)

        self.save_movie_path = QLabel(self)
        self.save_movie_path.setAutoFillBackground(True)
        self.save_movie_path.setPalette(gray_palette)
        self.save_movie_path.setFixedSize(300, 50)
        self.save_movie_path.move(280, 130)
        self.save_movie_path.setFont(self.show_font1)
        self.save_movie_path.setAlignment(Qt.AlignCenter)
        self.save_movie_path.setText("未选择保存位置")

        save_movie_bt = QPushButton(self)
        save_movie_bt.setText("选择保存的位置")
        save_movie_bt.setFixedSize(150, 50)
        save_movie_bt.move(600, 130)
        save_movie_bt.clicked.connect(self.save_path_choose)

        # 显示选择水印的字体样式
        self.show_font2 = QFont()
        self.show_font2.setFamily(font_family)
        self.show_font2.setPointSize(20)
        self.show_font2.setBold(True)
        self.show_font2.setWeight(75)

        choose_watermark = QLabel(self)
        choose_watermark.setAutoFillBackground(True)
        choose_watermark.setPalette(palette)

        choose_watermark.setFont(font)
        choose_watermark.setFixedSize(font_size[0], font_size[1])
        choose_watermark.setText("<font color="+font_color+">选择水印</font>")
        choose_watermark.setAlignment(Qt.AlignRight)
        choose_watermark.move(0, 210)

        self.watermark_path = QLabel(self)
        self.watermark_path.setAutoFillBackground(True)
        self.watermark_path.setPalette(gray_palette)
        self.watermark_path.setFixedSize(300, 50)
        self.watermark_path.move(280, 210)
        self.watermark_path.setFont(self.show_font2)
        self.watermark_path.setAlignment(Qt.AlignCenter)
        self.watermark_path.setText("未选择水印位置")

        water_mark_bt = QPushButton(self)
        water_mark_bt.setText("选择水印")
        water_mark_bt.setFixedSize(150, 50)
        water_mark_bt.move(600, 210)
        water_mark_bt.clicked.connect(self.water_choose)

        # 确认按钮
        yes_bt = QPushButton(self)
        yes_bt.setText("确认")
        yes_bt.setFixedSize(150, 50)
        yes_bt.move(250, 300)
        yes_bt.clicked.connect(self.ensure_enent)

        cancel_bt = QPushButton(self)
        cancel_bt.setText("取消")
        cancel_bt.setFixedSize(150, 50)
        cancel_bt.move(550, 300)
        cancel_bt.clicked.connect(self.cancel_event)


    #主要功能事件区域，添加功能时使用的事件

    def ensure_enent(self):
        ensure_dialog = QMessageBox.question(self, "请确认",
                                             "确定执行" + self.appName,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ensure_dialog == QMessageBox.Yes:
            if not os.path.exists(self.ori_movie_path.text()) and (not self.ori_movie_path.text().endswith(".mp3")
            or not self.ori_movie_path.text().endswith(".mp4") or not self.ori_movie_path.text().endswith(".avi")):
                QMessageBox.warning(self, "Warning",
                                    self.tr("请选择要转换的视频文件"),)
                return
            if not os.path.exists(self.watermark_path.text()) and (not self.watermark_path.text().endswith(".jpg")
            or not self.watermark_path.text().text().endswith(".png")):
                QMessageBox.warning(self, "Warning",
                                    self.tr("请选择要添加的水印"),)
                return

            start = datetime.datetime.now()
            INPUT = self.ori_movie_path.text()
            OUTPUT = self.save_movie_path.text()
            SAVE = self.save_movie_path.text()
            vc = ori.video2txt_jpg(INPUT)
            FPS = vc.get(cv2.CAP_PROP_FPS)
            vc.release()
            ori.jpg2video(OUTPUT, FPS)

            #
            ori.video2mp3(INPUT)
            ori.video_add_mp3(os.path.join(OUTPUT, 'convert.avi'), INPUT.split('.')[0] + '.mp3')
            #ori.video_add_mp3(INPUT.split('.')[0] + '.avi', INPUT.split('.')[0] + '.mp3')
            if (not SAVE):
                ori.remove_dir("./Cache")

            video = ori.mp.VideoFileClip(os.path.join(self.save_movie_path.text(), 'convert-tmp.mp4'))
            logo = (ori.mp.ImageClip(self.watermark_path.text())
                    .set_duration(video.duration)  # 水印持续时间
                    .resize(height=55)  # 水印的高度，会等比缩放
                    .margin(right=1, top=1, opacity=1)  # 水印边距和透明度
                    .set_pos(("right", "top")))  # 水印的位置
            final = ori.mp.CompositeVideoClip([video, logo])
            # mp4文件默认用libx264编码， 比特率单位bps

            final.write_videofile(os.path.join(self.save_movie_path.text(), 'convert.mp4'), codec="libx264", bitrate="10000000")
            if os.path.exists(os.path.join(self.save_movie_path.text(), 'convert.avi')):
                os.remove(os.path.join(self.save_movie_path.text(), 'convert.avi'))
            # if os.path.exists(os.path.join(self.save_movie_path.text(), 'convert-tmp.mp4')):
            #     os.remove(os.path.join(self.save_movie_path.text(), 'convert-tmp.mp4'))
            end = datetime.datetime.now()
            file_size = ori.get_FileSize(os.path.join(self.save_movie_path.text(), 'convert.mp4'))
            QMessageBox.information(self, "具体信息",
                                    self.tr("输出文件大小： " + str(file_size) + " MB "
                                            "<br \>运行时间: "+ str((end - start))[0:9]))

    def cancel_event(self):
        cancel_dialog = QMessageBox.question(self, "请确认",
                                           "确定取消" + self.appName,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if cancel_dialog == QMessageBox.Yes:
            self.show_font.setPointSize(20)
            self.show_font.setWeight(75)
            self.show_font1.setPointSize(20)
            self.show_font1.setWeight(75)
            self.show_font2.setPointSize(20)
            self.show_font2.setWeight(75)
            self.ori_movie_path.setFont(self.show_font)
            self.ori_movie_path.setText("未选择视频")
            self.save_movie_path.setFont(self.show_font1)
            self.save_movie_path.setText("未选择保存位置")
            self.watermark_path.setFont(self.show_font2)
            self.watermark_path.setAlignment(Qt.AlignCenter)
            self.watermark_path.setText("未选择水印位置")

    def center(self):
        #窗口居中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def load_ori_movie(self):
        fname = self.get_file('mp4;;*.mp3;;*.avi')
        point_size = 0
        weight = 0
        if 30 < len(fname):
            point_size = 10
            weight = 30
        elif 20 < len(fname) < 30:
            point_size = 15
            weight = 40
        self.show_font.setPointSize(point_size)
        self.show_font.setWeight(weight)
        self.ori_movie_path.setFont(self.show_font)
        self.ori_movie_path.setText(fname)

    def water_choose(self):
        fname = self.get_file('png;;*.jpg')
        point_size = 10
        weight = 30

        self.show_font2.setPointSize(point_size)
        self.show_font2.setWeight(weight)
        self.watermark_path.setFont(self.show_font2)
        self.watermark_path.setText(fname)

    def save_path_choose(self):
        fname = self.get_file('')
        point_size = 0
        weight = 0
        self.output_path = fname
        if 30 < len(fname):
            point_size = 10
            weight = 30
        elif 20 < len(fname) < 30:
            point_size = 15
            weight = 40
        self.show_font1.setPointSize(point_size)
        self.show_font1.setWeight(weight)
        self.save_movie_path.setFont(self.show_font1)
        self.save_movie_path.setText(fname)


    def get_file(self, type):
        if type == '':
            fname = QFileDialog.getExistingDirectory(self, 'Open File', self.open_file)
        else:
            fname, _ = QFileDialog.getOpenFileName(self, 'Open File', self.open_file, "*."+type)
        return fname

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()

    form.show()
    sys.exit(app.exec_())