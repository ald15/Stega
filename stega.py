from PIL import Image
import os
import time

#enc = 'latin-1'
# read_file
def readImg(name):
   with open(name, 'rb+') as f:
      main_bytes = f.read(54)
      image_bytes = []
      last_pos = [0, 1, 2]
      part = []
      while True:
         c_pos = f.tell()
         if c_pos !=  last_pos[-2]:
            if len(part) <3:
               part.append(f.read(1).hex())
            else:
               image_bytes.append(part)
               part = []
               part.append(f.read(1).hex())
            last_pos.append(f.tell())
         else: break
   if image_bytes[-1] == '': image_bytes.pop()
   print('Read Done!')
   #print(image_bytes)
   return main_bytes, image_bytes
#print(len(main_bytes), len(image_bytes))

#print(image_bytes[:752])



# write_file
def writeImg(name, main_bytes, image_bytes):
   image_bytes_1 = [(bytes.fromhex(i[0]) + bytes.fromhex(i[1]) + bytes.fromhex(i[2])) for i in image_bytes]
   '''for i in image_bytes:
      try:
         z = (bytes.fromhex(i[0]) + bytes.fromhex(i[1]) + bytes.fromhex(i[2]))
      except:
         print(i[0], i[1], i[2])
         '''
           
   
   #print(image_bytes_1)
   with open(name, 'wb+') as f:
      f.write(main_bytes)
      for elem in image_bytes_1: f.write(elem)
   print('Write Done!')


def getText():
   #data = input('Введите сообщение: ').strip()
   with open('data.txt', 'r+', encoding='utf8') as f: data = ''.join(f.readlines())
   #print(data)
   text = [bin(int(i.encode('utf8').hex(), 16))[2:] for i in data]
   print([i.encode('utf8').hex() for i in data])
   for i in range(len(text)):
      if len(text[i])<40: text[i] = '0'*(40-len(text[i])) + text[i]
   print(text)
   #text1 = ''.join([bytes.fromhex(hex(int(i, 2))[2:]).decode('utf8') for i in text])
   #print(text1)
   return ''.join(text)

def decodeImg(data):
   data1 = [[bin(int(j, 16))[2:] for j in i] for i in data]
   #print(data1)
   #print()
   for i in range(len(data1)):
      for j in range(len(data1[i])):
         if len(data1[i][j])<8: data1[i][j] = '0'*(8-len(data1[i][j])) + data1[i][j]
   #print(data1)
   return data1
   
def toHideText(data, text):
   x, y = 0, 0
   #print(text)
   l = len(text)
   l_bin = bin(l)[2:]
   if len(l_bin)<36: l_bin = '0'*(36-len(l_bin)) + l_bin
   #print(l_bin)
   for i in range(0, 36, 2):
      if y <= 2:
         data[x][y] = data[x][y][:-2] + l_bin[i] + l_bin[i+1]
         y += 1
      else:
         x +=1
         y = 0
         data[x][y] = data[x][y][:-2] + l_bin[i] + l_bin[i+1]
         y+=1
   #print(data[:7])
   x, y, = 6, 0
   for i in range(0, l, 2):
      if y <= 2:
         data[x][y] = data[x][y][:-2] + text[i] + text[i+1]
         y += 1
      else:
         x +=1
         y = 0
         data[x][y] = data[x][y][:-2] + text[i] + text[i+1]
         y+=1
   #print(data)
   return data
      
def encodeImg(data):
   data1 = [[hex(int(j, 2))[2:] for j in i] for i in data]
   for i in range(len(data1)):
      for j in range(len(data1[i])):
         if len(data1[i][j]) < 2: data1[i][j] = '0' + data1[i][j]
   #print(data1)
   return data1
   
def toExpandText(data):
   x, y = 0, 0
   l_bin = ''
   text = ''
   for i in range(0, 36, 2):
      if y <= 2:
         l_bin += data[x][y][-2] + data[x][y][-1]
         y += 1
      else:
         x +=1
         y = 0
         l_bin += data[x][y][-2] + data[x][y][-1]
         y+=1
   l = int(l_bin, 2)
   #print(l_bin)
   x, y = 6, 0
   for i in range(0, l, 2):
      if y <= 2:
         text += data[x][y][-2] + data[x][y][-1]
         y += 1
      else:
         x +=1
         y = 0
         text += data[x][y][-2] + data[x][y][-1]
         y+=1
   l_text, text_array = len(text), []
   #print(text)
   for i in range(l//40):
      text_array.append(text[:40])
      text = text[40:]
   print(text_array)
   '''
   for i in text_array:
      try:
         z = bytes.fromhex('0' + hex(int(i, 2))[2:] if len(hex(int(i, 2))[2:]) < 2 else hex(int(i, 2))[2:])
      except:
         print(i)
         '''
   text_array1 = [hex(int(i, 2))[2:] for i in text_array]
   print(text_array1)
   for i in range(len(text_array1)):
      if len(text_array1[i]) < 2: text_array1[i] = '0' + text_array1[i]
      '''
   for i in range(len(text_array1)):
      try:
         z = bytes.fromhex(text_array1[i]).decode('utf8')
      except:
         print(text_array1[i], i)
   
   text = ''.join([bytes.fromhex(i).decode('utf8') for i in text_array1])

   return text
   '''
   

def encrypt(rFile_name, wFile_name):
   text_data = getText()
   img_main_bytes, img_image_bytes = readImg(rFile_name)
   data = decodeImg(img_image_bytes)
   new_data = toHideText(data, text_data)
   prepared_data = encodeImg(new_data)
   writeImg(wFile_name, img_main_bytes, prepared_data)
   print('Img was created...')

def decrypt(rFile_name):
   img_main_bytes, img_image_bytes = readImg(rFile_name)
   data = decodeImg(img_image_bytes)
   text = toExpandText(data)
   return text

def writeText(data):
   with open('get_data.txt', 'w+') as f: f.write(data)
def main():
   print('\t\tSTEGO V1.0')
   menu()

def menu():
   print('\n\t\t  [MENU]')
   print('\n\t1 - Зашифровать данные\n\t2 - Расшифровать данные\n\t0 - Выйти\n')
   while True:
      user_choice = input('Введите команду: ')
      if user_choice == '0':
         print('Завершение программы...')
         break
      elif user_choice == '1':
         #rFile_name = '123.bmp'
         rFile_name = input('Исходное изображение : ')
         Image.open(rFile_name).convert(mode='RGB').save(rFile_name[:-4]+'.bmp')
         wFile_name = input('Выходное изображение (без .bmp): ') + '.bmp'
         #wFile_name = 'unnamed_2.bmp'
         encrypt(rFile_name[:-4]+'.bmp', wFile_name)
         Image.open(wFile_name).convert(mode='RGB').save(wFile_name[:-4]+'.png')
         os.system('del ' + rFile_name[:-4]+'.bmp ' + wFile_name)
         menu()
      elif user_choice == '2':
         rFile_name = input('Исходное изображение: ')
         Image.open(rFile_name).convert(mode='RGB').save(rFile_name[:-4]+'.bmp')
         print('Данные расшифрованны: ')
         decrypt(rFile_name[:-4]+'.bmp')
         #writeText(decrypt(rFile_name[:-4]+'.bmp'))
         os.system('del ' + rFile_name[:-4]+'.bmp')
         menu()
         
main()
