# Modified by: JackieZhai on Feb 20 2020. All Rights Reserved.

import sys
from os import system, path
from copy import deepcopy
from glob import glob
from imutils.video import FPS
import numpy as np
import cv2
import torch

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from window_ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QImage

from pysot.core.config import cfg
from pysot.models.model_builder import ModelBuilder
from pysot.tracker.tracker_builder import build_tracker

torch.set_num_threads(1)

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # Connect the on-clicked functions
        self.pushButton_locationLoading.clicked.connect(self.location_loading)
        self.pushButton_videoLoading.clicked.connect(self.video_loading)
        self.pushButton_cameraLoading.clicked.connect(self.camera_loading)
        self.pushButton_bboxSetting.clicked.connect(self.bbox_setting)
        self.pushButton_algorithmProcessing.clicked.connect(self.algorithm_processing)
        # Initialize trackers
        model_location = './pysot/experiments/siammaske_r50_l3'
        self.config = model_location + '/config.yaml'
        self.snapshot = model_location + '/model.pth'
        self.tracker_name = model_location.split('/')[-1]
        self.video_name = ''
        cfg.merge_from_file(self.config)
        cfg.CUDA = torch.cuda.is_available()
        device = torch.device('cuda' if cfg.CUDA else 'cpu')
        model = ModelBuilder()
        model.load_state_dict(torch.load(self.snapshot, map_location=lambda storage, loc: storage.cpu()))
        model.eval().to(device)
        self.tracker = build_tracker(model)
        self.vs = None
        self.analysis_box = None
        self.analysis_max = 10

    def cv2_to_qimge(self, cvImg):
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg

    def get_frames(self, video_name):
        if not video_name:
            return
        elif video_name.endswith('avi') or \
                video_name.endswith('mp4'):
            cap = cv2.VideoCapture(video_name)
            while True:
                ret, frame = cap.read()
                if ret:
                    yield frame
                else:
                    break
        else:
            images = glob(path.join(video_name, '*.jp*'))
            images = sorted(images,
                            key=lambda x: int(x.split('\\')[-1].split('.')[0]))
            for img in images:
                frame = cv2.imread(img)
                yield frame

    def analysis_init(self):
        self.analysis_box = []
        for i in range(len(self.bbox_list)):
            q_trans = []
            q_trans_loc = 0
            q_segmove = []
            q_segmove_loc = 0
            for j in range(self.analysis_max):
                q_trans.append(None)
                q_segmove.append(None)
            pre_center = None
            pre_mask = None
            self.analysis_box.append([q_trans, q_trans_loc, q_segmove, q_segmove_loc, pre_center, pre_mask])

    def behavior_analysis(self, frame, b, center, mask):
        if self.analysis_box[b][4] is None:
            self.analysis_box[b][0][self.analysis_box[b][1]] = center
        else:
            self.analysis_box[b][0][self.analysis_box[b][1]] = (center[0]-self.analysis_box[b][4][0],
                                                                center[1]-self.analysis_box[b][4][1])
        self.analysis_box[b][1] += 1
        if self.analysis_box[b][1] >= self.analysis_max:
            self.analysis_box[b][1] = 0
        mean_trans = 0.0
        for item in self.analysis_box[b][0]:
            if item is not None:
                mean_trans += np.sqrt(item[0]*item[0]+item[1]*item[1])
        mean_trans /= self.analysis_max

        if self.analysis_box[b][4] is None:
            self.analysis_box[b][2][self.analysis_box[b][3]] = (mask, mask)
        else:
            self.analysis_box[b][2][self.analysis_box[b][3]] = (np.bitwise_and(mask, self.analysis_box[b][5]),
                                                                np.bitwise_or(mask, self.analysis_box[b][5]))
        self.analysis_box[b][3] += 1
        if self.analysis_box[b][3] >= self.analysis_max:
            self.analysis_box[b][3] = 0
        mean_segmove = 0.0
        for item in self.analysis_box[b][2]:
            if item is not None:
                iou = np.sum(item[0]) / np.sum(item[1])
                mean_segmove += 1 - iou
        mean_segmove /= self.analysis_max

        if mean_trans > 10:
            mean_state_text = "State: LM(Locomotion)"
        else:
            if mean_segmove > 0.1:
                mean_state_text = "State: NM(Non-locomotor movement)"
            else:
                mean_state_text = "State: KS(Keep Stillness)"

        if b == self.spinBox.value():
            text = "Trans: {:.2f} pixel/frame".format(mean_trans)
            cv2.putText(frame, text, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            text = "SegMove: {:.2f} %/frame".format(mean_segmove*100)
            cv2.putText(frame, text, (60, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            cv2.putText(frame, mean_state_text, (60, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        # Figure 400 | 370, 400, 430

        self.analysis_box[b][4] = center
        self.analysis_box[b][5] = mask

    def location_loading(self):
        if self.isStatus == 1:
            self.isStatus = 0
            return
        elif self.isStatus != 0:
            print('[INFO] Error in interrupting algorithm.')
            QMessageBox.information(self, 'Warning', 'You Must Stop Algorithm Process First.\n'
                                                     '(Key: ... Suspending)', QMessageBox.Ok)
            return
        self.video_name = QFileDialog.getExistingDirectory(self, 'Choose Frames Location', './')
        if self.video_name == '':
            return
        self.label_source.setText(self.video_name)
        is_frame = False
        for frame in self.get_frames(self.video_name):
            is_frame = True
            self.label_image.setPixmap(QPixmap(self.cv2_to_qimge(frame)))
            self.paint_frame = frame
            QApplication.processEvents()
            break
        if not is_frame:
            print('[INFO] Error in location selecting.')
            QMessageBox.information(self, 'Warning', 'You Must Choose Some Location (That Contains Images).\n'
                                                     '(Shortcut Key: Alt + L)', QMessageBox.Ok)
            return
        self.isStatus = 1

    def video_loading(self):
        if self.isStatus == 2:
            self.isStatus = 0
            return
        elif self.isStatus != 0:
            print('[INFO] Error in interrupting algorithm.')
            QMessageBox.information(self, 'Warning', 'You Must Stop Algorithm Process First.\n'
                                                     '(Key: ... Suspending)', QMessageBox.Ok)
            return
        self.video_name = QFileDialog.getOpenFileName(self, 'Choose Frames File', './', 'Video file (*.avi *.mp4)')
        self.video_name, _ = self.video_name
        if self.video_name == '':
            return
        self.label_source.setText(self.video_name)
        is_frame = False
        for frame in self.get_frames(self.video_name):
            is_frame = True
            self.label_image.setPixmap(QPixmap(self.cv2_to_qimge(frame)))
            self.paint_frame = frame
            QApplication.processEvents()
            break
        if not is_frame:
            print('[INFO] Error in video reading.')
            QMessageBox.information(self, 'Warning', 'You Must Re-choose Some Video (That Could Be Read).\n'
                                                     '(Shortcut Key: Alt + V)', QMessageBox.Ok)
            return
        self.isStatus = 2

    def camera_loading(self):
        if self.isStatus == 1 or self.isStatus == 2:
            print('[INFO] Error in interrupting algorithm.')
            QMessageBox.information(self, 'Warning', 'You Must Stop Algorithm Process First.\n'
                                                     '(Key: ... Suspending)', QMessageBox.Ok)
            return
        if self.isStatus == 3:
            self.isStatus = 0
            print("[INFO] Exporting webcam stream.")
            self.pushButton_cameraLoading.setText('&Camera Loading')
            self.bbox_list = []
            self.rectList = []
            self.paint_frame = None
            if self.vs is not None:
                self.vs.release()
            self.isPainting = False
        else:
            self.isStatus = 3
            self.pushButton_cameraLoading.setText('&Camera Suspending')
        if self.isStatus == 3:
            trackers = []
            mirror = True
            print("[INFO] Importing webcam stream.")
            self.vs = cv2.VideoCapture(0)
            self.vs.set(3, 1280)
            self.vs.set(4, 720)
            fps_cal = None
            f = 0
            self.first_frame = True
            save_loc_d = './ans/' + '__webcam__'
            save_loc_t = save_loc_d + '/' + str(self.tracker_name)
            system('mkdir ' + save_loc_t.replace('/', '\\'))
            system('del /q ' + save_loc_t.replace('/', '\\'))
            while True:
                _, frame = self.vs.read()
                # 预处理的裁切 -> 800*600
                frame = frame[60:660, 240:1040, :]
                if mirror:
                    frame = cv2.flip(frame, 1)
                self.paint_frame = frame
                if (not self.isPainting) and len(self.bbox_list):
                    if self.first_frame:
                        print('[INFO] Here are initialization of processing webcam.')
                        for b in range(len(self.bbox_list)):
                            trackers.append(deepcopy(self.tracker))
                        for b in range(len(self.bbox_list)):
                            trackers[b].init(frame, self.bbox_list[b])
                        fps_cal = FPS().start()
                        self.analysis_init()
                        self.first_frame = False
                    else:
                        masks = None
                        for b in range(len(self.bbox_list)):
                            outputs = trackers[b].track(frame)
                            if 'polygon' in outputs:
                                polygon = np.array(outputs['polygon']).astype(np.int32)
                                cv2.polylines(frame, [polygon.reshape((-1, 1, 2))],
                                              True, (0, 255, 0), 3)
                                mask = ((outputs['mask'] > cfg.TRACK.MASK_THERSHOLD) * 255)
                                mask = mask.astype(np.uint8)
                                if masks is None:
                                    masks = mask
                                else:
                                    masks += mask
                                polygon_xmean = (polygon[0]+polygon[2]+polygon[4]+polygon[6])/4
                                polygon_ymean = (polygon[1]+polygon[3]+polygon[5]+polygon[7])/4
                                cv2.rectangle(frame, (int(polygon_xmean)-1, int(polygon_ymean)-1),
                                              (int(polygon_xmean)+1, int(polygon_ymean)+1), (0, 255, 0), 3)
                                self.behavior_analysis(frame, b,
                                                       (polygon_xmean, polygon_ymean), (mask > 0))
                            else:
                                bbox = list(map(int, outputs['bbox']))
                                cv2.rectangle(frame, (bbox[0], bbox[1]),
                                              (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 3)
                        frame[:, :, 2] = (masks > 0) * 255 * 0.75 + (masks == 0) * frame[:, :, 2]
                        fps_cal.update()
                        fps_cal.stop()
                        text = "FPS: {:.2f}".format(fps_cal.fps())
                        cv2.putText(frame, text, (60, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    # 非处理中，延迟取帧：0.05s
                    cv2.waitKey(50)
                f += 1
                if self.checkBox.checkState():
                    save_loc_i = save_loc_t + "/" + str(f).zfill(4) + ".jpg"
                    cv2.imwrite(save_loc_i, frame)
                self.label_image.setPixmap(QPixmap(self.cv2_to_qimge(frame)))
                QApplication.processEvents()
                if self.isStatus != 3:
                    self.vs.release()
                    self.label_image.setPixmap(QPixmap())
                    QApplication.processEvents()
                    break

    def bbox_setting(self):
        if self.isPainting:
            print('[INFO] Throw away the setting bbox of: ' + str(self.bbox_list))
            self.bbox_list = []
            self.rectList = []
            self.tempPix = QPixmap((self.cv2_to_qimge(self.paint_frame)))
        else:
            if self.paint_frame is None:
                QMessageBox.information(self, 'Warning', 'You Must Get Data First.\n(Alt + L / V / C)',
                                        QMessageBox.Ok)
            else:
                self.isPainting = True
                self.tempPix = QPixmap((self.cv2_to_qimge(self.paint_frame)))
                self.pushButton_bboxSetting.setText("&B-box Reconfiguring")

    def algorithm_processing(self):
        if len(self.bbox_list) == 0:
            print('[INFO] Error in b-box choosing.')
            QMessageBox.information(self, 'Warning', 'You Must Confirm B-box First.\n(Shortcut Key: Alt + B)',
                                    QMessageBox.Ok)
            return
        self.isPainting = False
        self.pushButton_bboxSetting.setText("&B-box Setting")
        if self.isStatus == 1:
            self.pushButton_locationLoading.setText('&Stream Suspending')
        elif self.isStatus == 2:
            self.pushButton_videoLoading.setText('&Stream Suspending')
        elif self.isStatus == 3:
            self.first_frame = True
            return
        trackers = []
        for b in range(len(self.bbox_list)):
            trackers.append(deepcopy(self.tracker))
        print("[INFO] Starting pictures stream.")
        fps_cal = None
        self.first_frame = True
        save_loc_d = './ans/' + self.video_name.split('/')[-1]
        save_loc_t = save_loc_d + '/' + str(self.tracker_name)
        f = 0
        for frame in self.get_frames(self.video_name):
            if self.first_frame:
                for b in range(len(self.bbox_list)):
                    trackers[b].init(frame, self.bbox_list[b])
                self.first_frame = False
                if self.checkBox.checkState():
                    system('mkdir ' + save_loc_t.replace('/', '\\'))
                fps_cal = FPS().start()
                self.analysis_init()
            else:
                if self.isStatus == 0:
                    break
                masks = None
                for b in range(len(self.bbox_list)):
                    outputs = trackers[b].track(frame)
                    if 'polygon' in outputs:
                        polygon = np.array(outputs['polygon']).astype(np.int32)
                        cv2.polylines(frame, [polygon.reshape((-1, 1, 2))],
                                      True, (0, 255, 0), 3)
                        mask = ((outputs['mask'] > cfg.TRACK.MASK_THERSHOLD) * 255)
                        mask = mask.astype(np.uint8)
                        if masks is None:
                            masks = mask
                        else:
                            masks += mask
                        polygon_xmean = (polygon[0] + polygon[2] + polygon[4] + polygon[6]) / 4
                        polygon_ymean = (polygon[1] + polygon[3] + polygon[5] + polygon[7]) / 4
                        cv2.rectangle(frame, (int(polygon_xmean) - 1, int(polygon_ymean) - 1),
                                      (int(polygon_xmean) + 1, int(polygon_ymean) + 1), (0, 255, 0), 3)
                        self.behavior_analysis(frame, b,
                                               (polygon_xmean, polygon_ymean), (mask > 0))
                    else:
                        bbox = list(map(int, outputs['bbox']))
                        cv2.rectangle(frame, (bbox[0], bbox[1]),
                                      (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                                      (0, 255, 0), 3)
                frame[:, :, 2] = (masks > 0) * 255 * 0.75 + (masks == 0) * frame[:, :, 2]
                fps_cal.update()
                fps_cal.stop()
                text = "FPS: {:.2f}".format(fps_cal.fps())
                cv2.putText(frame, text, (60, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                # Figure 400 | 340
                f += 1
                if self.checkBox.checkState():
                    save_loc_i = save_loc_t + "/" + str(f).zfill(4) + ".jpg"
                    cv2.imwrite(save_loc_i, frame)
                self.label_image.setPixmap(QPixmap(self.cv2_to_qimge(frame)))
                QApplication.processEvents()
        self.bbox_list = []
        self.rectList = []
        self.paint_frame = None
        del trackers, fps_cal
        print("[INFO] Ending pictures stream.")
        self.isStatus = 0
        self.pushButton_locationLoading.setText('&Location Loading')
        self.pushButton_videoLoading.setText('&Video Loading')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())