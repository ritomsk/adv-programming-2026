import pytest
from assignment_18.score_processor import ScoreProcessor 

def test_successful_calculation(tmp_path):
    """Validates the happy path: reading a valid number and multiplying by 10."""
    test_file = tmp_path / "valid_score.txt"
    test_file.write_text("85")
    
    processor = ScoreProcessor()
    
    result = processor.process_score_file(str(test_file))
    
    assert result == 850

def test_missing_file_handling():
    """Validates the error path: attempting to read a file that doesn't exist."""
    processor = ScoreProcessor()
    
    with pytest.raises(FileNotFoundError):
        processor.process_score_file("non_existent_file.txt")

def test_invalid_data_handling(tmp_path):
    """Validates the error path: attempting to parse letters as an integer."""
    test_file = tmp_path / "invalid_score.txt"
    test_file.write_text("eighty-five")
    
    processor = ScoreProcessor()
    
    with pytest.raises(ValueError):
        processor.process_score_file(str(test_file))