from covid_data_handler import parse_cvs_data
def test_parse_csv_data():
    data = parse_cvs_data("nation_21-10-28.csv")
    assert len(data) == 639

