# MarkConvert Beispiele

Dieses Verzeichnis enthält Beispielskripte für verschiedene Anwendungsfälle von MarkConvert.

## VLM (Vision Language Model) Beispiele

### vlm_example.py

Dieses Skript demonstriert die Verwendung der SmolDocling-256M VLM-Pipeline für erweiterte Dokumentenverarbeitung.

**Verwendung:**

```bash
# Navigiere zum Projektverzeichnis
cd MarkConvert

# Installiere MarkConvert (falls noch nicht geschehen)
uv pip install -e .

# Führe das Beispielskript aus
python examples/vlm_example.py
```

**Das Beispiel zeigt:**

1. **Automatische Backend-Erkennung**: System erkennt automatisch das beste Backend (MLX für macOS, Transformers für Linux/Windows)
2. **Manuelle MLX-Auswahl**: Explizite Verwendung des MLX-Backends (nur macOS)
3. **Manuelle Transformers-Auswahl**: Explizite Verwendung des Transformers-Backends (universal)
4. **Standard-Pipeline**: Verwendung ohne VLM (schneller, aber weniger genau)
5. **Batch-Konvertierung**: Mehrere PDFs nacheinander konvertieren

**Voraussetzungen für VLM:**

- **macOS (MLX Backend)**:
  - Apple Silicon Mac (M1/M2/M3/M4)
  - macOS 12.3 oder höher

- **Linux/Windows (Transformers Backend)**:
  - Python 3.10+
  - Optional: CUDA-fähige GPU für bessere Performance
  - CPU-Modus funktioniert auch, ist aber langsamer

**Systemanforderungen:**

- **RAM**: Mindestens 2GB frei (4GB empfohlen)
- **VRAM** (bei GPU-Nutzung): Unter 500MB
- **Festplatte**: Zusätzlich ~1GB für Modell-Download beim ersten Start

## Weitere Beispiele

Weitere Beispiele werden in Zukunft hinzugefügt. Vorschläge und Beiträge sind willkommen!

## Support

Bei Fragen oder Problemen öffne bitte ein Issue im Repository:
https://github.com/wittmannaaron/MarkConvert/issues
