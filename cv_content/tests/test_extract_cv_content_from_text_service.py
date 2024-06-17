from cv_content.schemas import JobPosition
from cv_content.services.extract_cv_content_from_pdf_service import ExtractCvContentFromTextService




from unittest.mock import MagicMock





class TestExtractCvContentFromTextService:

    def test_get_job_positions_from_text(self):
        cv_text = "Sample CV text with job positions"
        service = ExtractCvContentFromTextService()
        response_text = """
[
    {
        "job_position_id": 1,
        "title": "Data Engineer",
        "company": "Energinet",
        "start_date": "2022-12-01",
        "end_date": "2023-10-01",
        "location": "Denmark",
        "description": "As a data engineer at Energinet, I was responsible for developing a data project collecting massive amounts of data from the energy island in Denmark, from various providers. The main goal was to receive, perform quality control, and deliver data to the developers wanting to bid on the project. Relied on Spark and Databricks for scaling and flexibility with various data formats like GDB, DFSU, segy, xtf, etc. Used Sedona (GeoSpark) for spatial data support in Spark, storing data in Delta Parquet format, and performing spatial partitioning using geohashing for improved read performance.",
        "competencies": [
            "Spark",
            "Databricks",
            "Data Quality Control",
            "Geospatial Data Handling",
            "Data Partitioning",
            "Delta Parquet"
        ]
    },
    {
        "job_position_id": 2,
        "title": "Data Engineer",
        "company": "Ørsted",
        "start_date": "2020-03-01",
        "end_date": "2022-11-01",
        "location": "Copenhagen Area, Capital Region, Denmark",
        "description": "Developed a data validation component within data pipelines, integrated using Azure Service Bus, and reliant on Python and Pandas. Involved with data modeling with MS SQL Server and REST API using Python, SQLAlchemy, and SQLite for mock DBs mirroring production to test changes. Developed data analytics and visualization tools using Streamlit, Panel, Dash, and Bokeh. Utilized the SAFE framework for project management and relied on Azure DevOps, Docker, and K8S for DevOps.",
        "competencies": [
            "Data Validation",
            "Python",
            "Pandas",
            "Data Modelling",
            "SQL Server",
            "Azure DevOps",
            "Docker",
            "Kubernetes",
            "SAFE Framework",
            "Data Visualization"
        ]
    },
    {
        "job_position_id": 3,
        "title": "IT Consultant",
        "company": "Netcompany",
        "start_date": "2018-11-01",
        "end_date": "2019-11-01",
        "location": "København, Denmark",
        "description": "Worked on large-scale custom IT solutions with multiple integrations using Oracle, Groovy, Java REST APIs, and a bit of JavaScript. Employed Jira and Git with SCRUM methodology for project management and version control.",
        "competencies": [
            "Oracle",
            "Groovy",
            "REST APIs",
            "JavaScript",
            "Jira",
            "Git",
            "SCRUM"
        ]
    },
    {
        "job_position_id": 4,
        "title": "Softwareudvikler",
        "company": "NIRAS",
        "start_date": "2016-09-01",
        "end_date": "2018-03-01",
        "location": "Allerød, Capital Region, Denmark",
        "description": "Developed geodata algorithms for data transformation, including processing of LiDAR data and images. Created an image classifier for identifying buildings in spectral orthophotos and a model to analyze roadside height profiles using LiDAR and GIS data. Developed various plugins for QGIS using Qt and Python.",
        "competencies": [
            "Geodata Algorithms",
            "LiDAR Data Processing",
            "Image Classifier",
            "GIS",
            "QGIS Plugins",
            "Qt",
            "Python",
            "C#",
            "PostgreSQL",
            "PostGIS"
        ]
    },
    {
        "job_position_id": 5,
        "title": "Engineer",
        "company": "KK Wind Solutions",
        "start_date": "2014-03-01",
        "end_date": "2014-08-01",
        "location": "Ikast",
        "description": "Investigated the replacement of communication chips for IO boards in wind turbine control systems for product configuration flexibility. This involved programming in C and studying communication protocols like EtherCAT and Profinet.",
        "competencies": [
            "C Programming",
            "Communication Protocols",
            "EtherCAT",
            "Profinet",
            "Hardware Integration"
        ]
    },
    {
        "job_position_id": 6,
        "title": "Instructor",
        "company": "Det Tekniske Fakultet, Syddansk Universitet",
        "start_date": "2013-09-01",
        "end_date": "2014-01-01",
        "location": "Odense Area, Denmark",
        "description": "Instructor in Electronics courses teaching basic analog circuit design.",
        "competencies": [
            "Electronics Teaching",
            "Analog Circuit Design",
            "Educational Skills"
        ]
    },
    {
        "job_position_id": 7,
        "title": "Internship Electronics",
        "company": "VELUX",
        "start_date": "2013-02-01",
        "end_date": "2013-06-01",
        "location": "Skjern, Denmark",
        "description": "Developed a PCB for testing the durability of solar panels for automated Velux windows.",
        "competencies": [
            "PCB Design",
            "Solar Panel Testing",
            "Durability Analysis"
        ]
    }
]
"""
        service.llm_connector.ask_question = MagicMock(return_value=response_text)

        job_positions = service.get_job_positions_from_text(cv_text)
        assert isinstance(job_positions[0], JobPosition)
        assert len(job_positions) == 7
        assert job_positions[0].title == "Data Engineer"
        assert job_positions[0].job_position_id == 1