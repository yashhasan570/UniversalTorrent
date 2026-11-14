#!/usr/bin/env python3
"""Reapply the Universal Torrent rebrand after an upstream sync."""
from pathlib import Path
import re, shutil, os

SKIP_DIRS = {'.git'}

def sweep():
    pre = [
        ('org.qbittorrent.qBittorrent', 'org.universaltorrent.UniversalTorrent'),
        ('qBitTorrentDocument', 'universaltorrent_document'),
        ('qBitTorrentIncompleteData', 'universaltorrent_incompletedata'),
    ]
    pairs = [
        ('qBittorrent', 'Universal Torrent'),
        ('qbittorrent', 'universaltorrent'),
        ('QBITTORRENT', 'UNIVERSALTORRENT'),
        ('qBitTorrent', 'Universal Torrent'),
        ('qbittorrent-new', 'universaltorrent-new'),
        ('qBIttorrent', 'Universal Torrent'),
    ]
    binary_ext = {'.png','.jpg','.jpeg','.gif','.ico','.icns','.zip','.asc'}
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and d != '.github']
        for f in files:
            p = Path(root) / f
            if p.name in ('migrate.py', 'README.md') or p.suffix.lower() in binary_ext: continue
            try: t = p.read_text(encoding='utf-8')
            except Exception: continue
            orig = t
            for old, new in pre + pairs:
                t = t.replace(old, new)
            if t != orig: p.write_text(t)

def fixes():
    pu = Path('src/gui/programupdater.cpp')
    if pu.exists():
        s = pu.read_text()
        s = s.replace('https://www.universaltorrent.org/versions.json', 'https://github.com/yashhasan570/UniversalTorrent/releases/download/sync/versions.json')
        s = s.replace('https://universaltorrent.github.io/Universal Torrent-website/versions.json', 'https://github.com/yashhasan570/UniversalTorrent/releases/download/sync/versions.json')
        s = s.replace('https://www.universaltorrent.org/download', 'https://github.com/yashhasan570/UniversalTorrent/releases')
        s = s.replace('https://universaltorrent.github.io/Universal Torrent-website/download', 'https://github.com/yashhasan570/UniversalTorrent/releases')
        pu.write_text(s)
    ad = Path('src/gui/aboutdialog.cpp')
    if ad.exists():
        s = ad.read_text()
        s = s.replace('https://www.universaltorrent.org', 'https://github.com/yashhasan570/UniversalTorrent')
        s = s.replace('https://forum.universaltorrent.org', 'https://t.me/johnconstantine570')
        s = s.replace('https://bugs.universaltorrent.org', 'https://t.me/johnconstantine570')
        ad.write_text(s)
    sh = Path('src/app/signalhandler.cpp')
    if sh.exists():
        s = sh.read_text()
        s = s.replace('https://bug.universaltorrent.org', 'https://t.me/johnconstantine570')
        s = s.replace('Please file a bug report at https://t.me/johnconstantine570 and provide the following information', 'Please report this at https://t.me/johnconstantine570 and provide the following information')
        sh.write_text(s)
    for mf in ['dist/unix/org.universaltorrent.UniversalTorrent.metainfo.xml', 'dist/unix/org.universaltorrent.UniversalTorrent-nox.metainfo.xml']:
        p = Path(mf)
        if p.exists():
            s = p.read_text()
            s = re.sub(r'\s*<url type="donation">[^<]*</url>', '', s)
            s = s.replace('https://www.universaltorrent.org/', 'https://github.com/yashhasan570/UniversalTorrent/')
            s = s.replace('https://bugs.universaltorrent.org/', 'https://github.com/yashhasan570/UniversalTorrent/')
            s = s.replace('https://forum.universaltorrent.org/', 'https://t.me/johnconstantine570')
            s = s.replace('https://wiki.universaltorrent.org/Frequently-Asked-Questions', 'https://t.me/johnconstantine570')
            p.write_text(s)
    dsk = Path('dist/unix/org.universaltorrent.UniversalTorrent.desktop')
    if dsk.exists():
        s = dsk.read_text()
        s = s.replace('universaltorrent.org', 'github.com/yashhasan570/UniversalTorrent')
        dsk.write_text(s)
    mwui = Path('src/gui/mainwindow.ui')
    if mwui.exists():
        s = mwui.read_text()
        s = s.replace('    <addaction name="actionDonateMoney"/>\n', '')
        s = re.sub(r'  <action name="actionDonateMoney">[\s\S]*?</action>\n', '', s)
        mwui.write_text(s)
    mwh = Path('src/gui/mainwindow.h')
    if mwh.exists():
        s = mwh.read_text()
        s = s.replace('    void on_actionDonateMoney_triggered();\n', '')
        mwh.write_text(s)
    mwc = Path('src/gui/mainwindow.cpp')
    if mwc.exists():
        s = mwc.read_text()
        s = re.sub(r'    m_ui->actionDonateMoney->setIcon\([^;]*\);\n', '', s)
        s = re.sub(r'void MainWindow::on_actionDonateMoney_triggered\(\)\n\{\n[\s\S]*?\n\}\n\n', '', s)
        mwc.write_text(s)
    dc = Path('dist/unix/CMakeLists.txt')
    if dc.exists():
        s = dc.read_text()
        s = re.sub(r'set\(manPageLanguages\n    en\n    ru\n\)\n\nforeach\(manPageLanguage \$\{manPageLanguages\}\)\n    install\(FILES \$\{PROJECT_SOURCE_DIR\}/doc/[\s\S]*?endforeach\(\)\n\n', '', s)
        dc.write_text(s)

def renames():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and d != '.github']
        for f in list(files):
            if 'qbittorrent' in f or 'qBittorrent' in f or 'qBitTorrent' in f:
                p = Path(root) / f
                nf = f.replace('qBittorrent', 'UniversalTorrent').replace('qBitTorrent', 'UniversalTorrent').replace('qbittorrent', 'universaltorrent')
                p.rename(p.parent / nf)

def cleanup():
    for item in ['AGENTS.md','CODING_GUIDELINES.md','CONTRIBUTING.md','SECURITY.md','Changelog','INSTALL','WebAPI_Changelog.md',
                 'codingStyleQtCreator.xml','build_dist.sh','examples','doc','5B7CC9A2.asc']:
        p = Path(item)
        if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
        elif p.exists(): p.unlink()

def readme():
    Path('README.md').write_text("""# Universal Torrent

Free BitTorrent client for desktop with torrent search, RSS feeds, sequential downloading, and a built-in Web UI for remote control.

Built on open-source code under GPL-2.0+.

## Build

```
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

## Contact

Telegram: [@johnconstantine570](https://t.me/johnconstantine570)
""")

if __name__ == '__main__':
    sweep(); fixes(); renames(); cleanup(); readme()
    print('rebrand reapplied')
