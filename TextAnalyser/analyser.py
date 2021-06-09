'''
a Text Analyser based on jieba
@code: by 范皓年 1900012739 电子学系
'''

from os import name
import jieba
import jieba.posseg as pseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json


class TextAnalyser(object):
    """
    ## 基于jieba分词的文本分析器对象类
    构建对象之后，调用其start函数即可开始运行
    """

    def __init__(self, text_filename):
        '''
        ## 构造函数
        @param 
        @ text_filename：待分析的文件名称
        @ ignore_list：需要忽略的无实意词语
        @ syno_dict：需要替换的同义词词典
        @ cloud_material: 用于生成词云的长字符串
        @ word_dict: 各分词的词频保存在此
        '''
        self.txt_filename = text_filename
        self.ignore_list = []
        self.syno_dict = {}
        self.cloud_material = ""
        self.word_dict = {}  # 用字典统计每个词的出现次数

    def set_ignore_list(self, ignore_config_file='ignore_list.txt') -> list:
        """
        ## set_ignore_list
        从配置文件中读取信息，设定 ignore_list ，以便更好地获取分词结果
        """
        with open(ignore_config_file, 'r') as f:
            self.ignore_list = f.readline().strip()
        return self.ignore_list

    def set_syno_dict(self):
        """
        ## set_syno_list
        设定同义词列表，从而实现语词的同义合并
        """
        with open('syno_dict.json', 'r', encoding='utf-8') as f:
            self.syno_dict = json.load(f)

    def analyse(self, content, minlen=2, maxlen=10, nr=False):
        """
        ## analyse
        用于将输入的字符串进行有效的分词与过滤
        @param
        @ minlen & maxlen：满足条件的词语的字数
        @ nr：是否启动人名模式
        """
        # 分词
        print("word cutting...")
        word_list = jieba.lcut(content)
        if len(word_list):
            print("word cutting finished")

        if nr:
            print("word tagging...")
            psg_dict = dict(pseg.lcut(content))
            if len(psg_dict):
                print("word tagging finished")
            minlen = 2
            maxlen = 3

        for w in word_list:
            # 选出合适长度的
            if not minlen <= len(w) <= maxlen:
                continue
            # 跳过不想统计的词
            if w in self.ignore_list:
                continue

            if w in self.syno_dict:
                w = self.syno_dict[w]

            if nr:
                if w in psg_dict:
                    if psg_dict[w] != 'nr':
                        continue
                else:
                    continue

            # 已在字典中的词，将出现次数增加1；否则，添加进字典，次数记为1
            self.word_dict[w] = self.word_dict.get(w, 0) + 1
            # 将符合分词目标的词筛选出来作为词云素材
            self.cloud_material = self.cloud_material + " " + w

    def start(self, minlen=2, maxlen=10, bigfile=False, ignore=True, syno=True, show=True, nameren=False):
        """
        ## start
        基于已设定参数启动文本分析功能
        @param
        @ minlen & maxlen：最小最大字长
        @ bigfile：是否启动大文件读取模式
        @ ignore：是否弃用忽略列表
        @ syno：是否弃用同义词替换
        @ show：是否呈现结果
        @ nameren：是否启用人名模式
        """
        if ignore:
            self.set_ignore_list()
        if syno:
            self.set_syno_dict()

        if bigfile:
            with open(self.txt_filename, 'r', encoding='utf-8') as f:
                for line in f:
                    self.analyse(line, minlen=minlen,
                                 maxlen=maxlen, nr=nameren)
        else:
            # 从文件读取文本
            txt_file = open(self.txt_filename, 'r', encoding='utf-8')
            content = txt_file.read()
            txt_file.close()
            self.analyse(content, minlen=minlen, maxlen=maxlen, nr=nameren)
        if show:
            self.get_result()
            self.get_wordcloud()

    def get_wordcloud(self):
        """
        # get_wordcloud
        获得词云
        """
        wordcloud = WordCloud(
            # 生成中文字的字体,必须要加,不然看不到中文
            font_path="C:\Windows\Fonts\simhei.ttf"
        ).generate(self.cloud_material)
        image_produce = wordcloud.to_image()
        plt.figure(1)
        plt.imshow(image_produce)
        plt.axis('off')
        # plt.show() # 如果加这一句那么不能存图片

        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1,
                            left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.savefig('./wordcloud.png', bbox_inches='tight')

    def get_result(self, result_filename='./output.csv'):
        """
        # get_result
        打印结果，并输出到csv文件当中
        """
        # 把字典转成列表，并按原先“键值对”中的“值”从大到小排序
        items_list = list(self.word_dict.items())
        items_list.sort(key=lambda x: x[1], reverse=True)

        total_num = len(items_list)
        print('经统计，共有' + str(total_num) + '个不同的词')
        # 根据用户需求，打印排名前列的词，同时把统计结果存入文件
        num = input('您想查看前多少个词语？[10]: ')
        if not num.isdigit() or num == '':  # 如果输入的不全是数字，或者直接按了回车
            num = 10  # 设成查看前10名
        else:
            num = int(num)  # 如果输入了正常的数字，则按用户需求设置

        with open(result_filename, 'w') as f:  # 新建结果文件
            f.write('词语, 词频\n')  # 写入标题行
            print('位次\t词语\t\t词频')
            for i in range(num):
                word, cnt = items_list[i]
                message = str(i+1) + '\t' + word + '\t\t' + str(cnt)
                print(message)
                f.write(word + ',' + str(cnt) + '\n')

        print('已写入文件：' + result_filename)


if __name__ == "__main__":
    analyser = TextAnalyser('./红楼梦.txt')
    analyser.start(nameren=True)
