# リポジトリ

## 初期化

*lib/redmine.rb* でバージョン管理ソフトウェアが登録される。

```ruby
Redmine::Scm::Base.add "XXX"
```

登録した名前で以下が決まる。

- `Repository` モデルを継承したクラス名
- リポジトリを登録する画面を構成する `RepositoriesHelper` のメソッド名 (`#{XXX.demodulize.underscore}_field_tags`)
- リポジトリを登録する画面のヒントのロケールメッセージ (`text_#{XXX.downcase}_repository_note`)

## モデル

リポジトリの設定を保存する。

- クラス名

  クラス名は初期化時に登録した名前で `Repository::XXX` となる必要がある。

- `human_attribute_name(attribute_key_name, *args)`

  データベースのカラム名と UI の項目名を対応付ける。

- `scm_name`

  クラスの `scm_name` を返却する。

- `name`

  識別子、"メインリポジトリ"、`scm_name` の優先順で返却する。

- `identifier_param`

  メインリポジトリの場合は""、識別子、データベース id の優先順で返却する。

- `report_last_commit`

  リポジトリ内のファイルの最終コミットを表示するかどうか。

- `supports_all_revisions`

  「統計」、「リビジョン」テキストボックス、「すべてのリビジョンを表示」、Atom を表示するかどうか。

- `supports_directory_revisions`

  ディレクトリにリビジョンのリンクを表示するかどうか。

- `supports_revision_graph`

  リビジョンのグラフを表示するかどうか。

- `self.scm_command`

  管理画面で表示されるリポジトリのコマンドに表示する文字列となる。

- `self.scm_version_string`

  管理画面で表示されるリポジトリのバージョンに表示する文字列となる。

- `self.changeset_identifier(changeset)`

  `Changeset` モデルの `ideintifier` となる。

- `self.format_changeset_identifier(changeset)`

  `Changeset` モデルの `format_identifier` となる。

- `latest_changesets(path,rev,limit=10)`

  参照に関連するリビジョンを表示する。

## アダプタ

バージョン管理ソフトウェアを操作する。

- `client_command`

  `Repository.scm_command` となる。

- `client_version_string`

  `Repository.scm_version_string` となる。

- `adapter_name`

  未使用

- `info`

  `Info` クラスを返却する。

- `entry(path=nil, identifier=nil)`

  path の `Entry` を返却する。

- `entries(path=nil, identifier=nil, options={})`

  path にあるファイル、ディレクトリを返却する。

- `branches`

  `Branch` の配列を返却する。

- `tags`

  タグを示す文字列の配列を返却する。

- `valid_name`

  リビジョン名が妥当かどうかを返却する。

### Info

- `initialize(attributes={})`

  - root_url: string
  - lastrev: `Revision`

### Entry

- `initialize(attributes={})`

  - name: string
  - path: string
  - kind: string # 'file' or 'dir'
  - size: string / integer
  - lastrev: `Revision`

- `changeset`

  リビジョンへのリンク、`Changeset.messages` がコメントに表示される。
  `Repository.load_entries_changesets` で格納される。

### Revision

- `initialize(attributes={})`

  - identifier: string
  - scmid: string
  - name: strig
  - auhtor: string
  - time: Time # without time zone
  - message: string
  - paths: hash[]
    - action: string # [A]dd, [D]elete, [R]ename, [C]opy, [M]odified
    - path: string
    - from_path: string
    - from_revision: string
  - revision
  - branch: string
  - parents: string[] # 親リビジョンの名前

- `form_identifier`

  表示するとき使用する文字列を返却する。

### Annotate

- `add_line(line: String, revision: Revision)`

### Branch

- String
  - revision
  - scmid
