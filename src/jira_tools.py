from atlassian import Jira
import os
import sys



class JiraBridge:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            url = os.getenv("JIRA_URL")
            email = os.getenv("JIRA_EMAIL")
            token = os.getenv("JIRA_API_TOKEN")
            
            if not all([url, email, token]):
                raise ValueError(f"Missing Jira Config: URL={bool(url)}, Email={bool(email)}, Token={bool(token)}")
                
            self._client = Jira(
                url=url,
                username=email,
                password=token,
                cloud=True
            )
        return self._client
    
    def add_research_comment(self, issue_key: str, research_data: str):
        """Add a technical research summary as a comment to a Jira issue
        
        """
        try:    
            comment_body = f"AI Research Assistant Findings:\n\n{research_data}"
            self.client.issue_add_comment(issue_key, comment_body)
            return f"Research comment: {research_data} was added to: {issue_key}"
        except Exception as e:
            return f"Jira Error: {str(e)}"
    
    def get_all_issues(self, project):
        try:
            issues = self.client.get_all_project_issues(project, fields='summary,status', start=0, limit=50)
            return [
                {
                "key": i['key'],
                "summary": i['fields']['summary'],
                "status": i['fields']['status']['name']
                } 
                for i in issues
            ]
        except Exception as e:
            return f"Jira Error: {str(e)}"

    
    def assign_issue(self, issue_key: str, account_id: str):
        try:
            self.client.assign_issue(issue_key, account_id)
            return f"Ticket assigned: {issue_key}"
        except Exception as e:
            return f"Jira Error: {str(e)}"
    
    def delete_issue(self, issue_key: str):
        try:
            self.client.delete_issue(issue_key)
            return f"Ticket deleted: {issue_key}"
        except Exception as e:
            return f"Jira Error: {str(e)}"


    def create_issue(self, summary: str, description: str, project_key="KAN"):
        try:
            fields = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Task'},
                'assignee': {'name': os.getenv("JIRA_EMAIL")}
            }
            issue = self.client.create_issue(fields=fields)
            return f"Ticket created and assigned to you: {issue['key']}"
        except Exception as e:
            return f"Jira Error: {str(e)}"
    
    def list_my_issues(self):
        try:
            email = os.getenv("JIRA_EMAIL")
            jql = f'assignee = "{email}" AND status != Done'
            
            issues = self.client.jql(jql)
            
            print(f"JQL Query: {jql}", file=sys.stderr)
            
            return [
                {
                    "key": i['key'],
                    "summary": i['fields']['summary'],
                    "status": i['fields']['status']['name']
                } 
                for i in issues.get('issues', [])
            ]
        except Exception as e:
            return f"Jira Error: {str(e)}"