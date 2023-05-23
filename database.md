# データベース

## 関連 (チケット)

```mermaid
classDiagram

class enumerations {
    id
    type
    project_id
}

class issue_categories {
    id
    project_id
    assigned_to_id
}

class issue_relations {
    id
    issue_from_id
    issue_to_id
    relation_type
}

class issue_statuses {
    id
}

class issues {
    id
    tracker_id
    project_id
    category_id
    status_id
    assigned_to_id
    priority_id
    fixed_version_id
    author_id
    parent_id
    root_id
}

class projects {
    id
    parent_id
    default_version_id
    default_assigned_to_id
}

class users {
    id
}

class trackers {
    id
}

class versions {
    id
    project_id
}

erDiagram

projects -- issues : projects.id = issues.project_id
projects -- users : projects.default_assigned_to_id = users.id
projects -- issue_categories : projects.id = issue_categories.project_id
projects -- enumerations : projects.id = enumerations.project_id
projects -- versions : projects.id = versions.project_id

users -- issues : users.id = issues.assigned_to_id
users -- issues : users.id = issues.author_id

issue_categories -- users : issue_categories.assigned_to_id = users.id
issue_categories -- issues : issue_categories.id = issues.category_id

enumerations -- issues : enumerations.id = issues.priority_id AND enumerations.type = 'IssuePriority'

issues -- trackers : issues.tracker_id = trackers.id
issues -- issue_statuses : issues.status_id = issus_statuses.id
issues -- versions : issues.fixed_version_id = versions.id
issues -- issues : issues.id = issues.parent_id (child issues)
issues -- issues : issues.id = issues.root_id (child issues)
issues -- issue_relations : issues.id = issue_relations.issue_from_id AND issue_relations.relation_type = 'relates'
issues -- issue_relations : issues.id = issue_relations.issue_to_id
```

## 関連 (チケットとコメント)

```mermaid
classDiagram

class issues {
    id
    tracker_id
    project_id
    category_id
    status_id
    assigned_to_id
    priority_id
    fixed_version_id
    author_id
    parent_id
    root_id
}

class journal_details {
    journal_id
}

class journals {
    id
    journalized_id
    journalized_type
    user_id
}

class users {
    id
}

erDiagram

issues -- journals : issues.id = journals.journalized_id AND journals.journalized_type = 'Issue'

journals -- journal_details : jourals.id = journal_details.journal_id
journals -- users : journals.user_id = users.id
```

## 関連 (チケットとカスタムフィールド)


```mermaid
classDiagram

class custom_fields {
    id
}

class custom_fields_projects {
    custom_field_id
    project_id
}

class custom_fields_trackers {
    custom_field_id
    tracker_id
}

class custom_values {
    customized_type
    customized_id
    custom_field_id
}

class issues {
    id
    tracker_id
    project_id
    category_id
    status_id
    assigned_to_id
    priority_id
    fixed_version_id
    author_id
    parent_id
    root_id
}

class projects {
    id
    parent_id
    default_version_id
    default_assigned_to_id
}

class trackers {
    id
}

erDiagram

issues -- trackers : issues.tracker_id = trackers.id
issues -- projects : issues.project_id = projects.id
issues -- custom_values : issues.id = custom_values.customized_id AND custom_valus.customized_type = 'Issue'

trackers -- custom_fields_trackers : trackers.id = custom_fields_trackers.tracker_id

projects -- custom_fields_projects : projects.id = custom_fields_projects.project_id

custom_fields_projects -- custom_fields : custom_fields_projects.custom_field_id = custom_fields.id

custom_fields_trackers -- custom_fields : custom_fields_trackers.custom_field_id = custom_fields.id

custom_fields -- custom_values : custom_fields.id = custom_values.custom_field_id
```

## 関連 (チケットと作業時間)

```mermaid
classDiagram

class enumerations {
    id
    type
    project_id
}

class issues {
    id
    tracker_id
    project_id
    category_id
    status_id
    assigned_to_id
    priority_id
    fixed_version_id
    author_id
    parent_id
    root_id
}

class projects {
    id
    parent_id
    default_version_id
    default_assigned_to_id
}

class users {
    id
}

class time_entries {
    project_id
    user_id
    issue_id
    activity_id
}

erDiagram

issues -- projects : issues.project_id = projects.id
issues -- time_entries : issues.id = time_entries.issue_id

enumerations -- time_entries : enumerations.id = time_entries.activity_id AND enumerations.type = 'TimeEntryActivity'

time_entries -- projects : time_entries.project_id = projects.id
time_entries -- users : time_entries.user_id = users.id
```

## 関連 (チケットとリポジトリ)


```mermaid
classDiagram

class changesets {
    id
    user_id
}

class changesets_issues {
    changeset_id
    issue_id
}

class issues {
    id
    tracker_id
    project_id
    category_id
    status_id
    assigned_to_id
    priority_id
    fixed_version_id
    author_id
    parent_id
    root_id
}

class users {
    id
}

erDiagram

issues -- changesets_issues : issues.id = changesets_issues.issue_id

changesets_issues -- changesets : changesets_issues.changeset_id = changesets.id

changesets -- users : changesets.user_id = users.id
```

## 関連 (チケットとウォッチャー)


```mermaid
classDiagram

class issues {
    id
    tracker_id
    project_id
    category_id
    status_id
    assigned_to_id
    priority_id
    fixed_version_id
    author_id
    parent_id
    root_id
}

class users {
    id
}

class watchers {
    watchable_type
    watchable_id
    user_id
}

erDiagram

issues -- watchers : issues.id = watchers.watchable_id AND watchers.watchable_type = 'Issue'

watchers -- users : watchers.user_id = user.id
```

## 関連 (リポジトリ)

```mermaid
classDiagram

class changes {
    changeset_id
}

class changeset_parents {
    changeset_id
    parent_id
}

class changesets {
    id
    repository_id
    user_id
}

class projects {
    id
}

class repositories {
    id
    project_id
}

class users {
    id
}

erDiagram

projects -- repositories : project.id = repositories.project_id

repositories -- changesets : repositories.id = changesets_repository_id

changesets -- changes : changesets.id = changes.changeset_id
changesets -- changeset_parents : changesets.id == changeset_parents.changeset_id
changesets -- changeset_parents : changesets.id == changeset_parents.parent_id
changesets -- users : changesets.user_id = users.id
```

## 関連 (ユーザ)

```mermaid
classDiagram

class auth_sources {
    id
}

class email_addresses {
    user_id
}

class groups_users {
    group_id
    user_id
}

class member_roles {
    member_id
    role_id
}

class members {
    id
    user_id
    project_id
}

class projects {
    id
}

class roles {
    id
}

class roles_managed_roles {
    role_id
    managed_role_id
}

class tokens {
    user_id
}

class user_preferences {
    user_id
}

class users {
    id
    auth_source_id
}

erDiagram

users -- auth_sources : users.auth_id = auth_sources.id
users -- email_addresses : users.id = email_addresses.user_id
users -- groups_users : users.id = groups_users.group_id
users -- groups_users : users.id = groups_users.user_id
users -- members : users.id = members.user_id
users -- user_preferences : users.id = user_preferences.user_id
users -- tokens : users.id = tokens.user_id

members -- member_roles : members.id = member_roles.member_id
members -- projects : members.project_id = projects.id

member_roles -- roles : member_roles.role_id = roles.id

roles -- roles_managed_roles : roles.id = roles_managed_roles.role_id
roles -- roles_managed_roles : roles.id = roles_managed_roles.managed_role_id
```

## 関連 (Wiki)

```mermaid
classDiagram

class projects {
    id
}

class users {
    id
}

class wiki_content_versions {
    wiki_content_id
    page_id
    author_id
}

class wiki_contents {
    id
    page_id
    author_id
}

class wiki_pages {
    id
    wiki_id
    parent_id
}

class wiki_redirects {
    wiki_id
    redirects_to_wiki_id
}

class wikis {
    id
    project_id
}

erDiagram

projects -- wikis : projects.id = wikis.project_id

wikis -- wiki_pages : wikis.id = wiki_pages.wiki_id
wikis -- wiki_redirects : wikis.id = wiki_id
wikis -- wiki_redirects : wikis.id = wiki_redirects_to_wiki_id

wiki_pages -- wiki_content_versions : wiki_pages.id = wiki_content_versions.page_id
wiki_pages -- wiki_contents : wiki_pages.id = wiki_contents.page_id
wiki_pages -- wiki_pages : wiki_pages.id = wiki_pages.parent_id

wiki_contents -- wiki_content_versions : wiki_contents.id = wiki_content_versions.wiki_content_id
wiki_contents -- users : wiki_contents.author_id = users.id

wiki_content_versions -- users : wiki_content_versions.author_id = users.id
```

## auth_sources

| 型       | カラム名          |
| :------: | :---------------: |
| integer  | id                |
| string   | type              |
| string   | name              |
| string   | host              |
| integer  | port              |
| string   | account           |
| string   | account_password  |
| string   | base_dn           |
| string   | attr_login        |
| string   | attr_firstname    |
| string   | attr_lastname     |
| string   | attr_mail         |
| boolean  | onthefly_register |
| boolean  | tls               |
| string   | filter            |
| integer  | timeout           |

## changes

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | changeset_id     |
| string   | action           |
| string   | path             |
| string   | from_path        |
| string   | from_revision    |
| string   | revision         |
| string   | branch           |

## changeset_parents

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | changeset_id     |
| integer  | parent_id        |

## changesets

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | repository_id    |
| string   | revision         |
| string   | committer        |
| datetime | comitted_on      |
| string   | comments         |
| date     | comit_date       |
| string   | scmid            |
| integer  | user_id          |

## changesets_issues

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | changeset_id     |
| integer  | issue_id         |

## custom_fields

| 型       | カラム名         | 備考                     |
| :------: | :--------------: | :----------------------: |
| integer  | id               |                          |
| string   | type             | カスタムフィールドの対象 |
| string   | name             | 名前                     |
| string   | field_format     | 形式                     |
| string   | possible_values  | 選択肢                   |
| string   | regexp           | 正規表現                 |
| integer  | min_length       | 最短長                   |
| integer  | max_length       | 最大長                   |
| boolean  | is_required      | 必須                     |
| boolean  | is_for_adll      | すべてのユーザー         |
| boolean  | is_filter        | フィルタとして使用       |
| integer  | position         |                          |
| boolean  | searchable       | 検索対象                 |
| string   | default_value    | デフォルト値             |
| boolean  | editable         |                          |
| boolean  | visible          | 次のロールのみ           |
| boolean  | multiple         | 複数選択可               |
| string   | format_store     | ※                       |
| string   | description      | 説明                     |

- format_store に yaml 形式で保存される。
  - edit_tag_style: 表示 (ドロップダウンリスト: ''、チェックボックス: check_box)
  - extensions_allowed: 許可する拡張子
  - full_width_layout: ワイド表示 ('', '1')
  - text_formatting: テキスト書式 ('', '1')
  - url_pattern: 値に設定するリンクURL
  - user_role: ロール (形式がユーザの場合)
  - version_status: ステータス (形式がバージョンの場合)

## custom_fields_projects

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | custom_field_id  |
| integer  | project_id       |


## custom_fields_trackers

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | custom_field_id  |
| integer  | tracker_id       |

## custom_values

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| string   | customized_type  |
| integer  | customized_id    |
| integer  | custom_field_id  |
| string   | value            |

## email_addresses

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | user_id          |
| string   | address          |
| boolean  | is_default       |
| boolean  | notify           |
| datetime | created_on       |
| datetime | updated_on       |

## enumerations

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| string   | name             |
| integer  | position         |
| boolean  | is_default       |
| string   | type             |
| boolean  | active           |
| integer  | project_id       |
| integer  | parent_id        |
| string   | position_name    |

## groups_users

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | group_id         |
| integer  | user_id          |

## issue_categories

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | project_id       |
| string   | name             |
| integer  | assigned_to_id   |

## issue_relations

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | issue_from_id      |
| integer  | issue_to_id        |
| string   | relation_type      |
| integer  | delay              |

## issue_statuses

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| string   | name               |
| boolean  | is_closed          |
| integer  | position           |
| integer  | default_done_ratio |

## issues

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | tracker_id       |
| integer  | project_id       |
| string   | subject          |
| string   | description      |
| date     | due_date         |
| integer  | category_id      |
| integer  | status_id        |
| integer  | assigned_to_id   |
| integer  | priority_id      |
| integer  | fixed_version_id |
| integer  | author_id        |
| integer  | lock_version     |
| datetime | created_on       |
| datetime | updated_on       |
| date     | start_date       |
| integer  | done_ratio       |
| double   | estimated_hours  |
| integer  | parent_id        |
| integer  | root_id          |
| integer  | lft              |
| integer  | rgt              |
| boolean  | is_private       |
| datetime | cloed_on         |

`lock_version` は rails の [Optimistic Locking](https://guides.rubyonrails.org/active_record_querying.html#optimistic-locking) で使用する。

## journal_details

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | journal_id       |
| string   | property         |
| string   | prop_key         |
| string   | old_value        |
| string   | value            |

`property` が `attr` の場合は `prop_key` に `issues` のプロパティ名が格納される。
`property` が `cf` の場合は `prop_key` に `custom_fields.id` が格納される。

## journals

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | journalized_id   |
| string   | journalized_type |
| integer  | user_id          |
| string   | notes            |
| datetime | created_on       |
| boolean  | private_notes    |

## member_roles

| 型       | カラム名               |
| :------: | :--------------------: |
| integer  | id                     |
| integer  | member_id              |
| integer  | role_id                |
| integer  | inherited_from         |

## members

| 型       | カラム名               |
| :------: | :--------------------: |
| integer  | id                     |
| integer  | user_id                |
| integer  | project_id             |
| datetime | created_on             |
| boolean  | mail_notification      |

## projects

| 型       | カラム名               |
| :------: | :--------------------: |
| integer  | id                     |
| string   | name                   |
| string   | description            |
| string   | homepage               |
| boolean  | is_public              |
| integer  | parent_id              |
| datetime | created_on             |
| datetime | updated_on             |
| string   | identifier             |
| integer  | status                 |
| integer  | lft                    |
| integer  | rgt                    |
| boolean  | inherit_members        |
| integer  | default_version_id     |
| integer  | default_assigned_to_id |

## repositories

| 型       | カラム名               | 備考                                          |
| :------: | :--------------------: | :-------------------------------------------: |
| integer  | id                     |                                               |
| integer  | project_id             |                                               |
| string   | url                    |                                               |
| string   | login                  | ログインID                                    |
| string   | password               | パスワード                                    |
| string   | root_url               |                                               |
| string   | type                   | バージョン管理システム "Respotiory::Git" など |
| string   | path_encoding          | パスのエンコーディング                        |
| string   | log_encoding           | コミットメッセージのエンコーディング          |
| string   | extra_info             | ※                                            |
| string   | identifier             | 識別子                                        |
| boolean  | is_default             | メインリポジトリ                              |
| datetime | created_on             |                                               |

password は `database_cipher_key` で暗号化される。

extra_info に yaml の形式で保存される。
  - Git の場合
    - extra_report_last_commit: `report_last_commit` の値 (ファイルとディレクトリの最新コミットを表示する)
    - heads: ブランチの HEAD
    - db_consistent.ordering: ???

## roles

| 型       | カラム名                |
| :------: | :---------------------: |
| integer  | id                      |
| string   | name                    |
| integer  | position                |
| boolean  | assignable              |
| integer  | builtin                 |
| string   | permissions             |
| string   | issues_visibility       |
| string   | users_visibility        |
| string   | time_entries_visibility |
| boolean  | all_roles_managed       |
| string   | settings                |

## roles_managed_roles

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | role_id          |
| integer  | managed_role_id  |

## time_entries

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| integer  | project_id       |
| integer  | user_id          |
| integer  | issue_id         |
| double   | hours            |
| string   | comments         |
| integer  | activity_id      |
| date     | spent_on         |
| integer  | tryear           |
| integer  | tmonth           |
| integer  | tweek            |
| datetime | created_on       |
| datetime | updated_on       |

## tokens

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | user_id            |
| string   | action             |
| string   | value              |
| datetime | created_on         |
| datetime | updated_on         |

## trackers

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| string   | name               |
| boolean  | is_in_chlog        |
| integer  | position           |
| boolean  | is_in_roadmap      |
| integer  | fields_bits        |
| integer  | default_status_id  |

## user_preferences

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | user_id            |
| string   | others             |
| boolean  | hide_mail          |
| string   | time_zone          |

## users

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| string   | login              |
| string   | hashed_password    |
| string   | firstname          |
| string   | lastname           |
| boolean  | admin              |
| integer  | status             |
| datetime | last_login_on      |
| strng    | language           |
| integer  | auth_source_id     |
| datetime | created_on         |
| datetime | updated_on         |
| string   | type               |
| string   | identity_url       |
| string   | mail_notification  |
| string   | salt               |
| boolean  | must_change_passed |
| datetime | passed_changed_on  |

## versions

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | project_id         |
| string   | name               |
| string   | description        |
| date     | effective_date     |
| datetime | created_on         |
| datetime | updated_on         |
| string   | wiki_page_title    |
| string   | status             |
| string   | sharing            |

## watchers

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| string   | watchable_type     |
| integer  | watchable_id       |
| integer  | user_id            |

## wiki_content_versions

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | wiki_content_id    |
| integer  | page_id            |
| integer  | author_id          |
| bytes    | data               |
| string   | compression        |
| string   | comments           |
| datetime | updated_on         |
| integer  | version            |

## wiki_contents

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | page_id            |
| integer  | authtor_id         |
| string   | text               |
| string   | commments          |
| datetime | updated_on         |
| integer  | version            |

## wiki_pages

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | wiki_id            |
| string   | title              |
| datetime | created_on         |
| boolean  | protected          |
| integer  | parent_id          |

## wiki_redirects

| 型       | カラム名             |
| :------: | :------------------: |
| integer  | id                   |
| integer  | wiki_id              |
| string   | title                |
| string   | redirect_to          |
| datetime | created_on           |
| integer  | redirects_to_wiki_id |

## wikis

| 型       | カラム名           |
| :------: | :----------------: |
| integer  | id                 |
| integer  | project_id         |
| string   | start_page         |
| integer  | status             |

## 参照

- [Database Model](https://www.redmine.org/projects/redmine/wiki/DatabaseModel)
