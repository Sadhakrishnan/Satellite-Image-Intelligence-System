import rasterio
from rasterio.windows import Window
import os

def tile_image(image_path, output_dir, tile_size=512):
    """
    Tiles a large satellite image into smaller square patches.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with rasterio.open(image_path) as src:
        width = src.width
        height = src.height
        
        for i in range(0, width, tile_size):
            for j in range(0, height, tile_size):
                w = min(tile_size, width - i)
                h = min(tile_size, height - j)
                
                window = Window(i, j, w, h)
                transform = src.window_transform(window)
                
                kwargs = src.meta.copy()
                kwargs.update({
                    'driver': 'GTiff',
                    'height': h,
                    'width': w,
                    'transform': transform
                })
                
                tile_path = os.path.join(output_dir, f"tile_{i}_{j}.tif")
                with rasterio.open(tile_path, 'w', **kwargs) as dst:
                    dst.write(src.read(window=window))
                    
    print(f"Tiling complete. Tiles saved to {output_dir}")

if __name__ == "__main__":
    # Example usage
    # tile_image('large_image.tif', 'output_tiles')
    pass
