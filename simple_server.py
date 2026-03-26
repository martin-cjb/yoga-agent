#!/usr/bin/env python3
"""
瑜伽馆智能客服 - 轻量版
直接用 Python 实现，无需 Java/Maven
"""

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# 瑜伽馆知识库
KNOWLEDGE = {
    "address": "北京市朝阳区建国路88号SOHO现代城A座501室",
    "phone": "010-12345678",
    "hours": "营业时间：周一至周五 9:00-21:00，周六日 8:00-22:00",
    "courses": {
        "哈他瑜伽": {"price": "单次120元", "duration": "60分钟"},
        "流瑜伽": {"price": "单次150元", "duration": "75分钟"},
        "阴瑜伽": {"price": "单次130元", "duration": "60分钟"},
        "高温瑜伽": {"price": "单次180元", "duration": "90分钟"},
        "私教": {"price": "单次400元", "duration": "60分钟"},
    },
    "packages": {
        "10次卡": "1000元（有效期3个月）",
        "20次卡": "1800元（有效期6个月）",
        "30次卡": "2500元（有效期1年）",
        "年卡": "8800元（不限次数）",
    },
    "intro": "我们是一家专业瑜伽馆，成立于2015年，拥有8年教学经验。主打哈他瑜伽、流瑜伽、阴瑜伽、高温瑜伽等课程。"
}

def match_intent(message):
    """简单意图识别"""
    msg = message.lower()
    
    # 地址
    if any(w in msg for w in ["地址", "在哪", "位置", "怎么走"]):
        return "address"
    
    # 电话
    if any(w in msg for w in ["电话", "联系方式", "手机", "微信"]):
        return "phone"
    
    # 营业时间
    if any(w in msg for w in ["营业", "开门", "关门", "几点"]):
        return "hours"
    
    # 价格/收费
    if any(w in msg for w in ["价格", "收费", "多少钱", "费用", "便宜", "优惠"]):
        return "price"
    
    # 课程
    if any(w in msg for w in ["课程", "有什么课", "瑜伽类型", "上课"]):
        return "courses"
    
    # 预约
    if any(w in msg for w in ["预约", "报名", "上课", "预订", "约"]):
        return "book"
    
    # 介绍
    if any(w in msg for w in ["介绍", "你们是", "怎么样", "简介"]):
        return "intro"
    
    return "unknown"

def generate_response(message):
    """生成回复"""
    intent = match_intent(message)
    
    if intent == "address":
        return f"📍 我们位于：{KNOWLEDGE['address']}，欢迎来访~"
    
    elif intent == "phone":
        return f"📞 联系电话：{KNOWLEDGE['phone']}（微信同号）"
    
    elif intent == "hours":
        return f"🕐 {KNOWLEDGE['hours']}"
    
    elif intent == "price":
        response = "💰 课程价格：\n"
        for course, info in KNOWLEDGE["courses"].items():
            response += f"  • {course}: {info['price']}/{info['duration']}\n"
        response += "\n📦 套餐优惠：\n"
        for pkg, price in KNOWLEDGE["packages"].items():
            response += f"  • {pkg}: {price}\n"
        return response
    
    elif intent == "courses":
        response = "🧘 我们的课程：\n"
        for course, info in KNOWLEDGE["courses"].items():
            response += f"  • {course}: {info['price']} ({info['duration']})\n"
        return response
    
    elif intent == "book":
        return "📅 预约课程请告诉我：\n1. 想上的课程\n2. 预约日期和时间\n3. 您的联系方式\n我会帮您登记~"
    
    elif intent == "intro":
        return f"🏠 {KNOWLEDGE['intro']}"
    
    else:
        return "您好！我是瑜伽馆智能客服，请问有什么可以帮您？\n可以问我：价格、地址、课程、预约等~"

@app.route("/api/chat", methods=["POST"])
def chat():
    """聊天接口"""
    data = request.json
    message = data.get("message", "")
    
    response = generate_response(message)
    
    return jsonify({
        "code": 0,
        "message": response,
        "data": {
            "reply": response
        }
    })

@app.route("/api/chat/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def index():
    """主页 - 简单的 Web 界面"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🧘 瑜伽馆智能客服</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 600px;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 24px; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .chat-box {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .message {
            margin-bottom: 15px;
            max-width: 80%;
        }
        .message.bot {
            margin-right: auto;
        }
        .message.user {
            margin-left: auto;
            text-align: right;
        }
        .message .bubble {
            display: inline-block;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.5;
            white-space: pre-wrap;
        }
        .message.bot .bubble {
            background: white;
            color: #333;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .message.user .bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid #eee;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-area input:focus {
            border-color: #667eea;
        }
        .input-area button {
            padding: 14px 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .input-area button:hover {
            transform: scale(1.05);
        }
        .quick-replys {
            padding: 0 20px 15px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .quick-reply {
            padding: 8px 16px;
            background: #f0f0f0;
            border: none;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .quick-reply:hover {
            background: #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧘 瑜伽馆智能客服</h1>
            <p>专业瑜伽指导，预约咨询</p>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot">
                <div class="bubble">您好！欢迎光临瑜伽馆~ 🧘

有什么可以帮您？您可以问我：

• 课程价格
• 课程安排
• 预约上课
• 门店地址
• 联系方式</div>
            </div>
        </div>
        <div class="quick-replys">
            <button class="quick-reply" onclick="send('课程怎么收费？')">💰 课程价格</button>
            <button class="quick-reply" onclick="send('你们在哪？')">📍 门店地址</button>
            <button class="quick-reply" onclick="send('我想预约瑜伽课')">📅 预约课程</button>
            <button class="quick-reply" onclick="send('有什么课程？')">🧘 课程介绍</button>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="请输入您的问题..." onkeypress="if(event.key==='Enter')sendMessage()">
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>
    
    <script>
        function send(msg) {
            document.getElementById('userInput').value = msg;
            sendMessage();
        }
        
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;
            
            // 显示用户消息
            addMessage(message, 'user');
            input.value = '';
            
            // 调用 API
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message})
            })
            .then(r => r.json())
            .then(data => {
                addMessage(data.message || data.data.reply, 'bot');
            })
            .catch(err => {
                addMessage('抱歉，出了点问题，请稍后重试~', 'bot');
            });
        }
        
        function addMessage(text, type) {
            const box = document.getElementById('chatBox');
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.innerHTML = '<div class="bubble">' + text + '</div>';
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }
    </script>
</body>
</html>
    '''

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"🧘 启动瑜伽馆客服 on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)