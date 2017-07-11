import re
s = open("EDW_un_tnsnames.ora", 'r')
#s = open("EDW_gae_tnsnames.ora", 'r')
f = open("tnsnames_test.txt", 'w')
result=""

def SidServicename(A):
	pl = re.compile('\)')
	ml = pl.search( A )
	return A[:ml.start()]

lines = s.readlines()

for line in lines:
	line.strip()
	line=line.replace(" ","")

	p = re.compile('#.*')
	m = p.match( line )

	if not m:
		p0 = re.compile('\w')
		m0 = p0.match( line )

		if m0:
			pE = re.compile('=')
			mE = pE.search( line )
			result+=((line[0:mE.end()-1])+"+")

		else : 				
			p1 = re.compile('HOST.*[0-9]*',re.IGNORECASE)
			m1 = p1.search( line )
			p2 = re.compile('SERVICE_NAME.*\)',re.IGNORECASE)
			m2 = p2.search( line )
			p3 = re.compile('SID.*\)',re.IGNORECASE)
			m3 = p3.search( line )
	
			if m1 and ( m2 or m3 ) :
				line=(line[m1.start():m1.end()]).replace(")","")
				line=line.replace("(",",")
				line=line.replace("connect_data=","+")
				result+=(line+"\n")

			elif m1:
				line=(line[m1.start():m1.end()]).replace(")","")
				line=line.replace("(",",")
				result+=(line+",")	

			elif m2 :
				line = line[m2.start():m2.end()]
				line = SidServicename(line)
				result=result[:-1]+("+"+line+"\n")	

			elif m3 :
				line = line[m3.start():m3.end()]
				line = SidServicename(line)
				result=result[:-1]+("+"+line+"\n")	

#print(result)
f.write(result)
f.close()
s.close()
