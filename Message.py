class Message:
    def __init__(self, application_id, session_id, message_id,content, participants=[]):
        self.application_id = application_id
        self.session_id=session_id
        self.message_id=message_id
        self.participants=participants
        self.content=content

    def ParseToDicionary(self):
        return {
        'application_id': self.application_id,
        'session_id': self.session_id,
        'message_id': self.message_id,
        'participants': self.participants,
        'content': self.content
         }
