# -*- coding: utf-8 -*-
"""
村上春樹 文庫本管理アプリ
Pythonista 3 for iOS 対応

【使い方】
1. このファイルを Pythonista の Documents フォルダにコピーする
2. Pythonista で開き、実行ボタン（▶︎）を押す
3. データは ~/Documents/murakami_data.json に自動保存されます

【機能】
- 文庫本一覧（長編小説 / 短篇集 / エッセイ）
- カテゴリ・ステータスでフィルタリング
- 所持 / 未所持、読了 / 未読 を管理
- 5段階星評価
- 感想・メモ記入
"""

import ui
import json
import os

# ─────────────────────────────────────────────────────────────────────────────
# 書籍マスターデータ（上下巻は別エントリー、版違いは同一）
# ─────────────────────────────────────────────────────────────────────────────

BOOKS = [
    # ── 長編小説 ────────────────────────────────────────────────────────────
    {"id":  1, "title": "風の歌を聴け",                                   "year": 1979, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id":  2, "title": "1973年のピンボール",                             "year": 1980, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id":  3, "title": "羊をめぐる冒険 上",                              "year": 1982, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id":  4, "title": "羊をめぐる冒険 下",                              "year": 1982, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id":  5, "title": "世界の終りとハードボイルド・ワンダーランド 上",  "year": 1985, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id":  6, "title": "世界の終りとハードボイルド・ワンダーランド 下",  "year": 1985, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id":  7, "title": "ノルウェイの森 上",                              "year": 1987, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id":  8, "title": "ノルウェイの森 下",                              "year": 1987, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id":  9, "title": "ダンス・ダンス・ダンス 上",                      "year": 1988, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id": 10, "title": "ダンス・ダンス・ダンス 下",                      "year": 1988, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id": 11, "title": "国境の南、太陽の西",                             "year": 1992, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id": 12, "title": "ねじまき鳥クロニクル 第1部 泥棒かささぎ編",      "year": 1994, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 13, "title": "ねじまき鳥クロニクル 第2部 予言する鳥編",        "year": 1994, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 14, "title": "ねじまき鳥クロニクル 第3部 鳥刺し男編",          "year": 1995, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 15, "title": "スプートニクの恋人",                             "year": 1999, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id": 16, "title": "海辺のカフカ 上",                                "year": 2002, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 17, "title": "海辺のカフカ 下",                                "year": 2002, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 18, "title": "アフターダーク",                                 "year": 2004, "pub": "講談社文庫",  "cat": "長編小説"},
    {"id": 19, "title": "1Q84 BOOK 1 上",                                "year": 2009, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 20, "title": "1Q84 BOOK 1 下",                                "year": 2009, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 21, "title": "1Q84 BOOK 2 上",                                "year": 2009, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 22, "title": "1Q84 BOOK 2 下",                                "year": 2009, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 23, "title": "1Q84 BOOK 3 上",                                "year": 2010, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 24, "title": "1Q84 BOOK 3 下",                                "year": 2010, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 25, "title": "色彩を持たない多崎つくると、彼の巡礼の年",      "year": 2013, "pub": "文春文庫",    "cat": "長編小説"},
    {"id": 26, "title": "騎士団長殺し 第1部 顕れるイデア編",              "year": 2017, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 27, "title": "騎士団長殺し 第2部 遷ろうメタファー編",          "year": 2017, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 28, "title": "街とその不確かな壁 上",                          "year": 2023, "pub": "新潮文庫",    "cat": "長編小説"},
    {"id": 29, "title": "街とその不確かな壁 下",                          "year": 2023, "pub": "新潮文庫",    "cat": "長編小説"},
    # ── 短篇集 ────────────────────────────────────────────────────────────
    {"id": 30, "title": "中国行きのスロウ・ボート",                       "year": 1983, "pub": "中公文庫",    "cat": "短篇集"},
    {"id": 31, "title": "カンガルー日和",                                 "year": 1983, "pub": "講談社文庫",  "cat": "短篇集"},
    {"id": 32, "title": "螢・納屋を焼く・その他の短篇",                   "year": 1984, "pub": "新潮文庫",    "cat": "短篇集"},
    {"id": 33, "title": "回転木馬のデッド・ヒート",                       "year": 1985, "pub": "講談社文庫",  "cat": "短篇集"},
    {"id": 34, "title": "パン屋再襲撃",                                   "year": 1986, "pub": "文春文庫",    "cat": "短篇集"},
    {"id": 35, "title": "TVピープル",                                     "year": 1990, "pub": "文春文庫",    "cat": "短篇集"},
    {"id": 36, "title": "夜のくもざる",                                   "year": 1995, "pub": "平凡社文庫",  "cat": "短篇集"},
    {"id": 37, "title": "レキシントンの幽霊",                             "year": 1996, "pub": "文春文庫",    "cat": "短篇集"},
    {"id": 38, "title": "神の子どもたちはみな踊る",                       "year": 2000, "pub": "新潮文庫",    "cat": "短篇集"},
    {"id": 39, "title": "東京奇譚集",                                     "year": 2005, "pub": "新潮文庫",    "cat": "短篇集"},
    {"id": 40, "title": "夢で会いましょう",                               "year": 1981, "pub": "文春文庫",    "cat": "短篇集"},
    {"id": 41, "title": "女のいない男たち",                               "year": 2014, "pub": "文春文庫",    "cat": "短篇集"},
    {"id": 42, "title": "一人称単数",                                     "year": 2020, "pub": "文春文庫",    "cat": "短篇集"},
    # ── エッセイ ──────────────────────────────────────────────────────────
    {"id": 43, "title": "村上朝日堂",                                     "year": 1984, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 44, "title": "村上朝日堂の逆襲",                               "year": 1986, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 45, "title": "ランゲルハンス島の午後",                         "year": 1986, "pub": "文春文庫",    "cat": "エッセイ"},
    {"id": 46, "title": "遠い太鼓",                                       "year": 1990, "pub": "講談社文庫",  "cat": "エッセイ"},
    {"id": 47, "title": "雨天炎天",                                       "year": 1990, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 48, "title": "アンダーグラウンド",                             "year": 1997, "pub": "講談社文庫",  "cat": "エッセイ"},
    {"id": 49, "title": "約束された場所で",                               "year": 1998, "pub": "文春文庫",    "cat": "エッセイ"},
    {"id": 50, "title": "辺境・近境",                                     "year": 1998, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 51, "title": "もし僕らのことばがウィスキーであったなら",        "year": 1999, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 52, "title": "ポートレイト・イン・ジャズ",                     "year": 1997, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 53, "title": "意味がなければスイングはない",                    "year": 2008, "pub": "文春文庫",    "cat": "エッセイ"},
    {"id": 54, "title": "走ることについて語るときに僕の語ること",          "year": 2010, "pub": "文春文庫",    "cat": "エッセイ"},
    {"id": 55, "title": "村上ラヂオ",                                     "year": 2001, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 56, "title": "村上ラヂオ2 おおきなかぶ、むずかしいアボカド",   "year": 2011, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 57, "title": "村上ラヂオ3 サラダ好きのライオン",               "year": 2012, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 58, "title": "夢を見るために毎朝僕は目覚めるのです",            "year": 2010, "pub": "文春文庫",    "cat": "エッセイ"},
    {"id": 59, "title": "小澤征爾さんと、音楽について話をする",            "year": 2011, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 60, "title": "職業としての小説家",                             "year": 2016, "pub": "新潮文庫",    "cat": "エッセイ"},
    {"id": 61, "title": "村上T",                                          "year": 2020, "pub": "文春文庫",    "cat": "エッセイ"},
    {"id": 62, "title": "猫を棄てる",                                     "year": 2020, "pub": "文春文庫",    "cat": "エッセイ"},
]

CATEGORIES   = ['すべて', '長編小説', '短篇集', 'エッセイ']
STATUS_NAMES = ['全て', '読了', '未読', '所持', '未所持']

# ─────────────────────────────────────────────────────────────────────────────
# データマイグレーション
#
# v1（初版 40冊）→ v3、v2（2版 42冊）→ v3 の両方に対応
# 分割される巻は上下どちらにも同じステータス・感想をコピー
# ─────────────────────────────────────────────────────────────────────────────

DATA_VERSION = 3

# v1（初版）→ v3 の ID 対応表
_V1_TO_V3 = {
     1: [ 1],           # 風の歌を聴け
     2: [ 2],           # 1973年のピンボール
     3: [ 3,  4],       # 羊をめぐる冒険 → 上・下
     4: [ 5,  6],       # 世界の終り → 上・下
     5: [ 7],           # ノルウェイの森 上
     6: [ 8],           # ノルウェイの森 下
     7: [ 9],           # ダンス 上
     8: [10],           # ダンス 下
     9: [11],           # 国境の南
    10: [12],           # ねじまき鳥 第1部
    11: [13],           # ねじまき鳥 第2部
    12: [14],           # ねじまき鳥 第3部
    13: [15],           # スプートニク
    14: [16],           # 海辺のカフカ 上
    15: [17],           # 海辺のカフカ 下
    16: [18],           # アフターダーク
    17: [19, 20],       # 1Q84 BOOK 1 → 上・下
    18: [21, 22],       # 1Q84 BOOK 2 → 上・下
    19: [23, 24],       # 1Q84 BOOK 3 → 上・下
    20: [25],           # 色彩を持たない多崎つくると
    21: [26],           # 騎士団長殺し 第1部
    22: [27],           # 騎士団長殺し 第2部
    23: [28, 29],       # 街とその不確かな壁 → 上・下
    24: [30],           # 中国行きのスロウ・ボート
    25: [31],           # カンガルー日和
    26: [32],           # 螢・納屋を焼く
    27: [33],           # 回転木馬のデッド・ヒート
    28: [34],           # パン屋再襲撃
    29: [35],           # TVピープル
    30: [36],           # 夜のくもざる
    31: [37],           # レキシントンの幽霊
    32: [38],           # 神の子どもたちはみな踊る
    33: [39],           # 東京奇譚集
    34: [40],           # 夢で会いましょう
    35: [43],           # 村上朝日堂
    36: [44],           # 村上朝日堂の逆襲
    37: [53],           # 意味がなければスイングはない
    38: [54],           # 走ることについて語るとき
    39: [60],           # 職業としての小説家
    40: [62],           # 猫を棄てる
}

# v2（2版：羊・世界の終り 上下分割済み 42冊）→ v3 の ID 対応表
_V2_TO_V3 = {
     1: [ 1],  2: [ 2],  3: [ 3],  4: [ 4],  5: [ 5],
     6: [ 6],  7: [ 7],  8: [ 8],  9: [ 9], 10: [10],
    11: [11], 12: [12], 13: [13], 14: [14], 15: [15],
    16: [16], 17: [17], 18: [18],
    19: [19, 20],       # 1Q84 BOOK 1 → 上・下
    20: [21, 22],       # 1Q84 BOOK 2 → 上・下
    21: [23, 24],       # 1Q84 BOOK 3 → 上・下
    22: [25],           # 色彩を持たない多崎つくると
    23: [26], 24: [27],
    25: [28, 29],       # 街とその不確かな壁 → 上・下
    26: [30], 27: [31], 28: [32], 29: [33], 30: [34],
    31: [35], 32: [36], 33: [37], 34: [38], 35: [39],
    36: [40],
    37: [43], 38: [44],
    39: [53],           # 意味がなければスイングはない
    40: [54],           # 走ることについて語るとき
    41: [60],           # 職業としての小説家
    42: [62],           # 猫を棄てる
}


def _apply_map(data: dict, migration_map: dict) -> dict:
    new_data = {}
    for old_id, new_ids in migration_map.items():
        entry = data.get(str(old_id))
        if entry:
            for new_id in new_ids:
                new_data[str(new_id)] = dict(entry)
    return new_data


# ─────────────────────────────────────────────────────────────────────────────
# データ永続化
# ─────────────────────────────────────────────────────────────────────────────

DATA_PATH = os.path.expanduser('~/Documents/murakami_data.json')
_DATA: dict = {}


def load_all():
    global _DATA
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            version = raw.get('_version', 1)
            if version < DATA_VERSION:
                book_data = {k: v for k, v in raw.items() if k != '_version'}
                if version == 1:
                    book_data = _apply_map(book_data, _V1_TO_V3)
                elif version == 2:
                    book_data = _apply_map(book_data, _V2_TO_V3)
                book_data['_version'] = DATA_VERSION
                _DATA = book_data
                save_all()
            else:
                _DATA = raw
        except Exception:
            _DATA = {'_version': DATA_VERSION}
    else:
        _DATA = {'_version': DATA_VERSION}


def save_all():
    _DATA['_version'] = DATA_VERSION
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(_DATA, f, ensure_ascii=False, indent=2)


def get_entry(book_id: int) -> dict:
    return _DATA.get(str(book_id), {'owned': False, 'read': False, 'rating': 0, 'review': ''})


def save_entry(book_id: int, entry: dict):
    _DATA[str(book_id)] = entry
    save_all()


# ─────────────────────────────────────────────────────────────────────────────
# 詳細・編集画面
# ─────────────────────────────────────────────────────────────────────────────

class DetailView(ui.View):
    def __init__(self, book: dict, on_save_callback):
        self.book = book
        self.entry = dict(get_entry(book['id']))
        self.on_save_callback = on_save_callback
        self.name = book['title']
        self.background_color = 'white'
        self._built = False

    def layout(self):
        if not self._built:
            self._build()
        self.scroll.frame = (0, 0, self.width, self.height)

    def _build(self):
        self._built = True
        W = self.width or 375

        self.scroll = ui.ScrollView()
        self.scroll.frame = (0, 0, W, self.height)
        self.scroll.autoresizing = 'WH'
        self.add_subview(self.scroll)

        y = 16

        info_lbl = ui.Label(frame=(16, y, W - 32, 40))
        info_lbl.text = f"{self.book['pub']}  /  {self.book['year']}年  /  {self.book['cat']}"
        info_lbl.font = ('<system>', 14)
        info_lbl.text_color = '#888'
        info_lbl.number_of_lines = 0
        self.scroll.add_subview(info_lbl)
        y += 52

        y = self._add_toggle_row(W, y, '📚 所持している', 'owned')
        self._add_sep(W, y); y += 1

        y = self._add_toggle_row(W, y, '✅ 読んだ', 'read')
        self._add_sep(W, y); y += 1

        rating_lbl = ui.Label(frame=(16, y + 10, 60, 30))
        rating_lbl.text = '評価'
        rating_lbl.font = ('<system>', 16)
        self.scroll.add_subview(rating_lbl)

        self.star_btns = []
        for i in range(5):
            b = ui.Button(frame=(84 + i * 46, y + 4, 42, 42))
            b.font = ('<system>', 26)
            b.tag = i + 1
            b.action = self._on_star
            self.star_btns.append(b)
            self.scroll.add_subview(b)
        self._refresh_stars()
        y += 52

        self._add_sep(W, y); y += 1

        memo_lbl = ui.Label(frame=(16, y + 10, 200, 28))
        memo_lbl.text = '感想・メモ'
        memo_lbl.font = ('<system>', 16)
        self.scroll.add_subview(memo_lbl)
        y += 46

        self.review_tv = ui.TextView(frame=(16, y, W - 32, 150))
        self.review_tv.font = ('<system>', 15)
        self.review_tv.text = self.entry.get('review', '')
        self.review_tv.border_width = 0.5
        self.review_tv.border_color = '#ccc'
        self.review_tv.corner_radius = 8
        self.scroll.add_subview(self.review_tv)
        y += 162

        save_btn = ui.Button(frame=(16, y, W - 32, 46))
        save_btn.title = '保存する'
        save_btn.background_color = '#007AFF'
        save_btn.tint_color = 'white'
        save_btn.corner_radius = 10
        save_btn.font = ('<system-bold>', 17)
        save_btn.action = self._save
        self.scroll.add_subview(save_btn)
        y += 58

        self.scroll.content_size = (W, y + 20)

    def _add_toggle_row(self, W, y, label_text, key):
        lbl = ui.Label(frame=(16, y + 10, W - 90, 30))
        lbl.text = label_text
        lbl.font = ('<system>', 16)
        self.scroll.add_subview(lbl)

        sw = ui.Switch(frame=(W - 67, y + 10, 51, 31))
        sw.value = self.entry.get(key, False)
        sw.action = lambda s, k=key: self.entry.update({k: s.value})
        self.scroll.add_subview(sw)
        return y + 52

    def _add_sep(self, W, y):
        sep = ui.View(frame=(16, y, W - 32, 0.5))
        sep.background_color = '#e0e0e0'
        self.scroll.add_subview(sep)

    def _on_star(self, sender):
        self.entry['rating'] = sender.tag
        self._refresh_stars()

    def _refresh_stars(self):
        r = self.entry.get('rating', 0)
        for b in self.star_btns:
            filled = b.tag <= r
            b.title = '★' if filled else '☆'
            b.tint_color = '#FFB900' if filled else '#CCCCCC'

    def _save(self, sender):
        self.entry['review'] = self.review_tv.text
        save_entry(self.book['id'], self.entry)
        self.on_save_callback()
        if self.navigation_view:
            self.navigation_view.pop_view()


# ─────────────────────────────────────────────────────────────────────────────
# メインリスト画面
# ─────────────────────────────────────────────────────────────────────────────

class BookListView(ui.View):
    def __init__(self):
        self.name = '村上春樹 文庫本リスト'
        self.background_color = 'white'
        self._filtered = list(BOOKS)
        self._nav = None
        self._built = False

    def set_nav(self, nav):
        self._nav = nav

    def layout(self):
        if not self._built:
            self._build()
            return
        W, H = self.width, self.height
        self.cat_ctrl.frame    = (8,  8, W - 16, 32)
        self.status_ctrl.frame = (8, 48, W - 16, 32)
        self.stats_lbl.frame   = (8, 86, W - 16, 22)
        self.tbl.frame         = (0, 112, W, H - 112)

    def _build(self):
        self._built = True
        W, H = self.width, self.height

        self.cat_ctrl = ui.SegmentedControl(frame=(8, 8, W - 16, 32))
        self.cat_ctrl.segments = CATEGORIES
        self.cat_ctrl.action = self._on_filter
        self.add_subview(self.cat_ctrl)

        self.status_ctrl = ui.SegmentedControl(frame=(8, 48, W - 16, 32))
        self.status_ctrl.segments = STATUS_NAMES
        self.status_ctrl.action = self._on_filter
        self.add_subview(self.status_ctrl)

        self.stats_lbl = ui.Label(frame=(8, 86, W - 16, 22))
        self.stats_lbl.font = ('<system>', 12)
        self.stats_lbl.text_color = '#888'
        self.stats_lbl.text_alignment = ui.ALIGN_RIGHT
        self.add_subview(self.stats_lbl)

        self.tbl = ui.TableView(frame=(0, 112, W, H - 112))
        self.tbl.row_height = 66
        self.tbl.data_source = self
        self.tbl.delegate = self
        self.add_subview(self.tbl)

        self._update_stats()

    def _on_filter(self, _sender):
        cat_i    = self.cat_ctrl.selected_index
        status_i = self.status_ctrl.selected_index

        books = BOOKS
        if cat_i > 0:
            books = [b for b in books if b['cat'] == CATEGORIES[cat_i]]
        if status_i == 1:
            books = [b for b in books if get_entry(b['id']).get('read')]
        elif status_i == 2:
            books = [b for b in books if not get_entry(b['id']).get('read')]
        elif status_i == 3:
            books = [b for b in books if get_entry(b['id']).get('owned')]
        elif status_i == 4:
            books = [b for b in books if not get_entry(b['id']).get('owned')]

        self._filtered = books
        self.tbl.reload_data()
        self._update_stats()

    def _update_stats(self):
        total   = len(BOOKS)
        read_n  = sum(1 for b in BOOKS if get_entry(b['id']).get('read'))
        owned_n = sum(1 for b in BOOKS if get_entry(b['id']).get('owned'))
        shown   = len(self._filtered)
        self.stats_lbl.text = f'読了: {read_n}/{total}冊  所持: {owned_n}/{total}冊  表示: {shown}冊'

    # ── TableViewDataSource ──────────────────────────────────────────────────

    def tableview_number_of_sections(self, tv):
        return 1

    def tableview_number_of_rows(self, tv, section):
        return len(self._filtered)

    def tableview_cell_for_row(self, tv, section, row):
        book  = self._filtered[row]
        entry = get_entry(book['id'])

        cell = ui.TableViewCell('subtitle')
        cell.text_label.text = book['title']
        cell.text_label.number_of_lines = 2
        cell.text_label.font = ('<system>', 15)
        cell.text_label.text_color = '#111' if entry.get('read') else '#555'

        r = entry.get('rating', 0)
        stars      = '★' * r + '☆' * (5 - r) if r else '未評価'
        read_mark  = '✓ 読了' if entry.get('read')  else '○ 未読'
        owned_mark = '📚 所持' if entry.get('owned') else '× 未所持'

        cell.detail_text_label.text = f'{read_mark}  {owned_mark}  {stars}'
        cell.detail_text_label.font = ('<system>', 12)
        cell.detail_text_label.text_color = '#666'
        cell.accessory_type = 'disclosure_indicator'
        return cell

    # ── TableViewDelegate ────────────────────────────────────────────────────

    def tableview_did_select(self, tv, section, row):
        book   = self._filtered[row]
        detail = DetailView(book, self._on_return)
        if self._nav:
            self._nav.push_view(detail)

    def _on_return(self):
        if self._built:
            self.tbl.reload_data()
            self._update_stats()


# ─────────────────────────────────────────────────────────────────────────────
# エントリーポイント
# ─────────────────────────────────────────────────────────────────────────────

def main():
    load_all()
    list_view = BookListView()
    nav = ui.NavigationView(list_view)
    nav.name = '村上春樹 文庫本リスト'
    list_view.set_nav(nav)
    nav.present('fullscreen')


if __name__ == '__main__':
    main()
