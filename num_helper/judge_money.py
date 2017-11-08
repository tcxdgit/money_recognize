# coding:utf-8
# author: Tian

class Judge(object):
    def __init__(self):
        self.moneyList = ['2', '0', '万', '4', '5', '7', '9', '两', '百', '三', '四', '五', '六',
                            '七', '八', '1', '3', '6', '一', '千', '九', '8', '十', '二', '几', '分',
                          '角', '毛', '块', '元', '零', '多', '把']

    def main(self, sen_cut, POS_list):
        '''
        :return: 判断句子是否涉及到数量词
        '''
        sentence = ''
        index0 = 0
        index_cut = []
        for cut in sen_cut:
            sentence += cut[0]
            index_cut.append((index0, cut[1]))
            index0 += len(cut[0])

        senList = list(sentence)
        marks = []
        for char in senList:
            if char in self.moneyList:
                mark = 1
            else:
                mark = 0
            marks.append(mark)
        index = 0
        indexList = []
        for mark in marks:
            if mark == 0:
                pass
            else:
                indexList.append(index)
            index += 1

        seg_idx = []
        if len(indexList) > 0:
            list_all = []
            list_part = [indexList[0]]

            # 把含有金额字表中字的索引切分出来，例如[[2,3,4],[6,7,8],[11,12]]
            for i in range(1, len(indexList)):
                if indexList[i] - indexList[i-1] == 1:
                    list_part.append(indexList[i])
                else:
                    list_all.append(list_part)
                    list_part = [indexList[i]]
            list_all.append(list_part)

            # 判断每个连续的索引片段是否是金额,'N'表示不是,'Y'表示是
            flags = []
            list0 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十']  # '零', '几'
            # list1 = ['百', '万', '千', '分', '角', '毛', '块', '元']
            for list_part in list_all:  # list_part = [4,5,6,7], list_all = [[4,5,6,7]]
                count1 = -1
                for indexs in index_cut:   # index_cut: [(0, 'r'), (1, 'v'), (2, 'n'), (4, 'm'), (7, 'q')]
                    count1 += 1
                    if indexs[0] in list_part:

                        # 判断分词出来片段里面的字是否都在moneyList里面，不是的话句子就直接False
                        inlist = 'True'
                        for char in sen_cut[count1][0]:
                            if char not in self.moneyList:
                                inlist = 'False'
                            else:
                                pass

                        if inlist == 'False':
                            continue
                        else:
                            pos = [indexs[0]]

                        # 判断是否包含数量词
                        count = 0
                        for i in list_part:
                            if senList[i] in list0:  # 判断是否涉及数量
                                count += 1
                            else:
                                pass
                        if count > 0:
                            pos.append('C')  # 'C'表示有确定性数字
                        else:
                            pos.append('F')  # 'F'表示没有确定性数字

                        # 判断词性
                        flag = indexs[1]
                        if flag not in POS_list:     # 词性，换分词器的话，改这里！
                            pos.append('N')     # 'N'表示不是数词
                        else:
                            pos.append('Y')     # 'Y'表示是数词

                        flags.append(pos)

                    else:
                        pass

            result = 'False'

            for flag_part in flags:
                if 'Y' in flag_part and 'C' in flag_part:
                    result = 'True'
                    break
                elif 'Y' in flag_part and 'F' in flag_part:
                    result = 'Fuzzy'
                else:
                    pass

            for flag_part in flags:
                if 'Y' in flag_part and 'C' in flag_part:
                    seg_idx.append(flag_part[0])
                else:
                    pass

        else:
            result = 'False'

        return result, seg_idx

if __name__ == '__main__':
    judge = Judge()
    # 参数：结巴分词后的结果sen_cut, 数词词性POS_list
    # result:
    # True：有确定的数量词
    # Fuzzy：词性中有数词，但是没有确定的数量词
    # False：没有数词，或者分词后的字不全在字表里
    # idx_list:数量词的起始索引,list
    result, idx_list = judge.main([('我', 'r'), ('要', 'v'), ('存', 'v'), ('15001', 'm'), ('块', 'q')], ['m'])
    print(result, idx_list)


