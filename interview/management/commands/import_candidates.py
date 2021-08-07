# coding: utf-8
# 通过excel导入候选人信息
# python manage.py import_candidates --path file.csv
import csv
from django.core.management import BaseCommand
from interview.models import Candidate


class Command(BaseCommand):
    """ 将CSV文件中的候选人信息导入到数据库中
    """
    help = '从一个CSV文件的内容中读取候选人列表，导入到数据库中'

    def add_arguments(self, parser):
        """
        接收命令行参数
        Args:
            parser: 命令行参数
        """
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        """处理CSV文件解析的命令
        根据命令行的字符串解析命令行参数
        Args:
            args:
            kwargs: 命令行参数
        """
        path = kwargs['path']
        # with open(path , 'rt', encoding='gbk') 已gbk的字符集读取
        with open(path, 'rt') as f:
            # csv.reader(f, dialect='excel',delimiter=';') 解析excel格式以;为分隔符
            reader = csv.reader(f, dialect='excel')  # 执行解析excel格式
            for row in reader:
                candite = Candidate.objects.create(
                    username=row[0],
                    city=row[1],
                    phone=row[2],
                    bachelor_school=row[3],
                    major=row[4],
                    degree=row[5],
                    test_score_of_general_ability=row[6],
                    paper_score=row[7]
                )
