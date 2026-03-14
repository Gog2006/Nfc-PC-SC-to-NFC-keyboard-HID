# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['convertor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'smartcard',
        'smartcard.System',
        'smartcard.Exceptions',
        'smartcard.CardMonitoring',
        'smartcard.CardType',
        'smartcard.CardRequest',
        'smartcard.util',
        'pyautogui',
        'pyperclip',
        'ctypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NFC-Reader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
