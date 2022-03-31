"""
    程序功能： 游戏推荐展示
    作者：覃瀚辉
    时间：2021.12.15
"""

import wx
import csv

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='音乐推荐')
        self.data = self.loadSimpDat()
        self.com_game = self.recommend()
        panel = wx.Panel(self)
        panel.SetBackgroundColour([38,50,56])
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel,style=wx.TE_MULTILINE)
        font1 = wx.Font(15, wx.MODERN, wx.LIGHT, wx.NORMAL, False, 'Times New Roman')
        self.text_ctrl.SetFont(font1)
        self.text_ctrl.AppendText('Enter the games you have played')
        self.text_ctrl.SetBackgroundColour([255, 255, 229])
        my_sizer.Add(self.text_ctrl, 5, wx.ALL | wx.EXPAND, 5)
        my_btn = wx.Button(panel, label='推荐')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        self.text_ctrl2 = wx.TextCtrl(panel,style=wx.TE_MULTILINE)
        self.text_ctrl2.SetFont(font1)
        self.text_ctrl2.AppendText('Recommended Games')
        self.text_ctrl2.SetBackgroundColour([255, 255, 229])
        my_sizer.Add(self.text_ctrl2, 5, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def loadSimpDat(self):
        """
        :return:返回原始数据
        """
        dataSet = []
        with open('outputdata/like_song.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                dataSet.append(row)
        return dataSet

    def recommend(self):
        """
        :return:可能玩的游戏
        """
        dataSet = []
        with open('outputdata/tuijian_song.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                dataSet.append(row)
        return dataSet

    def RecommendDault(self):
        """
        :return:默认推荐游戏(排名前20)
        """
        dataSet = []
        with open('outputdata/tuijian_default.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                dataSet.append(row)
        return dataSet

    def on_press(self, event):
        keyword_str = self.text_ctrl.Value
        keyword_str = keyword_str.strip()#除去首尾空格
        keyword_list = keyword_str.split('\n')
        index = 0
        tuijian_str = ''
        tuijian_list = []
        for row in self.data:
            # 如果全部符合 直接加入
            if keyword_list == row:
                for va in self.com_game[index]:
                    va = va.strip()
                    tuijian_list.append(va)
            # 部分符合也推荐
            for keyword in keyword_list:
                if (keyword in row) or (keyword == row):
                    for va in self.com_game[index]:
                        va = va.strip()
                        tuijian_list.append(va)
            index += 1
        tuijian_list = list(set(tuijian_list))
        # 没找到推荐的，就推荐默认的
        if len(tuijian_list) == 0:
            Dault_String = ''
            Dault_list = self.RecommendDault()
            index = 0
            for row in Dault_list:
                Dault_String += str(index + 1) + '. '
                Dault_String += str(row[0])
                Dault_String += '\n'
                index += 1
            self.text_ctrl2.SetValue(Dault_String)
        else:
            #找到推荐了 就推荐有的
            index = 0
            for va in tuijian_list:
                if va != '':
                    tuijian_str += str(index + 1) + '. '
                    tuijian_str += va
                    tuijian_str += '\n'
                    tuijian_str.strip()
                    index += 1
            self.text_ctrl2.SetValue(tuijian_str)
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()