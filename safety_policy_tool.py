def safety_policy_tool(topic: str) -> dict:
    """Provide safety guidelines and marketplace policy information"""
    
    knowledge_base = {
        "allowed_items": [
            "Electronics & Gadgets",
            "Fashion & Accessories", 
            "Home & Garden Items",
            "Sports & Fitness Equipment",
            "Books & Educational Material",
            "Automotive Parts & Accessories",
            "Health & Beauty Products",
            "Toys & Games",
            "Professional Services",
            "Art & Collectibles",
            "Musical Instruments",
            "Pet Supplies (non-living)"
        ],
        "disallowed_items": [
            "Weapons and ammunition",
            "Illegal drugs and substances", 
            "Counterfeit or replica items",
            "Adult content and services",
            "Live animals",
            "Prescription medicines",
            "Stolen or suspicious goods",
            "Hazardous materials",
            "Tobacco products",
            "Alcoholic beverages",
            "Items violating intellectual property",
            "Services requiring licenses without proper documentation"
        ],
        "safety_tips": [
            "Always meet in well-lit, public places like malls, cafes, or community centers",
            "Bring a trusted friend or family member with you",
            "Meet during daytime hours when possible",
            "Verify the item condition thoroughly before making payment",
            "Use secure payment methods - cash for local meetings",
            "Trust your instincts - if something feels wrong, walk away",
            "Don't share personal information like home address unnecessarily",
            "Let someone know where you're going and when you'll be back",
            "Check the item's serial numbers and authenticity",
            "Take photos of the item and seller's contact details"
        ],
        "payment_safety": [
            "Use cash for local face-to-face transactions when possible",
            "For online payments, use secure platforms with buyer protection",
            "Never send money before seeing and verifying the item",
            "Avoid wire transfers, cryptocurrency, or gift card payments",
            "Use escrow services for high-value items (₹10,000+)",
            "Keep all receipts and transaction records",
            "Verify bank account details before making transfers",
            "Be cautious of overpayment scams",
            "Don't share your banking passwords or OTPs"
        ],
        "scam_prevention": [
            "Be extremely wary of deals that seem too good to be true",
            "Verify seller identity through multiple communication channels",
            "Don't share OTPs, banking passwords, or personal details",
            "Watch out for fake payment confirmations or screenshots",
            "Be suspicious of urgent sale pressures or time limits",
            "Verify item authenticity, especially for electronics and branded items",
            "Report suspicious behavior to platform administrators immediately",
            "Don't click on suspicious links sent by buyers/sellers",
            "Meet sellers who refuse to meet in person with extra caution"
        ],
        "legal_guidelines": [
            "Ensure you have legal ownership of items you're selling",
            "Don't sell items that require special licenses without proper documentation",
            "Be honest about item condition and defects",
            "Respect intellectual property rights",
            "Follow local laws regarding item categories",
            "Keep proof of purchase for expensive items"
        ]
    }
    
    topic_lower = topic.lower().strip()
    
    if any(word in topic_lower for word in ['safety', 'meetup', 'meet', 'secure', 'protection']):
        return {
            "topic": "Safety Guidelines", 
            "content": knowledge_base["safety_tips"],
            "summary": "Always prioritize your safety when meeting buyers/sellers"
        }
    elif any(word in topic_lower for word in ['payment', 'money', 'pay', 'transaction', 'banking']):
        return {
            "topic": "Payment Safety", 
            "content": knowledge_base["payment_safety"],
            "summary": "Use secure payment methods and never pay before verification"
        }
    elif any(word in topic_lower for word in ['scam', 'fraud', 'fake', 'cheat', 'suspicious']):
        return {
            "topic": "Scam Prevention", 
            "content": knowledge_base["scam_prevention"],
            "summary": "Stay alert for red flags and trust your instincts"
        }
    elif any(word in topic_lower for word in ['allowed', 'policy', 'rules', 'items', 'what can']):
        return {
            "topic": "Item Policy",
            "allowed_items": knowledge_base["allowed_items"],
            "disallowed_items": knowledge_base["disallowed_items"],
            "summary": "Check our policies before listing items"
        }
    elif any(word in topic_lower for word in ['legal', 'law', 'ownership', 'rights']):
        return {
            "topic": "Legal Guidelines",
            "content": knowledge_base["legal_guidelines"],
            "summary": "Follow all applicable laws and regulations"
        }
    else:
        return {
            "topic": "General Safety Help", 
            "content": [
                "🛡️ **I can help you with:**",
                "",
                "• **Safety guidelines** for secure meetups",
                "• **Payment safety** tips and secure methods",
                "• **Scam prevention** and red flag identification", 
                "• **Item policies** - what's allowed vs disallowed",
                "• **Legal guidelines** for responsible trading",
                "",
                "**Just ask me something like:**",
                "• 'What are the safety tips for meetups?'",
                "• 'How to pay safely?'",
                "• 'What items are not allowed?'",
                "• 'How to avoid scams?'"
            ],
            "summary": "Your safety and security are our top priority"
        }
