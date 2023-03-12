from random import shuffle
class Engine(object):
    def __init__(self, newyinwenlist, txt1, modes):
        self.New_WordDict = newyinwenlist
        self.modes = modes
        self.right_answer = 0
        self.txt1 = txt1   
    def again(self):
        global times,is_change_mode,time
        if self.modes == -1:
            self.txt1.close()
            return SystemError
        elif self.modes == 1:
            while times!=0:
                for yinwen, fanyi in self.New_WordDict.items():
                    print(f"题目:{yinwen}")
                    position = input('> ')
                    if position == "command change mode":
                        is_change_mode =1
                        self.modes = 0
                        print("原题目和答案进行切换")
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
                times-=1
                time+=1
                continue
        elif self.modes == 0:
            while times!=0:
                for yinwen, fanyi in self.New_WordDict.items():
                    print(f"题目:{fanyi}")
                    position = input('> ')
                    if position == "command change mode":
                        is_change_mode=1
                        self.modes = 1
                        print("原题目和答案进行切换")
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
                times -=1
                time +=1
                continue
        elif self.modes == 2:
            return [self.txt1, self.right_answer, self.New_WordDict, self.modes]
        self.modes =-2
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
        elif self.modes ==-2:
            return [self.New_WordDict, self.txt1, self.modes]
class Words(object):
    def __init__(self, txt_position, modes):
        self.txt = str(txt_position)
        self.WrodDict = {}
        self.WORDS = []
        self.WORDS2 = []
        self.yinwenlist = []
        self.newyinwenlist = {}
        self.txt1 = {}
        self.modes = modes
        self.lists = []
    def daluan(self):        
        print("使用command change mode可实现原题目和答案互换,使用command quit可重来或退出")
        if self.txt.startswith('"', 0, 1) == True:
            self.txt = self.txt.replace('"', '')
        self.txt1 = open(self.txt, encoding='utf-8')
        flag = 0
        for word in self.txt1.readlines():  
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
        for key in self.yinwenlist:
            self.newyinwenlist[key] = self.WrodDict[key]
        return [self.newyinwenlist, self.txt1, self.modes]
class Show(object):
    def __init__(self, txt_position, modes):
        global is_change_mode
        self.txt_position = txt_position
        self.a = Words(txt_position, modes).daluan()
        self.b = Engine(self.a[0], self.a[1], self.a[2]).again()
        is_change_mode=0
        self.c = Ended(self.b[0], self.b[1], self.b[2], self.b[3]).end()
    def to_again(self):
        try:
            global is_change_mode
            global txt_position
            global times,time
            while 1:
                self.b = Engine(self.c[0], self.c[1], self.c[2]).again()
                if is_change_mode ==1:
                    is_change_mode =0
                    self.c = Ended(self.b[0], self.b[1],self.b[2], self.b[3]).end()
                else:
                    break
            print(f"已完成{time}次复习,是否继续复习,是则请输入复习次数,换另一个复习文件请输入-1,退出复习请输入0")
            times = input(">")
            while len(times) == 0 or IsFloat(times) == True or int((times)) == ValueError:
                times = input("请输入数字>")
            times = int(times)
            if times==0:
                return SystemExit
            elif times==-1:
                txt_position = input("请输入文件路径或拖拽文件到此\n>")
                times = input("请问您想复习几轮>")
                while len(times) == 0 or IsFloat(times) == True or int((times)) == ValueError:
                    times = input("请输入数字>")
                times = int(times)
                time = 0
                return Show(txt_position, 1).to_again()
            else:
                print(f"继续复习{times}轮")
                time =0
                return Show(txt_position, 1).to_again()
        except SystemError:
            exit()
def IsFloat(str):  
    if str not in ',':
        return False
    s = str.split('.')
    if len(s) > 2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
            return True
txt_position = input("请输入文件路径或拖拽文件到此\n>")
times = input("请问您想复习几轮>")
while len(times) == 0 or IsFloat(times) == True or int((times)) == ValueError:
    times = input("请输入数字>")
    print("times 的数据", times)
times = int(times)
time = 0
is_change_mode = 0
Show(txt_position, 1).to_again()
