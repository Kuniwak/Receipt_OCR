# Receipt OCR

Google Vision APIを用いたレシートのOCRとその結果をCSVに変換することを目的としています。


## How to Use


### OCR

下記の設定を済ませる必要があります
https://cloud.google.com/docs/authentication/getting-started#create-service-account-gcloud

```console
$ export GOOGLE_APPLICATION_CREDENTIALS=<your json file>
```

```console
$ python main_scan.py <image folder>
```

jsonファイル達が`<image folder>/output/`に出来上がります。


### Labeling

```console
$ # JSON を output/rawjson へ移動
$ mkdir -p ./output/raw-json
$ find ./output -name '*.json' -type f -exec bash -c 'mv "{}" "$(echo "{}" | sed -e "s|^\./output/|./output/raw-json/|")"' \;

$ # JSON を文字列化
$ mkdir -p ./output/text
$ find ./output/raw-json -name '*.json' -type f -exec bash -c './bin/python3.14 ./main_tostring.py "{}" > "$(echo "{}" | sed -e "s|\.json$|.txt| -e "s|^\./output/raw-json/|./output/text/|")"' \;

$ pushd ./output/text

$ # Claude Code の場合
$ find . -name '*.txt' -exec bash -c '../../promptgen "{}" | cage --preset claude claude --dangerously-skip-permissions -p' \;

$ # Gemini の場合
$ find . -name '*.txt' -exec bash -c '../../promptgen "{}" | op run --env-file=.env -- cage --preset gemini gemini --yolo' \;

$ # 途中再開する場合は
$ ../../bin/python3.14 ../../main_subtract.py <(find . -name '*.txt' -maxdepth 1 -type f) <(cd ./out && find . -name '*.json' | sed -e 's|\.json$|.txt|') | ../../bin/python3.14 ../../main_exec.py -exec bash -c '../../promptgen "{}" | op run --env-file=.env -- cage --preset gemini gemini --yolo' \;

$ popd
```
