(function(b) {
    b.Zebra_DatePicker = function(B, v) {
        var P = {
            days: "日,一,二,三,四,五,六".split(","),
            direction: 0,
            disabled_dates: !1,
            first_day_of_week: 1,
            format: "Y-m-d",
            months: "一月,二月,三月,四月,五月,六月,七月,八月,九月,十月,十一月,十二月".split(","),
            offset: [20, -5],
            readonly_element: !0,
            show_week_number: !1,
            view: "days",
            weekend_days: [0, 6]
        }, n, k, w, s, t, x, y, G, C, L, e, h, p, o, f, H, I, J, D, A, l, E, c = this;
        c.settings = {};
        var F = b(B);
        c.hide = function() {
            M("hide");
            k.css("display",
                "none")
        };
        c.show = function() {
            z();
            var a = k.outerWidth(),
                d = k.outerHeight(),
                r = w.offset().left + c.settings.offset[0],
                i = w.offset().top - d + c.settings.offset[1],
                g = b(window).width(),
                N = b(window).height(),
                f = b(window).scrollTop(),
                j = b(window).scrollLeft();
            r + a > j + g && (r = j + g - a);
            r < j && (r = j);
            i + d > f + N && (i = f + N - d);
            i < f && (i = f);
            k.css({
                left: r,
                top: i
            });
            k.fadeIn(b.browser.msie && b.browser.version.match(/^[6-8]/) ? 0 : 150, "linear");
            M()
        };
        var R = function(a) {
            if (b.trim(a) != "") {
                for (var d = Q(c.settings.format.replace(/\s/g, "")), r = "d,D,j,l,N,S,w,F,m,M,n,Y,y".split(","),
                i = [], g = [], f = 0; f < r.length; f++)(position = d.indexOf(r[f])) > -1 && i.push({
                    character: r[f],
                    position: position
                });
                i.sort(function(a, d) {
                    return a.position - d.position
                });
                b.each(i, function(a, d) {
                    switch (d.character) {
                        case "d":
                            g.push("0[1-9]|[12][0-9]|3[01]");
                            break;
                        case "D":
                            g.push("[a-z]{3}");
                            break;
                        case "j":
                            g.push("[1-9]|[12][0-9]|3[01]");
                            break;
                        case "l":
                            g.push("[a-z]+");
                            break;
                        case "N":
                            g.push("[1-7]");
                            break;
                        case "S":
                            g.push("st|nd|rd|th");
                            break;
                        case "w":
                            g.push("[0-6]");
                            break;
                        case "F":
                            g.push("[a-z]+");
                            break;
                        case "m":
                            g.push("0[1-9]|1[012]+");
                            break;
                        case "M":
                            g.push("[a-z]{3}");
                            break;
                        case "n":
                            g.push("[1-9]|1[012]");
                            break;
                        case "Y":
                            g.push("[0-9]{4}");
                            break;
                        case "y":
                            g.push("[0-9]{2}")
                    }
                });
                if (g.length && (i.reverse(), b.each(i, function(a, b) {
                    d = d.replace(b.character, "(" + g[g.length - a - 1] + ")")
                }), g = RegExp("^" + d + "$", "ig"), segments = g.exec(a.replace(/\s/g, "")))) {
                    var k, e, h, l = "日,一,二,三,四,五,六".split(","),
                        m = "一月,二月,三月,四月,五月,六月,七月,八月,九月,十月,十一月,十二月".split(","),
                        o, n = !0;
                    i.reverse();
                    b.each(i, function(a, d) {
                        if (!n) return !0;
                        switch (d.character) {
                            case "m":
                            case "n":
                                e = j(segments[a + 1]);
                                break;
                            case "d":
                            case "j":
                                k = j(segments[a + 1]);
                                break;
                            case "D":
                            case "l":
                            case "F":
                            case "M":
                                o = d.character == "D" || d.character == "l" ? c.settings.days : c.settings.months;
                                n = !1;
                                b.each(o, function(b, c) {
                                    if (n) return !0;
                                    if (segments[a + 1].toLowerCase() == c.substring(0, d.character == "D" || d.character == "M" ? 3 : c.length).toLowerCase()) {
                                        switch (d.character) {
                                            case "D":
                                                segments[a + 1] = l[b].substring(0, 3);
                                                break;
                                            case "l":
                                                segments[a + 1] = l[b];
                                                break;
                                            case "F":
                                                segments[a + 1] = m[b];
                                                e = b + 1;
                                                break;
                                            case "M":
                                                segments[a + 1] = m[b].substring(0, 3), e = b + 1
                                        }
                                        n = !0
                                    }
                                });
                                break;
                            case "Y":
                                h = j(segments[a + 1]);
                                break;
                            case "y":
                                h = "19" + j(segments[a + 1])
                        }
                    });
                    if (n && (a = new Date(h, e - 1, k), a.getFullYear() == h && a.getDate() == k && a.getMonth() == e - 1)) return a
                }
                return !1
            }
        }, S = function(a) {
            b.browser.mozilla ? a.css("MozUserSelect", "none") : b.browser.msie ? a.bind("selectstart", function() {
                return !1
            }) : a.mousedown(function() {
                return !1
            })
        }, Q = function(a) {
            return a.replace(/([-.*+?^${}()|[\]\/\\])/g, "\\$1")
        }, T = function(a) {
            for (var d =
                "", b = a.getDate(), i = a.getDay(), g = c.settings.days[i], f = a.getMonth() + 1, j = c.settings.months[f - 1], a = a.getFullYear() + "", e = 0; e < c.settings.format.length; e++) {
                var h = c.settings.format.charAt(e);
                switch (h) {
                    case "y":
                        a = a.substr(2);
                    case "Y":
                        d += a;
                        break;
                    case "m":
                        f = m(f, 2);
                    case "n":
                        d += f;
                        break;
                    case "M":
                        j = j.substr(0, 3);
                    case "F":
                        d += j;
                        break;
                    case "d":
                        b = m(b, 2);
                    case "j":
                        d += b;
                        break;
                    case "D":
                        g = g.substr(0, 3);
                    case "l":
                        d += g;
                        break;
                    case "N":
                        i++;
                    case "w":
                        d += i;
                        break;
                    case "S":
                        d += b % 10 == 1 && b != "11" ? "st" : b % 10 == 2 && b != "12" ? "nd" : b % 10 == 3 && b != "13" ? "rd" : "th";
                        break;
                    default:
                        d += h
                }
            }
            return d
        }, O = function() {
            var a = (new Date(f, o + 1, 0)).getDate(),
                d = (new Date(f, o, 1)).getDay(),
                r = (new Date(f, o, 0)).getDate();
            d -= c.settings.first_day_of_week;
            d = d < 0 ? 7 + d : d;
            K(c.settings.months[o] + ", " + f);
            var i = "<tr>";
            c.settings.show_week_number && (i += "<th>" + c.settings.show_week_number + "</th>");
            for (var g = 0; g < 7; g++) i += "<th>" + c.settings.days[(c.settings.first_day_of_week + g) % 7].substr(0, 2) + "</th>";
            i += "</tr><tr>";
            for (g = 0; g < 42; g++) {
                g > 0 && g % 7 == 0 && (i += "</tr><tr>");
                if (g % 7 == 0 && c.settings.show_week_number) {
                    var e = new Date(f, o, g),
                        e = Math.ceil(((e - new Date(f, 0, 1)) / 864E5 + e.getDay() + 1) / 7);
                    i += '<td class="dp_week_number">' + e + "</td>"
                }
                e = g - d + 1;
                if (g < d) i += '<td class="dp_not_in_month">' + (r - d + g + 1) + "</td>";
                else if (e > a) i += '<td class="dp_not_in_month">' + (e - a) + "</td>";
                else {
                    var h = (c.settings.first_day_of_week + g) % 7,
                        k = j(q(f, m(o, 2), m(e, 2)));
                    class_name = "";
                    u(k) || void 0 != E && (c.settings.direction[0] > 0 && k > E || c.settings.direction[0] <= 0 && k < E) ? b.inArray(h, c.settings.weekend_days) > -1 ? class_name = "dp_weekend_disabled" : class_name += " dp_disabled" : (b.inArray(h, c.settings.weekend_days) > -1 && (class_name = "dp_weekend"), o == I && f == J && H == e ? class_name += " dp_selected" : o == G && f == C && L == e && (class_name += " dp_current"));
                    i += "<td" + (class_name != "" ? ' class="' + b.trim(class_name) + '"' : "") + ">" + m(e, 2) + "</td>"
                }
            }
            i += "</tr>";
            t.html(b(i));
            t.css("display", "")
        }, M = function(a) {
            if (b.browser.msie && b.browser.version.match(/^6/)) {
                if (!A) {
                    var d = j(k.css("zIndex")) - 1;
                    A = jQuery("<iframe>", {
                        src: 'javascript:document.write("")',
                        scrolling: "no",
                        frameborder: 0,
                        allowtransparency: "true",
                        css: {
                            zIndex: d,
                            position: "absolute",
                            top: -1E3,
                            left: -1E3,
                            width: k.outerWidth(),
                            height: k.outerHeight(),
                            filter: "progid:DXImageTransform.Microsoft.Alpha(opacity=0)",
                            display: "none"
                        }
                    });
                    b("body").append(A)
                }
                switch (a) {
                    case "hide":
                        A.css("display", "none");
                        break;
                    default:
                        a = k.offset(), A.css({
                            top: a.top,
                            left: a.left,
                            display: "block"
                        })
                }
            }
        }, u = function(a) {
            if (l !== 0) {
                var d = (a + "").length;
                if (d == 8 && (l && a < q(h, m(e, 2), m(p, 2)) || !l && a > q(h, m(e, 2), m(p, 2)))) return !0;
                else if (d == 6 && (l && a < q(h, m(e, 2)) || !l && a > q(h, m(e, 2)))) return !0;
                else if (d == 4 && (l && a < h || !l && a > h)) return !0
            }
            if (D) {
                a += "";
                var c = j(a.substr(0, 4)),
                    i = j(a.substr(4, 2)) + 1,
                    g = j(a.substr(6, 2)),
                    f = !1;
                b.each(D, function() {
                    if (!f && (b.inArray(c, this[2]) > -1 || b.inArray("*", this[2]) > -1)) if (void 0 != i && b.inArray(i, this[1]) > -1 || b.inArray("*", this[1]) > -1) if (void 0 != g && b.inArray(g, this[0]) > -1 || b.inArray("*", this[0]) > -1) {
                        if (this[3] == "*") return f = !0;
                        var a = (new Date(c, i - 1, g)).getDay();
                        if (b.inArray(a, this[3]) > -1) return f = !0
                    }
                });
                if (f) return !0
            }
            return !1
        }, K = function(a) {
            s.find(".dp_caption").html(a);
            if (l !== 0) {
                var a = f,
                    d = o,
                    b;
                n == "days" ? (l && --d < 0 ? (d = 11, a--) : !l && ++d > 11 && (d = 0, a++), b = q(a, m(d, 2))) : n == "months" ? (l ? a-- : a++, b = a) : n == "years" && (l ? a -= 7 : a += 7, b = a);
                u(b) ? (s.find(l ? ".dp_previous" : ".dp_next").addClass("dp_blocked"), s.find(l ? ".dp_previous" : ".dp_next").removeClass("dp_hover")) : s.find(l ? ".dp_previous" : ".dp_next").removeClass("dp_blocked")
            }
        }, z = function() {
            if (t.text() == "" || n == "days") {
                if (t.text() == "") {
                    k.css({
                        left: -1E3,
                        display: "block"
                    });
                    O();
                    var a = t.outerWidth(),
                        d = t.outerHeight();
                    s.css("width", a);
                    x.css({
                        width: a,
                        height: d
                    });
                    y.css({
                        width: a,
                        height: d
                    });
                    k.css({
                        display: "none"
                    })
                } else O();
                x.css("display", "none");
                y.css("display", "none")
            } else if (n == "months") {
                K(f);
                a = "<tr>";
                for (d = 0; d < 12; d++) {
                    d > 0 && d % 3 == 0 && (a += "</tr><tr>");
                    var e = "dp_month_" + d,
                        i = j(q(f, m(d, 2)));
                    u(i) ? e += " dp_disabled" : G == d && C == f && (e += " dp_current");
                    a += '<td class="' + b.trim(e) + '">' + c.settings.months[d].substr(0, 3) + "</td>"
                }
                a += "</tr>";
                x.html(b(a));
                x.css("display", "");
                t.css("display", "none");
                y.css("display", "none")
            } else if (n == "years") {
                K(f - 7 + " - " + (f + 4));
                a = "<tr>";
                for (d = 0; d < 12; d++) d > 0 && d % 3 == 0 && (a += "</tr><tr>"), e = "", i = j(f - 7 + d), u(i) ? e += " dp_disabled" : C == f - 7 + d && (e += " dp_current"), a += "<td" + (b.trim(e) != "" ? ' class="' + b.trim(e) + '"' : "") + ">" + (f - 7 + d) + "</td>";
                a += "</tr>";
                y.html(b(a));
                y.css("display", "");
                t.css("display", "none");
                x.css("display", "none")
            }
        }, m = function(a, d) {
            for (a += ""; a.length < d;) a = "0" + a;
            return a
        }, q = function() {
            for (var a = "", d = 0; d < arguments.length; d++) a += arguments[d] + "";
            return a
        }, j = function(a) {
            return parseInt(a === !0 || a === !1 ? 0 : a, 10)
        };
        c._keyup = function(a) {
            (k.css("display") == "block" || a.which == 27) && c.hide();
            return !0
        };
        c._mousedown = function(a) {
            if (k.css("display") == "block") {
                if (b(a.target).get(0) === w.get(0)) return !0;
                b(a.target).parents().filter(".Zebra_DatePicker").length == 0 && c.hide()
            }
            return !0
        };
        (function() {
            c.settings = b.extend({}, P, v);
            c.settings.readonly_element && F.attr("readonly", "readonly");
            n = c.settings.view;
            var a;
            w = b('<button type="button" class="Zebra_DatePicker_Icon">Pick a date</button>');
            c.icon = w;
            l = !b.isArray(c.settings.direction) && (c.settings.direction === !0 || j(c.settings.direction) > 0) || b.isArray(c.settings.direction) && c.settings.direction.length == 2 && (c.settings.direction[0] === !0 || j(c.settings.direction[0]) > 0) ? !0 : !b.isArray(c.settings.direction) && (c.settings.direction === !1 || j(c.settings.direction) < 0) || b.isArray(c.settings.direction) && c.settings.direction.length == 2 && (c.settings.direction[0] === !1 || j(c.settings.direction[0]) < 0) ? !1 : 0;
            a = new Date;
            e = a.getMonth();
            G = a.getMonth();
            h = a.getFullYear();
            C = a.getFullYear();
            p = a.getDate();
            L = a.getDate();
            l !== 0 && (a = new Date(h, e, p + j(b.isArray(c.settings.direction) ? c.settings.direction[0] : c.settings.direction)), e = a.getMonth(), h = a.getFullYear(), p = a.getDate());
            l !== 0 && b.isArray(c.settings.direction) && c.settings.direction.length == 2 && (a = new Date(h, e, p + (l > 0 ? 1 : -1) * j(c.settings.direction[1])), E = j(q(a.getFullYear(), m(a.getMonth(), 2), m(a.getDate(), 2))));
            if (u(q(h, m(e, 2), m(p, 2)))) {
                for (; u(h);) l ? h++ : h--, e = 0;
                for (; u(q(h, m(e, 2)));) l ? e++ : e--, e > 11 ? (h++, e = 0) : e < 0 && (h--, e = 0), p = 1;
                for (; u(q(h, m(e, 2), m(p, 2)));) l ? p++ : p--, a = new Date(h, e, p), h = a.getFullYear(), e = a.getMonth(), p = a.getDate()
            }(c.settings.readonly_element ? w.add(F) : w).bind("click", function(a) {
                a.preventDefault();
                k.css("display") != "none" ? c.hide() : ((a = R(F.val())) ? (I = a.getMonth(), o = a.getMonth(), J = a.getFullYear(), f = a.getFullYear(), H = a.getDate(), u(q(J, m(I, 2), m(H, 2))) && (o = e, f = h)) : (o = e, f = h), z(), c.show())
            });
            w.insertAfter(B);
            k = b('<div class="Zebra_DatePicker"><table class="dp_header"><tr><td class="dp_previous">&laquo;</td><td class="dp_caption">&nbsp;</td><td class="dp_next">&raquo;</td></tr></table><table class="dp_daypicker"></table><table class="dp_monthpicker"></table><table class="dp_yearpicker"></table></div>');
            c.datepicker = k;
            s = k.find("table.dp_header").first();
            t = k.find("table.dp_daypicker").first();
            x = k.find("table.dp_monthpicker").first();
            y = k.find("table.dp_yearpicker").first();
            b("body").append(k);
            k.delegate("td:not(.dp_disabled, .dp_weekend_disabled, .dp_not_in_month, .dp_blocked, .dp_week_number)", "mouseover", function() {
                b(this).addClass("dp_hover")
            }).delegate("td:not(.dp_disabled, .dp_weekend_disabled, .dp_not_in_month, .dp_blocked, .dp_week_number)", "mouseout", function() {
                b(this).removeClass("dp_hover")
            });
            S(s.find("td"));
            s.find(".dp_previous").bind("click", function() {
                b(this).hasClass("dp_blocked") || (n == "months" ? f-- : n == "years" ? f -= 12 : --o < 0 && (o = 11, f--), z())
            });
            s.find(".dp_caption").bind("click", function() {
                n = n == "days" ? "months" : n == "months" ? "years" : "days";
                z()
            });
            s.find(".dp_next").bind("click", function() {
                b(this).hasClass("dp_blocked") || (n == "months" ? f++ : n == "years" ? f += 12 : ++o == 12 && (o = 0, f++), z())
            });
            t.delegate("td:not(.dp_disabled, .dp_weekend_disabled, .dp_not_in_month, .dp_week_number)", "click", function() {
                F.val(T(new Date(f,
                o, j(b(this).html())))).change();
                c.hide()
            });
            x.delegate("td:not(.dp_disabled)", "click", function() {
                var a = b(this).attr("class").match(/dp\_month\_([0-9]+)/);
                o = j(a[1]);
                n = "days";
                z()
            });
            y.delegate("td:not(.dp_disabled)", "click", function() {
                f = j(b(this).html());
                n = "months";
                z()
            });
            b(document).bind({
                mousedown: c._mousedown,
                keyup: c._keyup
            });
            D = [];
            b.each(c.settings.disabled_dates, function() {
                for (var a = this.split(" "), c = 0; c < 4; c++) {
                    a[c] || (a[c] = "*");
                    a[c] = b.inArray(",", a[c]) > -1 ? a[c].split(",") : Array(a[c]);
                    for (var e = 0; e < a[c].length; e++) if (b.inArray("-",
                    a[c][e]) > -1) {
                        var f = a[c][e].match(/^([0-9]+)\-([0-9]+)/);
                        if (null != f) {
                            for (var h = j(f[1]); h <= j(f[2]); h++) b.inArray(h, a[c]) == -1 && a[c].push(h + "");
                            a[c].splice(e, 1)
                        }
                    }
                    for (e = 0; e < a[c].length; e++) a[c][e] = isNaN(j(a[c][e])) ? a[c][e] : j(a[c][e])
                }
                D.push(a)
            })
        })()
    };
    b.fn.Zebra_DatePicker = function(B) {
        return this.each(function() {
            if (void 0 != b(this).data("Zebra_DatePicker")) {
                var v = b(this).data("Zebra_DatePicker");
                v.icon.remove();
                v.datepicker.remove();
                b(document).unbind("keyup", v._keyup);
                b(document).unbind("mousedown", v._mousedown)
            }
            v = new b.Zebra_DatePicker(this, B);
            b(this).data("Zebra_DatePicker", v)
        })
    }
})(jQuery);