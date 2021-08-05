# coding: utf-8
# 通过excel导入候选人信息
# python manage.py import_candidates --path file.csv
import csv
from django.core.management import BaseCommand
from interview.model import Candiate

class Command(BaseCommand):
    """ 将CSV文件中的候选人信息导入到数据库中
    """
    help = '从一个CSV文件的内容中读取候选人列表，导入到数据库中'

    def add_arguments(self,parser):
        """
        接收命令行参数
        Args:
            parser: 命令行参数
        """
        parser.add_argument('--path',type=str)

    def handle(self,*args, **kwargs):
        """处理CSV文件解析的命令
        根据命令行的字符串解析命令行参数
        Args:
            args:
            kwargs:
        """
        path = kwargs['path']
        with open(path,'rt') as f:
            reader = csv.reader(f, dialect='excel') #执行解析excel格式
            for fow in reader:
                print(row[0])