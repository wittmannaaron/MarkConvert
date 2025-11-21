"""Ollama client for vision and text processing."""

import base64
import json
from pathlib import Path
from typing import Optional, Union, List
import requests


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "gemma3:27b",
        vision_model: Optional[str] = None
    ):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama server URL
            model: Default model for text processing
            vision_model: Model for vision tasks (defaults to qwen2.5vl:32b if available)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.vision_model = vision_model or "qwen2.5vl:32b"

    def _encode_image(self, image_path: Union[str, Path]) -> str:
        """Encode image to base64."""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: float = 0.1
    ) -> str:
        """
        Generate text response from Ollama.

        Args:
            prompt: User prompt
            model: Model to use (defaults to self.model)
            system: System prompt
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Generated text
        """
        model = model or self.model

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        if system:
            payload["system"] = system

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        result = response.json()
        return result.get("response", "")

    def analyze_image(
        self,
        image_path: Union[str, Path],
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: float = 0.1
    ) -> str:
        """
        Analyze image with vision model.

        Args:
            image_path: Path to image file
            prompt: Analysis prompt
            model: Vision model to use (defaults to self.vision_model)
            system: System prompt
            temperature: Sampling temperature

        Returns:
            Analysis result
        """
        model = model or self.vision_model

        # Encode image
        image_b64 = self._encode_image(image_path)

        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        if system:
            payload["system"] = system

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        result = response.json()
        return result.get("response", "")

    def classify_image_content(self, image_path: Union[str, Path]) -> str:
        """
        Classify if image contains document/table/chart or photo/artwork.

        Args:
            image_path: Path to image

        Returns:
            "document" or "photo"
        """
        prompt = """Analyze this image and classify it into one of two categories:

1. "document" - if it contains:
   - Text documents (letters, forms, contracts, etc.)
   - Tables or spreadsheets
   - Charts, graphs, or statistics
   - Technical diagrams
   - Screenshots with text

2. "photo" - if it contains:
   - Photographs of people, places, or objects
   - Artwork or illustrations
   - Natural scenes
   - Images without significant text content

Respond with ONLY ONE WORD: either "document" or "photo"."""

        result = self.analyze_image(
            image_path,
            prompt=prompt,
            temperature=0.0  # Deterministic for classification
        )

        # Extract classification from response
        result_lower = result.strip().lower()
        if "document" in result_lower:
            return "document"
        elif "photo" in result_lower:
            return "photo"
        else:
            # Default to document if unclear
            return "document"

    def transcribe_document(self, image_path: Union[str, Path]) -> str:
        """
        Transcribe document image to Markdown.

        Args:
            image_path: Path to document image

        Returns:
            Markdown transcription
        """
        system_prompt = """You are an expert document transcription assistant. Your task is to:
1. Extract ALL text from the document image with 100% accuracy
2. Preserve the document structure using Markdown formatting
3. Maintain original formatting (headings, lists, tables, emphasis)
4. Keep all numbers, dates, and special characters exactly as shown
5. Preserve line breaks and paragraph structure"""

        user_prompt = """Transcribe this document image to Markdown format.

Requirements:
- Use ## for main headings, ### for subheadings
- Convert tables to Markdown table format
- Use **bold** and *italic* where appropriate
- Preserve bullet points and numbered lists
- Include all text verbatim - do not summarize or paraphrase
- If text is unclear, include [unclear] marker

Output the transcription in valid Markdown format."""

        return self.analyze_image(
            image_path,
            prompt=user_prompt,
            system=system_prompt,
            temperature=0.1  # Low temperature for accurate transcription
        )

    def describe_image(self, image_path: Union[str, Path]) -> str:
        """
        Generate detailed description of photo/image.

        Args:
            image_path: Path to image

        Returns:
            Markdown description
        """
        system_prompt = """You are an expert image analyst. Your task is to provide detailed, accurate descriptions of images."""

        user_prompt = """Describe this image in detail.

Include:
- Main subjects and their characteristics
- Setting and environment
- Colors, lighting, and mood
- Composition and notable elements
- Any text or symbols visible

Provide a clear, structured description in Markdown format."""

        return self.analyze_image(
            image_path,
            prompt=user_prompt,
            system=system_prompt,
            temperature=0.3  # Slightly higher for creative descriptions
        )

    def _remove_markdown_code_blocks(self, text: str) -> str:
        """
        Remove markdown code block wrappers if present.
        LLMs often wrap their output in ```markdown ... ``` blocks.
        This function aggressively removes all code block markers.

        Args:
            text: Text potentially wrapped in code blocks

        Returns:
            Cleaned text without code block wrappers
        """
        import re

        text = text.strip()

        # Remove code block wrappers at start and end
        if text.startswith('```markdown'):
            text = text[len('```markdown'):].lstrip('\n')
        elif text.startswith('```'):
            first_newline = text.find('\n')
            if first_newline != -1:
                text = text[first_newline + 1:].lstrip('\n')

        if text.endswith('```'):
            text = text[:-3].rstrip('\n')

        # Remove all standalone ``` lines (code block markers)
        # This handles cases where LLM adds ``` in the middle
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()
            # Skip lines that are just code block markers
            if stripped == '```' or stripped == '```markdown':
                continue
            cleaned_lines.append(line)

        text = '\n'.join(cleaned_lines)

        return text.strip()

    def process_image_to_markdown(self, image_path: Union[str, Path]) -> str:
        """
        Process image to Markdown using two-step approach:
        1. Classify content type
        2. Either transcribe document or describe photo

        Args:
            image_path: Path to image

        Returns:
            Markdown output (cleaned of code block wrappers)
        """
        # Step 1: Classify
        content_type = self.classify_image_content(image_path)

        # Step 2: Process based on classification
        if content_type == "document":
            result = self.transcribe_document(image_path)
        else:
            # Wrap description in Markdown format
            description = self.describe_image(image_path)
            result = f"# Image Description\n\n{description}"

        # Step 3: Clean up code block wrappers
        return self._remove_markdown_code_blocks(result)
