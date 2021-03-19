import jieba.posseg
import jieba
jieba.add_word('这是')
print(jieba.lcut('这是菜鸡'))
words = jieba.posseg.lcut('这是菜鸡！')
print(words)
print(dict(words))
