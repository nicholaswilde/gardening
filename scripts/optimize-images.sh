#!/bin/bash
# scripts/optimize-images.sh

total_orig=0
total_new=0

# 1. Process JPEGs (Photos): Convert to WebP for maximum space savings
for file in docs/assets/images/*.jpg; do
  [ -f "$file" ] || continue
  output="${file%.jpg}.webp"
  
  orig_size=$(stat -c%s "$file")
  echo "Converting photo: $(basename "$file")..."
  
  cwebp -q 80 "$file" -o "$output"
  
  if [ $? -eq 0 ] && [ -f "$output" ]; then
    new_size=$(stat -c%s "$output")
    total_orig=$((total_orig + orig_size))
    total_new=$((total_new + new_size))
    rm "$file"
  fi
done

# 2. Process PNGs (Graphics): Optimize in-place to keep compatibility
for file in docs/assets/images/*.png; do
  [ -f "$file" ] || continue
  
  orig_size=$(stat -c%s "$file")
  echo "Optimizing graphic: $(basename "$file")..."
  
  oxipng -o 4 --strip all "$file"
  
  new_size=$(stat -c%s "$file")
  total_orig=$((total_orig + orig_size))
  total_new=$((total_new + new_size))
done

if [ "$total_orig" -gt 0 ]; then
  savings=$((100 - (total_new * 100 / total_orig)))
  echo "---------------------------------"
  echo "Optimization Complete."
  echo "Total Space Savings: ${savings}%"
fi
