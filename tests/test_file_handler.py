from cv_compiler.file_handler import FileHandler


class TestFileHandler:

    def test_read_write_jobs(self):
        file_handler = FileHandler()
        projects = file_handler.get_background_job_positions()
        file_handler.write_job_positions(projects)
