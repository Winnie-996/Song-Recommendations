from DataInitialization import DataOperate


class TreeNode:
    def __init__(self, nodeName, parent=None):
        self.count = 1  # 计数
        self.name = nodeName  # 名字
        self.parent = parent  # 父节点
        self.children = []  # 子节点
        self.childrenName = []  # 子节点的游戏名称，方便查找


class ListNode:
    def __init__(self, content=None, nextNode=None):
        self.content = content
        self.nextNode = nextNode


def run():
    print("\n")
def fptree_create(minSupport):
    """
    :param minSupport: 最小支持度
    :return: root：FP-tree的根节点
             listHead: 链表头节点列表
             gameNameList：listHead与gameNameList一一对应，listHead中第i个头节点对应的游戏即为gameNameList中第i个游戏名
    """
    root = TreeNode("root")
    gameDict, userDict = DataOperate(minSupport)
    listTail, gameNameList = [], []
    for item in gameDict.keys():
        listTail.append(ListNode())
        gameNameList.append(item)
    listHead = listTail.copy()
    for key, values in userDict.items():
        # 构建FP-tree
        cursor = root
        for game in values:
            gameName_Index_in_List = gameNameList.index(game)  # 游戏名在gameNameList中的索引
            try:
                # 游戏名称在childrenName中表示有子节点
                index = cursor.childrenName.index(game)
                cursor.children[index].count += 1
                cursor = cursor.children[index]
            except Exception as E:
                # 游戏名称没有在childrenName中
                listLen = len(cursor.childrenName)
                cursor.childrenName.append(game)
                cursor.children.append(TreeNode(game))
                parentNode = cursor
                cursor.children[listLen].parent = parentNode
                cursor = cursor.children[listLen]
                listTail[gameName_Index_in_List].content = cursor
                listTail[gameName_Index_in_List].nextNode = ListNode()
                listTail[gameName_Index_in_List] = listTail[gameName_Index_in_List].nextNode
    return root, listHead, gameNameList


if __name__ == '__main__':
    root, listHead, gameNameList = fptree_create(5)

    # 示例代码
    # 获取fp-tree某一节点的子节点信息
    print("获取fp-tree某一节点的子节点信息")
    print(root.childrenName)
    # 链表使用
    print("链表使用")
    print("获取 Dota 2 游戏在gameNameList中的索引:%d"%(gameNameList.index("Dota 2")))
    print("获取 Dota 2 游戏对应的链表头节点")
    print(listHead[gameNameList.index("Dota 2")])
    # 用listHead[index].nextNode 访问链表的下一个节点
    # 用listHead[index].content 获取当前列表节点包含的fp-tree节点
