# coding:utf-8
import logging
import time
import datetime
import os

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个


class Log:
    def __init__(self):
        self.logName = os.path.join(log_path, '%s.log' % time.strftime('%Y-%m-%d'))  # 文件的命名
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')  # 日志输出格式
        self.remove_logs()

    def TimeStampToTime(self, timestamp):
        """格式化时间"""
        timeStruct = time.localtime(timestamp)
        return str(time.strftime('%Y-%m-%d', timeStruct))

    def remove_logs(self):
        """到期删除日志文件"""
        dir_list = ['logs']  # 要删除文件的目录名
        for dir in dir_list:
            dirPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/' + dir  # 拼接删除目录完整路径
            file_list = os.listdir(dirPath)  # 返回目录下的文件list
            for i in file_list:
                file_path = os.path.join(dirPath, i)  # 拼接文件的完整路径
                t_list = self.TimeStampToTime(os.path.getctime(file_path)).split('-')
                now_list = self.TimeStampToTime(time.time()).split('-')
                t = datetime.datetime(int(t_list[0]), int(t_list[1]), int(t_list[2]))  # 将时间转换成datetime.datetime 类型
                now = datetime.datetime(int(now_list[0]), int(now_list[1]), int(now_list[2]))
                if (now - t).days > 6 or os.path.getsize(file_path) > 1048576:  # 时间大于6天，大小大于1m删除
                    os.remove(file_path)
            if len(file_list) > 4: # 日志和报告超过四条的删除
                file_list = file_list[0:-4]
                for i in file_list:
                    file_path = os.path.join(dirPath, i)  # 拼接文件的完整路径
                    os.remove(file_path)

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.logName, 'a')  # 追加模式  这个是python2的
        fh = logging.FileHandler(self.logName, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()  # 关闭打开的文件

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)
#
#
# if __name__ == "__main__":
#     log = Log()
#     log.info("---测试开始----")
#     log.info("公众号：%d 爬取开始" % 123)
#
#     log.remove_logs()
#     log.warning("----测试结束----")