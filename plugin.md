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

Rails4 は `Controller._helpers` に `include` される。
`ActionController::Base` -> `ActionView::Layouts` -> `ActionView::Rendering` で `include` されている
`ActionView::Rendering._render_template` で `view_context` として `ActionView::Base` が作成され `Controller._helpers` を `include` し
`ActionView::Renderer.render` に渡される。
`Controler._helpers` は `Controller.helpers` で取得できる `ActionView::Base` にも `extend` されている(*actionpack/lib/action_controller/metal/helpers.rb*)。
