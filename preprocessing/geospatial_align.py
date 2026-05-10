import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

def align_images(source_path, target_path, output_path):
    """
    Aligns the source image to the target image's CRS, transform, and dimensions.
    """
    with rasterio.open(target_path) as target:
        target_crs = target.crs
        target_transform = target.transform
        target_width = target.width
        target_height = target.height
        
        with rasterio.open(source_path) as src:
            transform, width, height = calculate_default_transform(
                src.crs, target_crs, src.width, src.height, *src.bounds)
            
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': target_crs,
                'transform': target_transform,
                'width': target_width,
                'height': target_height
            })

            with rasterio.open(output_path, 'w', **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=target_transform,
                        dst_crs=target_crs,
                        resampling=Resampling.nearest)
    
    print(f"Aligned image saved to {output_path}")

if __name__ == "__main__":
    # Example usage (placeholders)
    # align_images('path/to/2020_image.tif', 'path/to/2025_image.tif', 'path/to/2020_aligned.tif')
    pass
