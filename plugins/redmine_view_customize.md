# Redmine view customize plugin

## 添付ファイルとリポジトリのファイルプレビュー画面のキーボードショートカットを無効化する

* パスのパターン

  ```text
  /(attachments|repository)/
  ```

* タイプ

  ```text
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
  * [Pagination between repository entries and attachments of the same container](https://www.redmine.org/issues/29395)

## プロジェクトごとにヘッダの背景色を変更する

プロジェクトごとにヘッダの背景色を設定する。

* パスのパターン

  ```text
  /
  ```

* プロジェクトのパターン

  ```text
  ^<プロジェクトのID>$
  ```

* タイプ

  ```text
  CSS
  ```

* コード

  ```css
  #top-menu {
    background-color: #0000CD;
  }

  #header {
    background-color: #005FFF;
  }

  #main-menu li a.new-object, #main-menu li a:hover {
    background-color: #2C7CFF;
  }
  ```

プロジェクト横断の issue 作成の画面でプロジェクトの選択ごとに背景色を変更する。

* パスのパターン

  ```text
  (^/issues/new$|^/issues/\d+)
  ```

* タイプ

  ```text
  Javascript
  ```

* コード

  ```javascript
  function changeBackgroundColor() {
    let projectId = document.getElementById('issue_project_id');
    switch (projectId.value) {
      case '1':
        document.getElementById('top-menu').style.background = '#0000CD';
        document.getElementById('header').style.background = '#005FFF';
        break;
      default:
        document.getElementById('top-menu').style.background = '#3E5B76';
        document.getElementById('header').style.background = '#628DB6';
        break;
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    let body = document.getElementsByTagName('body')[0];
    body.addEventListener('change', changeBackgroundColor);
    changeBackgroundColor();
  });
  ```
