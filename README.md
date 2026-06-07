# Intl.Segmenter for Python

A Python implementation of the ECMAScript `Intl.Segmenter` API, ported from:

- [unicode-segmentation](https://github.com/unicode-rs/unicode-segmentation/commit/13862d88946469b9a32bd8064dec6594cb65c908) (word mode)
- [unicode-segmenter](https://github.com/cometkim/unicode-segmenter/commit/61a4701893f52bb69d5311e4fa3fa27275b090dd) (grapheme mode)

---

## 中文

### 用法
```python
from intl_segmenter_py import Segmenter, String

segmenter = Segmenter('en', {'granularity': 'word'})

# 输入字符串（自动转换为 UTF-16 String 类型）
text = String("Hello World")

# 分割
for segment in segmenter.segment(text):
    print(segment)
# 输出：
# {'segment': 'Hello', 'index': 0, 'input': 'Hello World', 'isWordLike': True}
# {'segment': ' ', 'index': 5, 'input': 'Hello World', 'isWordLike': False}
# {'segment': 'World', 'index': 6, 'input': 'Hello World', 'isWordLike': True}
```

### API
- `Segmenter(locale, granularity)` – `locale` 被忽略，`granularity` 支持 `'grapheme'` 或 `'word'`
- `segment(text: String)` – 返回可迭代对象，每个元素包含：
 - `'segment'`: `String` 类型（UTF-16 编码）
 - `'index'`: `int` – 分割起始位置（UTF-16 代码单元索引，与 JS 一致）
 - `'isWordLike'`: `bool` – 仅 word 模式有效，基于是否包含 `L`（字母）、`Nd`、`Nl` 类字符
 - `'input'`: `String` 类型（UTF-16 编码）

### 已知不足
1. 不支持 `sentence` 模式
2. 不支持 `locale` 定制，输出可能与 JS 行为不同
3. word 模式中 `isWordLike` 仅根据 `L/Nd/Nl` 类字符判断，可能与 JS 差异较大

### 特别说明
- 输出 `String` 类型模拟 JS UTF-16 字符串，可通过 `from intl_segmenter_py import String` 导入
- 所有 `index` 为 UTF-16 代码单元偏移（与 JS `segment.index` 完全一致）

---

## English

### Usage
```python
from intl_segmenter_py import Segmenter, String

segmenter = Segmenter('en', {'granularity': 'word'})

# Input string (automatically uses UTF-16 String type)
text = String("Hello World")

# Iterate segments
for segment in segmenter.segment(text):
    print(segment)
# output: 
# {'segment': 'Hello', 'index': 0, 'input': 'Hello World', 'isWordLike': True}
# {'segment': ' ', 'index': 5, 'input': 'Hello World', 'isWordLike': False}
# {'segment': 'World', 'index': 6, 'input': 'Hello World', 'isWordLike': True}
```

### API
- `Segmenter(locale, granularity)` – `locale` ignored; `granularity` supports `'grapheme'` or `'word'`
- `segment(text: String)` – returns iterable of segments, each with:
 - `'segment'`: `String` type (UTF-16 encoded)
 - `'index'`: `int` – start position in UTF-16 code units (matching JS behavior)
 - `'isWordLike'`: `bool` – word mode only, based on presence of `L` (letter), `Nd`, `Nl` characters
 - `'input'`: `String` type (UTF-16 encoded)

### Known Limitations
1. `sentence` mode is not supported
2. `locale` has no effect; output may differ from JS implementation
3. In word mode, `isWordLike` only checks for `L/Nd/Nl` categories – behavior may differ from JS

### Special Notes
- Output uses `String` type to simulate JS UTF-16 strings; import via `from intl_segmenter_py import String`
- All `index` values are UTF-16 code unit offsets (exactly matching JS `segment.index`)
