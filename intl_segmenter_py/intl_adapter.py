from .grapheme import graphemeSegments
from .word import word_bounds, is_word_like
from .compat_util import String


# 适配 `Intl.Segmenter` API
# @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter
class Segmenter:
    def __init__(self, locale: str, options = None):
        options = options or {}
        granularity = options.get('granularity', 'grapheme')
        
        if granularity == 'grapheme':
            pass
        elif granularity == 'word':
            pass
        elif granularity == 'sentence':
            raise TypeError('Unicode "sentence" segmenter is currently not implemented')
        else:
            raise TypeError(f'Value {granularity} out of range for Intl.Segmenter options property granularity')
    
        self.p_locale: str = locale or 'en'
        self.p_granularity: str = granularity
  
  
    # Impelements {@link Intl.Segmenter.segment}
    # @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter/segment
    def segment(self, _input: String):
        return SegmentsAdapter(_input, self.p_granularity)

    # Impelements {@link Intl.Segmenter.resolvedOptions}
    # @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter/resolvedOptions
    def resolvedOptions(self):
        return {
          'locale': self.p_locale,
          'granularity': self.p_granularity,
        }


# @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter/segment/Segments
class SegmentsAdapter:
    def __init__(self, _input: String, granularity: str):
        self.input = _input
        self.granularity = granularity
    
    def __iter__(self):
        if self.granularity == 'grapheme':
            for i in graphemeSegments(String(self.input)):
                yield {'segment': i['segment'], 'index': i['index'], 'input': i['input']}
        elif self.granularity == 'word':
            s = String(self.input)
            index = 0
            for _, c in word_bounds(str(self.input)):
                segment = String(c)
                yield {'segment': segment, 'index': index, 'input': s, 'isWordLike': is_word_like(c)}
                index += segment.length
    
    # @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter/segment/Segments/containing
    def containing(self, codeUnitIndex=0):
        offset = 0
        if self.granularity == 'grapheme':
            for x in graphemeSegments(self.input):
                offset += x['segment'].length
                if codeUnitIndex < offset:
                    return x
                    
        elif self.granularity == 'word':
            for _, c in word_bounds(str(self.input)):
                segment = String(c)
                offset += segment.length
                if codeUnitIndex < offset:
                    return {'segment': segment, 'index': offset - segment.length, 'input': String(self.input), 'isWordLike': is_word_like(c)}
        return None  # undefined

