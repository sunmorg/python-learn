# -*- coding:utf-8 -*-
# Author：sunmorg

import os, hashlib, time, pickle, shutil, configparser, logging

####读取配置文件####
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'conf/server.conf')
cf = configparser.ConfigParser()
cf.read(config_file)
####设定日志目录####
if os.path.exists(cf.get('log', 'usermgr_log')):
    logfile = cf.get('log', 'usermgr_log')
else:
    logfile = os.path.join(base_dir, 'log/usermgr.log')
####设定用户上传文件目录，这边用于创建用户家目录使用####
if os.path.exists(cf.get('upload', 'upload_dir')):
    file_dir = cf.get('upload', 'upload_dir')
else:
    file_dir = os.path.join(base_dir, 'user_files')
####设定用户信息存储位置####
if os.path.exists(cf.get('db', 'db_dir')):
    db_path = cf.get('db', 'db_dir')
else:
    db_path = os.path.join(base_dir, 'db')


def hashmd5(*args):  ####用于加密密码信息
    m = hashlib.md5()
    m.update(str(*args).encode())
    return m.hexdigest()


class useropr(object):
    def __init__(self, user_name, passwd='123456', phone_number=''):
        self.user_name = user_name
        self.id = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.phone_number = phone_number
        self.passwd = passwd
        self.space_size = 104857600  ####初始分配100MB存储空间
        self.member_level = 1  ####会员等级，初始为1，普通会员

    @staticmethod  ####使用静态方法，可以直接用类命调用，如user.search_user(username)，否则需要实例化一个对象后才能调用
    def query_user(user_name):  ####查询用户
        db_filelist = os.listdir(db_path)
        # print(db_filelist)
        dict = {}
        for filename in db_filelist:
            with open(os.path.join(db_path, filename), 'rb') as f:
                content = pickle.load(f)
                # print(filename,content)    ####开启会打印出所有用户信息
                if content['username'] == user_name:
                    # print(filename, content)
                    dict = {'filename': filename, 'content': content}
                    return dict

    def save_userinfo(self):  ####保存用户信息
        query_result = self.query_user(self.user_name)  ####检查是否已存在同名用户，如果没有查询结果应该为None
        if query_result == None:
            user_info = {
                'username': self.user_name,
                'id': self.id,
                'phonenumber': self.phone_number,
                'passwd': hashmd5(self.passwd),
                'spacesize': self.space_size,
                'level': self.member_level
            }
            with open(os.path.join(db_path, self.id), 'wb') as f:
                pickle.dump(user_info, f)
                print('用户信息保存完毕')
                try:  ####创建用户家目录
                    os.mkdir(os.path.join(file_dir, self.user_name))
                    print('用户目录创建成功！')
                except Exception as e:
                    print('用户目录创建失败,', e)

        else:
            print('用户名重复，信息未保存')

    @staticmethod
    def change_info(user_name, **kwargs):  ####修改信息
        query_result = useropr.query_user(user_name)  ####用于检测用户是否存在,不存在不处理
        if query_result != None:
            userinfo_filename = query_result['filename']
            user_info = query_result['content']
            print('before update:', user_info)
            for key in kwargs:
                if key in ('username', 'id'):  ####用户名和ID不可更改
                    print(key, '项不可更改')
                elif key in ('passwd', 'phonenumber', 'spacesize', 'level'):  ####允许修改的键值
                    if key == 'passwd':
                        user_info[key] = hashmd5(kwargs[key])  ####加密密码保存
                    else:
                        user_info[key] = kwargs[key]
                    with open(os.path.join(db_path, userinfo_filename), 'wb') as f:
                        pickle.dump(user_info, f)
                        print(key, '项用户信息变更保存完毕')
                else:
                    print('输入信息错误，', key, '项不存在')
            print('after update:', user_info)
        else:
            print('用户不存在')

    @staticmethod
    def delete_user(user_name):  ####删除用户
        query_result = useropr.query_user(user_name)  ####用于检测用户是否存在,不存在不处理
        if query_result != None:
            userinfo_filename = query_result['filename']
            userfile_path = os.path.join(db_path, userinfo_filename)
            os.remove(userfile_path)
            query_result_again = useropr.query_user(user_name)
            if query_result_again == None:
                print('用户DB文件删除成功')
                try:
                    shutil.rmtree(os.path.join(file_dir, user_name))
                    print('用户家目录删除成功')
                except Exception as e:
                    print('用户家目录删除失败：', e)
            else:
                print('用户DB文件删除失败')

        else:
            print('用户不存在或者已经被删除')

    @staticmethod
    def query_alluser():  ####查询所有用户信息，用于调试使用
        db_filelist = os.listdir(db_path)
        for filename in db_filelist:
            with open(os.path.join(db_path, filename), 'rb') as f:
                content = pickle.load(f)
                print(filename, content)

    @staticmethod
    def interactive():
        '''使用说明：
        新增用户请输入类似： a=useropr(username,passwd)
                            a.save_userinfo()
        查询用户请输入：useropr.query_user(username)
        更改用户信息请输入：useropr.change_info(username,id=123,level=1,passwd=123,phonenumber=123),其中字典部分为可选项
        用户删除请输入:useropr.delete_user(username)
        '''
        info = '''
        1、新增用户
        2、查询用户
        3、修改用户
        4、删除用户
        退出请按q
        '''

        # useropr.query_alluser()        ####查询所有用户信息，调试用

        while True:
            print(info)
            choice = input('请输入你的选择:').strip()
            # print('operation choice: %s' % choice)
            if choice == 'q':
                exit()
            else:
                username = input('请输入用户名：').strip()
                # print('username: %s' % username)
                if username == '':
                    print('用户不能为空')
                    continue
                elif choice == '1':
                    passwd = input('请输入密码：')
                    new_user = useropr(username, passwd)
                    new_user.save_userinfo()

                elif choice == '2':
                    print(useropr.query_user(username))

                elif choice == '3':
                    update_item = input('请输入要修改的项目，例如：level,passwd,phonenumber：')
                    print('update item: %s' % update_item)
                    update_value = input('请输入要修改的项目新值：')
                    useropr.change_info(username, **{
                        update_item: update_value})  #### ‘**{}’ 不加**系统无法识别为字典。不能直接使用update_item=update_value，update_item会直接被当成key值，而不是其中的变量。

                elif choice == '4':
                    useropr.delete_user(username)

                else:
                    print('输入错误')
                    continue


if __name__ == '__main__':
    useropr.interactive()