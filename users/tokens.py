import uuid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    
    #algorithm = PBKDF2PasswordHasher
    def __init__(self):
    	super(AccountActivationTokenGenerator, self).__init__()
    	self.key_salt = uuid.uuid4()#"oay2mu6phoo0eejael9Ool0eevaish8uthaSeiv1ahmaibiuZeecheeduthaa1Lieva7Neique6thooqueeBa3ciede4fahmiep1Ieteengoh3reep7Eer9Miet6eik7"

# account_activation_token = AccountActivationTokenGenerator()