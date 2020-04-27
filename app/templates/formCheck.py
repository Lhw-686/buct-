Legal_Str = "!@~`#$%^&*()_-+=,<>./?\'\"{}\\|[];"
Ok = 0
Illegal_Char = 1
Too_Long = 2
Too_Short = 3
Low_Security = 4
Length_Error = 5
First_Char_Error = 6


def check_pwd(pwd: str) -> int:
    '''
    检查密码正确性
    :param pwd:
    '''
    digital_num = 0 #数字个数
    alpha_num = 0 #字母个数
    legal_char_num = 0 #合法字符个数
    ch: str
    if len(pwd) < 8:
        return "密码至少为6位，请重新输入！"
    elif len(pwd) > 32:
        return "密码太长了，请重新输入！"
    for ch in pwd:
        if ch.isdigit():
            digital_num += 1
        elif ch.isalpha():
            alpha_num += 1
        elif ch in Legal_Str:
            legal_char_num += 1
        else:
            return "密码包含非法字符请重新输入！"

    if digital_num == 0 or alpha_num == 0 or legal_char_num == 0:
        return "密码必须包含字母、数字和字符"
    return ""

def check_phone(phone: str) -> int:
    if not phone.isdigit():
        return "电话号码只能由数字构成！"
    elif len(phone) != 11:
        return "电话号码必须为11位！"
    return ""

def check_id(idnum: str) -> int:
    if not idnum.isalnum():
        return "学工号包含非法字符"
    if len(idnum) < 10:
        return "学工号太短"
    elif len(idnum) > 10:
        return "学工号太长"
    return ""
'''
def check_email(email: str) -> int:
    if not email.endswith('.com'):
        return Illegal_Char
    email_sep = email[:-4].split('@')
    if len(email_sep) != 2:
        return Illegal_Char

    ch: str
    for ch in email_sep[0]:
        if ch.isdigit() or ch.isalpha() or ch == '_':
            continue
        return  Illegal_Char
    if (not email_sep[1][0].isalnum()) or email_sep[1][-1] == '.':
        return Illegal_Char
    for index, ch in enumerate(email_sep[1]):
        if ch.isalnum() or (ch == '.' and email_sep[1][index-1] != '.'):
            continue
        return Illegal_Char
    return ""
'''
