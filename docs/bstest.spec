# -*- mode: python -*-
a = Analysis(['C:\\Users\\wen\\Documents\\GitHub\\alarm_test\\bs2.py'],
             pathex=['C:\\tool\\Python2.7\\PyInstaller-2.1\\alarm_test'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='bstest.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , version='C:\\Users\\wen\\Documents\\GitHub\\alarm_test\\docs\\file_version_info.txt', icon='C:\\Users\\wen\\Documents\\GitHub\\alarm_test\\icons\\logo.ico')
