import cairosvg

# Define the SVG path for the logo based on the image
svg_code = """
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="95" stroke="black" stroke-width="5" fill="white" />
  <circle cx="100" cy="100" r="85" stroke="black" stroke-width="5" fill="white" />
  <path d="M 100,10 L 100,190 M 10,100 L 190,100" stroke="black" stroke-width="10" />
  <path d="M 100,10 L 100,50 L 50,50 L 50,100 L 10,100" stroke="black" stroke-width="10" fill="none" />
  <path d="M 100,10 L 100,50 L 150,50 L 150,100 L 190,100" stroke="black" stroke-width="10" fill="none" />
  <path d="M 100,190 L 100,150 L 50,150 L 50,100 L 10,100" stroke="black" stroke-width="10" fill="none" />
  <path d="M 100,190 L 100,150 L 150,150 L 150,100 L 190,100" stroke="black" stroke-width="10" fill="none" />
</svg>
"""

# Save the SVG code to a file
svg_file_path = r"D:\Docs\logo.svg"
with open(svg_file_path, "w") as svg_file:
    svg_file.write(svg_code)
