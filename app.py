from flask import Flask, redirect, render_template, send_from_directory, url_for
import os
import shutil
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from flask import jsonify
import subprocess

@app.route('/run_scraper', methods=['POST'])
def run_scraper():
    try:
        # Run the openprocessing_scraper.py script
        subprocess.run(['python', 'openprocessing_scraper.py'], check=True)
        return jsonify({"message": "Scraper completed successfully"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Scraper failed with error: {str(e)}"}), 500



@app.route('/downloadFOLDER/<path:filename>')
def serve_download_folder(filename):
    return send_from_directory('downloadFOLDER', filename)

if __name__ == '__main__':
    app.run(debug=True)
