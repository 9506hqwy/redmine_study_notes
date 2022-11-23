# プラグイン

## プラグインのロード

Rails のイニシャライザでプラグインがロードされる(*config/initializers/30-redmine.rb*)。

`plugins` ディレクトリにあるディレクトリをプラグインとして読み込み、
`to_prepare` イベント発生時にすべてのプラグインの `init.rb` がディレクトリを読み込んだ順番に実行される。
すべてのプラグインの `init.rb` の処理が完了したらフック `after_plugins_loaded` が実行される。

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

Rails4 は `Controller._helpers` に `include` される。
`ActionController::Base` -> `ActionView::Layouts` -> `ActionView::Rendering` で `include` されている
`ActionView::Rendering._render_template` で `view_context` として `ActionView::Base` が作成され `Controller._helpers` を `include` し
`ActionView::Renderer.render` に渡される。
`Controler._helpers` は `Controller.helpers` で取得できる `ActionView::Base` にも `extend` されている(*actionpack/lib/action_controller/metal/helpers.rb*)。
