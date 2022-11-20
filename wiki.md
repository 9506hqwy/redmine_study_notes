# Wiki

## 権限

Redmine 3.4-5.0 の権限を記載する。

### Wikiの管理(manage_wiki)

- app/helpers/projects_helper.rb
  - プロジェクト設定ページの [Wiki] タブを表示する。 ([#26579](https://www.redmine.org/issues/26579))
- app/models/wiki_page.rb
  - `WikiPage#safe_attributes(is_start_page)` ([#26579](https://www.redmine.org/issues/26579))
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikisController#edit`
  - `WikisController#destory`

### Wikiページ名の変更(rename_wiki_pages)

- app/helpers/wiki_helper.rb
  - `WikiHelper#wiki_page_wiki_options_for_select`
- app/models/wiki_page.rb
  - `WikiPage#safe_attributes`
  - `WikiPage#safe_attributes=`
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikiController#rename`

### Wikiページの削除(delete_wiki_pages)

- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikiController#destroy`
  - `WikiController#destroy_version`
- lib/redmine/default_data/loader.rb
  - 開発者ロール

### Wikiの閲覧(view_wiki_pages)

- app/controllers/auto_completes_controller.rb
  - `AutoCompletesController#wiki_pages` ([#33820](https://www.redmine.org/issues/33820))
- app/helpers/application_helper.rb
  - `ApplicationHelper#parse_wiki_links`
- app/models/wiki.rb
  - `Wiki#visible`
- app/models/wiki_page.rb
  - `WikiPage#acts_as_searchable`
  - `WikiPage#visible`
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikiController#index`
  - `WikiController#show`
  - `WikiController#special` (-1.1)
  - `WikiController#date_index`
- lib/redmine/default_data/loader.rb
  - 開発者ロール
  - 報告者ロール
  - 非メンバロール
  - 匿名ユーザロール
- lib/redmine/wiki_formatting/macros.rb
  - `child_pages` マクロ
  - `include` マクロ

### Wikiページを他の形式にエクスポート(export_wiki_pages)

- app/controllers/wiki_controller.rb
  - `WikiController#show`
- lib/redmine.rb
  - `WikiController#export`

### Wiki履歴の閲覧(view_wiki_edits)

- app/controllers/wiki_controller.rb
  - `WikiController#show`
- app/models/wiki_content.rb
  - `WikiContent.Version#acts_as_activity_provider` ([#26548](https://www.redmine.org/issues/26548))
- app/models/wiki_content_version.rb
  - `WikiContentVersion#acts_as_activity_provider` ([#26548](https://www.redmine.org/issues/26548))
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikiController#history`
  - `WikiController#diff`
  - `WikiController#annotate`
- lib/redmine/default_data/loader.rb
  - 開発者ロール
  - 報告者ロール
  - 非メンバロール
  - 匿名ユーザロール

### Wikiページの編集(edit_wiki_pages)

- app/controllers/wiki_controller.rb
  - `WikiController#new`
  - `WikiController#show`
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikiController#new`
  - `WikiController#edit`
  - `WikiController#update`
  - `WikiController#preview`
  - `WikiController#add_attachment`
- lib/redmine/default_data/loader.rb
  - 開発者ロール

### 添付ファイルの削除(delete_wiki_pages_attaachments)

- app/models/wiki_page.rb
  - `WikiPage#acts_as_attachable`
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - None

### Wikiページの凍結(-4.0) / Wikiページの保護(4.1-) (protect_wiki_pages)

- app/models/wiki_page.rb
  - `WikiPage#editable_by?`
- lib/redmine.rb(-4.2), lib/redmine/preparation.rb(5.0-)
  - `WikiController#protect`
