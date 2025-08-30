import ffmpeg
import os

target_size_kb=int(input("Enter size in kb: "))
input_file=input("Enter input file name: ") or 'input.jpg'
output_file=input("Enter output file name: ") or 'output.jpg'

video_ext=['mp4', 'mkv', 'avi']
image_ext=['jpg', 'png', 'jpeg']

input_ext = input_file[input_file.find('.')+1:]
output_ext = output_file[output_file.find('.')+1:]

width = 1500
quality = 5

#def compress():
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
    
format_map = {
    "mp4": "mp4",
    "mkv": "matroska",
    "avi": "avi"
}

def convert():
    # video to audio 
    if input_ext in video_ext and output_ext == 'mp3':
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='mp3', acodec='libmp3lame', q=2) 
            .run(overwrite_output=True)
        )
    # mkv to mp4 or vice-versa
    if input_ext in video_ext and output_ext in video_ext:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format= format_map[output_ext], vcodec="copy", acodec="copy") 
            .run(overwrite_output=True)
        )
    # jpg to png
    if input_ext in image_ext and output_ext in image_ext:
            (
                ffmpeg
                .input(input_file)
                .output(output_file,qscale=2) 
                .run(overwrite_output=True)
            )   
        
convert()