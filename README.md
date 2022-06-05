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

## Example

```json
{
    "title": "曖昧",
    "idx": "j_CRJC000136",
    "prn": "あいまい",
    "kanjis": [
        "曖昧"
    ],
    "defs": [
        {
            "order": "1",
            "chi_transs": [
                "含糊",
                "暧昧"
            ],
            "eng_transs": [
                "vagueness"
            ],
            "sent_exs": [
                {
                    "jpn_sent": "あいまいな結論が禍根を残した",
                    "chi_sent": "暧昧的结论留下了祸根"
                },
                {
                    "jpn_sent": "真偽をあいまいにしたまま審問は終わった",
                    "chi_sent": "还没分清真假, 审讯就结束了"
                },
                {
                    "jpn_sent": "あいまいな返事をしてごまかす",
                    "chi_sent": "做出模棱两可的答复蒙混过去"
                },
                {
                    "jpn_sent": "あいまいなことを言う",
                    "chi_sent": "含糊其辞"
                },
                {
                    "jpn_sent": "市民の申し入れに対してあいまいな態度を取る",
                    "chi_sent": "对于市民的建议不明确表态"
                },
                {
                    "jpn_sent": "あいまい模糊とした",
                    "chi_sent": "模糊不清"
                }
            ]
        }
    ],
    "phrs": [
        {
            "idx": "j_CRJC000136-HG001",
            "titles": [
                "あいまい検索",
                "あいまいけんさく",
                "曖昧検索"
            ],
            "secs": [
                {
                    "transs": [
                        "模糊匹配检索"
                    ]
                }
            ]
        }
    ]
}
```

