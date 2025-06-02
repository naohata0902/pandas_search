import pandas as pd 

def test_run():
    df = pd.read_excel("./major_results_2020.xlsx")
    print(df.head())


if __name__ == "__main__":
    test_run()