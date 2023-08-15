# 設定

## チケットトラッキング

### 休業日

休業日の曜日(non_working_week_days)を設定する。設定した値は以下の機能に影響する。

- ガントチャートのグレー表示 (ブラウザ表示とエクスポート時)
  - *app/views/gantts/show.html.erb*
  - *lib/redmine/helpers/gantt.rb*
- カレンダーのグレー表示
  - *app/helpers/calendars_helper.rb*
- 関連するチケットの設定で「次のチケットに先行」を設定したときに、
  遅延日から休業日を除いて関連されたチケットの開始日と期日を自動設定
  - reschedule_following_issues (*app/models/issue.rb*)
  - handle_issue_order (*app/models/issue_relation.rb*)
