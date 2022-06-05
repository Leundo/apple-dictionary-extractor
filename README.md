# apple-dictionary-extractor

I learned about the structure of Apple Dictionary data file from an exciting [blog](https://fmentzer.github.io/posts/2020/dictionary/), thanks to the author fmentzer!

This tool is use to extract entries from Apple Dictionary data file. Apple Dictionary is an application to look up words in various languages, which is available in macOS and iOS.

Supported dictionaries:

| Name                          | Feature       |
| ----------------------------- | ------------- |
| Simplified Chinese - Japanese | Parse to json |

## How to Run

**1**: Check that the dictionary data has been downloaded in Apple Dictionary (macOS).

**2**: Find and copy data file from `/System/Library/AssetsV2/com_apple_MobileAsset_DictionaryServices_dictionaryOSX` to `apple-dictionary-extractor/data`. For example, "Simplified Chinese - Japanese" Dictionary data file is in `AssetData/Simplified Chinese - Japanese.dictionary/Contents/Resources/Body.data`.

**3**: Configure `main.py` and run `python main.py`

