次の商品購入時のレシートのテキストから次のフォーマットの JSON 文字列を出力先に書き込んでください。
すでにファイルがある場合は上書きしてください。

# 出力先

```
%%OUTPUT%%
```

# フォーマット

```json
{
    "date": string, /* "YYYY-MM-DD" 形式のレシート発行日 /*
    "shop": string, /* レシートの発行店名。店名リストにある場合はその店名。ない場合は入力そのままの文字列 */
    "shopSymbol": string | null, /* 店名記号。店名リストにない場合は null */
    "products": Product[], /* 購入商品の一覧 */
    "total": int /* 商品総額 */
}
```

`Product` 型は次のとおりです：

```json
{
    "name": string, /* 商品名 */
    "categorySymbol": string | null, /* カテゴリ記号。カテゴリリストにない場合は null */
    "unitPriceYen": int, /* 商品の価格 */
    "count": int /* 商品数 */
}
```


# 店名記号と店名

店名リストは次のとおりです：

```tsv
店名記号	店名
mi	mister donut
ca	cainz
ka	kaldi
h	東林間青果
s	sanwa
c	CREATE
a	ave
shinsen	新鮮舘
life	ライフ
k	カイザー
co	コンビニ
t	てらす珈琲
o	Ozeki
w	welcia
gai	外食
aeon	イオン
ki	KISSYO SELECT
l	LITTLE MERMAID
to	TOKYU
oda	Odakyu OX
oka	おかしのまちおか
tsu	ツルハドラッグ
shokusenkan	食専館
mysweets	MY SWEETS
seijo	成城石井
ito	イトーヨーカドー
oka	おかしのまちおか
miyo	三吉野
unknown	不明
beard	ビアードパパ
tomi	富澤商店
```

# カテゴリ記号とカテゴリ

カテゴリリストは次のとおりです：

```tsv
カテゴリ記号	カテゴリ
sak	魚
n	肉
shu	主食
o	お菓子
so	その他材料
k	コーヒー
ya	野菜
a	アイス
r	レトルト
yui	結可
cho	調味料
gyu	牛乳
no	飲み物
sake	酒
syu	主食
gai	外食
t	卵
```


# レシート

```
%%RECEIPT%%
```
