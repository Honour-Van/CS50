import paddlehub as hub

senta = hub.Module(name="senta_bilstm")
test_text = [
    "这个宾馆比较陈旧了，特价的房间也很一般。总体来说一般", 
    "交通方便；环境很好；服务态度很好房间较小",
    "稍微重了点，可能是硬盘大的原故，还要再轻半斤就好了。" ,
    "服务很不错，下次还会来。" ,
    "前台接待太差，下次不会再选择入住此店啦", 
    "菜做的很好，味道很不错。" ,
    "19天硬盘就罢工了，算上运来的一周都没用上15天，你说这算什么事呀",
    "现在是高峰期，人太多了，我们晚点来吧"
]
input_dict = {"text": test_text}
results = senta.sentiment_classify(data=input_dict)

for result in results:
    print(result)
    print(result['text'])
    print(result['sentiment_label'])
    print(result['sentiment_key'])
    print(result['positive_probs'])
    print(result['negative_probs'])
