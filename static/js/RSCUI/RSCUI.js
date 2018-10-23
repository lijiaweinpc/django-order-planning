
var RSC = {
    Dialog: {
        Success: function (message, time) {
            return this.CustomMessage({ "message": message, "time": time, showTitle: true, showButton: true, messageType: 1 });
        },
        Error: function (message, time) {
            return this.CustomMessage({ "message": message, "time": time, showTitle: true, showButton: true, messageType: 2 });
        },
        SysError:function (message, time) {
            return this.CustomMessage({ "message": message, "time": time, showTitle: false, showButton: true, messageType: 2 });
        },
        Warning: function (message, time) {
            return this.CustomMessage({ "message": message, "time": time, showTitle: true, showButton: true, messageType: 3 });
        },
        Infomation: function (message, time) {
            return this.CustomMessage({ "message": message, "time": time, showTitle: true, showButton: true, messageType: 4 });
        },
        AutoLink: function (message, linkUrl, time) {
            return this.CustomMessage({ "message": message, "time": time || 10, toUrl: linkUrl, showTitle: true, showButton: true, messageType: 5 });
        },
        Confirm: function (message) {
            return this.CustomMessage({ "message": message, showTitle: true, showButton: true, messageType: 6 });
        },
        Confirm: function (message, actionOk, actionCancel) {
            return this.CustomMessage({ "message": message, btnOkAction: actionOk, btnCancelAction: actionCancel, showTitle: true, showButton: true, messageType: 6 });
        },
        CustomMessage: function (option) {
            return this.domFactory.message(option);
        },
        MessageFromDiv: function (divMark, textMark, message, width, height, time, showButton, showTitle, titleText, showCallback) {
            var _param = { fromDiv: { "divMark": divMark, "textMark": textMark } };
            width != undefined && width != null ? _param.width = width : null;
            height != undefined && height != null ? _param.height = height : null;
            message != undefined && message != null ? _param.message = message : null;
            time != undefined && time != null ? _param.time = time : null;
            showButton != undefined && showButton != null ? _param.showButton = showButton : null;
            showTitle != undefined && showTitle != null ? _param.showTitle = showTitle : null;
            titleText != undefined && titleText != null ? _param.title = titleText : null;
            showCallback != undefined && showCallback != null && typeof (showCallback) == "function" ? _param.showCallback = showCallback : null;
            return this.CustomMessage(_param);
        },
        PopDiv: function (divMark, width, height, showCallback) {
            return this.MessageFromDiv(divMark, null, null, width, height, null, false, false, null, showCallback);
        },
        MessageFromPage: function (pageUrl, passData, domMark, textMark, message, width, height, time, showButton, showTitle, titleText, showCallback) {
            var _param = { fromPage: { "pageUrl": pageUrl, "domMark": domMark, "textMark": textMark, "passData": passData } };
            width != undefined && width != null ? _param.width = width : null;
            height != undefined && height != null ? _param.height = height : null;
            message != undefined && message != null ? _param.message = message : null;
            time != undefined && time != null ? _param.time = time : null;
            showButton != undefined && showButton != null ? _param.showButton = showButton : null;
            showTitle != undefined && showTitle != null ? _param.showTitle = showTitle : null;
            titleText != undefined && titleText != null ? _param.title = titleText : null;
            showCallback != undefined && showCallback != null && typeof (showCallback) == "function" ? _param.showCallback = showCallback : null;
            return this.CustomMessage(_param);
        },
        PopPage: function (pageUrl, domMark, width, height, showCallback) {
            return this.MessageFromPage(pageUrl, {}, domMark, null, null, width, height, null, false, false, null, showCallback);
        },
        MessageFromNet: function (netUrl, width, height, time, showButton, showTitle, titleText, showCallback) {
            var _param = { fromUrl: { "netUrl": netUrl } };
            width != undefined && width != null ? _param.width = width : null;
            height != undefined && height != null ? _param.height = height : null;
            time != undefined && time != null ? _param.time = time : null;
            showButton != undefined && showButton != null ? _param.showButton = showButton : null;
            showTitle != undefined && showTitle != null ? _param.showTitle = showTitle : null;
            titleText != undefined && titleText != null ? _param.title = titleText : null;
            showCallback != undefined && showCallback != null && typeof (showCallback) == "function" ? _param.showCallback = showCallback : null;
            return this.CustomMessage(_param);
        },
        PopNet: function (netUrl, width, height, showCallback) {
            return this.MessageFromNet(netUrl, width, height, null, false, false, null, showCallback);
        },
        domFactory: {
            setting: {
                fromDiv: {
                    divMark: null,
                    textMark: null
                },
                fromPage: {
                    pageUrl: null,
                    domMark: null,
                    textMark: null,
                    passData: null
                },//构造标签内对象事件绑定列表
                fromUrl: { netUrl: null },
                toUrl:null,//自动跳转到指定地址
                title: "系统提示",
                message: "网络异常,请稍后再试",
                messageType: 0, // 1 Success, 2 Error, 3 Warning, 4 Infomation, 5 AutoLink, 6 Confirm
                time: -1,
                timeDisp:null,
                width: 560,
                height: 250,
                beforeCss: { "content": "", "position": "fixed", left: 0, top: 0, width: "100%", height: "100%", "background": "rgba(0,0,0,.65)", "z-index": 99999 },
                afterCss: { "content": "", "position": "absolute", left: 0, top: 0, width: "100%", height: "100%", "border-radius": "10px", "background": "#1a3c4b", "z-index": 99999 },

                dialogCss: { "position": "fixed", left: "50%", top: "50%", "text-align": "center", "z-index": 99999},
                dialogClass: "",

                showTitle: false,
                titleCss: { height: 40, width: "100%", "position": "relative", "text-indent": "25px", "line-height": "40px", "font-size": 20, "font-weight": "bold", "text-align": "left","background":"#000"},
                titleClass: "",
                contentCss: {},
                contentClass: "",
                showButton: false,
                btnBarCss: { height: 70, "line-height": "60px", width: "100%", "text-align": "center","z-index":99999,"position": "relative" },
                btnBarClass: "",
                okBtnCss: { /*"border": "none", "background": "#9f6e25",*/ "height": 40, "width": 135, "color": "white", "font-size": "20px", /*"-moz-border-radius": 4, "-webkit-border-radius": 4, "border-radius": 4, "margin": "0px 20px", "cursor": "pointer"*/ },
                okBtnClass: "",
                okBtnAction: null,
                cancelBtnCss: { "border": "none", "background": "#ff8400", "height": 35, "color": "white", "font-size": "20px", "-moz-border-radius": 4, "-webkit-border-radius": 4, "border-radius": 4, "margin": "0px 20px", "cursor": "pointer" },
                cancelBtnClass: "",
                cancelBtnAction: null,
                closeBtnCss: { "position": "absolute", "display": "block", right: 0, top: 0, width: 38, height: 38, "line-height": "38px", "background-color": "#000", "text-indent": "0px", "text-align": "center", "font-size": 32, "font-weight": "100", "color": "white", "cursor": "pointer", "-moz-border-radius": 4, "-webkit-border-radius": 4 },
                closeBtnClass: "",
                closeBtnAction: null,
                customButtons: [],
                active: [{ domTag: "", domEvent: "click", domDo: function () { } }],  //构造标签内对象事件绑定列表
                beforeCallback:null,//弹出前回调方法
                showCallback: null,//弹出后回调方法
                loadShowCallback:null,//加载完成页面后回调方法
                closeCallback:null//关闭后回调方法
            },
            construct: function (option) {
                var _dom = { pageDom: { dialogBox: null, dialogTitleBar: null, dialogContent: null, dialogButtonBar: null }, setting: option };
                var _h = _dom.setting.height;
                var _w = _dom.setting.width;
                var _css = $.extend(_dom.setting.dialogCss, { 'width': _dom.setting.width, height: _dom.setting.height });
                _dom.pageDom.dialogBox = $("<div class='dialogBox'></div>").css(_css).appendTo($("body")).hide().addClass(_dom.setting.dialogClass);
                if (_dom.setting.showTitle) {
                    _dom.pageDom.dialogTitleBar = $("<div class='dialogTitleBar'></div>").css(_dom.setting.titleCss).css({ "z-index": 99999 }).appendTo(_dom.pageDom.dialogBox).addClass(_dom.setting.titleClass);
                    _h -= _dom.pageDom.dialogTitleBar.height();
                    $("<div class='dialogClose'>×</div>").appendTo(_dom.pageDom.dialogTitleBar).css(_dom.setting.closeBtnCss).addClass(_dom.setting.closeBtnClass).click(function () {
                        if (_dom.setting.closeBtnAction && typeof (_dom.setting.closeBtnAction) == "function") { _dom.setting.closeBtnAction(_dom); }
                        _dom.close();
                    });
                    _dom.pageDom.dialogTitleBar.append(_dom.setting.title);
                }
                if (_dom.setting.showButton) {
                    //_dom.pageDom.dialogBox.css({"background-color": "#EEE"});
                    _dom.pageDom.dialogButtonBar = $("<div class='dialogButtonBar'></div>").css(_dom.setting.btnBarCss).appendTo(_dom.pageDom.dialogBox).addClass(_dom.setting.btnBarClass).css({"background-color":"#EEE","border-bottom-left-radius":10,"border-bottom-right-radius":10,"margin-top":"-1px"});
                    _h -= _dom.pageDom.dialogButtonBar.height();
                }
                _dom.setting.contentCss = $.extend(_dom.setting.contentCss, { height: _h, "z-index": 100000, "position": "relative","overflow-x":"hidden","overflow-y":"auto"});

                if (_dom.pageDom.dialogButtonBar) {
                    _dom.pageDom.dialogContent = $("<div class='dialogContent'></div>").insertBefore(_dom.pageDom.dialogButtonBar).css(_dom.setting.contentCss).addClass(_dom.setting.contentClass).css({"background-color":"#EEE","border-top-left-radius":10,"border-top-right-radius":10});
                } else {
                    _dom.pageDom.dialogContent = $("<div class='dialogContent'></div>").appendTo(_dom.pageDom.dialogBox).css(_dom.setting.contentCss).addClass(_dom.setting.contentClass);
                }
                if (_dom.setting.messageType) {
                    this.defaultContent(_dom, _dom.setting.message, _dom.setting.messageType, _h);
                } else if (_dom.setting.fromDiv.divMark) {
                    var _tmpDiv = $(_dom.setting.fromDiv.divMark);
                    if (_tmpDiv.length == 1) {
                        var _parent = _tmpDiv.parent();
                        _tmpDiv.clone(true).appendTo(_dom.pageDom.dialogContent).each(function () {
                            $(this).show();
                            if (typeof (_dom.setting.fromDiv.divMark) == "string" && _dom.setting.fromDiv.divMark.indexOf("#") == 0) {
                                _tmpDiv.hide().attr("id", _tmpDiv.attr("id") + "_bak");
                            } else if (typeof (_dom.setting.fromDiv.divMark) == "string" && _dom.setting.fromDiv.divMark.indexOf(".") == 0) {
                                _tmpDiv.hide().addClass(_dom.setting.fromDiv.divMark + "_bak").removeClass(_dom.setting.fromDiv.divMark);
                            }
                            _dom.setting.fromDiv.textMark ? $(this).find(_dom.setting.fromDiv.textMark).html(_dom.setting.message) : null;
                            if(_dom.setting.active && _dom.setting.active.length>0 ){
                                for (var i= 0; i < _dom.setting.active.length; i++) {
                                    var _tmpObj = _dom.setting.active[i];
                                    if (_tmpObj.domTag && _tmpObj.domTag != "") {
                                        $(_dom.pageDom.dialogBox).find(_tmpObj.domTag).on(_tmpObj.domEvent,_dom, _tmpObj.domDo);
                                    }
                                }
                            }
                        });
                    } else if (_tmpDiv.length <= 0) {
                        _tmpDiv = $(_dom.setting.fromDiv.divMark + "_bak");
                        if (_tmpDiv.length <= 0) { alert("没有找到可配置的显示对象!"); return null; }
                        _tmpDiv.clone(true).appendTo(_dom.pageDom.dialogContent).each(function () {
                            if (_dom.setting.fromDiv.divMark.indexOf("#") == 0) {
                                $(this).show().attr("id", _tmpDiv.attr("id").replace("_bak", ""));
                            } else if (_dom.setting.fromDiv.divMark.indexOf(".") == 0) {
                                $(this).show().addClass(_dom.setting.fromDiv.divMark).removeClass(_dom.setting.fromDiv.divMark + "_bak");
                            }
                            _dom.setting.fromDiv.textMark ? $(this).find(_dom.setting.fromDiv.textMark).html(_dom.setting.message) : null;
                            if(_dom.setting.active && _dom.setting.active.length>0 ){
                                for (var i= 0; i < _dom.setting.active.length; i++) {
                                    var _tmpObj = _dom.setting.active[i];
                                    if (_tmpObj.domTag && _tmpObj.domTag != "") {
                                        $(_dom.pageDom.dialogBox).find(_tmpObj.domTag).on(_tmpObj.domEvent,_dom, _tmpObj.domDo);
                                    }
                                }
                            }
                        });
                    } else { alert("找到多个配置元素!"); return null; }
                } else if (_dom.setting.fromPage.pageUrl) {
                    $(_dom.pageDom.dialogContent).load(_dom.setting.fromPage.pageUrl + " " + (_dom.setting.fromPage.domMark || ""), _dom.setting.fromPage.passData, function () {
                        if (_dom.setting.fromPage.textMark) {
                            $(this).find(_dom.setting.fromPage.textMark).html(_dom.setting.message);
                        }
                        if (_dom.setting.loadShowCallback) {
                            _dom.setting.loadShowCallback(_dom);
                        }
                        if(_dom.setting.active && _dom.setting.active.length>0 ){
                            for (var i= 0; i < _dom.setting.active.length; i++) {
                                var _tmpObj = _dom.setting.active[i];
                                if (_tmpObj.domTag && _tmpObj.domTag != "") {
                                    $(_dom.pageDom.dialogBox).find(_tmpObj.domTag).on(_tmpObj.domEvent,_dom, _tmpObj.domDo);
                                }
                            }
                        }
                    });
                } else if (_dom.setting.fromUrl.netUrl) {
                    $("<iframe id='ifrm' class='ifrm' src='" + _dom.setting.fromUrl.netUrl + "' scrolling='no' width='100%' height='100%' frameborder='0' ></iframe>").appendTo(_dom.pageDom.dialogContent);
                    var _iframe = document.getElementById("ifrm");
                    if (_iframe.attachEvent) {
                        _iframe.attachEvent("onload", function () {
                            //alert("load");
                            //$("#ifrm").appendTo(self.dialogContent);
                        });
                    } else {
                        _iframe.onload = function () {
                            //alert("load");
                            //$("#ifrm").appendTo(self.dialogContent);
                        };
                    }
                } else {
                    alert("初始化参数不完整,无法完成创建任务!");
                    return null;
                }
                _dom.pageDom.dialogBox.css({ "display": "none", height: _dom.setting.height, "margin-left": _dom.pageDom.dialogBox.width() / 2 * -1, "margin-top": _dom.pageDom.dialogBox.height() / 2 * -1 });

                _dom.close = function (data) {
                    
                    if (_dom.setting.closeCallback) {
                        _dom.setting.closeCallback(_dom);
                    }
                    _dom.pageDom.dialogBox.fadeOut(300, function () {
                        //self.cover.hide();
                        if (_dom.setting.closeBtnAction && typeof (_dom.setting.closeBtnAction) == "function") { _dom.setting.closeBtnAction(data); } _dom.pageDom.dialogBox.remove();
                    });
                };
                $(window).resize(function () {
                    if (_dom.pageDom.dialogBox) {
                        _dom.pageDom.dialogBox.css({ "margin-left": _dom.pageDom.dialogBox.width() / 2 * -1, "margin-top": _dom.pageDom.dialogBox.height() / 2 * -1 });
                    }
                });
                _dom.pageDom.dialogBox.fadeIn(400, function () {
                    if (_dom.setting.showCallback) {
                        _dom.setting.showCallback(_dom);
                    }
                    if (_dom.setting.time >= 0) {
                        if(_dom.setting.timeDisp){ $(_dom.pageDom.dialogBox).find(_dom.setting.timeDisp).html(_dom.setting.time); }
                        var _ikey = _dom.setting.time;
                        var _timer = window.setInterval(function () {
                            _ikey--;
                            $(_dom.pageDom.dialogBox).find(".msgIco").html(_ikey);
                            if(_dom.setting.timeDisp){ $(_dom.pageDom.dialogBox).find(_dom.setting.timeDisp).html(_ikey); }
                            $(_dom.pageDom.dialogBox).find(".msgIco").html(_ikey);
                            if (_ikey <= 0) {
                                window.clearInterval(_timer);
                                _dom.pageDom.dialogBox.fadeOut(400, function () {
                                    //if (_dom.setting.messageType == 5) { window.location.href = _dom.setting.toUrl; }
                                    if (_dom.setting.toUrl) { window.location.href = _dom.setting.toUrl; }
                                    //_dom.pageDom.dialogBox.remove();
                                    _dom.close();
                                });
                            }
                        }, 1000);
                    }
                });
                return _dom;
            },
            defaultContent: function (objDom, message, type, height) {
                var _height = height;
                var _tmpBox = $("<div style=clear:both; display:block;'></div>").appendTo(objDom.pageDom.dialogContent).css({ "width": objDom.setting.width - 20, "height": _height, "margin": "0px auto" });
                //如果当前状态为系统错误
                if(type==2){
                    var _close = $('<span class="close sysClose"></span>').appendTo(_tmpBox);
                    _close.click(function(){
                        objDom.close(); 
                    });
                }
                var _tmpIco = $("<div class='msgIco'></div>").css({ "-moz-border-radius": "50%", "-webkit-border-radius": "50%", "border-radius": "50%", "display": "block", width: 70, height: 70, "line-height": "70px", "text-align": "center", "font-size": 40, "position":"relative","left":"50%","margin-left":"-35px","top":40 }).appendTo(_tmpBox);
                var _width = objDom.setting.width - 80 - 25 * 2 - 2 * 10;
                var _tmpText = $("<div></div>").css({"word-break": "break-all", "word-wrap": "break-word", "font-size": 30,"margin-top":60,"color":"#171717"}).appendTo(_tmpBox)
                    .append($("<div class='msgText'>" + message + "</div>").css({ }));
                // 0 Success, 1 Error, 2 Warning, 3 Infomation, 4 AutoLink, 5 Confirm
                if (type == 1) { // success
                    _tmpIco.css({ "background-color": "green", "color": "white" }).html("✓");
                } else if (type == 2) { // error
                    _tmpIco.css({ "background-color": "red", "color": "white" }).html("!");
                } else if (type == 3) { // warning
                    _tmpIco.css({ "background-color": "#ff9000", "color": "white" }).html("!");
                } else if (type == 4) { // infomation
                    _tmpIco.css({ "background-color": "#e500ff", "color": "white" }).html("❤");
                } else if (type == 5) { // autolink
                    _tmpIco.css({ "background-color": "#00ffff", "color": "white" }).html(objDom.setting.time);
                } else if (type == 6) { // confirm
                    _tmpIco.css({ "background-color": "#003cff", "color": "white" }).html("?");
                }
                
                if (type != 5 && objDom.setting.showButton) {
                    objDom.pageDom.dialogButtonBar.append($("<input type='button' class='btnOk btn' value='  确 定  ' />").css(objDom.setting.okBtnCss).addClass(objDom.setting.okBtnClass).click(function () {
                        if (objDom.setting.okBtnAction && typeof (objDom.setting.okBtnAction) == "function") { objDom.setting.okBtnAction(); }
                        objDom.close();
                        return true;
                    }));
                }
                if (objDom.setting.messageType == 6 && objDom.setting.showButton) {
                    objDom.pageDom.dialogButtonBar.append($("<input type='button' class='btnCancel' value='  取 消  ' />").css(objDom.setting.cancelBtnCss).addClass(objDom.setting.cancelBtnClass).click(function () {
                        if (objDom.setting.cancelBtnAction && typeof (objDom.setting.cancelBtnAction) == "function") { objDom.setting.cancelBtnAction(); }
                        objDom.close();
                        return false;
                    }));
                }
            },
            message: function (option) {
                var tmpSetting = {};
                tmpSetting = $.extend(tmpSetting, this.setting, option);
                return this.construct(tmpSetting);
            }
        }
    }
}
