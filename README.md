
# CloudCine - Coud video streaming platform

CloudCine is a powerful video streaming platform that allows users to upload, stream, and edit videos seamlessly. Whether you’re a content creator, filmmaker, or just someone who loves sharing videos, CloudCine has got you covered.



## 📱Features

1 Video Upload and Storage :
 - Users can upload their videos to the platform.
 - AWS S3 buckets are used for secure and scalable video storage.
 
2 Video Streaming :
 - Stream videos directly from CloudCine.
 - Adaptive streaming for different resolutions and network conditions.

3 Video Editing :
 - CloudCine integrates video editing capabilities:

    - Cut: Trim unwanted parts of a video.
    - Split: Divide a video into segments.
    - Rotate: Adjust the video orientation.
    - Filter: Apply filters for creative effects.

4 User-Friendly Interface 
 - Intuitive UI for seamless navigation.
 - Clear instructions for video editing tools.


## 🤖Tech Stack

**Frontend:** HTML, CSS,

**Backend:**  Python, Flask

**Video Processing:** MoviePy

**AWS Integration:** Boto3

**File Handling:** Werkzeug


## 📲Installation

### Prerequisites

- Python 3.7 or higher
- AWS Account with S3 bucket setup
- AWS CLI configured with access keys

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/anuragganvir/CloudCine.git
   cd CloudCine

2. **Set Up AWS Credentials:**  
   ```bash
    AWS_ACCESS_KEY = 'your-access-key'
    AWS_SECRET_KEY = 'your-secret-key'
    S3_BUCKET_NAME = 'your-s3-bucket-name'

3. **Running the App:**
 *Run the Flask app:* 
 ```bash
 python app.py
```
 *Access the app in your browser:* http://localhost:5000

## 📩Feedback

If you have any feedback, please reach out to us at anuragganvir2019@gmail.com

