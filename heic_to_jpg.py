import argparse
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import pillow_heif
from tqdm import tqdm

# Register HEIF opener for Pillow
pillow_heif.register_heif_opener()

def convert_task(img_path, target_path, quality):
    """
    Core conversion logic. Using ThreadPool prevents WSL process overhead 
    and handles memory more efficiently than ProcessPool for image tasks.
    """
    try:
        with Image.open(img_path) as img:
            # Ensure the image is in RGB mode for JPEG compatibility
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(target_path, "JPEG", quality=quality, optimize=True)
        return True, None
    except Exception as e:
        return False, f"Failed {img_path.name}: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="High-performance HEIC to JPG batch converter for CLI."
    )
    parser.add_argument("-i", "--input", type=str, required=True, 
                        help="Path to input directory containing HEIC files.")
    parser.add_argument("-o", "--output", type=str, 
                        help="Path to output directory (default: 'converted' in input dir).")
    parser.add_argument("-q", "--quality", type=int, default=85, 
                        help="Output JPEG quality (1-100, default: 85).")
    parser.add_argument("-w", "--workers", type=int, default=4, 
                        help="Max concurrent threads (default: 4 for WSL stability).")

    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a valid directory.")
        sys.exit(1)

    output_dir = Path(args.output).resolve() if args.output else input_dir / "converted"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect HEIC files (case-insensitive extension check)
    files = [f for f in input_dir.iterdir() if f.suffix.lower() == ".heic"]
    
    if not files:
        print(f"Info: No HEIC files found in {input_dir}")
        return

    print(f"Processing {len(files)} files | Threads: {args.workers} | Quality: {args.quality}")

    errors = []
    # ThreadPoolExecutor is used to manage I/O and CPU without crashing WSL
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(convert_task, f, output_dir / f"{f.stem}.jpg", args.quality): f 
            for f in files
        }
        
        # Real-time progress bar tracking
        for future in tqdm(as_completed(futures), total=len(files), desc="Progress", unit="file"):
            success, error_msg = future.result()
            if not success:
                errors.append(error_msg)

    print(f"\nConversion finished.")
    print(f"Total processed: {len(files)}")
    print(f"Successful: {len(files) - len(errors)}")
    
    if errors:
        print(f"Failed: {len(errors)}")
        print("Error log (first 10 entries):")
        for err in errors[:10]:
            print(f"  - {err}")

if __name__ == "__main__":
    main()