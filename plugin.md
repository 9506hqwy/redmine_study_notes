# プラグイン

## プラグインのロード

Rails のイニシャライザでプラグインがロードされる(*config/initializers/30-redmine.rb*)。

Redmine4.2 以前は `plugins` ディレクトリにあるディレクトリをプラグインとして読み込み、プラグインの `init.rb` が実行される。
Redmine5.0 以降は `plugins` ディレクトリにあるディレクトリをプラグインとして読み込み、
`to_prepare` イベント発生時にすべてのプラグインの `init.rb` がディレクトリを読み込んだ順番に実行される。

Redmine4.2 以降の場合はすべてのプラグインの `init.rb` の処理が完了したら
フック `after_plugins_loaded` が実行される([#34072](https://www.redmine.org/issues/34072))。

## クラス拡張

### `include` と `prepend`

`include` でモジュールを拡張する前に、そのモジュールを `include` したクラスには影響はない。

```ruby
module Helper
end

module Included
  def a
  end
end

class Target
  include Helper
end

Helper.include(Included)

t = Target.new
Target.ancestors # [Target, Helper, Object, ...]
t.a # NoMethodError: undefined method `a' for
```

```ruby
module Helper
end

module Included
  def a
  end
end

Helper.include(Included)

class Target
  include Helper
end

t = Target.new
Target.ancestors # [Target, Helper, Included, Object, ...]
t.a
```

`prepend` も同じでモジュールを拡張する前に、そのモジュールを `include` したクラスには影響はない。

```ruby
module Helper
end

module Prepended
  def a
  end
end

class Target
  include Helper
end

Helper.prepend(Prepended)

t = Target.new
Target.ancestors # [Target, Helper, Object, ...]
t.a #NoMethodError: undefined method `a' for
```

```ruby
module Helper
end

module Prepended
  def a
  end
end

Helper.prepend(Prepended)

class Target
  include Helper
end

t = Target.new
Target.ancestors # [Target, Prepended, Helper, Object, ...]
t.a
```

プラグインがコントローラクラスを拡張したとで、
そのコントローラクラスに `include` されたモジュールを拡張してもコントローラから拡張した処理は実行できない。

ただし、Ruby3 ではあとから `include`, `prepend` したモジュールもコントローラから実行できる。

また、`include`, `prepend` のときに `Helper.class_eval` で定義した処理も実行できる。

### `alias` と `super`

`alias` と `super` で同じメソッドを上書きすると `alias` のあとの `super` の `include` は反映されない。

```ruby
module Included1
  def a
    puts '1'
  end
end

module Included2
  def self.included(base)
    base.class_eval do
      puts('class_eval')
      alias_method :a_orig, :a
      alias_method :a, :a_new
    end
  end

  def a_new
    puts '2'
    a_orig
  end
end

module Included3
  def a
    puts '3'
    super
  end
end

m = Module.new
m.include(Included1)
m.include(Included2)
m.include(Included3) # not affected

class Target
end

Target.include(m)

t = Target.new
Target.ancestors # [Target, #<Module:0x000055d4c650f4d8>, Included3, Included2, Included1, Object, ...]
t.a
# 2
# 1
```

### `alias` と `prepend`

`prepend` のあとに `alias`, `alias_method` すると無限ループする。

```ruby
class Target
  def a
    puts 'target'
  end
end

module Included
  def self.included(base)
    base.class_eval do
      alias a_without_b a
      alias a a_with_b
    end
  end

  def a_with_b
    puts 'included'
    a_without_b
  end
end

module Prepended
  def a
    puts 'prepended'
    super
  end
end

Target.prepend(Prepended)
Target.include(Included)

t = Target.new
Target.ancestors # [Prepended, Target, Included, Object, ...]
t.a
# prepended
# included
# prepended
# included
# ... loop ...
```

`alias`, `alias_method` のあとに `prepend` すると問題ない。

```ruby
class Target
  def a
    puts 'target'
  end
end

module Included
  def self.included(base)
    base.class_eval do
      alias a_without_b a
      alias a a_with_b
    end
  end

  def a_with_b
    puts 'included'
    a_without_b
  end
end

module Prepended
  def a
    puts 'prepended'
    super
  end
end

Target.include(Included)
Target.prepend(Prepended)

t = Target.new
Target.ancestors # [Prepended, Target, Included, Object, ...]
t.a
# prepended
# included
# target
```

### `helper` メソッド

`helper` メソッド (*actionpack/lib/abstract_controller/helpers.rb*) で `include` されたモジュールは view のみで使用できる。

`helper` メソッドはコントローラクラス内にある helper 用のモジュールに `include` される。
初回実行のとき `@_helpers` に格納される。`@_helpers` がない場合は継承しているクラスの helper が使用される。

Rails4 は `Controller._helpers` に `include` される。
`ActionController::Base` -> `ActionView::Layouts` -> `ActionView::Rendering` で `include` されている
`ActionView::Rendering._render_template` で `view_context` として `ActionView::Base` が作成され `Controller._helpers` を `include` し
`ActionView::Renderer.render` に渡される。
`Controler._helpers` は `Controller.helpers` で取得できる `ActionView::Base` にも `extend` されている(*actionpack/lib/action_controller/metal/helpers.rb*)。

`view_context` の作成元になる `view_context_class` は一度作成されると更新されない [with_empty_template_cache](https://github.com/rails/rails/blob/v7.2.2.1/actionview/lib/action_view/base.rb#L199-L211)。

Rails7.1 以降 eager_load が有効な場合(production モード)は `after_plugins_loaded` から `after_initialize` の間に `view_context_class` が生成されるため、
`after_initialize` で `helper` メソッドを実行して新規に `@_helpers` を格納しても `view_context_class` に反映されない [2fd3427](https://github.com/rails/rails/commit/2fd34270eb84854735426a75b9a9007cb10d90fa)。

eager_load は [Finisher](https://github.com/rails/rails/blob/v7.2.2.1/railties/lib/rails/application/finisher.rb#L82) で実行される。

## テスト

### カバレッジ

環境変数 `COVERAGE` を設定するとテスト時にコードカバレッジが *./coverage* ディレクトリに HTML 形式で格納される。

テストは以下のコマンドで実行できる。

1. タスクを使用する方法

   ```sh
   bundle exec rake redmine:plugins:test NAME=<プラグインの名前>
   ```

2. test コマンドを使用する方法

   ```sh
   bundle exec rake test TEST=plugins/<プラグインの名前>/test/**/*_test.rb
   ```

上記はプラグインのロードされるタイミングが異なる。
前者は `init.rb`, `test_helper.rb` の順に実行される。
後者は `test_helper.rb`, `init.rb` の順に実行される。

そのため、`test_helper.rb` 内で `SimpleCov.start` 前に `init.rb` で `require` する前者の実行方法では
*lib* ディレクトリのカバレッジを取得できない場合がある。

ただし Redmine6 以降はどちらも後者の動作となる。
[これ](https://github.com/redmine/redmine/commit/c38e847fa656e4007e44e7ee882e0abf105be8cb)
の影響か？

なぜか Redmine3 は影響を受けない。複数回 `init.rb` が呼ばれていそう。

```{note}
プラグインをシンボリックシンクでインストールしている場合に
*test/test_helper.rb* 内の `__FILE__` に格納されるパスはシンボリックリンクのままになる。
前者の場合、このシンボリックリンクが解決され絶対パスで `__FILE__` に格納される現象が発生した。
そのため Redmine の *test/test_helper.rb* を参照できずエラーが発生した。
原因は不明で devcontainer を再構築することで現象が発生しなくなった。
```

## その他

タスクの一覧を確認する。

```sh
bundle exec rails -T
```

```text
rails about                                       # List versions of all Rails frameworks and the environment
rails app:template                                # Applies the template supplied by LOCATION=(/path/to/template) or URL
 :
 :
```

タスクを実装している rake ファイルを確認する。

```sh
bundle exec rails -w
```

```text
rails about                          /usr/src/redmine/5.1/vendor/bundle/ruby/3.2.0/gems/railties-6.1.7.10/lib/rails/tasks/misc.rake:10:in `<top (required)>'
rails app:binstub:yarn               /usr/src/redmine/5.1/vendor/bundle/ruby/3.2.0/gems/railties-6.1.7.10/lib/rails/tasks/framework.rake:64:in `block (2 levels) in <top (required)>'
 :
 :
```

## 参照

- [Rails の初期化プロセス](https://railsguides.jp/initialization.html)
