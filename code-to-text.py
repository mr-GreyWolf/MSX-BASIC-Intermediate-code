#!/usr/bin/python
#coding=utf8
import binascii
import sys

if __name__=='__main__':
    if len(sys.argv)==3:
	file_i=sys.argv[1]	# исходный файл
	file_o=sys.argv[2]	# конечный файл
    else:
	print ('Не заданы файлы!')
	print ('Пример: '+sys.argv[0]+' file.bas file_a.txt')
	sys.exit(1)

def hex_text(hex):
    hex_to_text={
	'11':'0','12':'1','13':'2','14':'3','15':'4','16':'5','17':'6','18':'7','19':'8','1a':'9',
	'81':'END','82':'FOR','83':'NEXT','84':'DATA','85':'INPUT','86':'DIM','87':'READ','88':'LET','89':'GOTO',
	'90':'STOP','91':'PRINT','92':'CLEAR','93':'LIST','94':'NEW','95':'ON','96':'WAIT','97':'DEF','98':'POKE','99':'CONT',
	'8a':'RUN','8b':'IF','8c':'RESTORE','8d':'GOSUB','8e':'RETURN','8f':'REM','9a':'CSAVE','9b':'CLOAD','9c':'OUT','9d':'LPRINT','9e':'LLIST','9f':'CLS',
	'a0':'WIDTH','a1':'ELSE','a2':'TRON','a3':'TROFF','a4':'SWAP','a5':'ERASE','a6':'ERROR','a7':'RESUME','a8':'DELETE','a9':'AUTO',
	'aa':'RENUM','ab':'DEFSTR','ac':'DEFINT','ad':'DEFSNG','ae':'DEFDBL','af':'LINE',
	'b0':'OPEN','b1':'FIELD','b2':'GET','b3':'PUT','b4':'CLOSE','b5':'LOAD','b6':'MERGE','b7':'FILES','b8':'LSET','b9':'RSET',
	'ba':'SAVE','bb':'LFILES','bc':'CIRCLE','bd':'COLOR','be':'DRAW','bf':'PAINT',
	'c0':'BEEP','c1':'PLAY','c2':'PSET','c3':'PRESET','c4':'SOUND','c5':'SCREEN','c6':'VPOKE','c7':'SPRITE','c8':'VDP','c9':'BASE',
	'ca':'CALL','cb':'TIME','cc':'KEY','cd':'MAX','ce':'MOTOR','cf':'BLOAD',
	'd0':'BSAVE','d1':'DSKO$','d2':'SET','d3':'NAME','d4':'KILL','d5':'IPL','d6':'COPY','d7':'CMD','d8':'LOCATE','d9':'TO',
	'da':'THEN','db':'TAB','dc':'STEP','dd':'USR','de':'FN','df':'SPC',
	'e0':'NOT','e1':'ERL','e2':'ERR','e3':'STRING$','e4':'USING','e5':'INSTR','e7':'VARPTR','e8':'CRSLIN','e9':'ATTR$',
	'ea':'DSKI$','eb':'OFF','ec':'INKEY$','ed':'POINT',
	'ee':'>','ef':'=','f0':'<','f1':'+','f2':'-','f3':'*','f4':'/','f5':'^',
	'f6':'AND','f7':'OR','f8':'XOR','f9':'EQU','fa':'IMP',	'fb':'MOD',
	'fc':'\\', # Обратный слеш
#	'fd':'Перевод строки'
    }
    if hex in hex_to_text:
	text=(hex_to_text[hex])
    else:
	text='' # обработка отсутствия значения в словаре
    return text

def hex_text_ff (hex):
    hex_to_text_ff={
    # Префикс ff
	'81':'LEFT$','82':'RIGHT$','83':'MID$','84':'SGN','85':'INT','86':'ABS','87':'SQR','88':'RND','89':'SIN',
	'8a':'LOG','8b':'EXP','8c':'COS','8d':'TAN','8e':'ATN','8f':'FRE',
	'90':'INP','91':'POS','92':'LEN','93':'STR$','94':'VAL','95':'ASC','96':'CHR$','97':'PEEK','98':'VPEEK','99':'SPACE$',
	'9a':'OCT$','9b':'HEX$','9c':'LPOS','9d':'BIN$','9e':'CINT','9f':'CSNG',
	'a0':'CDBL','a1':'FIX','a2':'STICK','a3':'STRIG','a4':'PDL','a5':'PAD','a6':'DSKF','a7':'FPOS','a8':'CVI','a9':'CVS',
	'aa':'CVD','ab':'EOF','ac':'LOC','ad':'LOF','ae':'MKI$','af':'MKS$',
	'b0':'MKD$'
    }
    if hex in hex_to_text_ff:
	text=(hex_to_text_ff[hex])
    else:
	text='' # обработка отсутствия значения в словаре
    return text

data_out=''
file_in=open(file_i, 'rb')
data_in=file_in.read(1)
prefix_00=0	# Новая строка
prefix_ff=0	# FF hex_text_ff
prefix_0b=0	# 0B = Octal
prefix_0c=0	# 0C = Hex
prefix_1c=0	# 1C = Integer (256-32767)
prefix_1d=0	# 1D = Single
prefix_1d_2=0	# 1D = Single (второй полубайт)
prefix_0e=0	# 0E = номер строки
prefix_0f=0	# 0F = Integer 10-255
prefix_22=0	# кавычка (")
prefix_3a8fe6=0	# комментарий (') (3A 8F E6)
prefix_rem=0	# комментарий REM (8F)
line_end=binascii.unhexlify('0d'+'0a')	# перевод строки 00 (0D 0D)
file_end=binascii.unhexlify('1a')	# конец файла 00 00 (1A)

while data_in:
    processed=0
    code_dec=ord(data_in)
    code_hex=binascii.b2a_hex(data_in)
    code_bin=binascii.unhexlify(code_hex)
    code_hex_text=hex_text(code_hex)
    code_hex_text_ff=hex_text_ff(code_hex)

    # Разделитель операторов ELSE (3A A1)
    if prefix_3a8fe6==1 and code_hex=='a1':
        prefix_3a8fe6=0

    # Разделитель операторов (:) (3A)
    elif prefix_3a8fe6==1 and code_hex<>'8f':
        data_out=data_out+':'
        prefix_3a8fe6=0

    # Первая строка (как 00)
    if code_hex=='ff' and data_out=='':
	processed = 1
	prefix_00=1
    # 00 = Конец файла
    elif code_hex=='00' and prefix_00==2 and prefix_0f==0 and prefix_0e==0:
	data_out=data_out+file_end
	processed=1

    # 00 = Конец строки
    elif code_hex=='00'	and prefix_00==0 and prefix_0f==0 and prefix_0e==0 \
			and prefix_0b==0 and prefix_0c==0:
	data_out=data_out+line_end
	prefix_00=1
	prefix_22=0
	prefix_rem=0
	prefix_3a8fe6=0
	processed=1
    # Новая строка: младший байт (1) внутреннего номера строкм
    elif prefix_00==1:
	internal_string_number_2=code_hex
	prefix_00=2
	processed=1
    # Новая строка: старший байт (2) внутреннего номера строкм
    elif prefix_00==2:
	internal_string_number_1=code_hex
	prefix_00=3
	processed=1
    # Новая строка: младший байт (1) номера строкм
    elif prefix_00==3:
	string_number_2 = code_hex
	prefix_00=4
	processed=1
    # Новая строка: старший байт (2) номера строкм
    elif prefix_00==4:
	string_number_1=code_hex
	string_number=str(int(string_number_1+string_number_2,base=16))+' '
	prefix_00=0
	data_out=data_out+string_number
	processed=1

    # Кавычки (22): префикс
    elif code_hex=='22':
	if prefix_22==0:
		prefix_22=1
	else:
	    prefix_22=0
	    prefix_3a8fe6=0
	data_out=data_out+binascii.unhexlify(code_hex)
	processed=1
    # Кавычки (22):
    elif prefix_22==1:
	data_out=data_out+binascii.unhexlify(code_hex)
	processed=1

    # Коментарий (3a8fe6) (e6)
    elif prefix_3a8fe6==3:
	data_out=data_out+binascii.unhexlify(code_hex)

    elif prefix_3a8fe6==2 and code_hex=='e6' \
		and prefix_00==0 and prefix_22==0 and prefix_rem==0 \
		and prefix_0f==0 and prefix_0b==0 and prefix_0c==0:
	prefix_3a8fe6=3
	data_out = data_out+'\''
    # Коментарий (3a8fe6) (8f)
    elif prefix_3a8fe6==1 and code_hex=='8f' \
		and prefix_00==0 and prefix_22==0 and prefix_rem==0 \
		and prefix_0f==0 and prefix_0b==0 and prefix_0c==0:
	prefix_3a8fe6=2
    # Коментарий (3a8fe6): префикс
    elif code_hex=='3a' \
		and prefix_00==0 and prefix_22==0 and prefix_rem==0 \
		and prefix_0f==0 and prefix_0b==0 and prefix_0c==0:
	prefix_3a8fe6=1

    # REM (8f):
    elif prefix_rem==1:
	data_out=data_out + binascii.unhexlify(code_hex)
	processed=1
    # REM (8f): префикс
    elif code_hex=='8f':
	if prefix_rem==0:
		prefix_rem=1
		data_out=data_out + code_hex_text

    # Номер строки (0e)
    elif code_hex=='0e'	\
		and prefix_00==0 and prefix_ff==0 and prefix_0f==0 \
		and prefix_0b==0 and prefix_0c==0:
	prefix_0e=1
	processed=1
    # Номер строки (0e): младший байт (1) номера строкм
    elif prefix_0e==1:
	string_number_0e_2=code_hex
	prefix_0e=2
	processed=1
    # Номер строки (0e): старший байт (2) номера строкм
    elif prefix_0e==2:
	string_number_0e_1=code_hex
	string_number_0e=str(int(string_number_0e_1+string_number_0e_2,base=16))
	prefix_0e=0
	data_out=data_out+string_number_0e
	processed=1

    # Integer 1-255 (0f)
    elif prefix_0f==1:
	data_out=data_out+str(int(code_hex,base=16))
	prefix_0f=0
	processed=1
    # Integer 1-255 (0f): префикс
    elif code_hex=='0f':
	prefix_0f=1
	processed=1

    #  Octal (0b): префикс
    elif code_hex=='0b'	and prefix_00==0 and prefix_ff==0 and prefix_0f==0 \
			and prefix_0c==0:
	prefix_0b=1
    # Octal (0b): младший байт (1)
    elif prefix_0b==1:
	octal_0b_2=code_hex
	prefix_0b=2
	processed=1
    #  Octal (0b): старший байт (2)
    elif prefix_0b==2:
	octal_0b_1=code_hex
	prefix_0b=0
	data_out=data_out+'&O'+str(int(oct(int(octal_0b_1+octal_0b_2,base=16))))
	processed=1

    #  Hex (0c): префикс
    elif code_hex=='0c'	and prefix_00==0 and prefix_ff==0 and prefix_0f==0 \
			and prefix_0b==0 and prefix_1c==0:
	prefix_0c=1
    # Hex (0c): младший байт (1)
    elif prefix_0c==1:
	hex_0c_2=code_hex
	prefix_0c=2
	processed=1
    #  Hex (0c): старший байт (2)
    elif prefix_0c==2:
	hex_0c_1=code_hex
	prefix_0c=0
	if int(hex_0c_1,base=16)<=15:
	    # Убираем лидирующий ноль из старшего разряда
	    hex_0c_1=str(hex_0c_1.replace('0',''))
	if int(hex_0c_2,base=16)<=15:
	    # Убираем лидирующий ноль из младшего разряда
	    hex_0c_2=str(hex_0c_2.replace('0',''))
	data_out=data_out+'&H'+str(hex_0c_1+hex_0c_2).upper()
	processed=1

    #  Integer (1c) 256 32767 (%): префикс
    elif code_hex=='1c'	and prefix_00==0 and prefix_ff==0 and prefix_0f==0 \
			and prefix_0b==0 and prefix_0c==0:
	prefix_1c=1
    # Integer (1c) 256 32767 (%): младший байт (1)
    elif prefix_1c==1:
	int_1c_2=code_hex
	prefix_1c=2
	processed=1
    #  Integer (1c) 256 32767 (%): старший байт (2)
    elif prefix_1c==2:
	int_1c_1=code_hex
	prefix_1c=0
	data_out=data_out + str(int(int(int_1c_1 + int_1c_2,base=16)))
	processed=1

    #  Single (1d) : префикс
    elif code_hex=='1d'	and prefix_00==0 and prefix_ff==0 and prefix_0f==0 \
			and prefix_0b==0 and prefix_0c==0 and prefix_1c==0:
	prefix_1d=1
    # Single (1d) (1)
    elif prefix_1d==1:
	data_1d=''
	prefix_1d=2
	prefix_1d_2=((int(code_hex))-40)
	processed=1
    #  Single (1d) (2)
    elif prefix_1d==2:
	data_1d=data_1d+code_hex
	prefix_1d=3
	processed=1
    #  Single (1d) (3)
    elif prefix_1d==3:
	data_1d=data_1d+code_hex
	prefix_1d=4
	processed=1
    #  Single (1d) (4)
    elif prefix_1d==4:
	data_1d=data_1d+code_hex
	if prefix_1d_2==6:
	    data_out=data_out+data_1d+'!'
	else:
	    data_out=data_out+(data_1d[0:prefix_1d_2]+'.'+data_1d[prefix_1d_2:])
	processed=1
	prefix_1d=0
	prefix_1d_2=0

    # Таблица 2 (ff) префикс
    elif code_hex=='ff' and prefix_ff==0 and prefix_0e==0 and prefix_0f==0:
	prefix_ff=1
	processed=1
    # Таблица 2 (ff) текст
    elif prefix_ff==1 and prefix_0e==0 and code_hex_text_ff<>'' and prefix_0f==0:
	data_out=data_out+code_hex_text_ff
	prefix_ff=0
	processed=1

    # Таблица 1
    elif prefix_ff==0 and prefix_00==0 and prefix_0e==0 and code_hex_text<>'' and prefix_0f==0:
	data_out=data_out+code_hex_text
	processed=1

    # Обычный текст
    elif code_hex_text=="" and code_hex_text_ff=="" and processed==0:
	data_out=data_out+binascii.unhexlify(code_hex)
	processed=1

    data_in=file_in.read(1)

file_out = open(file_o, 'w')
file_out.write(data_out)

file_out.close()
file_in.close()
