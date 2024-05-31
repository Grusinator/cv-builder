from cv_compiler.models import JobPosition


class TestLlmConnector:
    def test_try_load_as_pydantic_list(self, mock_llm):
        content = """
        JSON. something [
            {
                "title": "Data Engineer",
                "company": "Ørsted",
                "start_date": "2020-01-01",
                "end_date": "2022-01-01",
                "location": "Copenhagen Area, Capital Region, Denmark",
                "description": "Developed components for data validation and data modelling for analytics tools, used python and pandas for abstraction, and integrated using Azure Service Bus. Developed data analytics and visualization tools utilizing streamlit, Panel, Dash, and bokeh.",
                "technologies": ["Python", "Pandas", "Azure Service Bus", "MS SQL Server", "REST API", "Python", "SQLAlchemy", "SQLite", "Streamlit", "Panel", "Dash", "Bokeh", "SAFE Framework", "Azure DevOps", "Docker", "K8S"]
            },
            {
                "title": "IT Consultant",
                "company": "Netcompany",
                "start_date": "2018-01-01",
                "end_date": "2019-01-01",
                "location": "Copenhagen Area, Denmark",
                "description": "Worked on large-scale IT solutions with multiple integrations; developed using Oracle, Groovy, REST, and JavaScript. Utilized Jira and Git with SCRUM for project management and version control.",
                "technologies": ["Oracle", "Groovy", "REST", "JavaScript", "Jira", "Git", "SCRUM"]
            }
        ]"""
        result = mock_llm.try_load_as_pydantic_list(content, JobPosition)
        assert len(result) == 2
