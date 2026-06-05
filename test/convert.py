import re

def convert_unicode_braces(s: str) -> str:
    # 匹配 \u{十六进制数字} 模式
    pattern = r'\\u\{([0-9a-fA-F]+)\}'
    
    def repl(match):
        hex_digits = match.group(1)
        code_point = int(hex_digits, 16)
        if code_point <= 0xFFFF:
            # 用 \u 后跟 4 位十六进制（大写）
            return f'\\u{code_point:04X}'
        else:
            # 用 \U 后跟 8 位十六进制（大写）
            return f'\\U{code_point:08X}'
    
    return re.sub(pattern, repl, s)

# 示例
'''with open('./_unicode_testdata.js', 'r') as f:
    test_str = f.read()
converted = convert_unicode_braces(test_str)

with open('./_unicode_testdata.py', 'w') as f:
    f.write(converted)'''
# print(converted)  # 输出: \u0000\u0308\U0001F1E6
with open('./_word_testdata.rs', 'r') as f:
    test_str = f.read()
converted = convert_unicode_braces(test_str)

with open('./_word_testdata.py', 'w') as f:
    f.write(converted.replace('&', ''))