# -*- coding: utf-8 -*-
import numpy as np

class mesh_wkt:
    　
    def __init__(self,categ):
        if categ == u"第1次地域区画":
            self.res_wkt = self.res_m1d_wkt
        elif categ == u"第2次地域区画":
            self.res_wkt = self.res_m2d_wkt
        elif categ == u"第3次地域区画":
            self.res_wkt = self.res_m3d_wkt
        elif categ == u"5倍地域メッシュ":
            self.res_wkt = self.res_m5x_wkt
        elif categ == u"2倍地域メッシュ":
            self.res_wkt = self.res_m2x_wkt
        elif categ == u"2分の1地域メッシュ":
            self.res_wkt = self.res_m2p_wkt
        elif categ == u"4分の1地域メッシュ":
            self.res_wkt = self.res_m4p_wkt
        elif categ == u"8分の1地域メッシュ":
            self.res_wkt == self.res_m8p_wkt
        elif categ == u"10分の１細分地域メッシュ":
            self.res_wkt = self.res_m10_wkt
            
            
                
    def res_m1d_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        
        x1d_arr = np.repeat(x1d,5) + [0,0,1,1,0]
        y1d_arr = np.repeat(y1d,5) + [0,1,1,0,0]
        
        laln_arr = np.core.defchararray.add((x1d_arr+100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,(y1d_arr/1.5).astype(np.str))

        return "POLYGON(( " + ",".join(laln_arr) + "))"

    def res_m2d_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        
        x2d_arr = np.repeat(x2d,5) + [0,0,1,1,0]
        y2d_arr = np.repeat(y2d,5) + [0,1,1,0,0]
        
        laln_arr = np.core.defchararray.add((x1d + x2d_arr/8 +100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d_arr/8)/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"

    def res_m3d_wkt(self,mcode):       
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        x3d = float(mcode[7])
        y3d = float(mcode[6])
        
        x3d_arr = np.repeat(x3d,5) + [0,0,1,1,0]
        y3d_arr = np.repeat(y3d,5) + [0,1,1,0,0]
        
        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x3d_arr/80 +100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8+ y3d_arr/80)/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
    
    def res_m5x_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        i5x = float(mcode[6])
        x5x = float((i5x-1)%2)
        y5x = float((i5x-1)//2)
        
        x5x_arr = np.repeat(x5x,5) + [0,0,1,1,0]
        y5x_arr = np.repeat(y5x,5) + [0,1,1,0,0]
        
        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x5x_arr/16 +100).astype(np.str),
                                            np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8 + y5x_arr/16)/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
    
    def res_m2x_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        x2x = float(mcode[7])/2
        y2x = float(mcode[6])/2
 
        x2x_arr = np.repeat(x2x,5) + [0,0,1,1,0]
        y2x_arr = np.repeat(y2x,5) + [0,1,1,0,0]
        
        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x2x_arr/40 +100).astype(np.str),
                                            np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8 + y2x_arr/40)/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
        
    def res_m2p_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        x3d = float(mcode[7])
        y3d = float(mcode[6])
        i2p = float(mcode[8])
        x2p = float((i2p-1)%2)
        y2p = float((i2p-1)//2)
        
        x2p_arr = np.repeat(x2p,5) + [0,0,1,1,0]
        y2p_arr = np.repeat(y2p,5) + [0,1,1,0,0]

        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x3d/80 + x2p_arr/160 +100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8+ y3d/80 + y2p_arr/160 )/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
    
    def res_m4p_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        x3d = float(mcode[7])
        y3d = float(mcode[6])
        i2p = float(mcode[8])
        x2p = float((i2p-1)%2)
        y2p = float((i2p-1)//2)
        i4p = float(mcode[9])
        x4p = float((i4p-1)%2)
        y4p = float((i4p-1)//2)
                
        x4p_arr = np.repeat(x4p,5) + [0,0,1,1,0]
        y4p_arr = np.repeat(y4p,5) + [0,1,1,0,0]

        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x3d/80 + x2p/160 + x4p_arr/320 +100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8+ y3d/80 + y2p/160 + y4p_arr/320 )/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
        
    def res_m8p_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        x3d = float(mcode[7])
        y3d = float(mcode[6])
        i2p = float(mcode[8])
        x2p = float((i2p-1)%2)
        y2p = float((i2p-1)//2)
        i4p = float(mcode[9])
        x4p = float((i4p-1)%2)
        y4p = float((i4p-1)//2)
        i8p = float(mcode[10])
        x8p = float((i8p-1)%2)
        y8p = float((i8p-1)//2)
        
        x8p_arr = np.repeat(x8p,5) + [0,0,1,1,0]
        y8p_arr = np.repeat(y8p,5) + [0,1,1,0,0]

        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x3d/80 + x2p/160 + x4p/320 + x8p_arr/640 +100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8+ y3d/80 + y2p/160 + y4p/320 + y8p_arr/640 )/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
    
    def res_m10_wkt(self,mcode):
        x1d = float(mcode[2:4])
        y1d = float(mcode[0:2])
        x2d = float(mcode[5])
        y2d = float(mcode[4])
        x3d = float(mcode[7])
        y3d = float(mcode[6])
        x10p = float(mcode[9])
        y10p = float(mcode[8])
        
        x10p_arr = np.repeat(x10p,5) + [0,0,1,1,0]
        y10p_arr = np.repeat(y10p,5) + [0,1,1,0,0]

        laln_arr = np.core.defchararray.add((x1d + x2d/8 + x3d/80 + x10p_arr/800 +100).astype(np.str),np.repeat(" ",5))
        laln_arr = np.core.defchararray.add(laln_arr,((y1d + y2d/8+ y3d/80 + y10p_arr/80 )/1.5).astype(np.str))
        
        return "POLYGON(( " + ",".join(laln_arr) + "))"
               
        