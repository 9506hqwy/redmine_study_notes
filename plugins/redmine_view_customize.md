# Redmine view customize plugin

## 添付ファイルとリポジトリのファイルプレビュー画面のキーボードショートカットを無効化する

* パスのパターン
  ```
  /(attachments|repository)/
  ```

* タイプ
  ```
  Javascript
  ```

* コード
  ```javascript
  document.addEventListener('DOMContentLoaded', function() {
      document.querySelectorAll('.filepreview').forEach(function(node) {
          node.classList.remove('filepreview');
      });
  });
  ```

* 参照
  - [Pagination between repository entries and attachments of the same container](https://www.redmine.org/issues/29395)
