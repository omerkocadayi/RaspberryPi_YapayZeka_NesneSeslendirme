# Paketleri import et

import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys

# Kamera Çözünürlük Değerleri
#IM_WIDTH = 1280
#IM_HEIGHT = 720
IM_WIDTH = 640 
IM_HEIGHT = 480

flite_frequency = 0

# Kamera tipi seçimi
camera_type = 'picamera'
parser = argparse.ArgumentParser()
parser.add_argument('--usbcam', help='Use a USB webcam instead of picamera',
                    action='store_true')
args = parser.parse_args()
if args.usbcam:
    camera_type = 'usb'

sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Kullanılan veritabanı ismi
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

# Şu an çalışılan klasör
CWD_PATH = os.getcwd()

# Nesta tanımlama için gerekli graflar
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Nesne Haritası
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

# Tanımlı Nesne Sayısı
NUM_CLASSES = 90

## Etiket haritasını yükle.
# Etiket haritası kategori isimlerini içerir.
# Sözlükten integer bir değer döner.
# Örnek olarak 5.. sonucun uçak olduğunu biliyoruz.
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Tensorflow modelini memory'ye yükle
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Giriş ve çıkış tensorlarını tanımla.
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Çıkış tensorları : kutucuklar, skorlar ve sınıflar
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Tanınan nesne sayısı
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# FPS ölçümü
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Picamera veya USB webcam.

### Picamera ###
if camera_type == 'picamera':
    # Picamera ayarları
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()
        
        # Kare elde etmek ve şekillendirmek için
        # Her bir ögenin sahip olduğu RGB değerleri
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)

        # Anlık görüntüyü, frame'i giriş olarak alıp modeli çalıştır. Nesneyi tanımla..
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # Tanımlanan nesneleri frame'e çiz
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.40)
        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        
        # Sonucu seslendir.
        for i in range (0,2):
            result_map = str(category_index[np.squeeze(classes).astype(np.int32)[i]])
            result_index = result_map.find("name")+8
            result_str = ""
            for j in range(result_index , result_map.find("'", result_index)):
                result_str += result_map[j]
            flite_frequency+=1
            if flite_frequency % 5 == 0:
                os.system('flite -t "'+result_str+'"')
                print(result_str)
                flite_frequency=0
        
        # Sonuçlar frame üstüne çizildi, bunu ekrana yansıt.
        cv2.imshow('Object detector', frame)

        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        # Çıkış
        if cv2.waitKey(1) == ord('q'):
            break

        rawCapture.truncate(0)

    camera.close()

### USB webcam ###
elif camera_type == 'usb':
    # USB webcam ayarları
    camera = cv2.VideoCapture(0)
    ret = camera.set(3,IM_WIDTH)
    ret = camera.set(4,IM_HEIGHT)

    while(True):

        t1 = cv2.getTickCount()

        # Kare elde etmek ve şekillendirmek için
        # Her bir ögenin sahip olduğu RGB değerleri
        ret, frame = camera.read()
        frame_expanded = np.expand_dims(frame, axis=0)

        #  Anlık görüntüyü, frame'i giriş olarak alıp modeli çalıştır. Nesneyi tanımla..
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # Tanımlanan nesneleri frame'e çiz
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.85)

        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        
        # Sonuçlar frame üstüne çizildi, bunu ekrana yansıt.
        cv2.imshow('Object detector', frame)

        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        # Çıkış
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()

cv2.destroyAllWindows()