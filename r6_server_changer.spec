# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['r6_server_changer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'json'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Clean up unnecessary binaries to reduce false positives
excluded_binaries = [
    'vcruntime140.dll',  # Already on most systems
    'VCRUNTIME140_1.dll',
    'api-ms-win',  # Windows system DLLs
    'Qt5',
]

a.binaries = TOC([x for x in a.binaries if not any(excluded in x[0] for excluded in excluded_binaries)])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='R6SiegeServerChanger',
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
    icon='r6_icon.ico' if os.path.exists('r6_icon.ico') else None,
    # Version information
    version='1.0.0',
    file_version='1.0.0',
    product_version='1.0.0',
    file_description='Rainbow Six Siege Server Changer',
    product_name='R6 Server Changer',
    company_name='',
    uac_admin=False,
)