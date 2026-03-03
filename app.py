from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-url', methods=['POST'])
def get_url():
    data = request.json
    video_url = data.get('url')
    res = data.get('resolution')

    if not video_url:
        return jsonify({'success': False, 'error': 'Link dewa hoyni'})

    if res == 'best':
        format_str = 'best'
    else:
        format_str = f'best[height<={res}]'

    # এখানে কুকি ফাইলের লোকেশন সেট করা হয়েছে
    ydl_opts = {
        'format': format_str,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': 'cookies.txt' # YouTube কে বোকা বানানোর জন্য কুকি
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            return jsonify({'success': True, 'download_url': download_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Render-এর জন্য PORT ডায়নামিকভাবে নেওয়া ভালো
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
