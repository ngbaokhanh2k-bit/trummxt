#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FREE FIRE BOT - BACKEND API (CHO RENDER)
"""

import asyncio
import json
import sys
import os
import traceback
import threading
import queue
from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS

# Import các file của bạn
try:
    from accessbanGUESTID import CompleteBot as GuestBot
    from accessbanFACEBOOK import CompleteBot as FBBot
    from accessbanGOOGLE import CompleteBot as GoogleBot
except ImportError as e:
    print(f"⚠️ Lỗi import: {e}")
    # Tạo class giả nếu chưa có file
    class GuestBot:
        async def run(self): return False
        async def cleanup(self): pass
    class FBBot:
        async def run(self): return False
        async def cleanup(self): pass
    class GoogleBot:
        async def run(self): return False
        async def cleanup(self): pass

app = Flask(__name__, static_folder='.')
CORS(app)

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Trang chủ"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>🔥 Free Fire Bot</title></head>
    <body style="font-family:Arial;text-align:center;padding:50px;background:#0a0a0a;color:#fff;">
        <h1 style="color:#ff4500;">🔥 Free Fire Bot</h1>
        <p>API đang chạy!</p>
        <p>Gửi POST tới <code>/run</code> để chạy bot</p>
        <hr>
        <p style="color:#666;font-size:12px;">Made with ❤️</p>
    </body>
    </html>
    '''

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Phục vụ file tĩnh"""
    return send_from_directory('.', filename)

@app.route('/run', methods=['POST', 'OPTIONS'])
def run_bot():
    """API chạy bot"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        mode = data.get('mode', 'token')
        
        def generate():
            log_queue = queue.Queue()
            
            def send_log(message, type='info'):
                log_queue.put(json.dumps({"message": message, "type": type}) + '\n')
            
            def run_async_bot():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    send_log('🚀 Đang khởi chạy bot...', 'info')
                    
                    if mode == 'token':
                        token = data.get('token')
                        openid = data.get('openid')
                        
                        if not token:
                            send_log('❌ Thiếu Access Token!', 'error')
                            return
                            
                        send_log(f'🔑 Token: {token[:20]}...', 'info')
                        
                        # Thử lấy open_id từ token
                        if not openid:
                            import requests
                            try:
                                resp = requests.get(
                                    f'https://100067.connect.garena.com/oauth/token/inspect?token={token}',
                                    timeout=10,
                                    verify=False
                                )
                                if resp.status_code == 200:
                                    data_resp = resp.json()
                                    openid = data_resp.get('open_id')
                                    if openid:
                                        send_log(f'✅ Lấy được Open ID: {openid[:16]}...', 'success')
                            except Exception as e:
                                send_log(f'⚠️ Không lấy được Open ID: {e}', 'warning')
                        
                        if not openid:
                            send_log('❌ Không có Open ID! Vui lòng nhập thủ công', 'error')
                            return
                            
                        bot = GuestBot(access_token=token, open_id=openid)
                        
                    else:  # guest mode
                        uid = data.get('uid')
                        password = data.get('password')
                        platform = data.get('platform', 'guest')
                        
                        if not uid or not password:
                            send_log('❌ Thiếu UID hoặc Password!', 'error')
                            return
                            
                        send_log(f'👤 Guest Login ({platform})', 'info')
                        send_log(f'   UID: {uid}', 'info')
                        
                        if platform == 'facebook':
                            bot = FBBot(uid=uid, password=password)
                        elif platform == 'google':
                            bot = GoogleBot(uid=uid, password=password)
                        else:
                            bot = GuestBot(uid=uid, password=password)
                    
                    # Override print
                    import builtins
                    original_print = builtins.print
                    
                    def custom_print(*args, **kwargs):
                        msg = ' '.join(str(a) for a in args)
                        send_log(msg, 'info')
                        original_print(*args, **kwargs)
                    
                    builtins.print = custom_print
                    
                    try:
                        result = loop.run_until_complete(bot.run())
                        if result:
                            send_log('✅✅✅ BOT CHẠY THÀNH CÔNG!', 'success')
                        else:
                            send_log('❌ Bot chạy thất bại!', 'error')
                    finally:
                        builtins.print = original_print
                        loop.run_until_complete(bot.cleanup())
                        
                except Exception as e:
                    send_log(f'❌ Lỗi: {str(e)}', 'error')
                    send_log(traceback.format_exc(), 'error')
                finally:
                    send_log('🏁 Bot đã dừng', 'info')
                    log_queue.put(None)
            
            # Chạy bot trong thread
            thread = threading.Thread(target=run_async_bot)
            thread.daemon = True
            thread.start()
            
            # Stream log
            while True:
                try:
                    log = log_queue.get(timeout=2)
                    if log is None:
                        break
                    yield log
                except queue.Empty:
                    yield json.dumps({"message": "⏳ Đang chạy...", "type": "info"}) + '\n'
                    continue
                    
        return Response(generate(), mimetype='text/plain', headers={
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-cache'
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "version": "3.0"})

# ============================================
# CHẠY
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("="*60)
    print("🔥 FREE FIRE BOT - BACKEND API")
    print("="*60)
    print(f"📌 Port: {port}")
    print("="*60)
    app.run(host='0.0.0.0', port=port, debug=False)