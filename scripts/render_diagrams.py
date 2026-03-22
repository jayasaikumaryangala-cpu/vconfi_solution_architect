#!/usr/bin/env python3
"""
VConfi Diagram Renderer — Converts Mermaid diagrams in markdown to PNG images

Usage:
    python render_diagrams.py <input.md> [--output-dir <dir>]
    
This script:
1. Extracts all Mermaid diagram blocks from markdown
2. Renders each to PNG using mermaid-cli (mmdc)
3. Replaces mermaid blocks with image references
4. Outputs a new markdown file with embedded images
"""

import sys
import os
import re
import subprocess
import argparse
import tempfile
import hashlib
from pathlib import Path


def extract_mermaid_diagrams(md_content):
    """Extract all mermaid code blocks from markdown."""
    # Pattern to match ```mermaid ... ``` blocks
    pattern = r'```mermaid\n(.*?)```'
    matches = re.findall(pattern, md_content, re.DOTALL)
    return matches


def generate_diagram_id(diagram_content):
    """Generate a unique ID for a diagram based on its content."""
    return hashlib.md5(diagram_content.encode()).hexdigest()[:8]


def render_diagram_to_png(diagram_content, output_path, width=1200, height=800):
    """Render a mermaid diagram to PNG using mermaid-cli."""
    # Create temporary file for mermaid source
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(diagram_content)
        temp_mmd = f.name
    
    try:
        # Run mermaid-cli
        cmd = [
            'mmdc',
            '-i', temp_mmd,
            '-o', output_path,
            '-w', str(width),
            '-h', str(height),
            '-b', 'white'  # White background
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error rendering diagram: {result.stderr}")
            return False
        
        return True
        
    finally:
        # Clean up temp file
        os.unlink(temp_mmd)


def process_markdown_file(input_path, output_dir=None, inline=True):
    """
    Process a markdown file:
    1. Extract mermaid diagrams
    2. Render each to PNG
    3. Replace with image references
    
    Args:
        input_path: Path to input markdown file
        output_dir: Directory for output PNGs (default: same as input)
        inline: If True, embed base64 images; if False, use file references
    
    Returns:
        Modified markdown content
    """
    if output_dir is None:
        output_dir = os.path.dirname(input_path) or '.'
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    diagrams = extract_mermaid_diagrams(md_content)
    
    if not diagrams:
        print(f"No mermaid diagrams found in {input_path}")
        return md_content
    
    print(f"Found {len(diagrams)} diagram(s) in {input_path}")
    
    # Process each diagram
    modified_content = md_content
    diagram_map = {}
    
    for i, diagram in enumerate(diagrams, 1):
        diagram_id = generate_diagram_id(diagram)
        output_filename = f"diagram_{diagram_id}.png"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"  Rendering diagram {i}/{len(diagrams)}... ", end='')
        
        if render_diagram_to_png(diagram, output_path):
            print(f"✓ {output_filename}")
            diagram_map[diagram] = output_path
        else:
            print(f"✗ Failed")
    
    # Replace mermaid blocks with image references
    for diagram, png_path in diagram_map.items():
        if inline:
            # Convert to base64 for embedding
            import base64
            with open(png_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            img_tag = f'<img src="data:image/png;base64,{img_data}" alt="Diagram" style="max-width:100%;" />'
        else:
            # Use relative path
            rel_path = os.path.basename(png_path)
            img_tag = f'![Diagram]({rel_path})'
        
        # Replace the mermaid block
        old_block = f'```mermaid\n{diagram}```'
        modified_content = modified_content.replace(old_block, img_tag)
    
    return modified_content


def main():
    parser = argparse.ArgumentParser(
        description='Render Mermaid diagrams in markdown to PNG images'
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('--output-dir', '-o', help='Output directory for PNGs')
    parser.add_argument('--output', '-O', help='Output markdown file (default: overwrite input)')
    parser.add_argument('--external', '-e', action='store_true', 
                        help='Use external image files instead of embedding')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    
    # Determine output directory
    output_dir = args.output_dir
    if output_dir is None:
        output_dir = os.path.dirname(args.input) or '.'
    
    # Process file
    modified_content = process_markdown_file(
        args.input, 
        output_dir=output_dir,
        inline=not args.external
    )
    
    # Write output
    output_path = args.output or args.input
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"\nOutput written to: {output_path}")
    print(f"Diagrams saved to: {output_dir}")


if __name__ == '__main__':
    main()
