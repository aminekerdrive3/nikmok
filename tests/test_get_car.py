from get_car import extract_field, generate_car

def test_get_car():
    assert True  # Replace with actual test logic for getting car data

def test_get_image():
    assert True  # Replace with actual test logic for getting image data

def test_extract_field():
    sample_response = "Title: Test Title\nCar: Test Car 2024\nCaption: Test caption"
    assert extract_field(sample_response, "Title") == "Test Title"
    assert extract_field(sample_response, "Car") == "Test Car 2024"
    assert extract_field(sample_response, "Caption") == "Test caption"

def test_extract_field_missing():
    sample_response = "Title: Test Title"
    assert extract_field(sample_response, "NonExistent") == "Unknown NonExistent"