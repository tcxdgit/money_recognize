# coding:utf-8
# author: Tian
# 对句子进行判断，看是否涉及到金额
# 涉及到金额的话，将金额转换成数字

import os,sys
sys.path.append("../..")
from benebot_prep.num_helper.judge_money import Judge
from benebot_prep.num_helper.money2digit import trans_money

class seg_digit():
    def __init__(self):
        self.money_list = ['2', '0', '万', '4', '5', '7', '9', '两', '百', '三', '四', '五', '六',
                      '七', '八', '1', '3', '6', '一', '千', '九', '8', '十', '二', '分',
                      '角', '毛', '块', '元', '零', '加', '又', '亿']

        self.special = ['多', '几']

        self.special2 = ['分', '角', '毛', '块', '元']

    def seg2digit(self, sen_cut, POS_list):

        # 把'多'替换成具体数值
        idx = 0
        new_sen_cut = []
        num_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for cut in sen_cut:
            cut = list(cut)
            chars = cut[0]
            if '多' in chars:
                idx_p = chars.index('多')
                if idx_p > 0:
                    if chars[idx_p-1] == '十':
                        cut[0] = chars.replace('多', '五')
                    elif chars[idx_p-1] == '百':
                        cut[0] = chars.replace('多', '五十')
                    elif chars[idx_p - 1] == '千':
                        cut[0] = chars.replace('多', '五百')
                    elif chars[idx_p - 1] == '万':
                        cut[0] = chars.replace('多', '五千')
                    elif chars[idx_p - 1] == '亿':
                        cut[0] = chars.replace('多', '五万')

                    # 数字情况
                    if idx_p > 1 and (chars[idx_p-1] == '0') and (chars[idx_p-2] in num_list):
                        num = int(chars[idx_p-2:idx_p])
                        num = num+5
                        num = str(num)
                        cut[0] = chars.replace(chars[idx_p-2:idx_p+1], num)
                    elif idx_p > 2 and (chars[idx_p-2:idx_p] == '00') and (chars[idx_p-3] in num_list):
                        num = int(chars[idx_p - 3:idx_p])
                        num = num + 50
                        num = str(num)
                        cut[0] = chars.replace(chars[idx_p - 3:idx_p + 1], num)
                    elif idx_p > 3 and (chars[idx_p-3:idx_p] == '000') and (chars[idx_p-3] in num_list):
                        num = int(chars[idx_p - 4:idx_p])
                        num = num + 500
                        num = str(num)
                        cut[0] = chars.replace(chars[idx_p - 4:idx_p + 1], num)
                    elif idx_p > 4 and (chars[idx_p-4:idx_p] == '0000') and (chars[idx_p-4] in num_list):
                        num = int(chars[idx_p - 5:idx_p])
                        num = num + 5000
                        num = str(num)
                        cut[0] = chars.replace(chars[idx_p - 5:idx_p + 1], num)
                    elif idx_p > 8 and (chars[idx_p-8:idx_p] == '00000000') and (chars[idx_p-9] in num_list):
                        num = int(chars[idx_p - 9:idx_p])
                        num = num + 50000000
                        num = str(num)
                        cut[0] = chars.replace(chars[idx_p - 9:idx_p + 1], num)

                    else:
                        pass

                elif idx_p == 0 and idx > 0:
                    chars_l = sen_cut[idx - 1][0]
                    if chars_l[-1] == '十':
                        cut[0] = chars.replace('多', '五')
                    elif chars_l[-1] == '百':
                        cut[0] = chars.replace('多', '五十')
                    elif chars_l[-1] == '千':
                        cut[0] = chars.replace('多', '五百')
                    elif chars_l[-1] == '万':
                        cut[0] = chars.replace('多', '五千')
                    elif chars_l[-1] == '亿':
                        cut[0] = chars.replace('多', '五千万')

                    # 数字情况.....
                    elif len(chars_l) > 1 and (chars_l[-1] == '0') and (chars_l[-2] in num_list):
                        num = int(chars_l[-2:])
                        num = num + 5
                        num = str(num)
                        new_sen_cut[idx-1][0] = chars_l.replace(chars_l[-2:], num)
                        cut[0] = chars.replace('多', '')
                    elif len(chars_l) > 2 and (chars_l[-2:] == '00') and (chars_l[-3] in num_list):
                        num = int(chars_l[-3:])
                        num = num + 50
                        num = str(num)
                        new_sen_cut[idx - 1][0] = chars_l.replace(chars_l[-3:], num)
                        cut[0] = chars.replace('多', '')
                    elif len(chars_l) > 3 and (chars_l[-3:] == '000') and (chars_l[-4] in num_list):
                        num = int(chars_l[-4:])
                        num = num + 500
                        num = str(num)
                        new_sen_cut[idx - 1][0] = chars_l.replace(chars_l[-4:], num)
                        cut[0] = chars.replace('多', '')
                    elif len(chars_l) > 4 and (chars_l[-4:] == '0000') and (chars_l[-5] in num_list):
                        num = int(chars_l[-5:])
                        num = num + 5000
                        num = str(num)
                        new_sen_cut[idx - 1][0] = chars_l.replace(chars_l[-5:], num)
                        cut[0] = chars.replace('多', '')
                    elif len(chars_l) > 8 and (chars_l[-8:] == '00000000') and (chars_l[-9] in num_list):
                        num = int(chars_l[-9:])
                        num = num + 50000000
                        num = str(num)
                        new_sen_cut[idx - 1][0] = chars_l.replace(chars_l[-9:], num)
                        cut[0] = chars.replace('多', '')
                    else:
                        pass
                else:
                    pass

            if '几' in chars:
                cut[0] = chars.replace('几', '五')
            else:
                pass

            idx += 1
            new_sen_cut.append(cut)

        sentence = ''
        rebuild_sen_cut = []
        for new_cut in new_sen_cut:
            sentence += new_cut[0]
            new_cut = tuple(new_cut)
            rebuild_sen_cut.append(new_cut)

        # 判断句子是否包含金额
        judge = Judge()
        # 参数：分词后的结果sen_cut, 数词词性POS_list
        # True：有确定的数量词
        # Fuzzy：词性中有数词，但是没有确定的数量词
        # False：没有数词，或者分词后的字不全在字表里
        result, idx_list = judge.main(rebuild_sen_cut, POS_list)

        if result == 'True':
            trans = trans_money()
            # digit_list = []
            for idx in idx_list:
                part_list = [sentence[idx]]
                idx_left = idx-1
                while (idx_left > -1) and (sentence[idx_left] in self.money_list):
                    part_list.insert(0, sentence[idx_left])
                    idx_left -= 1

                idx_right = idx+1
                while (idx_right < len(sentence)) and (sentence[idx_right] in self.money_list):
                    part_list.append(sentence[idx_right])
                    idx_right += 1
                    # 处理类似'我 要 取 350 块 钱'句子的状况
                    if (idx_right < len(sentence)) and (sentence[idx_right-1] in '块元毛角分')and \
                            (sentence[idx_right] == '钱'):
                        part_list.append(sentence[idx_right])
                        idx_right += 1

                part_str = ''.join(part_list)
                money = int(trans.mainfunc(part_list))
                money = str(money)
                new_sentence = sentence.replace(part_str, money)

                # digit_list.append(money)
            # digit_list = list(set(digit_list))
            return new_sentence
        else:
            pass

if __name__ == '__main__':
    seg = seg_digit()
    # 传入参数：1.经分词器分词后的结果
    #         2.词性列表
    # 返回结果：金额转换而成的数字,存在一个list中
    # new_sentence = seg.seg2digit([('我', 'r'), ('要取', 'v'), ('350', 'm'), ('块钱', 'n')], ['m'])
    new_sentence = seg.seg2digit([('我', 'PN'), ('来', 'VV'), ('办', 'VV'), ('一', 'CD'), ('张', 'M'), ('银行卡', 'NN')], ['CD'])
    print(new_sentence)
