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

| 型       | カラム名         |
| :------: | :--------------: |
| integer  | id               |
| string   | type             |
| string   | name             |
| string   | field_format     |
| string   | possible_values  |
| string   | regexp           |
| integer  | min_length       |
| integer  | max_length       |
| boolean  | is_required      |
| boolean  | is_for_adll      |
| boolean  | is_filter        |
| integer  | position         |
| boolean  | searchable       |
| string   | default_value    |
| boolean  | editable         |
| boolean  | visible          |
| boolean  | multiple         |
| string   | format_store     |
| string   | description      |

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

## 参照

- [Database Model](https://www.redmine.org/projects/redmine/wiki/DatabaseModel)
