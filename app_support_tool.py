def app_support_tool(action: str) -> dict:
    """Provide step-by-step help for using the marketplace app"""
    
    help_guides = {
        "edit_listing": [
            "1. **Open the app** and navigate to 'My Listings' tab",
            "2. **Find your listing** and tap the 'Edit' button (pencil icon)",
            "3. **Update details** - modify title, description, photos, or price",
            "4. **Add/remove photos** by tapping the camera icons",
            "5. **Save changes** by tapping 'Update Listing'",
            "6. **Your listing** will be updated and live immediately"
        ],
        "create_listing": [
            "1. **Tap the '+' button** on the home screen",
            "2. **Select category** that best fits your item",
            "3. **Add photos** - take up to 5 clear, well-lit photos",
            "4. **Write title** - be descriptive and include key details",
            "5. **Add description** - mention condition, features, reason for selling",
            "6. **Set price** - check similar items for competitive pricing",
            "7. **Select location** for meetups",
            "8. **Review everything** and tap 'Publish Listing'"
        ],
        "search_items": [
            "1. **Use search bar** on the home screen",
            "2. **Type keywords** for what you're looking for",
            "3. **Apply filters** - tap filter icon to narrow by category, price, location",
            "4. **Browse results** - scroll through matching items",
            "5. **Tap any item** to view full details and photos",
            "6. **Save favorites** by tapping the heart icon",
            "7. **Sort results** by price, date, or relevance"
        ],
        "contact_seller": [
            "1. **Open item listing** you're interested in",
            "2. **Tap 'Contact Seller'** button at the bottom",
            "3. **Send message** using the chat feature",
            "4. **Use quick templates** like 'Is this still available?'",
            "5. **Ask questions** about condition, meetup location, negotiation",
            "6. **Arrange meetup** through chat once you decide to buy",
            "7. **Keep communication** within the app for safety"
        ],
        "manage_account": [
            "1. **Go to Profile tab** in bottom navigation",
            "2. **Tap Settings** gear icon in top right",
            "3. **Update profile photo** by tapping your current picture",
            "4. **Edit personal info** - name, bio, contact preferences",
            "5. **Adjust notifications** - choose what alerts you want",
            "6. **Privacy settings** - control who can contact you",
            "7. **Save changes** to confirm updates"
        ],
        "report_issue": [
            "1. **Navigate to** the problematic listing or chat",
            "2. **Tap 'Report' button** (flag icon) usually in top right",
            "3. **Select reason** - spam, fake item, inappropriate content, etc.",
            "4. **Add details** in the text box explaining the issue",
            "5. **Attach evidence** if available (screenshots, photos)",
            "6. **Submit report** - our team reviews within 24 hours",
            "7. **Block user** if needed for immediate protection"
        ],
        "delete_listing": [
            "1. **Go to 'My Listings'** tab",
            "2. **Find the listing** you want to remove",
            "3. **Tap the three dots** (⋯) on the listing",
            "4. **Select 'Delete Listing'** from the menu",
            "5. **Confirm deletion** when prompted",
            "6. **Listing removed** immediately from search results"
        ],
        "boost_listing": [
            "1. **Open your listing** from 'My Listings'",
            "2. **Tap 'Boost Listing'** button",
            "3. **Choose boost duration** (24 hours, 3 days, 7 days)",
            "4. **Select payment method** for boost fee",
            "5. **Confirm purchase** to activate boost",
            "6. **Your listing** will appear higher in search results"
        ]
    }
    
    action_lower = action.lower().strip()
    
    action_matches = {
        'edit': 'edit_listing',
        'create': 'create_listing', 
        'post': 'create_listing',
        'sell': 'create_listing',
        'list': 'create_listing',
        'search': 'search_items',
        'find': 'search_items',
        'look': 'search_items',
        'contact': 'contact_seller',
        'message': 'contact_seller',
        'chat': 'contact_seller',
        'account': 'manage_account',
        'profile': 'manage_account',
        'settings': 'manage_account',
        'report': 'report_issue',
        'problem': 'report_issue',
        'complaint': 'report_issue',
        'delete': 'delete_listing',
        'remove': 'delete_listing',
        'boost': 'boost_listing',
        'promote': 'boost_listing'
    }
    
    
    matched_action = None
    for keyword, action_key in action_matches.items():
        if keyword in action_lower:
            matched_action = action_key
            break
    
    if matched_action and matched_action in help_guides:
        return {
            "action": matched_action.replace('_', ' ').title(),
            "steps": help_guides[matched_action],
            "tip": f"💡 **Pro tip:** Take your time with each step for the best results!"
        }
    
    for key, guide in help_guides.items():
        if key.replace('_', ' ') in action_lower:
            return {
                "action": key.replace('_', ' ').title(),
                "steps": guide,
                "tip": f"💡 **Pro tip:** Follow these steps carefully for success!"
            }
    
    return {
        "action": "General App Help",
        "steps": [
            "🛍️ **I can help you with these app features:**",
            "",
            "📝 **Selling:**",
            "• Creating new listings",
            "• Editing existing listings", 
            "• Boosting listings for better visibility",
            "• Deleting listings",
            "",
            "🔍 **Buying:**",
            "• Searching and filtering items",
            "• Contacting sellers",
            "• Saving favorite items",
            "",
            "⚙️ **Account Management:**",
            "• Updating profile and settings",
            "• Managing notifications",
            "• Privacy controls",
            "",
            "🛡️ **Safety & Support:**",
            "• Reporting issues or problems",
            "• Getting help with transactions",
            "",
            "**Just ask me specifically like:**",
            "• 'How do I create a listing?'",
            "• 'Help me search for items'",
            "• 'How to contact a seller?'",
            "• 'How do I edit my profile?'"
        ],
        "tip": "💬 **Ask me about any specific feature and I'll give you detailed steps!**"
    }
