from combine_hangul import join_jamos

def ch2hangul(input_string):
    # 0은 초성을, 1은 중성을, 2는 종성을 의미한다.
    # 3은 된소리 자음을 의미한다.
    # 4는 띄어쓰기를 의미한다.
    # 5는 약자 중 모음으로 시작하지 않는 것에 의미한다.
    # 초성에 나온 'ㅇ'은 음가가 없으므로 쓰지 않는다.
    # 문자 다음에 수표가 나오는 경우를 대비해 수표를 넣어놨다.
    letter = {'⠈': ('ㄱ', 0), '⠉': ('ㄴ', 0), '⠊': ('ㄷ', 0), '⠐': ('ㄹ', 0), \
            '⠑': ('ㅁ', 0), '⠘': ('ㅂ', 0), '⠠': ('ㅅ', 0), '⠨': ('ㅈ', 0), \
            '⠰': ('ㅊ', 0), '⠋': ('ㅋ', 0), '⠓': ('ㅌ', 0), '⠙': ('ㅍ', 0), '⠚': ('ㅎ', 0), \

            '⠣': ('ㅏ', 1), '⠜': ('ㅑ', 1), '⠎': ('ㅓ', 1), '⠱': ('ㅕ', 1), \
            '⠥': ('ㅗ', 1), '⠬': ('ㅛ', 1), '⠍': ('ㅜ', 1), '⠩': ('ㅠ', 1), \
            '⠪': ('ㅡ', 1), '⠕': ('ㅣ', 1), \
            '⠗': ('ㅐ', 1), '⠝': ('ㅔ', 1), '⠌': ('ㅖ', 1), \
            '⠧': ('ㅘ', 1), '⠽': ('ㅚ', 1), '⠏': ('ㅝ', 1), '⠺': ('ㅢ', 1), \

            '⠁': ('ㄱ', 2), '⠒': ('ㄴ', 2), '⠔': ('ㄷ', 2), '⠂': ('ㄹ', 2), \
            '⠢': ('ㅁ', 2), '⠃': ('ㅂ', 2), '⠄': ('ㅅ', 2), '⠶': ('ㅇ', 2), '⠅': ('ㅈ', 2), \
            '⠆': ('ㅊ', 2), '⠖': ('ㅋ', 2), '⠦': ('ㅌ', 2), '⠲': ('ㅍ', 2), '⠴': ('ㅎ', 2), \
            '⠌': ('ㅆ', 2), \

            '⠠': ('', 3), \

            '⠀': (' ', 4), \

            '⠤': ('-', 4), \

            '⠫': ('ㄱㅏ',5), '⠇': ('ㅅㅏ',5), '⠹': ('ㅓㄱ', 1), '⠾': ('ㅓㄴ', 1), \
            '⠞': ('ㅓㄹ', 1), '⠡': ('ㅕㄴ', 1), '⠳': ('ㅕㄹ', 1), '⠻': ('ㅕㅇ', 1), \
            '⠭': ('ㅗㄱ', 1), '⠷': ('ㅗㄴ', 1), '⠿': ('ㅗㅇ', 1), '⠛': ('ㅜㄴ', 1), \
            '⠯': ('ㅜㄹ', 1), '⠵': ('ㅡㄴ', 1), '⠮': ('ㅡㄹ', 1), '⠟': ('ㅣㄴ', 1), '⠸': ('ㄱㅓㅅ',5), \

            '⠼': ('', 6)
            }
    # 겹받침
    double_final_consonants = {'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ', \
                            'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ', \
                            'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ', \
                            'ㄱㄱ': 'ㄲ', 'ㅂㅂ': 'ㅃ', 'ㅅㅅ': 'ㅆ'}
    # 숫자는 수표⠼ 이후에 나온다.
    # 붙임표(-)도 넣어 주었다.
    number = {'⠚': '0', '⠁': '1', '⠃': '2', '⠉': '3', \
            '⠙': '4', '⠑': '5', '⠋': '6', '⠛': '7', \
            '⠓': '8', '⠊': '9', '⠤': '-'
            }

    # 약자(나,다,마,바,자,카,타,파,하)
    short1 = '⠉⠊⠑⠘⠨⠋⠓⠙⠚'
    short2 = '⠫⠇⠹⠾⠞⠡⠳⠻⠭⠷⠿⠛⠯⠵⠮⠟⠸'

    result = ''

    num_flag = False
    end_of_input = False
    i = 0
    while i < len(input_string) - 1:
        if input_string[i] == '⠼':
            num_flag = True
            i += 1
            while input_string[i] != '⠀' and i < len(input_string) - 1:
                result += number[input_string[i]]
                i += 1
            if input_string[i] == '⠀':
                result += '⠀'
                num_flag = False
        else:
            # [자모] 1-1. 초성 된소리
            if letter[input_string[i+1]][1] == 0 and letter[input_string[i]][1] == 3:
                match input_string[i+1]:
                    case '⠈':
                        result += 'ㄲ'
                        i += 1
                    case '⠊':
                        result += 'ㄸ'
                        i += 1
                    case '⠘':
                        result += 'ㅃ'
                        i += 1
                    case '⠠':
                        result += 'ㅆ'
                        i += 1
                    case '⠨':
                        result += 'ㅉ'
                        i += 1
                    # 위에 해당하지 않으면 아무것도 하지 않고 지나가기
                if letter[input_string[i+1]][1] != 1:
                    result += 'ㅏ'
            # [약자] 2-2. 초성 된소리 + 약자 (까, 싸, 껏)
            elif input_string[i] == '⠠' and (input_string[i+1] == '⠫' or input_string[i+1] == '⠇' or input_string[i+1] == '⠸'):
                match input_string[i + 1]:
                    case '⠫':
                        result += 'ㄲ' + 'ㅏ'
                        if i == len(input_string) - 2:
                            end_of_input = True
                        i += 1
                    case '⠇':
                        result += 'ㅆ' + 'ㅏ'
                        if i == len(input_string) - 2:
                            end_of_input = True
                        i += 1
                    case '⠸':
                        result += 'ㄲ' + 'ㅓ' + 'ㅅ'
                        if i == len(input_string) - 3:
                            end_of_input = True
                        i += 2
                if i == len(input_string) - 2:
                    end_of_input = True
            # [자모] 3. 이중 모음
            elif letter[input_string[i]][1] == 1 and input_string[i+1] == '⠗':
                if i == 0 or (letter[input_string[i-1]][1] and not input_string[i-1] == '⠠'):
                    result += 'ㅇ'
                match input_string[i]:
                    case '⠜':
                        result += 'ㅒ'
                        i += 1
                    case '⠧':
                        result += 'ㅙ'
                        i += 1
                    case '⠏':
                        result += 'ㅞ'
                        i += 1
                    case '⠍':
                        result += 'ㅟ'
                        i += 1
                    case _:
                        result += letter[input_string[i]][0]
            # [자모] 2-1. 종성 된소리 ㄲ
            elif input_string[i] == '⠁' and input_string[i+1] == '⠁':
                result += 'ㄲ'
                i += 1
                end_of_input = True
            # [자모] 2-2. 종성 겹받침
            elif (letter[input_string[i]][1] == 2 and not input_string[i] == '⠌') and letter[input_string[i+1]][1] == 2:
                result += double_final_consonants[letter[input_string[i]][0] + letter[input_string[i+1]][0]]
                if i == len(input_string) - 2:
                    end_of_input = True
                i += 1
            # 위의 조건에 하나도 부합하지 않을 시 result에 해당 글자 추가
            else:
                # [약자] 초성 약자(나,다,마,바,자,카,타,파,하) 판단
                if input_string[i] in short1:
                    if letter[input_string[i + 1]][1] == 1:  # 점자 다음에 중성이 나온다면 초성 추가
                        result += letter[input_string[i]][0]
                    else:  # 점자 다음에 초성 or 종성 or 띄어쓰기가 나온다면 ㅏ 추가
                        result += letter[input_string[i]][0] + 'ㅏ'
                else:
                    # [약자] 1,2. 나머지 약자들
                    if input_string[i] in short2:
                        if input_string[i] == '⠻':
                            # [약자] 2-5. 예외 ㅕㅇ
                            if input_string[i - 1] in '⠠⠨⠰' or (input_string[i - 2] == '⠠' and input_string[i - 1] in '⠠⠨'):
                                result += 'ㅓ' + 'ㅇ'
                            else:
                                # [자모] 1. 중성 앞에 초성이 없으면 ㅇ을 추가해야 함
                                # 모음 앞에 ㅅ이나 ㅆ이 오면 된소리표와 혼동 가능하므로 추가해줌
                                if input_string[i - 1] == '⠠':
                                    result += letter[input_string[i]][0]
                                elif i == 0:
                                    result += 'ㅇ' + letter[input_string[i]][0]
                                elif letter[input_string[i-1]][1]:
                                    result += 'ㅇ' + letter[input_string[i]][0]
                                else:
                                    result += letter[input_string[i]][0]
                        # [약자] 2. '것'은 점자 2개 차지하므로 i에 1 더 더해주기
                        elif input_string[i] == '⠸':
                            result += letter[input_string[i]][0]
                            if i == len(input_string) - 2:
                                end_of_input = True
                            i += 1
                        else:
                            # [자모] 1. 중성 앞에 초성이 없으면 ㅇ을 추가해야 함
                            if letter[input_string[i]][1] == 1:
                                # 모음 앞에 ㅅ이나 ㅆ이 오면 된소리표와 혼동 가능하므로 추가해줌
                                if input_string[i - 1] == '⠠':
                                    result += letter[input_string[i]][0]
                                elif i == 0:
                                    result += 'ㅇ' + letter[input_string[i]][0]
                                elif letter[input_string[i-1]][1]:
                                    result += 'ㅇ' + letter[input_string[i]][0]
                                else:
                                    result += letter[input_string[i]][0]
                                # 종성 뒤에 또 종성이 오는 경우 겹받침 처리
                                if letter[input_string[i+1]][1] == 2 and not input_string[i+1] == '⠌':
                                    if i == len(input_string) - 2:
                                        end_of_input = True
                                    if input_string[i] in '⠹⠭':
                                        result = result[:-1] + double_final_consonants['ㄱ' + letter[input_string[i+1]][0]]
                                        i += 1
                                    elif input_string[i] in '⠾⠡⠷⠛⠵⠟':
                                        result = result[:-1] + double_final_consonants['ㄴ' + letter[input_string[i+1]][0]]
                                        i += 1
                                    elif input_string[i] in '⠞⠳⠯⠮':
                                        result = result[:-1] + double_final_consonants['ㄹ' + letter[input_string[i+1]][0]]
                                        i += 1
                            # [약자] 1. 가, 사는 초성 ㅇ 신경쓰지 않아도 됨
                            else:
                                result += letter[input_string[i]][0]
                    elif input_string[i] == '⠤':
                        # [자모] 4-1,2. 붙임표가 모음 연쇄 때문에 나왔을 경우 pass
                        if letter[input_string[i-1]][1] == 1:
                            # ㅖ가 이어 나오는 모음 연쇄일 시 ㅆ과 구분해주기 위해 추가함
                            if input_string[i+1] == '⠌':
                                result += 'ㅇㅖ'
                                if i == len(input_string) - 2:
                                    end_of_input = True
                                i += 1
                            else:
                                pass
                        else:
                            result += '-'
                    else:
                        # [자모] 1. 중성 앞에 초성이 없으면 ㅇ을 추가해야 함
                        # 모음 앞에 ㅅ이나 ㅆ이 오면 된소리표와 혼동 가능하므로 추가해줌
                        if input_string[i - 1] == '⠠':
                            result += letter[input_string[i]][0]
                        elif i == 0 and letter[input_string[i]][1] == 1:
                            result += 'ㅇ' + letter[input_string[i]][0]
                        elif letter[input_string[i]][1] == 1 and letter[input_string[i-1]][1]:
                            result += 'ㅇ' + letter[input_string[i]][0]
                        else:
                            # 된소리 받침 ㅆ과 모음 ㅖ의 구분
                            if input_string[i] == '⠌':
                                if input_string[i - 1] in short1:
                                    result += 'ㅆ'
                                elif letter[input_string[i - 1]][1] == 5:
                                    result += 'ㅆ'
                                elif i == 0 or input_string[i - 1] in '⠤⠀' or letter[input_string[i - 1]][1] == 2 or input_string[i - 1] in short2:
                                    result += 'ㅇㅖ'
                                elif letter[input_string[i-1]][1] == 0:
                                    result += 'ㅖ'
                                else:
                                    result += 'ㅆ'
                            else:
                                if input_string[i] == '⠠' and input_string[i+1] == '⠠':
                                    result += 'ㅆ'
                                    i += 1
                                elif input_string[i] == '⠠':
                                    result += 'ㅅ'
                                else:
                                    result += letter[input_string[i]][0]
        i += 1
    # input의 마지막 글자 정하기
    # 숫자를 입력하던 경우 계속 숫자 입력
    if not end_of_input:
        if num_flag:
            result += number[input_string[-1]][0]
        else:
            # 만약 초성이 들어온다면 무조건 약자일 것
            if input_string[-1] in short1:
                if letter[input_string[-2]][1] == 3:
                    result += 'ㅏ'
                else:
                    result += letter[input_string[-1]][0] + 'ㅏ'
            # 약자 처리
            elif input_string[-1] in short2:
                if input_string[-1] == '⠻':
                    # [약자] 2-5. 예외
                    if input_string[-2] in '⠠⠨⠰' or (input_string[-3] == '⠠' and input_string[-2] in '⠠⠨'):
                        result += 'ㅓ' + 'ㅇ'
                    else:
                        # [자모] 1. 중성 앞에 초성이 없으면 ㅇ을 추가해야 함
                        # 모음 앞에 ㅅ이나 ㅆ이 오면 된소리표와 혼동 가능하므로 추가해줌
                        if input_string[-2] == '⠠':
                            result += letter[input_string[-1]][0]
                        elif letter[input_string[-2]][1]:
                            result += 'ㅇ' + letter[input_string[-1]][0]
                        else:
                            result += letter[input_string[-1]][0]
                elif input_string[-1] == '⠸':
                    result += letter[input_string[-1]][0]
                    i += 1
                else:
                    # [자모] 1. 중성 앞에 초성이 없으면 ㅇ을 추가해야 함
                    if letter[input_string[-1]][1] == 1:
                        # 모음 앞에 ㅅ이나 ㅆ이 오면 된소리표와 혼동 가능하므로 추가해줌
                        if input_string[2] == '⠠':
                            result += letter[input_string[1]][0]
                        elif letter[input_string[len(input_string) - 2]][1]:
                            result += 'ㅇ' + letter[input_string[1]][0]
                        else:
                            result += letter[input_string[1]][0]
                    # [약자] 1. 가, 사는 초성 ㅇ 신경쓰지 않아도 됨
                    else:
                        result += letter[input_string[-1]][0]
            # 나머지 경우 (종성 혹은 중성)
            else:
                # [자모] 1. 중성 앞에 초성이 없으면 ㅇ을 추가해야 함
                # 모음 앞에 ㅅ이나 ㅆ이 오면 된소리표와 혼동 가능하므로 추가해줌
                if letter[input_string[-1]][1] == 1 and input_string[-2] == '⠠':
                    result += letter[input_string[len(input_string) - 1]][0]
                elif letter[input_string[-1]][1] == 1 and letter[input_string[-2]][1]:
                    result += 'ㅇ' + letter[input_string[-1]][0]
                else:
                    # 된소리 받침 ㅆ과 모음 ㅖ의 구분
                    if input_string[-1] == '⠌':
                        if input_string[-2] in short1:
                            result += 'ㅆ'
                        elif letter[input_string[-2]][1] == 5:
                            result += 'ㅆ'
                        elif i == 0 or input_string[-2] in '⠤⠀' or letter[input_string[-2]][1] == 2 or input_string[-2] in short2:
                            result += 'ㅇㅖ'
                        elif letter[input_string[-2]][1] == 0:
                            result += 'ㅖ'
                        else:
                            result += 'ㅆ'
                    else:
                        if input_string[-1] == '⠠':
                            result += 'ㅅ'
                        else:
                            result += letter[input_string[-1]][0]


    result = join_jamos(result)
    return result