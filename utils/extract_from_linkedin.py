from linkedin import linkedin
import os
import json


class LinkedInAPI:
    def __init__(self):
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.application = linkedin.LinkedInApplication(token=self.access_token)

    def get_positions(self):
        positions = self.application.get_profile(selectors=['positions'])
        return positions

