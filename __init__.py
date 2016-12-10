# -*- coding: utf-8 -*-

#===================================
#標準地域メッシュコードインポートプラグイン
#
#===================================

def classFactory(iface):
    from .main import main
    return main(iface) 