# -*- coding: utf-8 -*-
from PyQt4.QtGui import QAction,QDialog
from PyQt4.QtGui import QVBoxLayout,QHBoxLayout,QGridLayout
from PyQt4.QtGui import QLabel,QDialogButtonBox,QCheckBox
from PyQt4.QtGui import QLineEdit,QPushButton,QSpinBox,QComboBox
from PyQt4.QtGui import QTableView,QStandardItemModel,QStandardItem
from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import QUrl
QString = str

from qgis._gui import QgsEncodingFileDialog
from qgis.core import QgsVectorLayer,QgsMapLayerRegistry

import numpy as np
import numpy.core.defchararray as def_c

from collections import OrderedDict
import csv

from mesh_wkt import mesh_wkt

class main:
    
    def __init__(self,iface):
        self.iface = iface
        self.f_len = np.vectorize(lambda x: len(x))
        
    def initGui(self):
        self.action = QAction(u"標準地域メッシュレイヤの追加",self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(u"&標準地域メッシュツール",self.action)
        
    def unload(self):        
        self.iface.removePluginMenu(u"&標準地域メッシュツール", self.action)
    
    def run(self):
        self.dlg_main = dlg_main()
        self.dlg_main.initGui()
        self.dlg_main.show()
        
        
class dlg_main(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.dlg_csv_error = dlg_csv_error(self) 
        self.dlg_csv_error.initGui()
        
        self.kukaku_dict = OrderedDict() 
        self.kukaku_dict[u"第1次地域区画"] = 4
        self.kukaku_dict[u"第2次地域区画"] = 6
        self.kukaku_dict[u"第3次地域区画"] = 8
        self.kukaku_dict[u"5倍地域メッシュ"] = 7
        self.kukaku_dict[u"2倍地域メッシュ"] = 9
        self.kukaku_dict[u"2分の1地域メッシュ"] = 9
        self.kukaku_dict[u"4分の1地域メッシュ"] = 10
        self.kukaku_dict[u"8分の1地域メッシュ"] = 11
        self.kukaku_dict[u"10分の１細分地域メッシュ"] = 10   
        
        self.dat_str = np.array([])
        self.table_header = np.array([])
        self.csv_dat_str = np.array([])
        
        self.EF_dia = myFileDialog(self)
    
        self.f_len = np.vectorize(lambda x: len(x))
        
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
        
        self.HBL_recopt.addWidget(self.Lab_recopt)
        self.HBL_recopt.addWidget(self.SpB_recopt)
        self.HBL_recopt.addWidget(self.ChB_recopt)        
        self.GrL_config.addLayout(self.HBL_recopt,0,1)
        
        self.Lab_mesh_titile = QLabel(u"メッシュ定義")
        self.GrL_config.addWidget(self.Lab_mesh_titile,1,0)
        
        self.HBL_mesh = QHBoxLayout()
        self.Lab_mesh_field = QLabel(u"メッシュコード列")
        self.CoB_mesh_field = QComboBox()
        
        self.Lab_mesh_category = QLabel(u"地域メッシュ区画")
        self.CoB_mesh_category = QComboBox()
        self.CoB_mesh_category.addItems(self.kukaku_dict.keys())
        
        self.HBL_mesh.addWidget(self.Lab_mesh_field)
        self.HBL_mesh.addWidget(self.CoB_mesh_field)
        self.HBL_mesh.addWidget(self.Lab_mesh_category)
        self.HBL_mesh.addWidget(self.CoB_mesh_category)
        
        self.GrL_config.addLayout(self.HBL_mesh,1,1)
        
        self.Lab_crs_title = QLabel(u"測地系")
        self.GrL_config.addWidget(self.Lab_crs_title,2,0)
        
        self.CoB_crs = QComboBox()
        self.CoB_crs.addItems([u"世界測地系(EPSG:4612)",u"日本測地系(EPSG:4301)"])
        self.GrL_config.addWidget(self.CoB_crs,2,1)       
        
        self.VBL_main.addLayout(self.GrL_config)
        
        self.model_content = QStandardItemModel()
        self.TB_content = QTableView()
        self.TB_content.setModel(self.model_content)
        
        self.VBL_main.addWidget(self.TB_content)
        
        self.DBB_main = QDialogButtonBox()
        self.DBB_main.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        
        self.VBL_main.addWidget(self.DBB_main)
        
        self.setLayout(self.VBL_main)
        
        self.ChB_recopt.setChecked(True)
        self.ChB_recopt.stateChanged.connect(self.update_csv_str)
        self.SpB_recopt.valueChanged.connect(self.update_csv_str)
        self.PuB_selectfile.clicked.connect(self.EF_dia.open)
        
        self.DBB_main.accepted.connect(self.accept)
        self.DBB_main.rejected.connect(self.reject)

        
    def update_csv_str(self):
        if len(self.dat_str) == 0:
            pass
        else:
            if  self.ChB_recopt.checkState() == 0:
                csv_header = np.array(["field_{0}".format(x) for x in np.arange(0,self.dat_str.shape[1])])
                self.csv_dat_str = self.dat_str[(self.SpB_recopt.value()):,]
            else:
                csv_header = self.dat_str[self.SpB_recopt.value(),]
                self.csv_dat_str =self.dat_str[(self.SpB_recopt.value()+1):,] 
                
            self.clear()
            
            self.table_header = np.array([hstr if hstr != u"" else 'field_{0}'.format(i) for i,hstr in enumerate(csv_header)])
            
            
            load_table(self.model_content, self.table_header, np.arange(0,11), self.csv_dat_str) 
            self.CoB_mesh_field.addItems(self.table_header)
        
    def clear(self):
        self.model_content.clear()
        self.CoB_mesh_field.clear()
        
    def accept(self):
        if len(self.LiE_selectfile.text()) == 0:
            QMessageBox.warning(self,u"警告",u"ファイルを選択してください")
        elif len(self.LiE_layername.text()) == 0:
            QMessageBox.warning(self,u"警告",u"レイヤ名を入力してください")
        else:
            self.csv_meshid_str = self.csv_dat_str[:,self.CoB_mesh_field.currentIndex()]
        
            if self.check_decimal():
                self.dlg_csv_error.LB_caution.setText(u"以下のデータのメッシュコードに空白\nまたは数値以外の文字が含まれています")
                load_table(self.dlg_csv_error.model_content,self.table_header, self.e_ind, self.csv_dat_str)
                self.dlg_csv_error.show()
            elif self.check_digit():
                str = u"以下のデータのメッシュコードの桁数が不正です\n"
                str += u'{0}コードは{1}桁の整数です。'.format(self.CoB_mesh_category.currentText(),
                                                  self.kukaku_dict[self.CoB_mesh_category.currentText()])
                self.dlg_csv_error.LB_caution.setText(str)
                load_table(self.dlg_csv_error.model_content,self.table_header, self.e_ind, self.csv_dat_str)
                self.dlg_csv_error.show()
            elif self.check_unique():
                str = u'以下のデータのメッシュコードが重複しています'
                self.dlg_csv_error.LB_caution.setText(str)
                load_table(self.dlg_csv_error.model_content,self.teble_header, self.e_ind, self.csv_dat_str)
                self.dlg_csv_error.show()
                    
            else:
                self.create_tmp_csv()
                self.load_wkt_csv()
                return QDialog.accept(self)

    def check_decimal(self):
        e_ind = np.where(~def_c.isdecimal(self.csv_meshid_str))[0]
        
        if len(e_ind) > 0:
            self.e_ind = e_ind
            return True
        else:
            return False
        
    def check_digit(self):
        digit_arr = self.f_len(self.csv_meshid_str)
        e_ind = np.where( digit_arr != self.kukaku_dict[self.CoB_mesh_category.currentText()])[0]
        
        if len(e_ind) > 0:
            self.e_ind = e_ind
            return True
        else:
            return False
        
    def check_unique(self):
        u,c = np.unique(self.csv_meshid_str,return_counts=True)
        tf = c > 1

        if tf.any():
            self.e_ind = np.where(np.in1d(self.csv_meshid_str, u[tf]))[0]
            return True
        else:
            return False
        
    def create_tmp_csv(self):


        
        m_wkt = mesh_wkt(self.CoB_mesh_category.currentText())
        
        infile_qstr = self.LiE_selectfile.text()
        self.outfile_qstr = self.LiE_selectfile.text().replace(".","_wkt.")
        
        in_fp = open(infile_qstr,"r")
        out_fp = open(self.outfile_qstr,"wb")
        reader = csv.reader(in_fp)
        writer = csv.writer(out_fp)
        
        n_skip = self.SpB_recopt.value()
        if n_skip > 0:
            for i in range(0,n_skip):
                next(reader,None)
            
        if self.ChB_recopt.checkState() == 2:
            header = next(reader,None)
            header.append("wkt")
            writer.writerow(header)
        
        for hrow in csv.reader(in_fp):
            hrow.append(m_wkt.res_wkt(hrow[0]))
            writer.writerow(hrow)
            
        in_fp.close()
        out_fp.close()  
        
    def load_wkt_csv(self):
        uri = QUrl.fromLocalFile(self.outfile_qstr)
        uri.addQueryItem("type","csv")
        uri.addQueryItem("delimiter",",")
        uri.addQueryItem("wktField",str(self.csv_dat_str.shape[1] + 1))
        uri.addQueryItem("encoding",self.EF_dia.encoding())        
        
        if self.ChB_recopt.checkState() == 2:
            uri.addQueryItem("useHeader","yes")
        else:
            uri.addQueryItem("useHeader","no")
            
        if self.CoB_crs.currentIndex() == 0:
            uri.addQueryItem("crs","EPSG:4612")
        elif self.CoB_crs.currentIndex() == 0:
            uri.addQueryItem("crs","EPSG:4301")

        self.vlayer = QgsVectorLayer(uri.toString(),self.LiE_layername.text(),"delimitedtext")
        
        if self.vlayer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer( self.vlayer )
        
        
    
    
class dlg_csv_error(QDialog):
    
    def __init__(self,parent):
        QDialog.__init__(self,parent=parent)
        self.initGui
        
    def initGui(self):
        self.VBL_main = QVBoxLayout()
        
        self.LB_caution = QLabel()
        
        self.VBL_main.addWidget(self.LB_caution)
        
        self.model_content = QStandardItemModel()
        self.TB_content = QTableView()
        self.TB_content.setModel(self.model_content)
        
        self.VBL_main.addWidget(self.TB_content)
        
        self.DBB_main = QDialogButtonBox()
        self.DBB_main.setStandardButtons(QDialogButtonBox.Close)
        
        self.VBL_main.addWidget(self.DBB_main)
        
        self.setLayout(self.VBL_main)
        
        self.DBB_main.rejected.connect(self.close)
        
class myFileDialog(QgsEncodingFileDialog):       
    
    def __init__(self,p_wid):
        QgsEncodingFileDialog.__init__(self)
        self.p_wid = p_wid
        self.dlg_csv_error = dlg_csv_error(self)  
        
    def accept(self):
        self.filename = self.selectedFiles()[0]
        self.f_enc = self.encoding()
        self.p_wid.clear() 
        
        try:
            dat_str = np.genfromtxt(self.filename,delimiter=",",dtype=np.str)            
            self.p_wid.dat_str = def_c.decode(dat_str,encoding=self.f_enc)
            self.p_wid.LiE_selectfile.setText(self.filename)
            self.p_wid.update_csv_str()
            
            return QgsEncodingFileDialog.accept(self)
                      
        except:
            msg = u"ファイルの文字コードが\n\r%sではありません" % self.f_enc
            QMessageBox.warning(self,u"インポートエラー",msg) 
        
        
        
          
def load_table(model_content,header,ind,csv_dat_str):
    model_content.clear()
    model_content.setHorizontalHeaderLabels(header)
        
    for i in ind:
            items = [ QStandardItem(field) for field in csv_dat_str[i]]
            model_content.appendRow(items)
            
    model_content.setVerticalHeaderLabels((ind+1).astype(np.str))
    

        


