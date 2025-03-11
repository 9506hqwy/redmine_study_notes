# アクセスコントロール

## Permission クラス

### プロパティ

- name: 権限名
- actions: アクションの配列 (*controller/action*)
- read: 読み取り権限かどうか

## Project モデル

- `Project.allow_to_condition`

  指定した User が permission を持つプロジェクトを検索するための SQL 条件式

- `Project.allow_to?`

  プロジェクトで action が許可されているかどうか。

  - アーカイブプロジェクトの場合は false
  - クローズプロジェクトかつ `read` アクションがない場合は false

- `Project.allowd_permissions` (private)

  プロジェクトで有効なモジュールの許可権限名を取得

- `Project.allow_actions` (private)

  プロジェクトで有効なモジュールの許可アクションを取得

## User モデル

- `User.allowed_to?`

  指定した action が許可されているかどうか。

  - `Project.allowed_to?` が false の場合は false
  - システム管理者の場合は true
  - ユーザにロールが設定されていない場合は false
  - すべての `Role.allowed_to?` が false の場合は false

## プラグイン

- `Plugin.permission`

  `Permission` を追加する。
