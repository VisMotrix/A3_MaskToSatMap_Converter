#     A Arma 3 Mask To SatMap Converter
#     Copyright (C) 2022  VisMotrix, rk-exxec

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import os
import logging


from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QCoreApplication, Slot, Signal, QSettings, Qt, QThread

from form import Ui_guiMain
from aboutDlg import AboutDialog

from maskToSatMap import *

from globals import *
from qtexteditlogger import CustomRichHandler

def qt_path(file):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = os.path.join(sys._MEIPASS, 'qt')
    except Exception:
        base_path = os.path.abspath("./qt")

    return os.path.join(base_path, file)

class CallbackWorker(QThread):
    """ Thread with callback function on exit """
    def __init__(self, target, *args, slotOnFinished=None, **kwargs):
        super(CallbackWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.target = target
        if slotOnFinished:
            self.finished.connect(slotOnFinished)

    def run(self):
        self.target(*self.args, **self.kwargs)

class MainWindow(QMainWindow, Ui_guiMain):

    progress_update_signal = Signal(int)

    def __init__(self):

        super(MainWindow, self).__init__()
        # init UI
        self.setupUi(self)

        # load stylesheet
        # with open(qt_path("Combinear.qss")) as fh:
        #     self.setStyleSheet(fh.read())

        self.settings = QSettings()

        self.log = self.plainTextEdit

        self.layers_path = self.settings.value("layers_path", "P:\\")
        self.mask_path = self.settings.value("mask_path", "P:\\")
        self.satmap_path = self.settings.value("satmap_path", "P:\\")
        self.workdrive_path = self.settings.value("workdrive_path", "P:\\")
        self.noise_type = self.settings.value("noise_type", 0)
        self.noise_strength = self.settings.value("noise_strength", [2,2,2])
        self.noise_coverage = self.settings.value("noise_coverage", 0.5)

        self.thread: CallbackWorker = None

        self.layerPathEdit.setText(self.layers_path)
        self.maskPathEdit.setText(self.mask_path)
        self.satmapPathEdit.setText(self.satmap_path)
        self.workDrivePathEdit.setText(self.workdrive_path)
        self.noiseCombo.setCurrentIndex(self.noise_type)
        self.rNoiseSpin.setValue(int(self.noise_strength[0]))
        self.gNoiseSpin.setValue(int(self.noise_strength[1]))
        self.bNoiseSpin.setValue(int(self.noise_strength[2]))
        self.coverageSpin.setValue(float(self.noise_coverage))

        self.openLayersBtn.clicked.connect(self.loadLayersCfg)
        self.openMaskBtn.clicked.connect(self.loadMask)
        self.saveAsBtn.clicked.connect(self.saveAs)
        self.openPDrvBtn.clicked.connect(self.open_p_drive)
        self.startBtn.clicked.connect(self.start)
        self.resultBtn.clicked.connect(self.show_result)
        self.actionLicense.triggered.connect(self.show_license)

        self.layerPathEdit.editingFinished.connect(self.update_path(self.layers_path, self.layerPathEdit))
        self.maskPathEdit.editingFinished.connect(self.update_path(self.mask_path, self.maskPathEdit))
        self.satmapPathEdit.editingFinished.connect(self.update_path(self.satmap_path, self.satmapPathEdit))
        self.workDrivePathEdit.editingFinished.connect(self.update_path(self.workdrive_path, self.workDrivePathEdit))
        self.noiseCombo.currentIndexChanged.connect(self.update_noise_type)
        self.rNoiseSpin.valueChanged.connect(lambda x: self.update_noise_strength(0,x))
        self.gNoiseSpin.valueChanged.connect(lambda x: self.update_noise_strength(1,x))
        self.bNoiseSpin.valueChanged.connect(lambda x: self.update_noise_strength(2,x))
        self.coverageSpin.valueChanged.connect(self.update_noise_coverage)

        self.update_noise_type(self.noise_type)

        self.progressBar.setValue(0)
        self.progress_update_signal.connect(self.update_progress)

    @Slot()
    def start(self):
        global MEMMAP, TEMPDIR, logger

        self.startBtn.setEnabled(False)

        self.progressBar.setValue(0)
        app.processEvents()

        if self.actionVerbose_Output.isChecked():
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("Starting ...")
        logger.debug(f"Params: Layers {self.layers_path}, Mask {self.mask_path}, Satmap {self.satmap_path}, Noise Type {self.noise_type}, Noise Strength {self.noise_strength}, Noise Coverage {self.noise_coverage}%")
        MEMMAP = True
        if MEMMAP:
            logger.info("Creating tempdir")
            TEMPDIR = TemporaryDirectory(prefix="satmapconv_", ignore_cleanup_errors=False)

        
        if self.thread:
            self.thread.wait()
        self.thread = CallbackWorker(self.execute, slotOnFinished=self.finished)
        self.thread.start()

    def finished(self):
        global MEMMAP, TEMPDIR, logger
        if MEMMAP:
            shutil.rmtree(TEMPDIR.name)
            # TEMPDIR.cleanup()
        logger.info("... Done")
        self.progressBar.setValue(100)
        self.startBtn.setEnabled(True)

    def execute(self):
        global logger
        logger.info("Reading layers.cfg")
        surfaces = read_layers_cfg(self.layers_path)
        self.progress_update_signal.emit(25)

        logger.info("Loading average colors from textures")
        surfaces = load_average_colors(surfaces)
        self.progress_update_signal.emit(33)

        logger.info("Starting sat map generation")
        sat_map = replace_mask_color(self.mask_path, surfaces)
        self.progress_update_signal.emit(50)

        if self.noise_type == 2:
            logger.info("Starting sat map noise generation")
            sat_map = rgb_noise_generation(sat_map, self.noise_strength, self.noise_coverage/100)
        elif self.noise_type == 1:
            logger.info("Starting sat map noise generation")
            sat_map = lum_noise_generation(sat_map, self.noise_strength[1], self.noise_coverage/100)
        self.progress_update_signal.emit(75)

        logger.info("Saving sat map")
        export_map(sat_map, self.satmap_path)
        self.progress_update_signal.emit(99)

    @Slot(int)
    def update_progress(self, val):
        self.progressBar.setValue(val)

    @Slot()
    def loadLayersCfg(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select layer file", os.path.dirname(self.layers_path), filter="Config file (*.txt *.cfg *.conf)")
        if file:
            self.layerPathEdit.setText(file)
            self.layers_path = file
            self.settings.setValue("layers_path", file)

    @Slot()
    def loadMask(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select mask image", os.path.dirname(self.mask_path), filter="Image (*.png *.jpg *.jpeg *.tif *.tiff *.bmp)")
        if file:
            self.maskPathEdit.setText(file)
            self.mask_path = file
            self.settings.setValue("mask_path", file)

    @Slot()
    def saveAs(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save sat map as", os.path.dirname(self.satmap_path), filter="Image (*.tif *.tiff)")
        if file:
            self.satmapPathEdit.setText(file)
            self.satmap_path = file
            self.settings.setValue("satmap_path", file)

    @Slot()
    def open_p_drive(self):
        dir = QFileDialog.getExistingDirectory(self, "A3 Tools working directory", dir=os.path.expanduser("~"))
        if dir:
            self.workDrivePathEdit.setText(dir)
            self.workdrive_path = dir
            self.settings.setValue("workdrive_path", dir)

    @Slot()
    def show_result(self):
        os.startfile(os.path.dirname(self.satmap_path))

    @Slot()
    def show_license(self):
        dlg = AboutDialog(self)

    def update_path(self, path, lineEdit):
        path = lineEdit.text

    @Slot()
    def update_noise_type(self, idx):
        self.noise_type = idx
        self.settings.setValue("noise_type", idx)
        if idx == 0:
            self.rNoiseSpin.setEnabled(False)
            self.gNoiseSpin.setEnabled(False)
            self.bNoiseSpin.setEnabled(False)
            self.coverageSpin.setEnabled(False)
            self.rLabel.setText("")
            self.gLabel.setText("")
            self.bLabel.setText("")
        elif idx == 1:
            self.rNoiseSpin.setEnabled(False)
            self.rNoiseSpin.hide()
            self.gNoiseSpin.setEnabled(True)
            self.bNoiseSpin.setEnabled(False)
            self.bNoiseSpin.hide()
            self.coverageSpin.setEnabled(True)
            self.rLabel.setText("")
            self.gLabel.setText("L")
            self.bLabel.setText("")
        else:
            self.rNoiseSpin.setEnabled(True)
            self.rNoiseSpin.show()
            self.gNoiseSpin.setEnabled(True)
            self.bNoiseSpin.setEnabled(True)
            self.bNoiseSpin.show()
            self.coverageSpin.setEnabled(True)
            self.rLabel.setText("R")
            self.gLabel.setText("G")
            self.bLabel.setText("B")

    @Slot()
    def update_noise_strength(self, col, val):
        self.noise_strength[col] = val
        self.settings.setValue("noise_strength", self.noise_strength)

    @Slot()
    def update_noise_coverage(self, val):
        self.noise_coverage = val
        self.settings.setValue("noise_coverage", val)





if __name__ == "__main__":

    QCoreApplication.setOrganizationName("AVS")
    QCoreApplication.setApplicationName("A3MaskToSatMap")
    app = QApplication()
    app.processEvents()
    window  = MainWindow()

    logger = initialize_logger(CustomRichHandler(window.log))

    window.show()

    sys.exit(app.exec())
