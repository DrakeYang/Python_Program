import re

# 사용법 
# tnsnames.ora 파일을 엑셀에 맞게 변형시켜주는 프로그램
# 소스, 타겟 파일을 설정 해주고 실행
# 타겟파일을 열어서 복사, 엑셀에 붙여넣기
# 데이터 나누기에 구분자를 '+' 로 설정하면 나누기 완성
# alias,host,port,servicename 순서의 컬럼으로 나누게됨
# 각 컬럼 내부 내용의 구분은 ',' 로 이루어짐
# 컬럼의 구분은 '+' 로 구분 
# 이하의 코드의 '+' 는 전부 구분자 이므로 임의로 변형 가능

# 소스 파일
s = open("EDW_un_tnsnames.ora", 'r') 
# 타겟 파일
f = open("tnsnames_test.txt", 'w')

# 결과물 적재용 변수
result=""

# 호스트, 커넥트 정보가 나왔는지를 체크하는 플래그
flagHost = 0
flagSid = 0
# 호스트,포트값이 여거개인 경우를 위한 변수
strHost = ""
strPort = ""

# 시드,서비스명 앞에서 자르기 위한 함수
def SidServicename(A):
	pl = re.compile('\)')
	ml = pl.search( A )
	return A[:ml.start()]

# 괄호를 제거해 주는 함수
def removeParenthesis(A):
	return (A.replace(")","")).replace("(","") 	

# 소스 읽기 시작
lines = s.readlines()

for line in lines:
	line.strip()
	# 빈칸을 없애줌
	line=line.replace(" ","")

	# 주석이 있는 줄은 무시하기 위한 정규식
	p = re.compile('#.*')
	m = p.match( line )

	if not m: # 주석용 #가 있을경우 무시 
		p0 = re.compile('\w')
		m0 = p0.match( line )

		if m0:
			pE = re.compile('=')
			mE = pE.search( line )
			if flagSid == 1 :  #SID 가 나왔을 경우 (정상적)
				flagSid = 0
				strHost = ""
				strPort = ""

			else : # SID 안나옴 (비정상일 경우)
				result=result+removeParenthesis(strHost[:-1] +"+" + strPort[:-1] +"\n")
			# 비정상적이면 밑에서 추가되지 않기때문에 여기서 결과물을 추가	
			result+=((line[0:mE.end()-1])+"+")

		else : 				
			# 이것저것 검색용 정규식
			pHost = re.compile('HOST.*[\w]*\){1}',re.IGNORECASE)
			mHost = pHost.search( line )
			pPort = re.compile('PORT.*=.*[0-9]{4}',re.IGNORECASE)
			mPort = pPort.search( line )
			pServiceName = re.compile('SERVICE_NAME.*\)',re.IGNORECASE)
			mServiceName = pServiceName.search( line )
			pSid = re.compile('SID.*\)',re.IGNORECASE)
			mSid = pSid.search( line )
			pConnectData = re.compile('connect_data=',re.IGNORECASE)
			mConnectData = pPort.search( line )
			
			# host,sid 가 한줄에 있을 경우 
			if mHost and ( mServiceName or mSid ) :				
				strHost = (line[mHost.start():mPort.start()]) +"+"
				strPort = (line[mPort.start():mPort.end()]) +"+"

				# sid 부분 첫글자부터 시작
				line = (line[mConnectData.end()+17:])
				result+=removeParenthesis(strHost + strPort + line+"\n")
				flagSid = 1 # sid 출현하여 flag 성립
				strHost = "" # 초기화
				strPort = "" # 초기화

			# host 먼저 발견 시 
			elif mHost:
				# host 부분 잘라내기. 다만 포트도 같이 나옴. 한방에 자를수 있으면 좋겠음..
				strSubHost = (line[mHost.start():mHost.end()])
				# host 문장의 가로닫기 부분을 검색
				pParen = re.compile('\)',re.IGNORECASE)
				mParen = pParen.search( strSubHost)
				# 호스트 부분만 추가
				strHost +=(strSubHost[:mParen.start()]) +","

				# 한줄에 포트도 있을경우 
				if mPort :					
					strPort += removeParenthesis((line[mPort.start():mPort.end()]) +",")

			# 포트가 호스트와 따로 있을 경우
			elif mPort:
				strPort += removeParenthesis((line[mPort.start():mPort.end()]) +",")

			# 서비스네임만 있을 경우
			elif mServiceName :
				# 서비스네임 부분 검색
				line = line[mServiceName.start():mServiceName.end()]
				line = SidServicename(line)
				# 서비스네임이 나오게 되면 더이상 호스트가 안나옴
				# 호스트와 포트 정리
				result += strHost[:-1] + "+" + strPort[:-1] + "\n"
				result=result[:-1]+("+"+line+"\n") # 마무리로 문장 넘김 추가
				flagSid = 1	# 플래그 온 

			# sid 만 있을 경우
			elif mSid :
				line = line[mSid.start():mSid.end()]
				line = SidServicename(line)
				# 서비스네임이 나오게 되면 더이상 호스트가 안나옴
				# 호스트와 포트 정리
				result += strHost[:-1] + "+" + strPort[:-1] + "\n"
				result = result[:-1]+("+"+line+"\n")	
				flagSid = 1	# 플래그 온 

# 결과물을 파일에 쓴다
f.write(result)
# 닫아준다 
f.close()
s.close()

# 추가 작성 예정
# 파일 입출력 부분 try 구문 만들기 
# 명령어로 실행
# 실행가능 파일로 패키지화
