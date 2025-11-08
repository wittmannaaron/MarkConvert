#!/usr/bin/env python3
"""Main entry point for MarkConvert application."""

import os
import sys
import platform
import webbrowser
from pathlib import Path
from threading import Timer


def setup_macos_libraries():
    """Set up library paths for macOS (required for WeasyPrint)."""
    if platform.system() == 'Darwin':  # macOS
        # Check if Homebrew is installed
        homebrew_paths = ['/opt/homebrew/lib', '/usr/local/lib']
        for lib_path in homebrew_paths:
            if Path(lib_path).exists():
                # Set DYLD_FALLBACK_LIBRARY_PATH for WeasyPrint
                current_path = os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')
                if lib_path not in current_path:
                    new_path = f"{lib_path}:{current_path}" if current_path else lib_path
                    os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = new_path
                break


# Set up macOS library paths before importing the app
setup_macos_libraries()

from markconvert.app import app


def open_browser():
    """Open the default browser to the application URL."""
    webbrowser.open('http://127.0.0.1:5000')


def main():
    """Start the MarkConvert web application."""
    print("=" * 60)
    print("  MarkConvert - Online Markdown Editor")
    print("=" * 60)
    print()
    print("  🚀 Server wird gestartet...")
    print("  📍 URL: http://127.0.0.1:5000")
    print()
    print("  💡 Tipps:")
    print("     - Der Browser öffnet sich automatisch")
    print("     - Drücken Sie Strg+C zum Beenden")
    print("     - Alle Daten bleiben auf Ihrem Computer")
    print()
    print("=" * 60)
    print()

    # Open browser after a short delay
    Timer(1.5, open_browser).start()

    # Start Flask application
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n✅ MarkConvert wurde beendet. Auf Wiedersehen!")
        sys.exit(0)


if __name__ == '__main__':
    main()
