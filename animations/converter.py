import os

for f in os.listdir("."):
	if f == "converter.py":
		continue

	file_name = f.split(".")[0]
	os.system("ffmpeg -f gif -i " + f + " " + file_name + ".mp4")