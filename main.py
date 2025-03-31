#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка

from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
app = QApplication([])
w = QWidget()
w.resize(700,500)
w.setWindowTitle("Easy editor")
btn_l= QPushButton("Лево")
btn_r= QPushButton("Право")
btn_flip= QPushButton("Зеркало")
btn_sh= QPushButton("Резкость")
btn_save= QPushButton("Cохранить")
btn_res= QPushButton("Сбросить фильтр")
btn_bw= QPushButton("Ч/Б")
btn_dir= QPushButton("Папка")
lw_files = QListWidget()
lb_image = QLabel("Картинка")
row= QHBoxLayout()
col1 =QVBoxLayout()
col2 = QVBoxLayout()
row_t = QHBoxLayout()
row_t.addWidget(btn_l)
row_t.addWidget(btn_r)
row_t.addWidget(btn_flip)
row_t.addWidget(btn_sh)
row_t.addWidget(btn_bw)
row_t.addWidget(btn_save)
row_t.addWidget(btn_res)
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image)
col2.addLayout(row_t)
row.addLayout(col1)
row.addLayout(col2)
w.setLayout(row)
wdir =""
def chooseWorkdir():    
     
     global wdir
     wdir = QFileDialog.getExistingDirectory()     
          

def filter(files,exs):
   result = []
   for filename in files :
      for ex in exs:
         if filename.endswith(ex):
            result.append(filename)
   return result
def showfilename():
     try:
          extensions = ['.jpeg','.jpg','.png','.bmp']
          chooseWorkdir()
          filenames = filter(os.listdir(wdir),extensions)
          lw_files.clear()
          for filename in filenames:
               lw_files.addItem(filename)
     except:
          pass
class ImageProcessor():
     def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = 'Modified/'
        self.original_image = None
     def saveImage(self):
          try:
               path = os.path.join(wdir, self.save_dir)
               if not(os.path.exists(path) or os.path.isdir(path)):
                    os.mkdir(path)
               image_path = os.path.join(path, self.filename)
               self.image.save(image_path)
          except:
               pass 

    
     def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()


     def showImage(self, image):
        qimage = ImageQt(image)
        pixmapimage = QPixmap.fromImage(qimage)
        width, height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(width, height, Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)
     def do_bw(self):
        self.image = self.image.convert('L')
        self.showImage(self.image)

     def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showImage(self.image)

     def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showImage(self.image)

     def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.showImage(self.image)

     def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage(self.image)

     def resetImage(self):
        self.image = self.original_image.copy()
        self.showImage(self.original_image)
workimage= ImageProcessor()
def showCH():
   if lw_files.currentRow() >= 0:
      filename =  lw_files.currentItem().text()
      workimage.loadimage(filename)
      image_path = os.path.join(wdir,workimage.filename)
      workimage.show_image(image_path)
lw_files.currentRowChanged.connect(showCH)

btn_dir.clicked.connect(showfilename)
btn_bw.clicked.connect(workimage.do_bw)
btn_l.clicked.connect(workimage.do_left)
btn_r.clicked.connect(workimage.do_right)










































btn_sh.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
btn_res.clicked.connect(workimage.resetImage)
btn_save.clicked.connect(workimage.saveImage)
w.show()
app.exec()