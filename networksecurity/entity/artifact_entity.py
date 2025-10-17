from dataclasses import dataclass
"""
It acts like an decorator which creates an variable for an empty class
"""

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str