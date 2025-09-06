from flask import Flask, request, jsonify, render_template, session
from marketplace_ai import MarketplaceAI
import os
from dotenv import load_dotenv
import uuid


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

try:
    marketplace_ai = MarketplaceAI()
    print("✅ Marketplace AI initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing Marketplace AI: {str(e)}")
    marketplace_ai = None

@app.route('/')
def index():
    """Serve the main chat interface"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests from the frontend"""
    if not marketplace_ai:
        return jsonify({
            "success": False,
            "error": "AI system not initialized. Please check your API key configuration."
        }), 500
    
    try:
        data = request.json
        user_query = data.get('message', '').strip()
        images = data.get('images', [])
        
        # Get user ID from session
        user_id = session.get('user_id', 'default')
        
        # Validate input
        if not user_query and not images:
            return jsonify({
                "success": False,
                "error": "Please enter a message or upload images"
            }), 400
        
        
        print(f"User {user_id}: {user_query}")
        if images:
            print(f"Images uploaded: {len(images)}")
        
        
        context = {}
        if images:
            context['images'] = images
            context['has_images'] = True
        
        response = marketplace_ai.run(user_query, user_id, context)
        
        return jsonify({
            "success": True,
            "response": response.content,
            "type": "ai_response",
            "needs_images": response.needs_images
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error in chat endpoint: {error_msg}")
        
        return jsonify({
            "success": False,
            "error": f"An error occurred: {error_msg}"
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history for current user"""
    try:
        user_id = session.get('user_id', 'default')
        marketplace_ai.clear_history(user_id)
        
        return jsonify({
            "success": True,
            "message": "Conversation history cleared"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "ai_initialized": marketplace_ai is not None,
        "timestamp": "2025-09-06"
    })

if __name__ == '__main__':
    print("🚀 Starting Dynamic Marketplace AI Assistant...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
