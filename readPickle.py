import pickle
import os

data_file_name = "data/"

def main():
	for directory in os.listdir(data_file_name):
		for f in os.listdir(data_file_name+directory):
			records = pickle.load(open(data_file_name+directory+"/"+f, "rb"))
			print(records["A"])
			print(records["B"])
			print(records["stat"])

if __name__ == '__main__':
	main()