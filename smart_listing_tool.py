from conversation_manager import conversation_manager
import json

def smart_listing_tool(user_input: str, user_id: str = "default") -> dict:
    """LLM-powered conversational listing tool that dynamically asks relevant questions"""
    
    session = conversation_manager.get_session(user_id)
    listing_data = session.get("listing_data", {})
    
    # Let the LLM decide what to ask based on context
    conversation_prompt = f"""
    You are a helpful marketplace assistant helping a user create a listing.
    
    **Current conversation state:**
    - User input: "{user_input}"
    - Information collected so far: {json.dumps(listing_data, indent=2)}
    
    **Your job:**
    1. If this is the first selling message, start a conversation to collect listing details
    2. If user is answering questions, extract the info and ask the next logical question
    3. If you have enough info, generate the final listing
    
    **Information needed for a good listing:**
    - Item type/category
    - Brand/manufacturer  
    - Model/specific name
    - Condition (excellent/good/fair/poor)
    - Any defects or issues
    - Price expectations
    - Reason for selling (optional)
    - Accessories included
    - Photos needed
    
    **Response format:**
    {{
        "action": "ask_question" | "collect_info" | "generate_listing",
        "question": "Next question to ask (if asking)",
        "extracted_info": {{"key": "value"}},
        "response": "Friendly response to user",
        "needs_images": true/false,
        "listing_ready": true/false
    }}
    
    Be conversational, friendly, and ask one question at a time. Don't overwhelm the user.
    """
    
    from gemini_wrapper import GeminiWrapper
    gemini = GeminiWrapper()
    
    try:
        llm_response = gemini.generate_response(conversation_prompt)
        
        # Extract JSON from LLM response
        import re
        json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if json_match:
            response_data = json.loads(json_match.group())
            
            # Update session with extracted info
            if response_data.get("extracted_info"):
                listing_data.update(response_data["extracted_info"])
                conversation_manager.update_session(user_id, {
                    "listing_data": listing_data,
                    "state": "listing_creation"
                })
            
            # Check if listing is ready
            if response_data.get("listing_ready"):
                return generate_final_listing(listing_data, user_id)
            
            return {
                "type": "question",
                "response": response_data.get("response", "Tell me more about your item!"),
                "conversation_active": True,
                "needs_images": response_data.get("needs_images", False),
                "action": response_data.get("action", "ask_question")
            }
        
    except Exception as e:
        print(f"Error in LLM processing: {e}")
    
    # Fallback response
    return {
        "type": "question",
        "response": "I'd love to help you create a great listing! Tell me what you're selling and I'll ask you the right questions to make it attractive to buyers.",
        "conversation_active": True
    }

def generate_final_listing(listing_data: dict, user_id: str) -> dict:
    """Generate final listing using LLM with collected data"""
    
    # Reset conversation
    conversation_manager.update_session(user_id, {
        "state": "completed",
        "current_step": 0
    })
    
    listing_prompt = f"""
    Create an optimized marketplace listing based on this information:
    {json.dumps(listing_data, indent=2)}
    
    Generate:
    1. 4 compelling title options
    2. Detailed description with all key info
    3. Suggested price range based on item type and condition
    4. Category classification
    5. Relevant tags/keywords
    6. Pro tips for successful selling
    
    Format as JSON:
    {{
        "titles": ["title1", "title2", "title3", "title4"],
        "description": "detailed description",
        "category": "category name",
        "price_range": {{"min": 0, "max": 0, "suggested": 0, "currency": "INR"}},
        "tags": ["tag1", "tag2"],
        "tips": ["tip1", "tip2"]
    }}
    
    Make it professional, honest, and attractive to buyers.
    """
    
    from gemini_wrapper import GeminiWrapper
    gemini = GeminiWrapper()
    
    try:
        llm_response = gemini.generate_response(listing_prompt)
        
        import re
        json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if json_match:
            listing_result = json.loads(json_match.group())
            
            return {
                "type": "final_listing",
                "success": True,
                "collected_data": listing_data,
                "generated_listing": listing_result,
                "needs_images": True
            }
    except Exception as e:
        print(f"Error generating final listing: {e}")
    
    # Fallback
    return {
        "type": "final_listing",
        "success": False,
        "message": "I have all your information! Please upload photos of your item to complete the listing."
    }
