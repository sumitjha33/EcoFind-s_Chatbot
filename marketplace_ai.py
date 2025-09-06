from gemini_wrapper import GeminiWrapper
import json

class MarketplaceAI:
    def __init__(self):
        self.gemini = GeminiWrapper()
        self.user_sessions = {}

    def detect_intent(self, user_query: str, conversation_history: list) -> str:
        """Use LLM to intelligently detect user intent"""
        
        recent_context = ""
        if conversation_history:
            recent_messages = conversation_history[-3:]
            recent_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
        
        intent_prompt = f"""
Analyze this conversation and determine the user's primary intent:

**Recent Context:**
{recent_context}

**Current User Message:** "{user_query}"

**Intent Options:**
- SELL: User wants to sell an item 
- BUY: User wants to buy/find items 
- SAFETY: User asks about safety, policies
- APP_HELP: User needs help with app features
- GENERAL: General conversation

Respond with just one word: SELL, BUY, SAFETY, APP_HELP, or GENERAL
"""
        
        try:
            response = self.gemini.generate_response(intent_prompt)
            intent = response.strip().upper()
            
            valid_intents = ['SELL', 'BUY', 'SAFETY', 'APP_HELP', 'GENERAL']
            if intent in valid_intents:
                return intent
            else:
                # Fallback keyword detection
                query_lower = user_query.lower()
                if any(word in query_lower for word in ['sell', 'selling', 'list my']):
                    return 'SELL'
                elif any(word in query_lower for word in ['buy', 'find', 'search', 'looking for', 'budget', 'show me']):
                    return 'BUY'
                else:
                    return 'GENERAL'
        except:
            # Fallback keyword detection
            query_lower = user_query.lower()
            if any(word in query_lower for word in ['sell', 'selling', 'list my']):
                return 'SELL'
            elif any(word in query_lower for word in ['buy', 'find', 'search', 'looking for', 'budget', 'show me']):
                return 'BUY'
            else:
                return 'GENERAL'

    def search_products_online(self, item_type: str, requirements: str) -> str:
        """Universal product search for ANY item type"""
        
        search_prompt = f"""
You are a universal product search expert with access to current Indian market data (September 2025).

**Search Request:**
Item Type: {item_type}
Requirements: {requirements}

**Your Task:**
Provide 5-6 specific product recommendations with:
- Exact product names and brands
- Current market prices in INR
- Key specifications relevant to this item type
- Where to buy (Flipkart, Amazon, brand stores, local markets)
- Why each product fits the user's requirements
- Brief comparison between options

**Be Specific and Realistic:**
- Use current 2025 market prices
- Include various price ranges within their budget
- Mention both premium and budget options
- Consider Indian market availability

Respond with detailed product information that helps the user make an informed decision.
"""
        
        return self.gemini.generate_response(search_prompt)

    def run(self, user_query: str, user_id: str = "default", context: dict = None):
        # Get or create conversation history
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        
        conversation_history = self.user_sessions[user_id]
        
        # Detect intent
        intent = self.detect_intent(user_query, conversation_history)
        
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_query})
        
        # Route based on intent
        if intent == 'SELL':
            response = self.handle_selling(user_query, conversation_history, context)
        elif intent == 'BUY':
            response = self.handle_buying(user_query, conversation_history)
        elif intent == 'SAFETY':
            response = self.handle_safety(user_query)
        elif intent == 'APP_HELP':
            response = self.handle_app_help(user_query)
        else:
            response = self.handle_general(user_query)
        
        # Add AI response to history
        conversation_history.append({"role": "assistant", "content": response})
        
        # Update session
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        self.user_sessions[user_id] = conversation_history
        
        # Check if needs images
        needs_images = any(phrase in response.lower() for phrase in [
            'upload photo', 'upload image', 'take photo', 'share photo', 
            'send photo', 'show me photo', 'picture', 'pics', 'photograph',
            'take pictures', 'send pictures', 'share images', '📸'
        ])
        
        class Response:
            def __init__(self, content, needs_images=False):
                self.content = content
                self.needs_images = needs_images
        
        return Response(response, needs_images)

    def handle_selling(self, user_query: str, conversation_history: list, context: dict = None):
        """Handle selling-related queries - keep existing logic"""
        
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-10:]])
        
        image_context = ""
        if context and context.get("images"):
            image_count = len(context["images"])
            image_context = f"\n[User has uploaded {image_count} images of their item]"
        
        selling_prompt = f"""
You are a smart marketplace assistant helping someone sell their item.

**Your Smart Decision Making:**
1. **What item** they're selling (extract from conversation)
2. **What information** you already have vs what you still need
3. **When to request photos** (after getting basic details but before final pricing)
4. **When to provide final pricing** (when you have enough information)

**Information Collection:** Item type, brand, model, age, condition, defects, accessories, original price

**Photo Request Phase:** Request specific photos based on item type before final pricing

**Final Listing Phase:** Create complete listing with smart market pricing, multiple titles, detailed description

**Current Conversation:**
{history_text}{image_context}

**CRITICAL INSTRUCTIONS:**
1. **READ THE CONVERSATION** - Don't ask for information already provided
2. **BE DECISION-SMART** - Request photos when you have basic details, provide final pricing when ready
3. **PRICING INTELLIGENCE** - Research current market values for the specific item

**Latest User Message:** "{user_query}"

Respond helpfully as a selling expert!
"""
        
        return self.gemini.generate_response(selling_prompt)

    def handle_buying(self, user_query: str, conversation_history: list):
        """Universal buying handler - works for ANY product type"""
        
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-10:]])
        
        buying_prompt = f"""
You are a smart marketplace assistant helping someone find and buy ANY type of product.

**Your Universal Buying Intelligence:**

🎯 **ANALYZE THE CONVERSATION** to extract:
- What item/product they want to buy
- Budget mentioned 
- Requirements/specifications discussed
- Preferences mentioned

**UNIVERSAL QUESTIONING STRATEGY:**
Based on the product type, ask 4-5 KEY questions that will narrow down the search:

**For Electronics** (phones, laptops, TVs, etc.):
- Budget range, brand preferences, key features needed, usage purpose

**For Vehicles** (cars, bikes, etc.):
- Budget, fuel type, year range, brand preference, usage type

**For Furniture** (sofa, bed, table, etc.):
- Budget, size requirements, material preference, style, room type

**For Fashion** (clothes, shoes, etc.):
- Budget, size, brand preference, style, occasion type

**For Books**:
- Subject, level, condition preference, budget

**For Sports Equipment**:
- Sport type, skill level, budget, brand preference

**For Appliances** (AC, fridge, etc.):
- Budget, capacity/size needed, energy rating, brand preference

**SMART DECISION LOGIC:**
- If you have MINIMAL INFO: Ask 2-3 key questions
- If you have GOOD INFO: Ask 1-2 clarifying questions  
- If you have COMPREHENSIVE INFO: **PROVIDE 5-6 PRODUCT RECOMMENDATIONS**

**Current Conversation:**
{history_text}

**Latest User Message:** "{user_query}"

**INSTRUCTIONS:**
- Identify what product they want to buy
- Ask the RIGHT questions for that specific product type
- After 4-5 questions, provide detailed product recommendations
- Be adaptive and intelligent - different products need different questions!
"""
        
        # Check if we have enough information to provide recommendations
        conversation_text = " ".join([msg['content'].lower() for msg in conversation_history])
        
        # Dynamic criteria based on conversation length and information richness
        question_count = len([msg for msg in conversation_history if msg['role'] == 'assistant' and '?' in msg['content']])
        
        # If we've asked 4+ questions or have detailed info, provide recommendations
        if question_count >= 4 or len(conversation_history) >= 8:
            
            # Extract item type and requirements from conversation
            item_extraction_prompt = f"""
            Based on this buying conversation: {history_text}
            
            Extract:
            1. What product/item type they want to buy
            2. All their requirements, budget, preferences mentioned
            
            Format: 
            Item Type: [specific item they want]
            Requirements: [all details mentioned - budget, features, preferences, etc.]
            """
            
            extraction_response = self.gemini.generate_response(item_extraction_prompt)
            
            # Search for products based on extracted information
            online_results = self.search_products_online(extraction_response, conversation_text)
            
            # Generate final comprehensive recommendations
            final_response = self.gemini.generate_response(f"""
            Based on this buying conversation: {history_text}
            
            And these product search results: {online_results}
            
            Provide a comprehensive buying guide with 5-6 specific product recommendations that match their exact requirements:
            
            **Format your response as:**
            🛒 **Perfect [Product Type] Options for You:**
            
            **1. [Product Name] - ₹[Price]**
            • **Specifications:** [Key specs relevant to this product type]
            • **Why it's perfect:** [How it matches their specific needs]
            • **Where to buy:** [Specific stores/platforms]
            
            **2. [Product Name] - ₹[Price]**
            [Same format for each product]
            
            **💡 Pro Buying Tips:**
            • [Product-specific buying advice]
            • [What to look for when buying this item type]  
            • [Negotiation tips for this product category]
            
            **🎯 My Recommendation:** [Which specific product you'd recommend and why]
            
            Make it actionable, specific, and helpful!
            """)
            
            return final_response
        else:
            # Still need more information - ask smart questions
            return self.gemini.generate_response(buying_prompt)

    def handle_safety(self, user_query: str):
        """Handle safety and policy queries"""
        
        safety_prompt = f"""
You are a marketplace safety expert. Provide helpful safety information.

**Safety Topics:**
🛡️ **Meeting Safety:** Safe locations, bringing friends, daytime meetings
💰 **Payment Safety:** Secure methods, avoiding scams, escrow for high-value items
🚨 **Scam Prevention:** Red flags, too-good-to-be-true deals, verification tips
📋 **Policies:** Allowed/disallowed items, platform rules

**User Query:** "{user_query}"

Provide specific, actionable safety advice relevant to their question.
"""
        
        return self.gemini.generate_response(safety_prompt)

    def handle_app_help(self, user_query: str):
        """Handle app usage help"""
        
        app_help_prompt = f"""
You are an app support expert. Help users with marketplace app features.

**Common Help Topics:**
📝 **Listing Management:** Create, edit, delete, boost listings
🔍 **Search & Browse:** Filters, categories, saved searches
💬 **Communication:** Messaging sellers/buyers, offers, negotiations
👤 **Account:** Profile setup, settings, notifications
🛡️ **Safety Features:** Reporting, blocking, verification

**User Query:** "{user_query}"

Provide clear, step-by-step instructions for their specific question.
"""
        
        return self.gemini.generate_response(app_help_prompt)

    def handle_general(self, user_query: str):
        """Handle general conversation"""
        
        general_prompt = f"""
You are a friendly marketplace assistant. The user said: "{user_query}"

**Respond helpfully and guide them to:**
🛍️ **Selling:** "I want to sell my [item]" - I'll help create optimized listings
🔍 **Buying:** "I want to buy [item]" - I'll help you find the best deals
🛡️ **Safety:** Ask about safety tips, policies, or scam prevention
📱 **App Help:** Get help with using marketplace features

Be conversational, friendly, and helpful!
"""
        
        return self.gemini.generate_response(general_prompt)

    def clear_history(self, user_id: str):
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]

class Response:
    def __init__(self, content, needs_images=False):
        self.content = content
        self.needs_images = needs_images