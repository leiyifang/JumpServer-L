# JumpServer-L
自己开发的堡垒机带病毒和木马扫描功能

1.本项目是基于刘江明的IronFort堡垒机项目做的二次开发。
2.添加了针对Linux系统的病毒和木马扫描功能，目前项目还没有开发完成，还在开发中，后续有时间会持续更新。
3.环境说明：
  OS:Ubuntu 16.04
  Python: 3.6.6
  Mysql:5.7.23

  其他的软件包版本信息如下：
  Package          Version
---------------- -------
asn1crypto       0.24.0 
bcrypt           3.1.4  
cffi             1.11.5 
cryptography     2.3    
Django           2.0.1  
gevent           1.3.5  
gevent-websocket 0.10.1 
greenlet         0.4.14 
idna             2.7    
paramiko         2.4.1  
pip              18.0   
pyasn1           0.4.4  
pyClamd          0.4.0  
pycparser        2.18   
PyMySQL          0.9.2  
PyNaCl           1.2.1  
pytz             2018.5 
setuptools       40.0.0 
six              1.11.0 
wheel            0.31.1 
  
  
4.本项目中使用的数据库为MySQL 5.7，在使用阿里云的RDS的时候在make migrate的时候都报错：
django.db.utils.InternalError: (1071, 'Specified key was too long; max key length is 767 bytes')
目前暂时没有好的解决方法，建议自己搭建数据库并且使用UTF8字符集。
create database ironfort CHARACTER SET utf8 COLLATE utf8_general_ci;

5.运行方式为：python start_ironfort.py 

6.运行效果如下：
 ![image](https://github.com/leiyifang/JumpServer-L/blob/master/show_img/1.jpg)
 ![image](https://github.com/leiyifang/JumpServer-L/blob/master/show_img/2.jpg)
 ![image](https://github.com/leiyifang/JumpServer-L/blob/master/show_img/3.jpg)
