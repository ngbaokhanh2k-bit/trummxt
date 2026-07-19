#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
FREE FIRE BOT - BACKEND API
============================================================
Chạy bot từ web interface
"""

import asyncio
import json
import sys
import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import traceback

# Import các file của bạn
from accessbanGUESTID import CompleteBot as GuestBot
from accessbanFACEBOOK import CompleteBot as FBBot
from accessbanGOOGLE import CompleteBot as GoogleBot

app = Flask(__name__)
CORS(app)  # Cho phép mọi domain gọi API


@app.route('/')
def index():
    """Trả về trang chủ"""
    return '''
    <h1>🔥 Free Fire Bot API</h1>
    <p>Đang chạy... Gửi POST tới /run để chạy bot</p>
    <p>Hoặc mở <a href="/static/index.html">index.html</a></p>
    '''


@app.route('/run', methods=['POST'])
def run_bot():
    """API chạy bot"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        mode = data.get('mode', 'token')
        
        def generate():
            """Generator để stream log ra client"""
            import queue
            import threading
            
            log_queue = queue.Queue()
            
            def send_log(message, type='info'):
                log_queue.put(json.dumps({"message": message, "type": type}) + '\n')
            
            def run_async_bot():
                try:
                    # Tạo event loop mới
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    if mode == 'token':
                        token = data.get('token')
                        openid = data.get('openid')
                        send_log(f'🔑 Đang chạy với Access Token: {token[:20]}...', 'info')
                        
                        if not openid:
                            send_log('⚠️ Không có Open ID, thử lấy từ token...', 'warning')
                            # Thử lấy open_id từ token
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
                            except:
                                pass
                        
                        if not openid:
                            send_log('❌ Không có Open ID!', 'error')
                            return
                            
                        bot = GuestBot(access_token=token, open_id=openid)
                        
                    else:  # guest mode
                        uid = data.get('uid')
                        password = data.get('password')
                        platform = data.get('platform', 'guest')
                        
                        send_log(f'👤 Đang chạy Guest Login ({platform})', 'info')
                        send_log(f'   UID: {uid}', 'info')
                        
                        if platform == 'facebook':
                            bot = FBBot(uid=uid, password=password)
                        elif platform == 'google':
                            bot = GoogleBot(uid=uid, password=password)
                        else:
                            bot = GuestBot(uid=uid, password=password)
                    
                    # Chạy bot
                    send_log('🚀 Đang kết nối...', 'info')
                    
                    # Override print để capture log
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
                    log_queue.put(None)  # Signal kết thúc
            
            # Chạy bot trong thread riêng
            thread = threading.Thread(target=run_async_bot)
            thread.daemon = True
            thread.start()
            
            # Stream log từ queue
            while True:
                try:
                    log = log_queue.get(timeout=1)
                    if log is None:
                        break
                    yield log
                except queue.Empty:
                    yield json.dumps({"message": "⏳ Đang chạy...", "type": "info"}) + '\n'
                    continue
                    
        return Response(generate(), mimetype='text/plain')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Kiểm tra sức khỏe"""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    print("="*60)
    print("🔥 FREE FIRE BOT - BACKEND SERVER")
    print("="*60)
    print("📌 Địa chỉ: http://localhost:5000")
    print("📌 Mở index.html để dùng giao diện")
    print("="*60)
    print("⚠️  Nhấn Ctrl+C để dừng")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)