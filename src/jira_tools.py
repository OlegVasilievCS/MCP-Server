from atlassian import Jira
import os

class JiraBridge:
    def __init__(self):
        self.client = Jira(
            url=os.getenv("JIRA_URL"),
            username=os.getenv("JIRA_EMAIL"),
            password=os.getenv("JIRA_API_TOKEN"),
            cloud=True
        )

    def create_task(self, summary: str, description: str, project_key="KAN"):
        try:
            fields = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Task'},
            }
            issue = self.client.create_issue(fields=fields)
            return f"Ticket created: {issue['key']}"
        except Exception as e:
            return f"Jira Error: {str(e)}"