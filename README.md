# MarkConvert - Online Markdown Editor

Online Tool zum Konvertieren von Dokumentformaten in Markdown und umgekehrt.

## 🚀 Sofort loslegen

**Keine Installation erforderlich!** Starten Sie MarkConvert mit einem einzigen Befehl:

```bash
uvx markconvert
```

Das war's! Der Editor öffnet sich automatisch in Ihrem Browser und läuft lokal auf `http://127.0.0.1:5000`

### Voraussetzungen

- Python 3.10 oder höher
- [uv](https://docs.astral.sh/uv/) installiert (oder nutzen Sie `uvx` direkt - es lädt alles automatisch)

### System-Abhängigkeiten installieren

**Für PDF-Export (WeasyPrint) benötigt:**

**macOS:**
```bash
# Pango und Cairo via Homebrew installieren
brew install pango
```

**Linux (Ubuntu/Debian):**
```bash
# WeasyPrint System-Bibliotheken installieren
sudo apt-get install python3-dev libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install pango gdk-pixbuf2 libffi-devel
```

**Windows:**
```bash
# GTK3 Runtime installieren von:
# https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
```

### Installation von uv (falls noch nicht vorhanden)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## ✨ Features

### 📂 Dokument-Import mit Docling
Importieren Sie verschiedenste Dokumentformate und konvertieren Sie diese automatisch zu Markdown:
- **PDF-Dateien**: Inklusive Layout-Erkennung und Textextraktion
- **Word-Dokumente**: DOCX und DOC
- **PowerPoint**: PPTX-Präsentationen
- **HTML-Dateien**: Webseiten und HTML-Dokumente
- **Text-Dateien**: TXT und MD

**Powered by [Docling](https://github.com/DS4SD/docling)** - Hochmoderne Dokumentenverarbeitung

### 📝 Markdown Editor mit Live-Vorschau
- Schreiben Sie Markdown-Text im Editor (linke Seite)
- Sehen Sie die formatierte Vorschau in Echtzeit (rechte Seite)
- Vollständige GitHub Flavored Markdown (GFM) Unterstützung
- Syntax-Highlighting für Code-Blöcke

### 💾 Zuverlässiger Export
Exportieren Sie Ihre Markdown-Dokumente in verschiedene Formate:
- **Markdown (.md)**: Reiner Markdown-Text
- **Microsoft Word (.docx)**: Professionelle Word-Dokumente mit voller Unicode-Unterstützung
- **PDF**: Perfekt formatierte PDFs mit Emoji-Unterstützung
- **Rich Text Format (.rtf)**: Für maximale Kompatibilität

**Alle Exporte mit vollständiger Emoji- und Unicode-Unterstützung!** 🎉

### 🎨 Benutzeroberfläche
- Moderne, intuitive Oberfläche
- Drag & Drop für Datei-Upload
- Responsive Design für Desktop und Mobile
- Echtzeit-Statusmeldungen

## 📖 Verwendungsbeispiele

### Markdown-Syntax

```markdown
# Überschrift 1
## Überschrift 2
### Überschrift 3

**Fetter Text** und *kursiver Text*

- Listenelement 1
- Listenelement 2
- Listenelement 3

1. Nummerierte Liste
2. Element zwei
3. Element drei

[Link](https://example.com)

![Bild](bild-url.jpg)

> Zitat oder wichtiger Hinweis

` ``python
def beispiel():
    print("Code-Block mit Syntax-Highlighting")
` ``

| Spalte 1 | Spalte 2 |
|----------|----------|
| Wert 1   | Wert 2   |
```

## 🎯 Anwendungsfälle

- **Notizen erstellen**: Schnelle und formatierte Notizen
- **Blog-Artikel schreiben**: Markdown ist perfekt für Blog-Posts
- **Dokumentation**: Technische Dokumentationen erstellen
- **Berichte**: Professionelle Berichte in verschiedenen Formaten
- **README-Dateien**: Für GitHub, GitLab und andere Plattformen
- **PDF-Konvertierung**: PDFs in bearbeitbares Markdown umwandeln
- **Präsentationen extrahieren**: Text aus PowerPoint-Folien extrahieren

## 🔒 Datenschutz

- **100% lokal**: Alle Daten bleiben auf Ihrem Computer
- **Kein Cloud-Upload**: Keine Datenübertragung an externe Server
- **Offline-fähig**: Läuft komplett lokal ohne Internet (nach Installation)
- **Open Source**: Quellcode ist öffentlich einsehbar

## 💡 Tipps & Tricks

1. **Schnellstart**: `uvx markconvert` startet die App sofort ohne Installation
2. **Drag & Drop**: Ziehen Sie Dateien direkt in den Upload-Bereich
3. **Batch-Konvertierung**: Konvertieren Sie mehrere Dokumente nacheinander
4. **Format-Erhaltung**: Überschriften, Listen und Formatierungen bleiben erhalten

## 🛠️ Technische Details

### Backend (Python)
- **Flask**: Webserver-Framework
- **Docling**: Dokumentenkonvertierung (PDF, DOCX, PPTX, HTML → Markdown)
- **python-docx**: DOCX-Export
- **WeasyPrint**: PDF-Generierung mit vollständiger Unicode-Unterstützung
- **markdown**: HTML-Rendering für Vorschau

### Frontend
- **Marked.js**: Markdown-Parsing und Live-Vorschau
- **Vanilla JavaScript**: Keine schweren Frameworks
- **Responsive CSS**: Funktioniert auf allen Geräten

### Architektur
```
MarkConvert/
├── src/markconvert/
│   ├── __main__.py          # Entry Point
│   ├── app.py               # Flask Web Application
│   ├── converter.py         # Import/Export Logik
│   └── templates/
│       └── index.html       # Web UI
├── pyproject.toml           # Python Projekt-Konfiguration
└── README.md                # Diese Datei
```

## 📋 Systemanforderungen

- **Python**: Version 3.10 oder höher
- **Betriebssystem**: Windows, macOS, oder Linux
- **Browser**: Moderner Webbrowser (Chrome, Firefox, Safari, Edge)
- **RAM**: Mindestens 2GB (4GB empfohlen für große PDFs)

## 🚀 Entwicklung

### Lokale Installation für Entwickler

```bash
# Repository klonen
git clone https://github.com/wittmannaaron/MarkConvert.git
cd MarkConvert

# Mit uv installieren
uv pip install -e .

# Starten
python -m markconvert
```

### Tests ausführen

```bash
# Tests ausführen (wenn vorhanden)
pytest
```

## 🐛 Fehlerbehebung

### "uvx: command not found"
Installieren Sie uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### WeasyPrint Import-Fehler / "cannot load library 'libgobject-2.0-0'"
**Problem**: Die Anwendung startet nicht und zeigt einen Fehler mit WeasyPrint oder libgobject.

**Lösung**: System-Bibliotheken für PDF-Export installieren:

**macOS:**
```bash
brew install pango
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0
```

**Windows:**
- GTK3 Runtime installieren von: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

### "Port 5000 already in use"
Ein anderer Prozess nutzt bereits Port 5000. Beenden Sie diesen oder ändern Sie den Port in `src/markconvert/__main__.py`.

### Import-Fehler bei PDFs
Stellen Sie sicher, dass die PDF-Datei nicht verschlüsselt oder beschädigt ist.

## 📞 Support & Feedback

Für Fehlerberichte oder Feature-Anfragen öffnen Sie bitte ein Issue im Repository:
https://github.com/wittmannaaron/MarkConvert/issues

## 📄 Lizenz

Dieses Projekt ist Open Source und kann frei verwendet werden.

## 🙏 Danksagungen

- [Docling](https://github.com/DS4SD/docling) für exzellente Dokumentenkonvertierung
- [WeasyPrint](https://weasyprint.org/) für zuverlässige PDF-Generierung
- [Flask](https://flask.palletsprojects.com/) für das schlanke Web-Framework

---

**Viel Spaß beim Schreiben mit MarkConvert!** 🎉
