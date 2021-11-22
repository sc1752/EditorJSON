# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['EdtiorJSON.py'],
             pathex=['D:\\sandbox\\EditorJSON'],
             binaries=[],
             datas=[('icon\\btn_addchild.png', 'icon'), ('icon\\btn_collaspe.png', 'icon'), 
             ('icon\\btn_compact.png', 'icon'), ('icon\\btn_delete.png', 'icon'), ('icon\\btn_edit.png', 'icon'), 
             ('icon\\btn_expand.png', 'icon'), ('icon\\btn_formatted.png', 'icon'), ('icon\\btn_insert.png', 'icon'),
             ('icon\\btn_json.png', 'icon'), ('icon\\btn_redo.png', 'icon'), ('icon\\btn_treeview.png', 'icon'),
             ('icon\\btn_undo.png', 'icon'), ('icon\\btn_validate.png', 'icon')],
             hiddenimports=[],
             hookspath=[],
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
          name='EdtiorJSON',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
