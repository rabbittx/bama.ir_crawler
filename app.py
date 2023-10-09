from flask import Flask, render_template, request, jsonify
from panel import panel 
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # ایجاد صفحه‌ای ساده که در آن دکمه‌هایی برای اسکن سریع و عمیق وجود داشته باشد

@app.route('/fast_scan', methods=['POST'])
def fast_scan_route():
    try:
        pages = int(request.form.get('pages', 100))  # Default to 100 if not provided
        crawler_panel.do_fast_scan(crawler_panel.BA_MA_URL, pages)
        return jsonify({"success": True, "message": "Fast scan completed successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/deep_scan', methods=['POST'])
def deep_scan_route():
    try:
        pages = int(request.form.get('pages', 50))  # Default to 50 if not provided
        crawler_panel.do_deep_scan(crawler_panel.BA_MA_URL, pages)
        return jsonify({"success": True, "message": "Deep scan completed successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
if __name__ == '__main__':
    crawler_panel = panel(fast_scan_scroll=100, deep_scan_scroll=50)
    app.run(debug=True)