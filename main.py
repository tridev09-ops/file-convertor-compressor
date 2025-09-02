from flask import (
    Flask,
    request,
    Response,
    render_template,
    after_this_request,
    send_file,
    jsonify,
)
import ffmpeg, os, zipfile

app = Flask(__name__)

DOWNLOAD_FOLDER = "static/download"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/delete")
def delete():
    @after_this_request
    def remove_files(response):
        try:
            for filename in os.listdir(DOWNLOAD_FOLDER):
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)

        except Exception as e:
            app.logger.error("Error cleaning folder: %s", e)
        
        return response
    
    return jsonify("Files deleted successfully")


@app.route("/convert", methods=["POST"])
def convert():
    try:
        input_files = request.files.getlist("files")

        output_ext = request.form.get("ext")

        image_ext = ["jpg", "png", "jpeg"]
        video_ext = ["mp4", "mkv", "avi"]
        format_map = {"mp4": "mp4", "mkv": "matroska", "avi": "avi"}

        files_list = []

        for input_file in input_files:
            input_name = input_file.filename
            output_name = "convert-" + os.path.splitext(input_name)[0]+'.'+ output_ext

            input_ext = os.path.splitext(input_name)[1][1:]

            input_path = os.path.join(DOWNLOAD_FOLDER, input_name)
            output_path = os.path.join(DOWNLOAD_FOLDER, output_name)

            input_file.save(input_path)

            files_list.append(
                {
                    "input_path": input_path,
                    "output_path": output_path,
                    "output_name": output_name,
                    "input_ext": input_ext,
                    "output_ext": output_ext,
                }
            )

        for file in files_list:
            input_path = file["input_path"]
            output_path = file["output_path"]
            input_ext = file["input_ext"]
            output_ext = file["output_ext"]

            # video to audio
            if input_ext in video_ext and output_ext == "mp3":
                (
                    ffmpeg.input(input_path)
                    .output(output_path, format="mp3", acodec="libmp3lame", q=2)
                    .run(overwrite_output=True)
                )
            # mkv to mp4 or vice-versa
            elif input_ext in video_ext and output_ext in video_ext:
                (
                    ffmpeg.input(input_path)
                    .output(
                        output_path,
                        format=format_map[output_ext],
                        vcodec="copy",
                        acodec="copy",
                    )
                    .run(overwrite_output=True)
                )
            # jpg to png
            elif input_ext in image_ext and output_ext in image_ext:
                (
                    ffmpeg.input(input_path)
                    .output(output_path, qscale=20)
                    .run()
                )

        output_list=[]
        for file in files_list:
            output_list.append(file["output_path"])
        
        print(output_list)
        return jsonify(output_list)

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)})


@app.route("/compress", methods=["POST"])
def compress():
    try:
        input_files = request.files.getlist("files")
        
        image_ext = ["jpg", "png", "jpeg"]
        video_ext = ["mp4", "mkv", "avi"]

        files_list = []

        for input_file in input_files:
            input_name = input_file.filename
            output_name = "compress-" + input_name

            ext = os.path.splitext(input_name)[1][1:]

            input_path = os.path.join(DOWNLOAD_FOLDER, input_name)
            output_path = os.path.join(DOWNLOAD_FOLDER, output_name)

            input_file.save(input_path)

            files_list.append(
                {
                    "input_path": input_path,
                    "output_path": output_path,
                    "output_name": output_name,
                    "ext": ext,
                }
            )

        for file in files_list:
            input_path = file["input_path"]
            output_path = file["output_path"]
            ext = file["ext"]

            target_size = (
                int(request.form.get("size")) * 1024 if ext in image_ext else None
            )
            video_quality = request.form.get("quality") if ext in video_ext else None

            if ext in image_ext:
                width = 1500
                quality = 5

                while True:
                    (
                        ffmpeg.input(input_path)
                        .output(output_path, **{"q:v": quality}, vf=f"scale={width}:-1")
                        .run(overwrite_output=True)
                    )

                    quality += 2
                    width = int(width * 0.9)

                    if os.path.getsize(output_path) <= target_size:
                        print("...got the size....")
                        break

                    if quality > 30 or width < 400:
                        print("...can't compress more than this....")
                        break

            elif ext in video_ext:
                if video_quality == "high":
                    (
                        ffmpeg.input(input_path)
                        .output(
                            output_path,
                            vf="scale=720:-2",
                            crf=26,
                            preset="veryfast",
                            **{"c:a": "aac", "b:a": "128k"},
                        )
                        .run(overwrite_output=True)
                    )
                elif video_quality == "medium":
                    (
                        ffmpeg.input(input_path)
                        .output(
                            output_path,
                            vf="scale=480:-2",
                            crf=28,
                            preset="veryfast",
                            **{"c:a": "aac", "b:a": "96k"},
                        )
                        .run(overwrite_output=True)
                    )
                elif video_quality == "low":
                    (
                        ffmpeg.input(input_path)
                        .output(
                            output_path,
                            vf="scale=360:-2",
                            crf=30,
                            preset="veryfast",
                            **{"c:a": "aac", "b:a": "64k"},
                        )
                        .run(overwrite_output=True)
                    )

        output_list=[]
        for file in files_list:
            output_list.append(file["output_path"])
        
        print(output_list)
        return jsonify(output_list)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
