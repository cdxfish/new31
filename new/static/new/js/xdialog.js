// JavaScript Document

function xDialog() {
    // document.write('<style type="text/css">');
    // document.write('#DialogWindow{ background-color:#fff;border:solid 1px #d3d3d3;}');
    // document.write('#DialogWindow h2{}');
    // document.write('#DialogWindow h2 span{float:left;}');
    // document.write('#DialogWindow h2 *{font-size:12px;}');
    // document.write('#DialogWindow h2 #DialogClose{color:#F00; position:absolute;right:0;}');
    // document.write('#DialogWindow #DialogForm{background-color:#fff;}');
    // document.write('</style>');
}
xDialog.prototype = {
    b: function() {
        alert("b");
    },
    c: "c",
    defaults: {
        width: 300,
        height: 200,
        title: '',
        dislogBack: '<div id="DialogBlock" style="background-color:#666666; position:absolute; z-index:99; left:0; top:0; display:; width:100%; height:1000px;opacity:0.5;filter: alpha(opacity=50);-moz-opacity: 0.5;"></div>',
        dialogbox: '<div id="DialogWindow" style="display:none;z-index:999;"> \
                                            <h2><a href="#this" id="DialogClose">CLOSE</a></h2> \
                                                <div id="DialogForm"> \
                                                </div> \
                                            </div>',
        left: 0,
        top: 0,
        Block: true //True 为显示遮照层
    },
    form: function(table, options) {
        options = $.extend({}, this.defaults, options || {});
        var forms = '<form id="DialogFormWindow" name="DialogFormWindow" method="post" action="">' + table + '</form>';
        this.show(forms, options);
        return $("#DialogFormWindow");
    },
    frame: function(url, options) {
        options = $.extend({}, this.defaults, options || {});
        var frames = '<iframe name="dialogiFrame" id="dialogiFrame" src="' + url + '" frameborder="0" scrolling="no" width="' + (options.width) + '" height="' + (options.height) + '"></iframe>';
        this.show(frames, options);
    },
    show: function(dialog, options) {
        options = $.extend({}, this.defaults, options || {});


        if (options.Block) $("body").append(options.dislogBack);
        $("body").append(options.dialogbox);

        //                          位置
        //                      
        var Scroll = this.GetScroll();
        var height = this.PageHeighe();
        var width = document.body.clientWidth;
        var bodyh = document.body.clientHeight < height ? height + Scroll : document.body.clientHeight;
        var wheight = options.height;
        var Top = options.top == 0 ? Scroll + (height - wheight) / 2 : options.top;
        var left = options.left == 0 ? (width - options.width) / 2 : options.left;


        //                          设置样式
        //                      
        $("#DialogBlock").css({
            height: (bodyh) + "px"
        });
        $("#DialogWindow").css({
            zIndex: "9999",
            width: options.width + "px",
            height: wheight + "px",
            position: "absolute",
            top: Top,
            left: left
        });
        $("#DialogForm").html(dialog);
        if (options.title != '') { //$("#DialogTitle").html(options.title); 
        }


        //                          显示
        //                      
        $("#DialogWindow").fadeIn(function() {
            $(this).animate({
                width: options.width + 'px',
                height: wheight + 'px'
                //                                                  left    : ( ( width - options.width ) / 2 ) + "px",
                //                                                  top     : ( Scroll + ( height- wheight )/2 ) + "px"
            }, 'slow');
        })

        //                          绑定
        //                      
        $("#DialogClose").bind("click", function() {
            $("#DialogWindow").remove();
            $("#DialogBlock").remove();
        })
    },
    GetScroll: function() {
        var yScroll;
        if (self.pageYOffset) {
            yScroll = self.pageYOffset;
        } else if (document.documentElement && document.documentElement.scrollTop) { // Explorer 6 Strict
            yScroll = document.documentElement.scrollTop;
        } else if (document.body) { // all other Explorers
            yScroll = document.body.scrollTop;
        }
        return yScroll;
    },
    PageHeighe: function() {
        var windowHeight
        if (self.innerHeight) { // all except Explorer
            windowHeight = self.innerHeight;
        } else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
            windowHeight = document.documentElement.clientHeight;
        } else if (document.body) { // other Explorers
            windowHeight = document.body.clientHeight;
        }
        return windowHeight
    },
    close: function() {
        $("#DialogWindow").remove();
        $("#DialogBlock").remove();
    },
    get: function(url) {
        $.get(url, function(data) {
            return data;
        })
    }
}