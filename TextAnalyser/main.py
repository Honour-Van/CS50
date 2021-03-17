import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class TextAnalyser(object):
    """
    # 基于jieba分词的文本分析器类
    """
    def __init__(self, text_filename):
        self.txt_filename = text_filename
        self.ignore_list = []
        self.minlen = 2
        self.maxlen = 100

        self.cloud_material = ""
        self.word_dict = {} # 用字典统计每个词的出现次数


    def set_len_range(self, minlen, maxlen):
        """
        # set_len_range
        设定分词筛选长度，获取制定长度区间的词语结果
        """
        self.minlen=minlen
        self.maxlen=maxlen
        
    def set_ignore_list(self, ignore_config_file='ignore_list.txt') -> list:
        """
        # set_ignore_list
        从配置文件中读取信息，设定 ignore_list ，以便更好地获取分词结果
        """
        with open(ignore_config_file, 'r') as f:
            self.ignore_list = f.readline().strip()
        return self.ignore_list
    
    def set_syno_dict(self):
        """
        # set_syno_list
        设定同义词列表，从而实现合并
        """
        
    def analyse(self, content):
        """
        docstring
        """
        # 分词
        word_list = jieba.lcut(content)

        for w in word_list:
            # 跳过单字
            if not self.minlen <= len(w) <= self.maxlen:
                continue
            
            # 跳过不想统计的词
            if w in self.ignore_list:
                continue

            # 已在字典中的词，将出现次数增加1；否则，添加进字典，次数记为1
            self.word_dict[w] = self.word_dict.get(w, 0) + 1

            self.cloud_material = self.cloud_material + " " + w

        
    def readfile(self, bigfile=False):
        """
        docstring
        """
        if bigfile:
            pass
        else:
            # 从文件读取文本
            txt_file = open(self.txt_filename, 'r', encoding='utf-8')
            content = txt_file.read()
            txt_file.close()



    def get_wordcloud(self):
        """
        docstring
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
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.savefig('./wordcloud.png', bbox_inches='tight')
        
    def get_result(self, result_filename='./output.csv'):
        """
        docstring
        """
        # 把字典转成列表，并按原先“键值对”中的“值”从大到小排序
        items_list = list(self.word_dict.items())
        items_list.sort(key=lambda x: x[1], reverse=True)

        total_num = len(items_list)
        print('经统计，共有' + str(total_num) + '个不同的词')
        # 根据用户需求，打印排名前列的词，同时把统计结果存入文件
        num = input('您想查看前多少个词语？[10]:')
        if not num.isdigit() or num == '':  # 如果输入的不全是数字，或者直接按了回车
            num = 10  # 设成查看前10名
        else:
            num = int(num)  # 如果输入了正常的数字，则按用户需求设置

        with open(result_filename, 'w') as f:  # 新建结果文件
            f.write('词语, 词频\n')  # 写入标题行

            for i in range(num):
                word, cnt = items_list[i]
                message = str(i+1) + '. ' + word + '\t' + str(cnt)
                print(message)
                f.write(word + ',' + str(cnt) + '\n')

        print('已写入文件：' + result_filename)


if __name__ == "__main__":
    analyser = TextAnalyser('./srt/raw.txt')