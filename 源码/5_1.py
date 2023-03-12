#增加抽背，全背功能
from random import shuffle


class Engine(object):
    def __init__(self, newyinwenlist, txt1, modes):
        self.New_WordDict = newyinwenlist
        self.modes = modes
        self.right_answer = 0
        self.txt1 = txt1

    def again(self):
        if self.modes == -1:
            self.txt1.close()
            return [self.txt1, self.right_answer, self.New_WordDict, self.modes]
        elif self.modes == 1:
            for yinwen, fanyi in self.New_WordDict.items():
                print(f"题目:{yinwen} 模式1")
                position = input('> ')
                if position == "command change mode":
                    self.modes = 0
                    print("切换为中译英")
                    return [self.txt1, self.right_answer, self.New_WordDict, self.modes]

                elif position in fanyi:
                    print("正确")
                    print(f"答案:{fanyi}")
                    self.right_answer += 1
                elif position == "command quit":
                    self.modes = 2
                    return [self.txt1, self.right_answer, self.New_WordDict, self.modes]
                elif position not in fanyi and position != "change mode":
                    print("错误")
                    print(f"答案:{fanyi}")
        elif self.modes == 0:
            for yinwen, fanyi in self.New_WordDict.items():
                print(f"题目:{fanyi} 模式2")
                position = input('> ')
                if position == "command change mode":
                    self.modes = 1
                    print("切换为英译中")
                    return [self.txt1, self.right_answer, self.New_WordDict, self.modes]
                elif position == yinwen:
                    print("正确")
                    self.right_answer += 1
                elif position == "command quit":
                    self.modes = 2
                    return [self.txt1, self.right_answer, self.New_WordDict, self.modes]
                elif position != yinwen and position != "change mode":
                    print("错误")

                print(f"答案:{yinwen}")
        elif self.modes == 2:
            return [self.txt1, self.right_answer, self.New_WordDict, self.modes]


class Ended(object):
    def __init__(self, txt1, right_answer, New_WordDict, modes):
        self.txt1 = txt1
        self.modes = modes
        self.right_answer = right_answer
        self.New_WordDict = New_WordDict

    def end(self):
        if self.modes == 2:
            print(f"共答对{self.right_answer}次\n是否再试一次(y\\n)")
            choice = input(">")
            if choice in "yes":
                print("好的")
                self.modes = 1
                return [self.New_WordDict, self.txt1, self.modes]
            else:
                self.modes = -1
                return [self.New_WordDict, self.txt1, self.modes]
        elif self.modes == 0 or self.modes == 1:
            return [self.New_WordDict, self.txt1, self.modes]


class Words(object):
    def __init__(self, txt_position, modes):
        self.txt = str(txt_position)
        self.WrodDict = {}
        self.WORDS = []
        self.WORDS2 = []
        self.yinwenlist = []
        self.newyinwenlist = []
        self.txt1 = {}
        self.modes = modes

    def daluan(self):        # BASE_DIR = path.dirname(path.abspath(__file__))
        print("使用command change mode可实现中英互换,使用command quit可重来或退出")
        if self.txt.startswith('"', 0, 1) == True:
            self.txt = self.txt.replace('"', '')
        self.txt1 = open(self.txt, encoding='utf-8')
        flag = 0
        for word in self.txt1.readlines():  # 逐行读取
            if flag == 0:
                self.WORDS.append(str(word.strip()))
                flag = 1
            else:
                self.WORDS2.append(str(word.strip()))
                flag = 0
        for i in range(0, len(self.WORDS)):
            self.WrodDict[self.WORDS[i]] = self.WORDS2[i]
        self.yinwenlist = list(self.WrodDict.keys())
        shuffle(self.yinwenlist)
        self.newyinwenlist = {}
        for key in self.yinwenlist:
            self.newyinwenlist[key] = self.WrodDict[key]
        return [self.newyinwenlist, self.txt1, self.modes]
# ended需要txt1,right_answer,New_WordDict,mode
# Engine需要newyinwenlist,txt1,mode


class Show(object):

    def __init__(self, txt_position, modes):
        # Words().daluan()返回 newyinwenlist,txt1,modes
        self.a = Words(txt_position, modes).daluan()
        self.b = Engine(self.a[0], self.a[1], self.a[2]).again()
        self.c = Ended(self.b[0], self.b[1], self.b[2], self.b[3]).end()

    def to_again(self):
        try:
            while 1:
                self.b = Engine(self.c[0], self.c[1], self.c[2]).again()
                self.c = Ended(self.b[0], self.b[1],
                               self.b[2], self.b[3]).end()
        except TypeError:
            exit()


txt_position = input("请输入文件路径或拖拽文件到此\n>")
Show(txt_position, 1).to_again()
# 二次转换mode的值导致不能出现双模式
#
