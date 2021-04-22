# 删除空白行


with open(r'D:\SGF\ViterbiTest\output\处理1.txt',"r",encoding="utf-8") as f:
    for line in f.readlines():
        if len(line)>2:
            print(line)
            with open(r'D:\SGF\ViterbiTest\output\最终文档.txt',"a+",encoding="utf-8") as f1:
                f1.write(line)
            f1.close()

f.close()