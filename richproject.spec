# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\\\my_games\\\\richproject\\\\data_rich', './data_rich'), ('C:\\\\my_games\\\\richproject\\\\mysettings', './mysettings'), ('rich_project.ico', './')],
    hiddenimports=['PyQt5', 'PyQt5.QtTest', 'pandas', 'pyserial', 'requests', 'chardet'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='richproject',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['rich_project.ico','rich_project.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='richproject',
)
