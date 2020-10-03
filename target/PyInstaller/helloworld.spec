# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/howardwang/Desktop/excel-application/src/main/python/main.py'],
             pathex=['/Users/howardwang/Desktop/excel-application/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Users/howardwang/Desktop/excel-application/myenv/lib/python3.6/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/Users/howardwang/Desktop/excel-application/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='helloworld',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/howardwang/Desktop/excel-application/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='helloworld')
app = BUNDLE(coll,
             name='helloworld.app',
             icon='/Users/howardwang/Desktop/excel-application/target/Icon.icns',
             bundle_identifier=None)
