from flask import Flask, redirect, render_template, send_from_directory, url_for, jsonify
import os
import shutil
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_scraper', methods=['POST'])
def run_scraper():
    try:
        # Run the openprocessing_scraper.py script and capture its output
        result = subprocess.run(['python', 'openprocessing_scraper.py'], 
                                check=True, 
                                capture_output=True, 
                                text=True)
        
        # Extract the sketch_id from the output
        output_lines = result.stdout.split('\n')
        sketch_id = None
        for line in output_lines:
            if line.startswith("Processed sketch:"):
                sketch_id = line.split(":")[1].strip()
                break
        
        if sketch_id:
            return jsonify({"message": "Scraper completed successfully", "sketch_id": sketch_id}), 200
        else:
            return jsonify({"error": "Scraper completed but sketch_id not found"}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Scraper failed with error: {str(e)}"}), 500

@app.route('/downloadFOLDER/<path:filename>')
def serve_download_folder(filename):
    return send_from_directory('downloadFOLDER', filename)

if __name__ == '__main__':
    app.run(debug=True)
