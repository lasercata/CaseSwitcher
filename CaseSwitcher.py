# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2022.07.17
# Version           : v1.0
#
#--------------------------------

##-Ini
alf_lower = 'azertyuiopqsdfghjklmwxcvbn'
alf_upper = alf_lower.upper()

version = '1.0'

upper_to_lower_dct = {
    '2': 'é',
    '7': 'è',
    '9': 'ç',
    '0': 'à',
    '%': 'ù',
    '?': ',',
    ';': '.',
    '/': ':',
    '§': '!'
}


##-Imports
#------gui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QCloseEvent, QPalette, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QStyleFactory,
    QLabel, QGridLayout, QLineEdit, QMessageBox, QWidget, QPushButton, QCheckBox,
    QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget, QTableWidget, QFileDialog,
    QRadioButton, QTextEdit, QButtonGroup, QSizePolicy, QSpinBox, QFormLayout,
    QSlider, QMenuBar, QMenu, QPlainTextEdit, QAction, QToolBar, QShortcut, QDialog)

#------other
import sys
import pyperclip
import webbrowser


##-Case switching
def to_lower(s):
    return s.lower()


def to_upper(s):
    return s.upper()


def switch(s, to_lower=True):
    '''Switch case of s.'''

    ret = ''

    for k in s:
        if k in alf_lower:
            ret += k.upper()

        elif k in alf_upper:
            ret += k.lower()

        else:
            ret += k


    if to_lower:
        for k in upper_to_lower_dct:
            ret = ret.replace(k, upper_to_lower_dct[k])

    return ret

##-GUI
class CaseSwitcherGUI(QMainWindow):
    '''CaseSwitcher window'''

    def __init__(self, parent=None):
        '''Initialize the window'''

        #------ini
        super().__init__(parent)
        self.setWindowTitle('CaseSwitcher v' + version)
        self.setWindowIcon(QIcon('icon.png'))

        self.auto_switch_activated = True

        #------Widgets
        #---Central widget
        #-font
        self.fixed_font = QFont('monospace')
        self.fixed_font.setStyleHint(QFont.TypeWriter)

        #-The widget
        self.txt_in = QPlainTextEdit()
        self.txt_in.textChanged.connect(self._auto_switch)
        self.txt_in.setFont(self.fixed_font)
        self.setCentralWidget(self.txt_in)

        #---Statusbar
        # self._create_statusbar()

        #---Toolbars
        self.setContextMenuPolicy(Qt.NoContextMenu) #Not be able to hide bar.
        self._create_out_txt()
        self._create_bt_toolbar()

        #---Menu
        self._create_menu_bar()

        #------Show
        self.show()
        self.resize(800, 400)


    def _create_menu_bar(self):
        '''Create the menu bar.'''

        #------Menu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        #------The menus
        #---File
        self.file_m = menu_bar.addMenu('&Fichier')

        #-Copy
        self.copy_ac = QAction('&Copier dans le presse-papier', self)
        self.copy_ac.triggered.connect(self._copy_to_paperclip)
        self.file_m.addAction(self.copy_ac)

        self.file_m.addSeparator()

        #-Quit
        self.quit_ac = QAction('&Quitter', self)
        self.quit_ac.triggered.connect(self.close)
        self.file_m.addAction(self.quit_ac)


        #---Edit
        self.edit_m = menu_bar.addMenu('&Edition')

        #-Switch
        self.switch_ac = QAction('&Intervertir la casse', self)
        self.switch_ac.triggered.connect(self._switch_case)
        self.edit_m.addAction(self.switch_ac)

        #-Uppercase
        self.upper_ac = QAction('&MAJUSCULES', self)
        self.upper_ac.triggered.connect(self._set_uppercase)
        self.edit_m.addAction(self.upper_ac)

        #-Lowercase
        self.lower_ac = QAction('Mi&nuscules', self)
        self.lower_ac.triggered.connect(self._set_lowercase)
        self.edit_m.addAction(self.lower_ac)

        self.edit_m.addSeparator()

        #-Auto switch
        self.auto_switch_ac = QAction('Interversion &automatique', self, checkable=True)
        self.auto_switch_ac.triggered.connect(self._update_auto)
        self.auto_switch_ac.setChecked(True)
        self.edit_m.addAction(self.auto_switch_ac)


        #---View
        self.view_m = menu_bar.addMenu('&Affichage')

        #-Show toolbar
        self.show_toolbar_ac = QAction('&Barre visible', self, checkable=True)
        self.show_toolbar_ac.triggered.connect(self.bt_toolbar.setVisible)
        self.show_toolbar_ac.setChecked(True)
        self.view_m.addAction(self.show_toolbar_ac)


        #---About
        self.about_m = menu_bar.addMenu('À &propos')

        #-About
        self.about_ac = QAction('À &propos ...')
        self.about_ac.triggered.connect(self.show_about)
        self.about_m.addAction(self.about_ac)

        #-Source
        self.src_ac = QAction('Voir le code source ...')
        self.src_ac.triggered.connect(lambda: webbrowser.open_new_tab('https://github.com/lasercata/CaseSwitcher'))
        self.about_m.addAction(self.src_ac)


    def _update_auto(self):
        '''Update the check boxes to be syncronized.'''

        self.auto_switch_activated = 1 - self.auto_switch_activated

        self.auto_chk.setChecked(self.auto_switch_activated)
        self.auto_switch_ac.setChecked(self.auto_switch_activated)


    def _create_bt_toolbar(self):
        '''Create the buttons toolbar.'''

        #------Ini
        self.bt_toolbar = QToolBar('Actions', self)
        self.bt_toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.bt_toolbar)

        bt_wid = QWidget()
        bt_toolbar_lay = QGridLayout()
        bt_wid.setLayout(bt_toolbar_lay)
        self.bt_toolbar.addWidget(bt_wid)

        #------Widgets
        #---Auto switch
        self.auto_chk = QCheckBox('Interversion automatique')
        self.auto_chk.clicked.connect(self._update_auto)
        self.auto_chk.setChecked(True)
        bt_toolbar_lay.addWidget(self.auto_chk, 0, 4, Qt.AlignRight)

        #---Button switch
        self.bt_switch = QPushButton('Intervertir la casse')
        self.bt_switch.clicked.connect(self._switch_case)
        bt_toolbar_lay.addWidget(self.bt_switch, 0, 0)

        #---Button UPPERCASE
        self.bt_upper = QPushButton('MAJUSCULES')
        self.bt_upper.clicked.connect(self._set_uppercase)
        bt_toolbar_lay.addWidget(self.bt_upper, 0, 1)

        #---Button lowercase
        self.bt_lower = QPushButton('minuscules')
        self.bt_lower.clicked.connect(self._set_lowercase)
        bt_toolbar_lay.addWidget(self.bt_lower, 0, 2)

        #---Button copy
        self.bt_copy = QPushButton('Copier dans le presse-papier')
        self.bt_copy.clicked.connect(self._copy_to_paperclip)
        bt_toolbar_lay.addWidget(self.bt_copy, 0, 3)


    def _create_out_txt(self):
        '''Create the output text viewer.'''

        self.out_toolbar = QToolBar('Output', self)
        self.out_toolbar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea, self.out_toolbar)

        self.txt_out = QPlainTextEdit()
        #self.txt_out.textChanged.connect(self._show_wc)
        #self.txt_out.textChanged.connect(lambda: self._txt_changed('out'))
        self.txt_out.setReadOnly(True)
        self.txt_out.setMaximumHeight(130)
        self.txt_out.setFont(self.fixed_font)
        self.out_toolbar.addWidget(self.txt_out)


    def _create_statusbar(self):
        '''Create the status bar.'''

        self.statusbar = self.statusBar()


    def _switch_case(self):
        '''Switch the case of the text and write the result in output.'''

        self.txt_out.setPlainText(switch(self.txt_in.toPlainText()))


    def _auto_switch(self):
        '''Check if activated, and switch case.'''

        if self.auto_chk.isChecked():
            self._switch_case()


    def _set_uppercase(self):
        '''Set the uppercased input text in the output.'''

        self.txt_out.setPlainText(to_upper(self.txt_in.toPlainText()))


    def _set_lowercase(self):
        '''Set the lowercased input text in the output.'''

        self.txt_out.setPlainText(to_lower(self.txt_in.toPlainText()))


    def _copy_to_paperclip(self):
        '''Copy output text to the paperclip.'''

        pyperclip.copy(self.txt_out.toPlainText())


    def show_about(self):
        '''Show the about popup.'''

        about = '<center><h1>Case Switcher v{}</h1></center>\n'.format(version)

        about += "Case Switcher permet de changer la casse d'un texte facilement."

        about += '<h2>Auteur :</h2>'
        about += '<p>Lasercata (https://github.com/lasercata)</p>'

        QMessageBox.about(self, 'À propos — CaseSwitcher', about)


    #---------use
    def use():
        '''Launch the application.'''

        global app, win

        app = QApplication(sys.argv)
        win = CaseSwitcherGUI()

        #---Show 'Ready' in status bar
        # win.statusbar.showMessage('Prêt !', 3000)

        sys.exit(app.exec_())



##-run
if __name__ == '__main__':
    #------Launch the GUI
    CaseSwitcherGUI.use()
