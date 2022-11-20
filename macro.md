# マクロ

## 登録

`Redmine::WikiFormatting::Macros.register` を使用して登録する。

- `desc`: マクロの説明。`macro` の前に実行する。
- `macro`: マクロの本体。

  - arg0: マクロ名
  - arg1: オプション

    - `desc`: マクロの説明
    - `parse_args`: マクロ引数を , で分割するかどうか

  - &block: 本体

`Macro.available_macros` に小文字のマクロ名をキーにオプションを登録する。
`Macro::Definitions` モジュールに `define_method` を使用して `macro_マクロ名` のメソッド名で本体を定義する。
