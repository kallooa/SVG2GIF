from PIL import Image
import argparse
from pathlib import Path

def crop_gif(input_path, output_path, left, top, right, bottom):
    """
    Crop a GIF file while maintaining animation.
    
    Args:
        input_path (str): Path to input GIF file
        output_path (str): Path to save cropped GIF
        left (int): Left coordinate of crop box
        top (int): Top coordinate of crop box
        right (int): Right coordinate of crop box
        bottom (int): Bottom coordinate of crop box
    """
    try:
        # Open the GIF file
        with Image.open(input_path) as img:
            # Get basic info about the animation
            duration = img.info.get('duration', 100)  # Default to 100ms if not specified
            loop = img.info.get('loop', 0)  # 0 means infinite loop
            
            # Extract all frames
            frames = []
            try:
                while True:
                    # Copy the current frame
                    current = img.copy()
                    
                    # Crop the frame
                    cropped_frame = current.crop((left, top, right, bottom))
                    
                    # Convert to RGBA if needed (to preserve transparency)
                    if cropped_frame.mode not in ['RGBA', 'P']:
                        cropped_frame = cropped_frame.convert('RGBA')
                    
                    frames.append(cropped_frame)
                    
                    # Move to next frame
                    img.seek(img.tell() + 1)
                    
            except EOFError:
                # We've reached the end of the frames
                pass
            
            # Save the cropped animation
            if frames:
                frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=duration,
                    loop=loop,
                    optimize=True
                )
                print(f"Successfully saved cropped GIF to {output_path}")
            else:
                raise ValueError("No frames were extracted from the GIF")
                
    except Exception as e:
        print(f"Error processing GIF: {str(e)}")
        raise

def validate_dimensions(left, top, right, bottom):
    """Validate crop dimensions"""
    if left >= right:
        raise ValueError("Left coordinate must be less than right coordinate")
    if top >= bottom:
        raise ValueError("Top coordinate must be less than bottom coordinate")
    if any(x < 0 for x in [left, top, right, bottom]):
        raise ValueError("Coordinates cannot be negative")

def main():
    parser = argparse.ArgumentParser(description='Crop a GIF file')
    parser.add_argument('input', help='Input GIF file path')
    parser.add_argument('output', help='Output GIF file path')
    parser.add_argument('--left', type=int, required=True, help='Left coordinate')
    parser.add_argument('--top', type=int, required=True, help='Top coordinate')
    parser.add_argument('--right', type=int, required=True, help='Right coordinate')
    parser.add_argument('--bottom', type=int, required=True, help='Bottom coordinate')
    
    args = parser.parse_args()
    
    try:
        # Validate input file
        if not Path(args.input).exists():
            raise FileNotFoundError(f"Input file not found: {args.input}")
        
        # Validate dimensions
        validate_dimensions(args.left, args.top, args.right, args.bottom)
        
        # Crop the GIF
        crop_gif(args.input, args.output, args.left, args.top, args.right, args.bottom)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())