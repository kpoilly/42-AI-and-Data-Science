from utils import load_data


def main():
    data_path = None
    while (data_path is None):
        data_path = input("dataset: ")
        X, res = load_data(data_path)
        if X is None:
            print("Error: dataset not found.")
            data_path = None
    
        

if __name__ == "__main__":
    main()