from covid_data_handler import parse_csv_data
def test_parse_csv_data():
    data = parse_csv_data("nation_2021-10-28.csv")
    assert len(data) == 639

test_parse_csv_data()