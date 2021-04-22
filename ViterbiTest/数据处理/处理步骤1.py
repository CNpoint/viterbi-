#删除不必要字符

import re
with open(r'D:\SGF\ViterbiTest\data\199801.txt',"r",encoding="GBK") as f:
    text = f.read()
    text = text.replace(' ', '\n')
    # for line in text:
    strl = re.sub("\[", "", text)
    strl = re.sub("]nt", "", strl)
    strl = re.sub("]ns", "", strl)
    strl = re.sub("]nz", "", strl)
    strl = re.sub("]l", "", strl)
    strl = re.sub("]i", "", strl)
    strl = re.sub("\n", "@", strl)
    strl = re.sub("\s+", " ", strl)
    strl = re.sub("@", "\n", strl)
    strl = re.sub(" \n", "\n", strl)
    strl = re.sub(" ", "@", strl)
    strl = re.sub("\s+", "\n", strl)
    strl = re.sub("@", " ", strl)

    print(text)
    with open(r'D:\SGF\ViterbiTest\output\处理1.txt',"a+",encoding="utf-8") as f1:
        f1.write(text)
    f1.close()
f.close()