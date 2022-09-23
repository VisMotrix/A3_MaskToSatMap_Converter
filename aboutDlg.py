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

from PySide6.QtWidgets import QDialog, QPlainTextEdit, QPushButton, QFrame
from PySide6.QtCore import QCoreApplication, QRect, Qt


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUI()

        # Add button signal to greetings slot
        self.okButton.clicked.connect(self.hide)

        self.show()


    def setupUI(self):
        self.resize(431, 260)
        self.licenseText = QPlainTextEdit(self)
        self.licenseText.setObjectName(u"licenseText")
        self.licenseText.setEnabled(True)
        self.licenseText.setGeometry(QRect(10, 10, 411, 211))
        self.licenseText.setFrameShape(QFrame.StyledPanel)
        self.licenseText.setFrameShadow(QFrame.Sunken)
        self.licenseText.setUndoRedoEnabled(False)
        self.licenseText.setTextInteractionFlags(Qt.NoTextInteraction)
        self.okButton = QPushButton(self)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setGeometry(QRect(350, 230, 75, 23))

        self.retranslateUi()
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("about", u"About MAEsure", None))
        self.licenseText.setPlainText(QCoreApplication.translate("about", u"""A Arma 3 Mask To SatMap Converter
Copyright (C) 2022  VisMotrix, rk-exxec

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.""", None))
        self.licenseText.setPlaceholderText("")
        self.okButton.setText(QCoreApplication.translate("about", u"OK", None))
    # retranslateUi
