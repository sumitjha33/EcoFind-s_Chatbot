class ConversationManager:
    def __init__(self):
        self.user_sessions = {}  
    
    def get_session(self, user_id="default"):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "state": "initial",
                "listing_data": {},
                "questions_asked": [],
                "current_step": 0
            }
        return self.user_sessions[user_id]
    
    def update_session(self, user_id, data):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {"state": "initial", "listing_data": {}, "questions_asked": [], "current_step": 0}
        self.user_sessions[user_id].update(data)

conversation_manager = ConversationManager()
