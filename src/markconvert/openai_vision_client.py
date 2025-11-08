"""OpenAI GPT-5 client for document and image processing with Responses API."""

import base64
import os
from pathlib import Path
from typing import Union

from openai import OpenAI


class OpenAIVisionClient:
    """Client for interacting with OpenAI GPT-5 Responses API."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-5-nano"
    ):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: GPT-5 model to use ("gpt-5-nano" or "gpt-5-mini")
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def _encode_image(self, image_path: Union[str, Path]) -> tuple[str, str]:
        """
        Encode image to base64.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (base64_string, mime_type)
        """
        image_path = Path(image_path)

        # Determine MIME type
        suffix = image_path.suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(suffix, 'image/jpeg')

        with open(image_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')

        return b64, mime_type

    def classify_image_content(self, image_path: Union[str, Path]) -> str:
        """
        Classify if image contains document/table/chart or photo/artwork.

        Args:
            image_path: Path to image

        Returns:
            "document" or "photo"
        """
        b64, mime_type = self._encode_image(image_path)

        prompt = """Analysiere dieses Bild und klassifiziere es in eine der beiden Kategorien:

1. "document" - wenn es enthält:
   - Textdokumente (Briefe, Formulare, Verträge, etc.)
   - Tabellen oder Spreadsheets
   - Diagramme, Grafiken oder Statistiken
   - Technische Diagramme
   - Screenshots mit Text

2. "photo" - wenn es enthält:
   - Fotografien von Menschen, Orten oder Objekten
   - Kunstwerke oder Illustrationen
   - Natürliche Szenen
   - Bilder ohne signifikanten Textinhalt

Antworte mit NUR EINEM WORT: entweder "document" oder "photo"."""

        resp = self.client.responses.create(
            model=self.model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{b64}",
                        "detail": "high"
                    }
                ]
            }]
        )

        result = resp.output_text.strip().lower()
        if "document" in result:
            return "document"
        elif "photo" in result:
            return "photo"
        else:
            return "document"  # Default

    def transcribe_document(self, image_path: Union[str, Path]) -> str:
        """
        Transcribe document image to Markdown.

        Args:
            image_path: Path to document image

        Returns:
            Markdown transcription
        """
        b64, mime_type = self._encode_image(image_path)

        prompt = """Transkribiere dieses Dokumentenbild zu Markdown-Format.

Anforderungen:
- Extrahiere ALLEN Text mit 100% Genauigkeit
- Bewahre die Dokumentstruktur mit Markdown-Formatierung
- Verwende ## für Hauptüberschriften, ### für Unterüberschriften
- Konvertiere Tabellen in Markdown-Tabellenformat
- Verwende **fett** und *kursiv* wo angemessen
- Bewahre Aufzählungen und nummerierte Listen
- Füge allen Text wortwörtlich ein - nicht zusammenfassen oder paraphrasieren
- Wenn Text unklar ist, füge [unklar] Markierung ein
- Gib die Transkription in gültigem Markdown-Format aus
- Der Text ist in Deutsch

WICHTIG: Gib NUR das Markdown aus, keine zusätzlichen Erklärungen oder Kommentare."""

        resp = self.client.responses.create(
            model=self.model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{b64}",
                        "detail": "high"
                    }
                ]
            }]
        )

        return resp.output_text.strip()

    def describe_image(self, image_path: Union[str, Path]) -> str:
        """
        Generate detailed description of photo/image.

        Args:
            image_path: Path to image

        Returns:
            Markdown description
        """
        b64, mime_type = self._encode_image(image_path)

        prompt = """Beschreibe dieses Bild detailliert.

Füge ein:
- Hauptmotive und ihre Eigenschaften
- Umgebung und Setting
- Farben, Beleuchtung und Stimmung
- Komposition und bemerkenswerte Elemente
- Sichtbare Texte oder Symbole

Gib eine klare, strukturierte Beschreibung in Markdown-Format."""

        resp = self.client.responses.create(
            model=self.model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{b64}",
                        "detail": "high"
                    }
                ]
            }]
        )

        return resp.output_text.strip()

    def process_pdf(self, pdf_path: Union[str, Path]) -> str:
        """
        Process entire PDF document to Markdown.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown transcription
        """
        pdf_path = Path(pdf_path)

        with open(pdf_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')

        prompt = """Transkribiere dieses PDF-Dokument zu Markdown-Format.

Anforderungen:
- Extrahiere ALLEN Text mit 100% Genauigkeit
- Bewahre die Dokumentstruktur mit Markdown-Formatierung
- Verwende ## für Hauptüberschriften, ### für Unterüberschriften
- Konvertiere Tabellen in Markdown-Tabellenformat
- Verwende **fett** und *kursiv** wo angemessen
- Bewahre Aufzählungen und nummerierte Listen
- Füge allen Text wortwörtlich ein - nicht zusammenfassen oder paraphrasieren
- Wenn mehrere Seiten: Füge "---" zwischen Seiten ein
- Wenn Text unklar ist, füge [unklar] Markierung ein
- Der Text ist in Deutsch

WICHTIG: Gib NUR das Markdown aus, keine zusätzlichen Erklärungen oder Kommentare."""

        resp = self.client.responses.create(
            model=self.model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_file",
                        "file_data": f"data:application/pdf;base64,{b64}",
                        "filename": pdf_path.name
                    }
                ]
            }]
        )

        return resp.output_text.strip()

    def process_image_to_markdown(self, image_path: Union[str, Path]) -> str:
        """
        Process image to Markdown using two-step approach:
        1. Classify content type
        2. Either transcribe document or describe photo

        Args:
            image_path: Path to image

        Returns:
            Markdown output
        """
        # Step 1: Classify
        content_type = self.classify_image_content(image_path)

        # Step 2: Process based on classification
        if content_type == "document":
            return self.transcribe_document(image_path)
        else:
            # Wrap description in Markdown format
            description = self.describe_image(image_path)
            return f"# Bildbeschreibung\n\n{description}"
