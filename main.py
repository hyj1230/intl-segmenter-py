from intl_segmenter_py import Segmenter


text = "Hello world. I'm so happy. a̐éö̲ 树梢树枝树根根，亲山亲水有亲人。 🇮🇴🇷🇸🇮👻👩‍👩‍👦‍👦"

a = Segmenter('en', {'granularity': 'grapheme'})
print(list(map(lambda s: s['segment'], a.segment(text))))

b = Segmenter('en', {'granularity': 'word'})
print(list(map(lambda s: s['segment'], b.segment(text))))

c = iter(b.segment("I'm fine"))
print(next(c))
print(next(c))
print(next(c))

text2 = '🐱‍🐉🐱‍💻🐱‍🚀🐱‍👓🐱‍👤🐱‍🏍💑👩‍❤️‍👩👩‍❤️‍👩👨‍❤️‍👨💏👩‍❤️‍💋‍👩👨‍👨‍👧‍👦👩‍👧‍👦👭👬👩‍👧👨‍👨‍👧👨‍👨‍👦👩‍👩‍👧‍👧👨‍👧‍👦👩‍👩‍👧👩‍👩‍👧👨‍👨‍👧‍👧👩‍👧‍👧👩‍👦‍👦👨‍❤️‍💋‍👨👯‍♂️👯‍♀️🤼‍♂️🤼‍♀️🚵‍♀️🚵‍♂️'
print(list(map(lambda s: s['segment'], a.segment(text2))))
