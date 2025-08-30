import ffmpeg
import os

target_size_kb=int(input("Enter size in kb: "))
input_file=input("Enter input file name: ") or 'input.jpg'
output_file=input("Enter output file name: ") or 'output.jpg'

width = 1500
quality = 5

while True:
    (
        ffmpeg
        .input(input_file)
        .output(output_file, qscale=quality,
        vf=f"scale={width}:-1")
        .run(overwrite_output=True)
    )
    
    quality += 2
    width = int(width * 0.9)
    
    if os.path.getsize(input_file) <= target_size_kb:
        break
        
    if quality < 30 or width < 400:
        break
    
    #        .output(output_file, format='mp3', acodec='libmp3lame', q=2)