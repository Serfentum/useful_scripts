import re


# Prepare regexp and variables
reg = re.compile('ftp.{60,75}\.gz')
list_of_ftps = []


with open('PRJEB2794.txt', 'r') as in_f, open('ftpsnew.txt', 'w') as out_f:
	# Find pattern throughout the file
	# Make sorted list of unique links
    list_of_ftps = sorted(list(set(reg.findall(in_f.read()))))
    
	# Write full links to output file
    for line in list_of_ftps:
        out_f.write('http://{}\n'.format(line))

print('ftps quantity:', len(list_of_ftps))
