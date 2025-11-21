#!/usr/bin/env python3
"""
Example: Using MarkConvert with VLM (Vision Language Model) Pipeline

This script demonstrates how to use the SmolDocling-256M vision language model
for enhanced PDF document processing with automatic backend detection.
"""

from markconvert.converter import MarkdownConverter
import sys


def example_auto_detection():
    """
    Example 1: Automatic backend detection
    The converter will automatically choose:
    - MLX backend on macOS (optimized for Apple Silicon)
    - Transformers backend on Linux/Windows
    """
    print("Example 1: Automatic VLM Backend Detection")
    print("-" * 50)

    # Initialize converter with VLM enabled
    converter = MarkdownConverter(use_vlm=True)

    # Convert a PDF document
    pdf_path = "sample_document.pdf"  # Replace with your PDF path

    try:
        markdown_text = converter.import_document(pdf_path)
        print(f"✓ Successfully converted {pdf_path}")
        print(f"Output length: {len(markdown_text)} characters")
        print("\nFirst 500 characters:")
        print(markdown_text[:500])
    except FileNotFoundError:
        print(f"✗ File not found: {pdf_path}")
        print("  Please replace 'sample_document.pdf' with a valid PDF path")
    except Exception as e:
        print(f"✗ Error during conversion: {e}")


def example_manual_mlx():
    """
    Example 2: Manually specify MLX backend (macOS only)
    This is useful for testing or when auto-detection doesn't work as expected.
    """
    print("\n\nExample 2: Manual MLX Backend (macOS only)")
    print("-" * 50)

    # Initialize converter with MLX backend
    converter = MarkdownConverter(use_vlm=True, vlm_backend='mlx')

    print("✓ Converter initialized with MLX backend")
    print("  This backend is optimized for Apple Silicon (M1/M2/M3/M4)")


def example_manual_transformers():
    """
    Example 3: Manually specify Transformers backend (universal)
    This backend works on all platforms (CPU/GPU).
    """
    print("\n\nExample 3: Manual Transformers Backend (Universal)")
    print("-" * 50)

    # Initialize converter with Transformers backend
    converter = MarkdownConverter(use_vlm=True, vlm_backend='transformers')

    print("✓ Converter initialized with Transformers backend")
    print("  This backend works on all platforms (CPU/GPU)")


def example_standard_pipeline():
    """
    Example 4: Standard pipeline (no VLM)
    This is the default behavior without VLM enhancements.
    """
    print("\n\nExample 4: Standard Pipeline (No VLM)")
    print("-" * 50)

    # Initialize converter without VLM
    converter = MarkdownConverter(use_vlm=False)

    print("✓ Converter initialized with standard pipeline")
    print("  This is the default, faster option without AI enhancements")


def example_batch_conversion():
    """
    Example 5: Batch convert multiple PDFs with VLM
    """
    print("\n\nExample 5: Batch Conversion with VLM")
    print("-" * 50)

    # Initialize once for better performance
    converter = MarkdownConverter(use_vlm=True)

    pdf_files = [
        "document1.pdf",
        "document2.pdf",
        "document3.pdf",
    ]

    for pdf_file in pdf_files:
        try:
            markdown_text = converter.import_document(pdf_file)

            # Save to markdown file
            output_file = pdf_file.replace('.pdf', '.md')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_text)

            print(f"✓ Converted {pdf_file} → {output_file}")
        except FileNotFoundError:
            print(f"✗ File not found: {pdf_file}")
        except Exception as e:
            print(f"✗ Error converting {pdf_file}: {e}")


def main():
    """Run all examples"""
    print("=" * 50)
    print("MarkConvert VLM Examples")
    print("=" * 50)

    # Run examples
    example_auto_detection()
    example_manual_mlx()
    example_manual_transformers()
    example_standard_pipeline()
    example_batch_conversion()

    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
