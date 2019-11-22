#/cmd 7bcfab368dc137d4628dcf45d41f8885 always return 'ls -l' 
#-> server use only one iv
x='ls -l'+' '*11
y=';cat flag.txt # '
/cmd 7bcfab368dc137d4628dcf45d41f8885+AES(key, CBC, 7bcfab368dc137d4628dcf45d41f8885).encrypt(;)
