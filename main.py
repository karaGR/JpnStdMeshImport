# -*- coding: utf-8 -*-
from PyQt4.QtGui import QAction,QDialog
from PyQt4.QtGui import QVBoxLayout,QHBoxLayout,QGridLayout
from PyQt4.QtGui import QLabel,QDialogButtonBox,QCheckBox
from PyQt4.QtGui import QLineEdit,QPushButton,QSpinBox
from PyQt4.QtGui import QTableView,QStandardItemModel,QStandardItem

import numpy as np
from PySide.QtGui import QComboBox

from collections import OrderedDict


class main:
    
    def __init__(self,iface):
        self.iface = iface
        self.kukaku_dict = QrderdDict() 
        self.kukaku_dict[u"第1次地域区画"] = 4
        self.kukaku_dict[u"第2次地域区画"] = 6
        self.kukaku_dict[u"第3次地域区画"] = 8
        self.kukaku_dict[u"5倍地域メッシュ"] = 7
        self.kukaku_dict[u"2倍地域メッシュ"] = 9
        self.kukaku_dict[u"2分の1地域メッシュ"] = 9
        self.kukaku_dict[u"4分の1地域メッシュ"] = 10
        self.kukaku_dict[u"8分の1地域メッシュ"] = 11
        self.kukaku_dict[u"10分の１細分地域メッシュ"] = 10        
        
    def initGui(self):
        self.action = QAction(u"標準地域メッシュレイヤの追加",self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(u"&標準地域メッシュツール",self.action)
        
    def unload(self):        
        self.iface.removePluginMenu(u"&標準地域メッシュツール", self.action)
    
    def run(self):
        self.dlg_main = dlg_main()
        
        
class dlg_main(QDialog):
    
    def __init__(self,pearent=pearent):
        self.dlg_csv_error = dlg_csv_error(self) 
        
    
    def initGui(self):
        self.VBL_main = QVBoxLayout()
       
        self.HBL_selectfile = QHBoxLayout()
        self.Lab_selectfile = QLabel(u"ファイル名")
        self.LiE_selectfile = QLineEdit()
        self.PuB_selectfile = QPushButton()
        self.PuB_selectfile.setText(u"参照")
        
        self.HBL_selectfile.addWidget(self.Lab_selectfile)
        self.HBL_selectfile.addWidget(self.LiE_selectfile)
        self.HBL_selectfile.addWidget(self.PuB_selectfile)
        self.VBL_main.addLayout(self.HBL_selectfile)
        
        self.HBL_layername = QHBoxLayout()
        self.Lab_layername = QLabel(u"レイヤ名")
        self.LiE_layername = QLineEdit()
        
        self.HBL_layername.addWidget(self.Lab_layername)
        self.HBL_layername.addWidget(self.LiE_layername)
        self.VBL_main.addLayout(self.HBL_layername)
        
        self.GrL_config = QGridLayout()
        
        self.Lab_recopt_title = QLabel(u"レコードオプション")
        self.GrL_config.addWidget(self.Lab_recopt_title, 0, 0)
        
        self.HBL_recopt = QHBoxLayout()
        self.Lab_recopt = QLabel(u"無視するヘッダー行")
        self.SpB_recopt = QSpinBox()
        self.ChB_recopt = QCheckBox()
        self.ChB_recopt.setText(u"最初のレコードはフィールド名を保持している")
        
        self.HBL_mesh = QHBoxLayout()
        self.Lab_mesh_titile = QLabel(u"メッシュ定義")
        
        self.Lab_mesh_field = QLabel(u"メッシュコード列")
        self.CoB_mesh_field = QComboBox()
        
        self.Lab_mesh_category = QLabel(u"地域メッシュ区画")
        
        
        
        
        
        
        
        
        
        
        
    
    
class dlg_csv_error(QDialog):
    
    def __init__(self,parent):
        QDialog.__init__(self,parent=parent)
        self.iniGui
        
    def initGui(self):
        self.VBL_main = QVBoxLayout()
        
        self.LB_coution = QLabel()
        
        self.VBL_main.addWidget(self.LB_coution)
        
        self.model_content = QStandardItemModel()
        self.TB_content = QTableView()
        self.TB_content.setModel(self.model_content)
        
        self.VBL_main.addWidget(self.TB_content)
        
        self.DBB_main = QDialogButtonBox()
        self.DBB_main.setStandardButtons(QDialogButtonBox.Close)
        
        self.VBL_main.addWidget(self.DBB_main)
        
        self.setLayout(self.VBL_main)
        
        self.DBB_main.rejected.connect(self.close)
        
def load_table(self,model_content,header,ind,table):
    model_content.clear()
    model_content.setHorizontalHeaderLabels(header)
        
    for hrow in table:
            items = [ QStandardItem(field) for field in hrow]
            self.model_content.appendRow(items)
            
    model_content.setVerticalHeaderLabels((ind+1).astype(np.str).tolist())
        
    
        

        

