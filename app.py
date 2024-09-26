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




@app.route('/update_p5js')
def update_p5js():
    try:
        # 1. Copy content from index.html to p5js.html
        source_html = 'downloadFOLDER/sketch_001/index.html'
        dest_html = 'templates/p5js.html'
        shutil.copy2(source_html, dest_html)

        # 2. Copy JS files from sketch_001 to static/js/
        source_js_dir = 'downloadFOLDER/sketch_001'
        dest_js_dir = 'static/js'
        for file in os.listdir(source_js_dir):
            if file.endswith('.js'):
                shutil.copy2(os.path.join(source_js_dir, file), dest_js_dir)

        # 3. Copy CSS files from sketch_001 to static/css/
        source_css_dir = 'downloadFOLDER/sketch_001'
        dest_css_dir = 'static/css'
        for file in os.listdir(source_css_dir):
            if file.endswith('.css'):
                shutil.copy2(os.path.join(source_css_dir, file), dest_css_dir)


        p5js_html_path = os.path.join(app.root_path, 'templates', 'p5js.html')
        
        # Read the content of p5js.html
        with open(p5js_html_path, 'r') as file:
            content = file.read()
        
        # Modify the script src
        modified_content = content.replace(
            '<script src="mySketch.js',
            '<script src="../static/js/mySketch.js'
        )
        
        # Write the modified content back to p5js.html
        with open(p5js_html_path, 'w') as file:
            file.write(modified_content)

        return jsonify({"message": "P5.js files updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update P5.js files: {str(e)}"}), 500

@app.route('/p5js')
def render_p5js():
    try:
        return render_template('p5js.html')
    except Exception as e:
        app.logger.error(f"Error rendering p5js.html: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route('/load_p5js')
def load_p5js():
    try:
        return redirect('/p5js')
    except Exception as e:
        app.logger.error(f"Error redirecting to p5js: {str(e)}")
        return f"An error occurred: {str(e)}", 500





if __name__ == '__main__':
    app.run(debug=True)
