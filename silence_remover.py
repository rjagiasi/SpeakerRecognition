import os

file_array = os.listdir("/home/punit/Downloads/test");
for file_name in file_array :
#/home/punit/Downloads/test/{}  directory which contains raw files 
#/home/punit/Downloads/processed/{} directory which contains processed files
#install sox before the script is run. 
#Meaning of parameters refer this article https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/
	cmd = "sox /home/punit/Downloads/test/{} /home/punit/Downloads/processed/{} silence 1 0.1 1% -1 0.1 1%".format(file_name, file_name)
	#print(cmd);	
	os.system(cmd);
