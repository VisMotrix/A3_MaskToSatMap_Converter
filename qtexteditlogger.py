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



from logging import LogRecord
from rich.logging import RichHandler
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QTextCursor

class QTextEditLogger(QTextEdit):

    update_message_signal_ = Signal(str)

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.update_message_signal_.connect(self.handle_msg)
        self.setReadOnly(True)

    @Slot(str)
    def handle_msg(self, record):
        self.append(record)
        self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().maximum())  
        c = self.textCursor()
        c.movePosition(QTextCursor.End)
        self.setTextCursor(c)

class CustomRichHandler(RichHandler):
    def __init__(self, out: QTextEditLogger):
        RichHandler.__init__(self)
        self.qobj = out

    def emit(self, record):
        msg = self.format(record)
        self.qobj.update_message_signal_.emit(msg)