import paramiko
import datetime
import os

hostname = '192.168.10.202'
username = 'mapreduce'
password = 'mapreduce'
port = 22
local_dir = r'D:\photo\test'

# windows文件夹所在位置
local_dir_csv = local_dir + "\csv"
local_dir_config = local_dir + "\config"
local_dir_etc = local_dir + "\etc"
local_dir_ini = local_dir + "\ini"
local_dir_script = local_dir + "\script"
local_dir_soft = local_dir + "\soft\\3.0"
local_dir_tcc = local_dir + "\\tcc\cfg"

# linux端所在位置
remote_dir = '/home/mapreduce/test/'
remote_dir_config = '/home/trade/test/backup/config/xml_trade/'
remote_dir_csv = '/home/trade/test/backup/csv/csv_trade/'
remote_dir_ini = '/home/trade/test/backup/ini/ini_trade/'
remote_dir_soft = '/home/trade/test/backup/soft/3.9.0/'
remote_dir_script = '/home/trade/test/sql/'
remote_dir_tcc = '/home/trade/test/cfg/'
remote_dir_etc = '/home/trade/test/backup/etc/'


def upload(local_dir, remote_dir):
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print(1)
        print('upload file start %s ' % datetime.datetime.now())
        for root, dirs, files in os.walk(local_dir):
            print('[root%s][dirs%s][files%s]' % (root, dirs, files))
            for filespath in files:
                local_file = os.path.join(root, filespath)
                print(11, '[%s][%s][%s][%s]' % (root, filespath, local_file, local_dir))
                a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                print('01', a, '[%s]' % remote_dir)
                remote_file = os.path.join(remote_dir, a)
                print(22, remote_file)
                try:
                    sftp.put(local_file, remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file, remote_file)
                    print("66 upload %s to remote %s" % (local_file, remote_file))
            for name in dirs:
                local_path = os.path.join(root, name)
                print(0, local_path, local_dir)
                a = local_path.replace(local_dir, '').replace('\\', '')
                print(1, a)
                print(1, remote_dir)
                remote_path = os.path.join(remote_dir, a)
                print(33, remote_path)
                try:
                    sftp.mkdir(remote_path)
                    print(44, "mkdir path %s" % remote_path)
                except Exception as e:
                    print(55, e)
        print('77,upload file success %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(88, e)


if __name__ == '__main__':
    # local_dir = r'E:\work\tmp'
    # remote_dir = '/home/trade/test/'     #只支持一级目录
    upload(local_dir, remote_dir)
    '''
    print(local_dir_soft)
    upload(local_dir_config, remote_dir_config)
    upload(local_dir_csv, remote_dir_csv)
    upload(local_dir_ini, remote_dir_ini)
    upload(local_dir_etc, remote_dir_etc)
    upload(local_dir_tcc, remote_dir_tcc)
    upload(local_dir_soft, remote_dir_soft)
    upload(local_dir_script, remote_dir_script)
    '''