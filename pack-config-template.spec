# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py',
'func\\CommonTools.py',
'func\\ExcelFunc.py',
'gui\\gui.py',
'venv\\Lib\\site-packages\\openpyxl\\__init__.py'
],
             pathex=['D:\\Projects\\Python\\lottery_game'],
             binaries=[],
             datas=[('assets', 'assets')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='菲姐点名器v1.0',
          debug=False,
          icon='./assets/icon128.ico',
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
