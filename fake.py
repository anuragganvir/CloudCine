from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template_string
import boto3
from werkzeug.utils import secure_filename 
import os
import time
from botocore.exceptions import NoCredentialsError
from botocore.config import Config
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS S3 Credentials
ACCESS_KEY = ''                    # specify the aws access key here
SECRET_KEY = ''                    # specify the aws secret access key here
BUCKET_NAME = ''                   # specify the aws bucket name here
region = ''                        # specify the aws bucket region here


s3_client = boto3.client(
    's3',
    region_name = region,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version='s3v4')
)


# Set the path for the uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Upload to S3
            s3_client.upload_file(
                os.path.join(app.config['UPLOAD_FOLDER'], filename),
                BUCKET_NAME,
                filename
            )

            time.sleep(2)
            return jsonify({'message': 'Upload successful', 'filename': filename})
    else:
        # This is what will be displayed for GET requests
        return render_template('upload.html')


@app.route('/videos', methods=['GET'])
def videos():
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    videos = [video['Key'] for video in response.get('Contents', []) if video['Key'].endswith('.mp4')]
    # print(videos)
    # videos_html = ''.join(f'<li>{video} <a href="/view/{video}">View</a> | <a href="/delete/{video}">Delete</a> | <a href="/edit/{video}">Edit</a></li>' for video in videos)
    return render_template('videos.html',videos=videos)

@app.route('/view/<filename>', methods=['GET'])
def view_video(filename):
    try:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': filename}, ExpiresIn=3600)
    except Exception as e:
        return str(e)
    return render_template_string('<video src="{{ url }}" controls></video>', url=url)

@app.route('/delete/<filename>', methods=['GET'])
def delete_video(filename):
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return f"Video {filename} has been deleted."
    except Exception as e:
        return str(e)


@app.route('/edit/<filename>', methods=['GET'])
def edit_video(filename):
    try:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': filename}, ExpiresIn=3600)
    except Exception as e:
        return str(e)
    return render_template('edit.html', url=url)  # render the edit.html template

@app.route('/save/<filename>', methods=['POST'])
def save_video(filename):
    try:
        # Get the start and end times from the request data
        data = request.get_json()
        start_time = float(data['start'])
        end_time = float(data['end'])
        trim_time = float(data['trim'])
        rotate_degrees = int(data.get('rotate', 0))
        mute = data.get('mute', False)
        filter_name = data.get('filter')  # filter is optional

        # Download the video from S3
        s3_client.download_file(BUCKET_NAME, filename, filename)

        # Cut the video using moviepy
        clip = mp.VideoFileClip(filename).subclip(start_time, end_time)

        # Rotate the video if requested
        if rotate_degrees:
            clip = clip.rotate(rotate_degrees)

        # Mute the video if requested
        if mute:
            clip = clip.without_audio()

        # Apply a filter to the video if requested
        if filter_name == 'colorx':
            clip = clip.fx(vfx.colorx, 1.3)
        elif filter_name == 'mirror':
            clip = clip.fx(vfx.mirror_x)

        # Save the cut video locally
        output_filename = 'output_' + secure_filename(filename)
        clip.write_videofile(os.path.join(app.config['UPLOAD_FOLDER'], output_filename))

        # Upload the cut video to S3
        s3_client.upload_file(
            os.path.join(app.config['UPLOAD_FOLDER'], output_filename),
            BUCKET_NAME,
            output_filename
        )

        # Delete the local video files
        os.remove(filename)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], output_filename))

        return jsonify({'message': 'Video processed and uploaded to S3 successfully', 'filename': output_filename})
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
