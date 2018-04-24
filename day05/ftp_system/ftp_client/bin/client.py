# -*- coding:utf-8 -*-
# Author：sunmorg

import socket, json, os, sys, hashlib, getpass, logging, configparser, time

####读取配置文件####
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'conf/client.conf')
cf = configparser.ConfigParser()
cf.read(config_file)
####设定日志目录####
if os.path.exists(cf.get('log', 'logfile')):
    logfile = cf.get('log', 'logfile')
else:
    logfile = os.path.join(base_dir, 'log/client.log')
####设定下载目录####
if os.path.exists(cf.get('download', 'download_dir')):
    download_dir = cf.get('download', 'download_dir')
else:
    download_dir = os.path.join(base_dir, 'temp')

####设置日志格式###
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=logfile,
                    filemode='a+')


def hashmd5(*args):  ####用于加密密码信息
    m = hashlib.md5()
    m.update(str(*args).encode())
    return m.hexdigest()


def ProcessBar(part, total):  ####进度条模块
    if total != 0:
        i = round(part * 100 / total)
        sys.stdout.write(
            '[' + '>' * i + '-' * (100 - i) + ']' + str(i) + '%' + ' ' * 3 + str(part) + '/' + str(total) + '\r')
        sys.stdout.flush()


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def exec_linux_cmd(self, dict):  ####用于后面调用linux命令
        logging.info(dict)  ####将发送给服务端的命令保存到日志中
        self.client.send(json.dumps(dict).encode('utf-8'))
        server_response = json.loads(self.client.recv(4096).decode('utf-8'))
        if isinstance(server_response, list):
            for i in server_response:
                print(i)
        else:
            print(server_response)

    def help(self):
        info = '''
        仅支持如下命令：
        ls
        du
        pwd
        cd dirname/cd ./cd ..
        mkdir dirname
        rm  filename
        rmdir dirname
        put filename
        get filename
        mv filename/dirname filename/dirname
        newput filename (后续增加的新功能，支持断点续传)
        newget filename (后续增加的新功能，支持断点续传)
        '''
        print(info)

    def interactive(self):
        while True:
            self.pwd()  ####打印当前目录位置
            cmd = input('>>>:').strip()
            if len(cmd) == 0: continue
            action = cmd.split()[0]
            if hasattr(self, action):
                func = getattr(self, action)
                func(cmd)
            else:
                self.help()

    def put(self, *args):  ####上传文件
        cmd = args[0].split()
        override = cmd[-1]  ####override：是否覆盖参数,放在最后一位
        if override != 'True':
            override = 'False'
        # print(cmd,override)
        if len(cmd) > 1:
            filename = cmd[1]
            if os.path.isfile(filename):
                filesize = os.path.getsize(filename)
                filemd5 = os.popen('md5sum %s' % filename).read().split()[
                    0]  ####直接调用系统命令取得MD5值，如果使用hashlib，需要写open打开文件-》read读取文件（可能文件大会很耗时）-》m.update计算三部，代码量更多，效率也低
                msg = {
                    'action': 'put',
                    'filename': filename,
                    'filesize': filesize,
                    'filemd5': filemd5,
                    'override': override  ####True ,or False
                }
                logging.info(msg)
                self.client.send(json.dumps(msg).encode('utf-8'))
                server_response = self.client.recv(1024)  ####等待服务器确认信号，防止粘包
                logging.info(server_response)
                if server_response == b'file have exits, do nothing!':
                    override_tag = input('文件已存在，要覆盖文件请输入yes >>>:')
                    if override_tag == 'yes':
                        self.put('put %s True' % filename)
                    else:
                        print('文件未上传')

                else:
                    self.client.send(b'client have ready to send')  ####发送确认信号，防止粘包，代号：P01
                    server_response = self.client.recv(1024).decode('utf-8')
                    print(server_response)  ####注意：用于打印服务器反馈信息，例如磁盘空间不足信息，不能取消
                    if server_response == 'begin':
                        fk = open(filename, 'rb')
                        send_size = 0
                        for line in fk:
                            # print(len(line))
                            send_size += len(line)
                            self.client.send(line)
                            ProcessBar(send_size, filesize)
                        else:
                            print('\r\n', '文件传输完毕')
                            fk.close()
                            server_response = self.client.recv(1024).decode('utf-8')
                            print(server_response)

            else:
                print('文件不存在')
        else:
            print('请输入文件名')

    def get(self, *args):  ####下载文件
        cmd = args[0].split()
        # print(args[0],cmd)
        if len(cmd) > 1:
            filename = cmd[1]
            filepath = os.path.join(download_dir, filename)
            if os.path.isfile(filepath):  ####判断下载目录是否已存在同名文件
                override_tag = input('文件已存在，要覆盖文件请输入yes >>>:').strip()
                if override_tag == 'yes':
                    msg = {
                        'action': 'get',
                        'filename': filename,
                        'filesize': 0,
                        'filemd5': '',
                        'override': 'True'
                    }
                    logging.info(msg)
                    self.client.send(json.dumps(msg).encode('utf-8'))
                    server_response = json.loads(self.client.recv(1024).decode('utf-8'))
                    logging.info(server_response)
                    if server_response == 'Filenotfound':
                        print('File no found!')
                    else:
                        print(server_response)
                        self.client.send(b'client have been ready to receive')  ####发送信号，防止粘包
                        filesize = server_response['filesize']
                        filemd5 = server_response['filemd5']
                        receive_size = 0
                        fk = open(filepath, 'wb')
                        while filesize > receive_size:
                            if filesize - receive_size > 1024:
                                size = 1024
                            else:
                                size = filesize - receive_size
                            data = self.client.recv(size)
                            fk.write(data)
                            receive_size += len(data)
                            # print(receive_size, len(data))          ####打印数据流情况
                            ProcessBar(receive_size, filesize)  ####打印进度条

                        fk.close()
                        receive_filemd5 = os.popen('md5sum %s' % filepath).read().split()[0]
                        print('\r\n', filename, 'md5:', receive_filemd5, '原文件md5:', filemd5)
                        if receive_filemd5 == filemd5:
                            print('文件接收完成！')
                        else:
                            print('Error,文件接收异常！')
                else:
                    print('下载取消')
        else:
            print('请输入文件名')

    def newput(self, *args):  ####上传文件，具有断点续传功能
        cmd = args[0].split()
        override = cmd[-1]  ####override：是否覆盖参数,放在最后一位
        if override != 'True':
            override = 'False'
        # print(cmd,override)
        if len(cmd) > 1:
            filename = cmd[1]
            if os.path.isfile(filename):
                filesize = os.path.getsize(filename)
                filemd5 = os.popen('md5sum %s' % filename).read().split()[
                    0]  ####直接调用系统命令取得MD5值，如果使用hashlib，需要写open打开文件-》read读取文件（可能文件大会很耗时）-》m.update计算三部，代码量更多，效率也低
                msg = {
                    'action': 'newput',
                    'filename': filename,
                    'filesize': filesize,
                    'filemd5': filemd5,
                    'override': override  ####True ,or False
                }
                logging.info(msg)
                self.client.send(json.dumps(msg).encode('utf-8'))
                server_response = self.client.recv(1024)  ####等待服务器确认信号，防止粘包
                logging.info(server_response)
                print(server_response)
                if server_response == b'file have exits, and is a directory, do nothing!':
                    print('文件已存在且为目录，请先修改文件或目录名字，然后再上传')
                elif server_response == b'file have exits, do nothing!':
                    override_tag = input('文件已存在，要覆盖文件请输入yes，要断点续传请输入r >>>:').strip()
                    if override_tag == 'yes':
                        self.client.send(b'no need to do anything')  ####服务端在等待是否续传的信号，发送给服务端确认(功能号：s1)
                        time.sleep(0.5)  ####防止黏贴
                        self.put('put %s True' % filename)
                    elif override_tag == 'r':
                        self.client.send(b'ready to resume from break point')  ####服务端在等待是否续传的信号，发送给服务端确认(功能号：s1)
                        self.client.recv(1024)  ####这边接收服务端发送过来的du信息，不显示，直接丢弃
                        server_response = json.loads((self.client.recv(1024)).decode())
                        print(server_response)
                        if server_response['state'] == True:
                            exits_file_size = server_response['position']
                            fk = open(filename, 'rb')
                            fk.seek(exits_file_size, 0)
                            send_size = exits_file_size
                            for line in fk:
                                # print(len(line))
                                send_size += len(line)
                                self.client.send(line)
                                ProcessBar(send_size, filesize)
                            else:
                                print('\r\n', '文件传输完毕')
                                fk.close()
                                server_response = self.client.recv(1024).decode('utf-8')
                                print(server_response)
                        else:
                            print(server_response['content'])

                    else:
                        self.client.send(b'no need to do anything')  ####服务端在等待是否续传的信号，发送给服务端确认(功能号：s1)
                        print('文件未上传')

                else:
                    self.client.send(b'client have ready to send')  ####发送确认信号，防止粘包，代号：P01
                    server_response = self.client.recv(1024).decode('utf-8')
                    print(server_response)  ####注意：用于打印服务器反馈信息，例如磁盘空间不足信息，不能取消
                    if server_response == 'begin':
                        fk = open(filename, 'rb')
                        send_size = 0
                        for line in fk:
                            # print(len(line))
                            send_size += len(line)
                            self.client.send(line)
                            ProcessBar(send_size, filesize)
                        else:
                            print('\r\n', '文件传输完毕')
                            fk.close()
                            server_response = self.client.recv(1024).decode('utf-8')
                            print(server_response)

            else:
                print('文件不存在')
        else:
            print('请输入文件名')

    def newget(self, *args):  ####下载文件，具有断点续传功能
        cmd = args[0].split()
        # print(args[0],cmd)
        if len(cmd) > 1:
            filename = cmd[1]
            filepath = os.path.join(download_dir, filename)
            transfer_tag = True  ####传输控制信号，默认True为下载
            resume_tag = False  ####断点续传信号
            local_filesize = 0  ####本地文件大小，后面判断是否有同名文件使用
            if os.path.isfile(filepath):  ####判断下载目录是否已存在同名文件
                override_tag = input('文件已存在，要覆盖文件请输入yes，要断点续传请输入r >>>:').strip()
                if override_tag == 'yes':
                    pass
                elif override_tag == 'r':
                    local_filesize = os.path.getsize(filepath)
                    resume_tag = True
                else:
                    print('下载取消')
                    transfer_tag = False

            if transfer_tag == True:
                msg = {
                    'action': 'newget',
                    'filename': filename,
                    'filesize': local_filesize,
                    'filemd5': '',
                    'override': 'True'
                }
                logging.info(msg)
                self.client.send(json.dumps(msg).encode('utf-8'))
                server_response = json.loads(self.client.recv(1024).decode('utf-8'))
                logging.info(server_response)
                if server_response == 'Filenotfound':
                    print('File no found!')
                else:
                    print(server_response)
                    self.client.send(b'client have been ready to receive')  ####发送信号，防止粘包
                    filesize = server_response['filesize']
                    filemd5 = server_response['filemd5']
                    receive_size = local_filesize
                    if resume_tag == True:
                        fk = open(filepath, 'ab+')  ####用于断点续传
                    else:
                        fk = open(filepath, 'wb+')  ####用于覆盖或者新生成文件
                    while filesize > receive_size:
                        if filesize - receive_size > 1024:
                            size = 1024
                        else:
                            size = filesize - receive_size
                        data = self.client.recv(size)
                        fk.write(data)
                        receive_size += len(data)
                        # print(receive_size, len(data))          ####打印数据流情况
                        ProcessBar(receive_size, filesize)  ####打印进度条

                    fk.close()
                    receive_filemd5 = os.popen('md5sum %s' % filepath).read().split()[0]
                    print('\r\n', filename, 'md5:', receive_filemd5, '原文件md5:', filemd5)
                    if receive_filemd5 == filemd5:
                        print('文件接收完成！')
                    else:
                        print('Error,文件接收异常！')
        else:
            print('请输入文件名')

    def pwd(self, *args):  ####查看用户目录
        msg = {
            'action': 'pwd',
        }
        self.exec_linux_cmd(msg)

    def ls(self, *args):  ####查看文件信息
        msg = {
            'action': 'ls',
        }
        self.exec_linux_cmd(msg)

    def du(self, *args):  ####查看当前目录大小
        msg = {
            'action': 'du',
        }
        self.exec_linux_cmd(msg)

    def cd(self, *args):  ####切换目录
        try:  ####如果是直接输入cd,dirname=''
            dirname = args[0].split()[1]
        except IndexError:
            dirname = ''
        msg = {
            'action': 'cd',
            'dir': dirname
        }
        self.exec_linux_cmd(msg)

    def mkdir(self, *args):  ####生成目录
        try:  ####如果是直接输入rm,跳出
            dirname = args[0].split()[1]
            msg = {
                'action': 'mkdir',
                'dirname': dirname,
            }
            self.exec_linux_cmd(msg)
        except IndexError:
            print('Not dirname input, do nothing.')
            pass

    def rm(self, *args):  ####删除文件
        try:  ####如果是直接输入rm,跳出
            filename = args[0].split()[1]
            msg = {
                'action': 'rm',
                'filename': filename,
                'confirm': True  ####确认是否直接删除标志
            }
            self.exec_linux_cmd(msg)
        except IndexError:
            print('Not filename input, do nothing.')
            pass

    def rmdir(self, *args):
        try:  ####如果是直接输入rm,跳出
            dirname = args[0].split()[1]
            msg = {
                'action': 'rmdir',
                'dirname': dirname,
                'confirm': True  ####确认是否直接删除标志
            }
            self.exec_linux_cmd(msg)
        except IndexError:
            print('Not dirname input, do nothing.')
            pass

    def mv(self, *args):  ####实现功能：移动文件，移动目录，文件重命名，目录重命名
        try:
            objectname = args[0].split()[1]
            dstname = args[0].split()[2]
            msg = {
                'action': 'mv',
                'objectname': objectname,
                'dstname': dstname
            }
            print(msg)
            self.exec_linux_cmd(msg)
        except Exception as e:
            print(e)
            pass

    def auth(self):
        user_name = input('请输入用户名>>>:').strip()
        passwd = getpass.getpass('请输入密码>>>：').strip()  ####在linux上输入密码不显示
        msg = {
            'username': user_name,
            'passwd': hashmd5(passwd)
        }
        self.client.send(json.dumps(msg).encode('utf-8'))
        server_response = self.client.recv(1024).decode('utf-8')
        if server_response == 'ok':
            print('认证通过！')
            return True
        else:
            print(server_response)
            return False


if __name__ == '__main__':
    ftp = FtpClient()
    ftp.connect('127.0.0.1', 9999)
    auth_tag = False
    while auth_tag != True:
        auth_tag = ftp.auth()
    ftp.interactive()