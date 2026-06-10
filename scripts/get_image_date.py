#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_date_taken(image_path):
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if exif:
                # 1. Check main EXIF tags
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ('DateTimeOriginal', 'DateTimeDigitized', 'DateTime'):
                        date_str = value.split()[0].replace(':', '-')
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            return date_str
                        except ValueError:
                            pass
                
                # 2. Check ExifIFD subgroup (0x8769)
                exif_ifd = exif.get_ifd(0x8769)
                if exif_ifd:
                    for tag_id, value in exif_ifd.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag in ('DateTimeOriginal', 'DateTimeDigitized', 'DateTime'):
                            date_str = value.split()[0].replace(':', '-')
                            try:
                                datetime.strptime(date_str, '%Y-%m-%d')
                                return date_str
                            except ValueError:
                                pass
    except Exception:
        pass
    
    # Fallback to file modification time
    try:
        mtime = os.path.getmtime(image_path)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except Exception:
        return datetime.now().strftime('%Y-%m-%d')

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/get_image_date.py <image_path>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} does not exist", file=sys.stderr)
        sys.exit(1)
        
    print(get_date_taken(image_path))

if __name__ == "__main__":
    main()
