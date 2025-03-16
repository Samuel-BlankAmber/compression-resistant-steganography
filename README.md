# Compression Resistant Steganography

## Warning

This is not cryptographically secure.

## Usage

```python
py encode.py <width> <height> <message> <output_image> [colour_size]
```

```python
py decode.py <image_path>
```

## Example

```python
py encode.py 1584 396 "REDACTED" linkedin-banner.png 44
```

![LinkedIn Banner](linkedin-banner.png)

After compression, this may become:

![LinkedIn Banner Compressed](linkedin-banner-with-compression.jpg)

```python
py decode.py linkedin-banner.png
py decode.py linkedin-banner-with-compression.jpg
```

Both of these will output `REDACTED` despite the latter being lossy compressed.
