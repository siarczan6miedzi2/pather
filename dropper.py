import os

def main():
	for i in range(1000):
		print("+------------+\n| TEST %4d: |\n+------------+" % (i+1))
		os.system("pather.py")


if __name__ == "__main__": main()
