# -*- coding:utf-8 -*-
# Author：sunmorg

import socketserver, json, os, sys, time, shutil, configparser, logging
from usermanagement import useropr

####读取配置文件####
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'conf/server.conf')
cf = configparser.ConfigParser()
cf.read(config_file)
####设定日志目录####
if os.path.exists(cf.get('log', 'logfile')):
    logfile = cf.get('log', 'logfile')
else:
    logfile = os.path.join(base_dir, 'log/server.log')
####设定用户上传文件目录####
if os.path.exists(cf.get('upload', 'upload_dir')):
    file_dir = cf.get('upload', 'upload_dir')
else:
    file_dir = os.path.join(base_dir, 'user_files')

####设置日志格式###
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d    %H:%M:%S',
                    filename=logfile,
                    filemode='a+')


def TimeStampToTime(timestamp):  ####输入timestamp格式化输出时间，输出格式如：2017-09-16 16:32:35
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def ProcessBar(part, total):  ####进度条模块，运行会导致程序变慢
    if total != 0:
        i = round(part * 100 / total)
        sys.stdout.write(
            '[' + '>' * i + '-' * (100 - i) + ']' + str(i) + '%' + ' ' * 3 + str(part) + '/' + str(total) + '\r')
        sys.stdout.flush()
        # if part == total:
        #     print()


class MyTCPHandler(socketserver.BaseRequestHandler):

    def put(self, *args):  ####接收客户端文件
        # self.request.send(b'server have been ready to receive')    ####发送ACK
        cmd_dict = args[0]
        filename = os.path.basename(cmd_dict['filename'])  ####传输进来的文件名可能带有路径，将路径去掉
        filesize = cmd_dict['filesize']
        filemd5 = cmd_dict['filemd5']
        override = cmd_dict['override']
        receive_size = 0
        file_path = os.path.join(self.position, filename)
        if override != 'True' and os.path.exists(file_path):  ####检测文件是否已经存在
            self.request.send(b'file have exits, do nothing!')
        else:
            if os.path.isfile(file_path):  ####如果文件已经存在，先删除，再计算磁盘空间大小
                os.remove(file_path)
            current_size = self.du()  ####调用du查看用户磁盘空间大小，但是du命令的最后会发送一个结果信息给client，会和前面和后面的信息粘包，需要注意
            self.request.recv(1024)  ####接收客户端ack信号，防止粘包，代号：P01
            print(self.user_spacesize, current_size, filesize)
            if self.user_spacesize >= current_size + filesize:
                self.request.send(b'begin')  ####发送开始传输信号
                fk = open(file_path, 'wb')
                while filesize > receive_size:
                    if filesize - receive_size > 1024:
                        size = 1024
                    else:
                        size = filesize - receive_size
                    data = self.request.recv(size)
                    fk.write(data)
                    receive_size += len(data)
                    # print(receive_size,len(data))   ####打印每次接收的数据
                    # ProcessBar(receive_size, filesize)  ####服务端进度条，不需要可以注释掉

                fk.close()
                receive_filemd5 = os.popen('md5sum %s' % file_path).read().split()[0]
                print('\r\n', file_path, 'md5:', receive_filemd5, '原文件md5:', filemd5)
                if receive_filemd5 == filemd5:
                    self.request.send(b'file received successfully!')
                else:
                    self.request.send(b'Error, file received have problems!')
            else:
                self.request.send(
                    b'Error, disk space do not enough! Nothing done! Total: %d, current: %d, rest:%d, filesize:%d' % (
                        self.user_spacesize, current_size, self.user_spacesize - current_size, filesize))

    def get(self, *args):  ####发送给客户端文件
        # print('get receive the cmd',args[0])
        filename = args[0]['filename']
        print(filename)
        # self.request.send(b'server have been ready to send')  ####发送ACK
        file_path = os.path.join(self.position, filename)
        if os.path.isfile(file_path):
            filesize = os.path.getsize(file_path)
            ####直接调用系统命令取得MD5值，如果使用hashlib，需要写open打开文件-》read读取文件（可能文件大会很耗时）-》m.update计算三部，代码量更多，效率也低
            filemd5 = os.popen('md5sum %s' % file_path).read().split()[0]
            msg = {
                'action': 'get',
                'filename': filename,
                'filesize': filesize,
                'filemd5': filemd5,
                'override': 'True'
            }
            print(msg)
            self.request.send(json.dumps(msg).encode('utf-8'))

            '''接下来发送文件给客户端'''
            self.request.recv(1024)  ####接收ACK信号，下一步发送文件
            fk = open(file_path, 'rb')
            send_size = 0
            for line in fk:
                send_size += len(line)
                self.request.send(line)
                # ProcessBar(send_size, filesize)     ####服务端进度条，不需要可以注释掉
            else:
                print('文件传输完毕')
                fk.close()

        else:
            print(file_path, '文件未找到')
            self.request.send(json.dumps('Filenotfound').encode('utf-8'))

    def newput(self, *args):  ####接收客户端文件，具有断点续传功能
        # self.request.send(b'server have been ready to receive')    ####发送ACK
        cmd_dict = args[0]
        filename = os.path.basename(cmd_dict['filename'])  ####传输进来的文件名可能带有路径，将路径去掉
        filesize = cmd_dict['filesize']
        filemd5 = cmd_dict['filemd5']
        override = cmd_dict['override']
        receive_size = 0
        file_path = os.path.join(self.position, filename)
        print(file_path, os.path.isdir(file_path))
        if override != 'True' and os.path.exists(file_path):  ####检测文件是否已经存在
            if os.path.isdir(file_path):
                self.request.send(b'file have exits, and is a directory, do nothing!')
            elif os.path.isfile(file_path):
                self.request.send(b'file have exits, do nothing!')
                resume_signal = self.request.recv(1024)  ####接收客户端发来的是否从文件断点续传的信号
                if resume_signal == b'ready to resume from break point':  ####执行断点续传功能
                    exits_file_size = os.path.getsize(file_path)
                    current_size = self.du()
                    time.sleep(0.5)  ####防止粘包
                    print('用户空间上限：%d, 当前已用空间：%d, 已存在文件大小：%d, 上传文件大小：%d ' % (
                    self.user_spacesize, current_size, exits_file_size, filesize))
                    if self.user_spacesize >= (current_size - exits_file_size + filesize):  ####判断剩余空间是否足够
                        if exits_file_size < filesize:
                            receive_size = exits_file_size
                            print('服务器上已存在的文件大小为：', exits_file_size)
                            msg = {
                                'state': True,
                                'position': exits_file_size,
                                'content': 'ready to receive file'
                            }
                            self.request.send(json.dumps(msg).encode('utf-8'))
                            fk = open(file_path, 'ab+')
                            while filesize > receive_size:
                                if filesize - receive_size > 1024:
                                    size = 1024
                                else:
                                    size = filesize - receive_size
                                data = self.request.recv(size)
                                fk.write(data)
                                receive_size += len(data)
                                # print(receive_size,len(data))   ####打印每次接收的数据
                                # ProcessBar(receive_size, filesize)  ####服务端进度条，不需要可以注释掉

                            fk.close()
                            receive_filemd5 = os.popen('md5sum %s' % file_path).read().split()[0]
                            print('\r\n', file_path, 'md5:', receive_filemd5, '原文件md5:', filemd5)
                            if receive_filemd5 == filemd5:
                                self.request.send(b'file received successfully!')
                            else:
                                self.request.send(b'Error, file received have problems!')

                        else:  ####如果上传的文件小于当前服务器上的文件，则为同名但不同文件，不上传。实际还需要增加其他判断条件，判断是否为同一文件。
                            msg = {
                                'state': False,
                                'position': '',
                                'content': 'Error, file mismatch, do nothing!'
                            }
                            self.request.send(json.dumps(msg).encode('utf-8'))
                    else:  ####如果续传后的用户空间大于上限，拒接续传
                        msg = {
                            'state': False,
                            'position': '',
                            'content': 'Error, disk space do not enough! Nothing done! Total: %d, current: %d, rest:%d, need_size:%d' % (
                            self.user_spacesize, current_size, self.user_spacesize - current_size,
                            filesize - exits_file_size)
                        }
                        self.request.send(json.dumps(msg).encode('utf-8'))
                else:
                    pass

        else:
            if os.path.isfile(file_path):  ####如果文件已经存在，先删除，再计算磁盘空间大小
                os.remove(file_path)
            current_size = self.du()  ####调用du查看用户磁盘空间大小，但是du命令的最后会发送一个结果信息给client，会和前面和后面的信息粘包，需要注意
            self.request.recv(1024)  ####接收客户端ack信号，防止粘包，代号：P01
            print(self.user_spacesize, current_size, filesize)
            if self.user_spacesize >= current_size + filesize:
                self.request.send(b'begin')  ####发送开始传输信号
                fk = open(file_path, 'wb')
                while filesize > receive_size:
                    if filesize - receive_size > 1024:
                        size = 1024
                    else:
                        size = filesize - receive_size
                    data = self.request.recv(size)
                    fk.write(data)
                    receive_size += len(data)
                    # print(receive_size,len(data))   ####打印每次接收的数据
                    # ProcessBar(receive_size, filesize)  ####服务端进度条，不需要可以注释掉

                fk.close()
                receive_filemd5 = os.popen('md5sum %s' % file_path).read().split()[0]
                print('\r\n', file_path, 'md5:', receive_filemd5, '原文件md5:', filemd5)
                if receive_filemd5 == filemd5:
                    self.request.send(b'file received successfully!')
                else:
                    self.request.send(b'Error, file received have problems!')
            else:
                self.request.send(
                    b'Error, disk space do not enough! Nothing done! Total: %d, current: %d, rest:%d, filesize:%d' % (
                        self.user_spacesize, current_size, self.user_spacesize - current_size, filesize))

    def newget(self, *args):  ####发送给客户端文件，具有断点续传功能
        # print('get receive the cmd',args[0])
        filename = args[0]['filename']
        remote_local_filesize = args[0]['filesize']
        print(filename)
        # self.request.send(b'server have been ready to send')  ####发送ACK
        file_path = os.path.join(self.position, filename)
        if os.path.isfile(file_path):
            filesize = os.path.getsize(file_path)
            ####直接调用系统命令取得MD5值，如果使用hashlib，需要写open打开文件-》read读取文件（可能文件大会很耗时）-》m.update计算三部，代码量更多，效率也低
            filemd5 = os.popen('md5sum %s' % file_path).read().split()[0]
            msg = {
                'action': 'newget',
                'filename': filename,
                'filesize': filesize,
                'filemd5': filemd5,
                'override': 'True'
            }
            print(msg)
            self.request.send(json.dumps(msg).encode('utf-8'))

            '''接下来发送文件给客户端'''
            self.request.recv(1024)  ####接收ACK信号，下一步发送文件
            fk = open(file_path, 'rb')
            fk.seek(remote_local_filesize, 0)
            send_size = remote_local_filesize
            for line in fk:
                send_size += len(line)
                self.request.send(line)
                # ProcessBar(send_size, filesize)     ####服务端进度条，不需要可以注释掉
            else:
                print('文件传输完毕')
                fk.close()

        else:
            print(file_path, '文件未找到')
            self.request.send(json.dumps('Filenotfound').encode('utf-8'))

    def pwd(self, *args):
        current_position = self.position
        result = current_position.replace(file_dir, '')  ####截断目录信息，使用户只能看到自己的家目录信息
        self.request.send(json.dumps(result).encode('utf-8'))

    def ls(self, *args):  ####列出当前目录下的所有文件信息，类型，字节数，生成时间。
        result = ['%-20s%-7s%-10s%-23s' % ('filename', 'type', 'bytes', 'creationtime')]  ####信息标题
        for f in os.listdir(self.position):
            type = 'unknown'
            f_abspath = os.path.join(self.position, f)  ####给出文件的绝对路径，不然程序会找不到文件
            if os.path.isdir(f_abspath):
                type = 'd'
            elif os.path.isfile(f_abspath):
                type = 'f'
            result.append('%-20s%-7s%-10s%-23s' % (
                f, type, os.path.getsize(f_abspath), TimeStampToTime(os.path.getctime(f_abspath))))
        self.request.send(json.dumps(result).encode('utf-8'))

    def du(self, *args):
        '''统计纯文件和目录占用空间大小，结果小于在OS上使用du -s查询，因为有一些（例如'.','..'）隐藏文件未包含在内'''
        totalsize = 0
        if os.path.isdir(self.position):
            dirsize, filesize = 0, 0
            for root, dirs, files in os.walk(self.position):
                for d_item in dirs:  ####计算目录占用空间，Linux中每个目录占用4096bytes，实际上也可以按这个值来相加
                    if d_item != '':
                        dirsize += os.path.getsize(os.path.join(root, d_item))
                for f_item in files:  ####计算文件占用空间
                    if f_item != '':
                        filesize += os.path.getsize(os.path.join(root, f_item))
            totalsize = dirsize + filesize
            result = 'current directory total sizes: %d' % totalsize
        else:
            result = 'Error,%s is not path ,or path does not exist!' % self.position
        self.request.send(json.dumps(result).encode('utf-8'))
        return totalsize

    def cd(self, *args):
        print(*args)
        user_homedir = os.path.join(file_dir, self.username)
        cmd_dict = args[0]
        error_tag = False
        '''判断目录信息'''
        if cmd_dict['dir'] == '':
            self.position = user_homedir
        elif cmd_dict['dir'] == '.' or cmd_dict['dir'] == '/' or '//' in cmd_dict['dir']:  ####'.','/','//','///+'匹配
            pass
        elif cmd_dict['dir'] == '..':
            if user_homedir != self.position and user_homedir in self.position:  ####当前目录不是家目录，并且当前目录是家目录下的子目录
                self.position = os.path.dirname(self.position)
        elif '.' not in cmd_dict['dir'] and os.path.isdir(
                os.path.join(self.position, cmd_dict['dir'])):  ####'.' not in cmd_dict['dir'] 防止../..输入
            self.position = os.path.join(self.position, cmd_dict['dir'])
        else:
            error_tag = True
        '''发送结果'''
        if error_tag:
            result = 'Error,%s is not path here, or path does not exist!' % cmd_dict['dir']
            self.request.send(json.dumps(result).encode('utf-8'))
        else:
            self.pwd()

    def mv(self, *args):
        print(*args)
        try:
            objectname = args[0]['objectname']
            dstname = args[0]['dstname']
            abs_objectname = os.path.join(self.position, objectname)
            abs_dstname = os.path.join(self.position, dstname)
            print(abs_objectname, abs_dstname, os.path.isfile(abs_objectname), os.path.isdir(abs_objectname),
                  os.path.isdir(abs_dstname))
            result = ''
            if os.path.isfile(abs_objectname):
                if os.path.isdir(abs_dstname) or not os.path.exists(abs_dstname):
                    shutil.move(abs_objectname, abs_dstname)
                    print('moving success')
                    result = 'moving success'

                elif os.path.isfile(abs_dstname):
                    print('moving cancel, file has been exits')
                    result = 'moving cancel, file has been exits'

            elif os.path.isdir(abs_objectname):
                if os.path.isdir(abs_dstname) or not os.path.exists(abs_dstname):
                    shutil.move(abs_objectname, abs_dstname)
                    print('moving success')
                    result = 'moving success'

                elif os.path.isfile(abs_dstname):
                    print('moving cancel, %s is file' % dstname)
                    result = 'moving cancel, %s is file' % dstname

            else:
                print('nothing done')
                result = 'nothing done'
            self.request.send(json.dumps(result).encode('utf-8'))

        except Exception as e:
            print(e)
            result = 'moving fail,' + e
            self.request.send(json.dumps(result).encode('utf-8'))

    def mkdir(self, *args):  ####创建目录
        try:
            dirname = args[0]['dirname']
            if dirname.isalnum():  ####判断文件是否只有数字和字母
                if os.path.exists(os.path.join(self.position, dirname)):
                    result = '%s have existed' % dirname
                else:
                    os.mkdir(os.path.join(self.position, dirname))
                    result = '%s created succes' % dirname
            else:
                result = 'Illegal character %s, dirname can only by string and num here.' % dirname
        except TypeError:
            result = 'please input dirname'
        self.request.send(json.dumps(result).encode('utf-8'))

    def rm(self, *args):  ####删除文件
        filename = args[0]['filename']
        confirm = args[0]['confirm']
        file_abspath = os.path.join(self.position, filename)
        if os.path.isfile(file_abspath):
            if confirm == True:
                os.remove(file_abspath)
                result = '%s have been delete.' % filename
            else:
                result = 'Not file deleted'
        elif os.path.isdir(file_abspath):
            result = '%s is a dir, plsese using rmdir' % filename
        else:
            result = 'File %s not exist!' % filename
        self.request.send(json.dumps(result).encode('utf-8'))

    def rmdir(self, *args):  ###删除目录
        dirname = args[0]['dirname']
        confirm = args[0]['confirm']
        file_abspath = os.path.join(self.position, dirname)
        if '.' in dirname or '/' in dirname:  ####不能跨目录删除
            result = 'should not rmdir %s this way' % dirname
        elif os.path.isdir(file_abspath):
            if confirm == True:
                shutil.rmtree(file_abspath)
                result = '%s have been delete.' % dirname
            else:
                result = 'Not file deleted'
        elif os.path.isfile(file_abspath):
            result = '%s is a file, not directory deleted' % dirname
        else:
            result = 'directory %s not exist!' % dirname
        self.request.send(json.dumps(result).encode('utf-8'))

    def auth(self):
        self.data = json.loads(self.request.recv(1024).decode('utf-8'))
        print(self.data)
        recv_username = self.data['username']
        recv_passwd = self.data['passwd']
        query_result = useropr.query_user(recv_username)
        print(query_result)
        if query_result == None:
            self.request.send(b'user does not exits')
        elif query_result['content']['passwd'] == recv_passwd:
            self.request.send(b'ok')
            return query_result  ####返回查询结果
        elif query_result['content']['passwd'] != recv_passwd:
            self.request.send(b'password error')
        else:
            self.request.send(b'unknown error')

    def handle(self):  ####处理类，调用以上方法
        # self.position = file_dir
        # print(self.position)
        auth_tag = False
        while auth_tag != True:
            auth_result = self.auth()  ####用户认证，如果通过，返回用户名，不通过为None
            print('the authentication result is:', auth_result)
            if auth_result != None:
                self.username = auth_result['content']['username']
                self.user_spacesize = auth_result['content']['spacesize']
                auth_tag = True
        print(self.username, self.user_spacesize)
        user_homedir = os.path.join(file_dir, self.username)
        if os.path.isdir(user_homedir):
            self.position = user_homedir  ####定锚，用户家目录
            print(self.position)
            while True:
                print('当前连接：', self.client_address)
                self.data = self.request.recv(1024).strip()
                print(self.data)
                logging.info(self.client_address)
                if len(self.data) == 0:
                    print('客户端断开连接')
                    break  ####检查发送来的命令是否为空
                cmd_dict = json.loads(self.data.decode('utf-8'))
                action = cmd_dict['action']
                logging.info(cmd_dict)
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dict)
                else:
                    print('未支持指令：', action)
                logging.info('current directory：%s' % self.position)


if __name__ == '__main__':
    ip, port = '0.0.0.0', 9999
    server = socketserver.ThreadingTCPServer((ip, port), MyTCPHandler)
    server.serve_forever()