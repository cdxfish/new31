/*
 *
 * sloadimg 1.0 - jquery异步滚动加载图片插件
 * Version 1.1.1
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 * 增加对img标签点击强制加载图片
 *
 *
 */
(function($) {
    $.fn.extend({
        sloadimg: function(options) {
            var $this = $(this);
            // 插件基本配置
            var conf = $.extend({
                src: "data-src",
                wrap: $(window),
                wrapHeight: $(window).height(),
                dom: $(this)
            }, options || {});
            // 像素分割
            var seg = function(px) {
                return Math.floor(px / conf.wrapHeight / 4);
            };
            // 重组数据
            var params = function(self) {
                var p = {};
                $('img', self).each(function() {
                    var $this = $(this);
                    $this.src = $this.attr(conf.src);
                    var i = seg($this.offset().top); !! p[i] ? p[i].push($this) : p[i] = [$this];
                }).click(function(){
                    var $this = $(this);
                    if(!$this.attr('src')){
                        $this.attr('src', $this.attr(conf.src));
                    }
                });
                return p
            };
            return {
                // 滚动条锚点
                s: 0,
                seg: seg,
                conf: conf,
                params: params($this),
                // 加载图片
                loading: function(i) { !! this.params[i] && $.each(this.params[i], function(v, n) {
                        !n.attr('src') && n.attr('src', n.src);
                    });
                },
                // 滚动定位
                location: function() {
                    var m = this.conf.wrap.scrollTop();
                    var s = this.s;
                    this.s = m;
                    return this.seg(m) + (m > s ? 1 : -1);
                },
                // 立即加载图片
                loadnow: function() {
                    this.loading(this.seg(this.conf.wrap.scrollTop()));
                    return this;
                },
                // 初始化
                ready: function() {
                    var self = this;
                    self.conf.wrap.on('scroll', function() {
                        self.loading(self.location());
                    });
                    return this;
                }
            }.ready();
        }
    })
})(jQuery);