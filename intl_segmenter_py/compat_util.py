import math


def get_encode_type():
    check_str = '𠮷'
    be = check_str.encode('utf-16be')
    le = check_str.encode('utf-16le')
    if be[0] * 0x100 + be[1] == 55362:
        return 'utf-16be'
    if le[0] * 0x100 + le[1] == 55362:
        return 'utf-16le'
    raise EnvironmentError


ENCODE_TYPE = get_encode_type()


class String:
    def __init__(self, data):
        if isinstance(data, str):
            self.data = data.encode(ENCODE_TYPE)
        elif isinstance(data, String):
            self.data = data.data
        elif isinstance(data, (bytes, bytearray)):
            self.data = data
        else:
            raise ValueError('Unknown data type')
    
    @property
    def length(self):
        return len(self.data) // 2
    
    def charCodeAt(self, index: int):
        if index < 0 or index >= self.length:
            return math.nan
        return self.data[index * 2] * 0x100 + self.data[index * 2 + 1]
    
    def _codePointAt(self, index: int):  # @deprecate
        if index < 0 or index >= self.length:
            return None
        first = self.data[index * 2] * 0x100 + self.data[index * 2 + 1]
        if not (0xD800 <= first <= 0xDBFF) and not (0xDC00 <= first <= 0xDFFF):
            return first
        if (0xDC00 <= first <= 0xDFFF) or (index + 1 == self.length):
            return first
        second = self.data[index * 2 + 2] * 0x100 + self.data[index * 2 + 3]
        if not (0xDC00 <= second <= 0xDFFF):
            return first
        return (first - 0xD800) * 0x400 + (second - 0xDC00) + 0x10000
    
    def codePointAt(self, index: int):
        if index < 0 or index >= self.length:
            return None
        first = self.data[index * 2] * 0x100 + self.data[index * 2 + 1]
        # 尝试解码代理对（仅当 first 是高代理且存在有效的低代理时）
        if 0xD800 <= first <= 0xDBFF and index + 1 < self.length:
            second = self.data[index * 2 + 2] * 0x100 + self.data[index * 2 + 3]
            if 0xDC00 <= second <= 0xDFFF:
                return (first - 0xD800) * 0x400 + (second - 0xDC00) + 0x10000
        return first
    
    def __str__(self):
        return self.data.decode(ENCODE_TYPE)
    
    def __repr__(self):
        return repr(self.data.decode(ENCODE_TYPE))

    def slice(self, start: int, end: int = None):
        start = start or 0
        start = max(start + self.length, 0) if start < 0 else start
        end = self.length if end is None or end >= self.length else end
        end = max(end + self.length, 0) if end < 0 else end
        
        if start >= self.length or end <= start:
            return String('')
        
        return String(self.data[start * 2: end * 2])
     
    def __eq__(self, other):
        if isinstance(other, String):
            return self.data == other.data
        if isinstance(other, str):
            return str(self) == other
        return False
    
    def __bool__(self):
        return bool(self.data)
    
    def __add__(self, other):
        if isinstance(other, str):
            other = String(other)
        if isinstance(other, String):
            return String(self.data + other.data)
        else:
            raise TypeError
    
    def contain_code(self, codes: tuple):
        for i in range(0, len(self.data), 2):
            ch = self.data[i] * 0x100 + self.data[i + 1]
            if ch in codes: return True
        return False
   
    def repeat(self, count: int):
        return String(self.data * count)
   
    @staticmethod
    def measure_length(s: int):
        return len(s.encode(ENCODE_TYPE)) // 2

