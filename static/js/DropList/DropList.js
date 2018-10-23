// JavaScript Document
/*
*zengfengjiao 2018-06-21
*名称：下拉列表
*功能：
*
*/
(function($){
    $.fn.DropList = function(options){
        var self = $(this);
        var domObj = {
            settings: {
                data:null,          //数据源
                width:"auto",
                height:"auto",
                defaultCheck:false,  //多选框默认是否选中
                maxWidth:300,
                maxHeight:400,
                isCheck:true,        //是否多选
                isGetVal:true,       //是否把选中的值赋值到文本框中
                isSelectClass:false   //是否添加鼠标悬浮样式和选中样式
            },
            selfDom: $(this),
            _initDom: function(){
                if(self && self.length > 0){
                    this.container = $('<div class="dropListContainer"><ul class="dropListUl"></ul></div>');
                    self.after(this.container);
                    var left = self.position().left;
                    this.container.css({"left":left,"maxWidth":this.settings.maxWidth,"maxHeight":this.settings.maxHeight,"width":this.settings.width,"height":this.settings.height});
                    if(this.settings.isSelectClass){
                        this.container.addClass("selectClass");
                    }
                    this._createItem(this.settings.data,this.container.find("ul"),0,true);
                    this._event();
                }
            },//创建下拉数据
            _createItem: function(data,dom,_level,first){
                _level++;
                if(data && data.length > 0){
                    for(var i=0;i<data.length;i++){
                        if(first){
                            this._level = 0;
                        }
                        
                        var li = $('<li></li>').appendTo(dom);
                        var checkDom = '';
                        if(this.settings.isCheck){
                            var checkbox = this.settings.defaultCheck ? "checkbox_true" : "checkbox_false";
                            checkDom = '<span class="chk '+checkbox+'"></span>';
                        }
                        if(data[i].childs && data[i].childs.length > 0){
                            li.addClass("parent");
                            $('<span class="treeDom"><span class="switch roots_close"></span>'+checkDom+'<span class="text" title='+data[i].value+'>'+data[i].title+'</span></span>').appendTo(li);
                            var ul = $("<ul class='child child"+_level+"'></ul>").appendTo(li);
                            this._createItem(data[i].childs,ul,_level);
                        }else{
                            li.addClass("noChild");
                            $(checkDom+'<span class="text" title='+data[i].value+'>'+data[i].title+'</span>').appendTo(li);
                        }
                        if(data[i].state == "all"){
                            li.attr("state","all");
                        }
                    }
                }
            },
            //事件绑定
            _event: function(){
                var that = this;
                //显示下拉列表
                self.bind("click",function(){
                    var self = $(this);
                    var dCon = self.next(".dropListContainer");
                    if(dCon.hasClass("open")){
                        dCon.hide();
                        dCon.removeClass("open");
                    }else{
                        $(".dropListContainer").hide().removeClass("open");
                        dCon.show();
                        dCon.addClass("open");
                    }
                })
                //下拉列表点击展开子级项
                this.container.delegate(".switch,.text","click",function(){
                    var treeDom = $(this).parents(".treeDom");
                    var state = treeDom.attr("state");
                    //合起子项
                    if(state == "open"){
                        treeDom.find(".switch").removeClass("roots_open").addClass("roots_close");
                        treeDom.attr("state","close");
                        treeDom.next(".child").fadeOut();
                    }else{
                        treeDom.find(".switch").addClass("roots_open").removeClass("roots_close");
                        treeDom.attr("state","open");
                        treeDom.next(".child").fadeIn();
                    }
                })
                //下拉列表多选框事件
                this.container.find(".chk,.text").unbind("click").bind("click",function(){
                    var objDom = $(this);
                    if($(this).parent(".treeDom").length>0 && $(this).hasClass("text")){
                        return;
                    }
                    if($(this).parent(".noChild").length>0 && $(this).hasClass("text")){
                        objDom = $(this).prev(".chk");
                    }
                    //取消选中
                    if(objDom.hasClass("checkbox_true")){
                        if($(this).parent("li").attr("state") == "all"){
                            that.container.find(".chk").removeClass("checkbox_true").addClass("checkbox_false");
                        }else{
                            objDom.removeClass("checkbox_true").addClass("checkbox_false");
                            //如果操作的是父级
                            if(objDom.parents(".treeDom").parent(".parent").length > 0){
                                objDom.parents(".treeDom").parent(".parent").find(".child .chk").removeClass("checkbox_true").addClass("checkbox_false");
                            }
                            $(this).parents("li").parents(".parent").each(function(){
                                if($(this).find(".child").find(".checkbox_true").length < $(this).find(".child").find(".chk").length){
                                    $(this).children(".treeDom").children(".chk").removeClass("checkbox_true").addClass("checkbox_false");
                                }
                            })
                        }
                    }else{//选中
                        if($(this).parent("li").attr("state") == "all"){
                            that.container.find(".chk").addClass("checkbox_true").removeClass("checkbox_false");
                        }else{
                            objDom.addClass("checkbox_true").removeClass("checkbox_false");
                            //如果操作的是父级
                            if(objDom.parents(".treeDom").parent(".parent").length > 0){
                                objDom.parents(".treeDom").parent(".parent").find(".child .chk").addClass("checkbox_true").removeClass("checkbox_false");
                            }
                            $(this).parents("li").parents(".parent").each(function(){
                                if($(this).find(".child").find(".checkbox_true").length == $(this).find(".child").find(".chk").length){
                                    $(this).children(".treeDom").children(".chk").addClass("checkbox_true").removeClass("checkbox_false");
                                }
                            })
                        }
                    }
                    
                    if(that.settings.isGetVal){
                        var value = "";
                        var titleValue = "";

                        var count = 0;
                        var cLength = that.container.find("li[state!='all']").find(".chk.checkbox_true").length;
                        //记录选中数据
                        that.container.find("li[state!='all']").each(function(){
                            if($(this).find(".chk").hasClass("checkbox_true")){
                                $(this).addClass("active");
                                if(cLength == $(this).parents(".dropListUl").find("li").length-1){
                                    $(this).parents(".dropListUl").find("li[state='all']").addClass("active");
                                    $(this).parents(".dropListUl").find("li[state='all']").find(".chk").addClass("checkbox_true").removeClass("checkbox_false");
                                }
                                else if(cLength < $(this).parents(".dropListUl").find("li").length-1){
                                    $(this).parents(".dropListUl").find("li[state='all']").removeClass("active");
                                    $(this).parents(".dropListUl").find("li[state='all']").find(".chk").removeClass("checkbox_true").addClass("checkbox_false");
                                }
                                
                                if(count> 0 && count <=2){
                                    value += ",";
                                }
                                value += $(this).find(".text").text();
                                count ++;
                            }else{
                                $(this).removeClass("active");
                            }
                            
                        });
                        titleValue = value;
                        if(count > 3){
                            value = count+" selected";
                        }
                        if(count == 0){
                            value = "None selected";
                        }
                        console.log(value);
                        self.val(value).attr("titleValue",titleValue);
                    }
                })
                
                //下拉列表项点击事件
                this.container.find("ul").delegate("input","click",function(){
                    var value = "";
                    var titleValue = "";

                    var count = 0;
                    
                    //选中取消所有
                    if($(this).is(":checked") && $(this).parents(".dItem").attr("state") == "all"){
                        $(this).parents(".dropListUl").find("input").prop("checked","checked");
                        $(this).parents(".dropListUl").find("li").addClass("active");
                    }
                    else if(!$(this).is(":checked") && $(this).parents(".dItem").attr("state") == "all"){
                        $(this).parents(".dropListUl").find("input").prop("checked",false);
                        $(this).parents(".dropListUl").find("li").removeClass("active");
                    }
                    var cLength = $(this).parents(".dropListUl").find("li[state!='all']").find("input:checked").length;
                    
                    //记录选中数据
                    $(this).parents(".dropListUl").find("li[state!='all']").each(function(){
                        if($(this).find("input").is(":checked")){
                            $(this).addClass("active");
                            if(cLength == $(this).parents(".dropListUl").find("li").length-1){
                                $(this).parents(".dropListUl").find("li[state='all']").find("input").prop("checked",true);
                                $(this).parents(".dropListUl").find("li[state='all']").addClass("active");
                            }
                            else if(cLength < $(this).parents(".dropListUl").find("li").length-1){
                                $(this).parents(".dropListUl").find("li[state='all']").find("input").prop("checked",false);
                                $(this).parents(".dropListUl").find("li[state='all']").removeClass("active");
                            }
                            
                            if(count> 0 && count <=2){
                                value += ",";
                            }
                            value += $(this).find("label").text();
                            count ++;
                        }else{
                            $(this).removeClass("active");
                        }
                        
                    });
                    titleValue = value;
                    if(count > 3){
                        value = count+" selected";
                    }
                    if(count == 0){
                        value = "None selected";
                    }
                    $(this).parents(".dropListContainer").find(".dropListBtn").val(value).attr("titleValue",titleValue);
                })
                
                //点击空白区域隐藏下拉列表
                $("body").click(function(e){
                    if($(e.target).attr("class") == self.attr("class") || $(e.target).hasClass("dropListContainer") || $(e.target).parents(".dropListContainer").length > 0){return;}
                    that.container.hide();
                    that.container.removeClass("open");
                })
                
            },
            init: function(options){
                this.settings = $.extend(this.settings,options || {});
                this._initDom();
                return this;
            }
        }
        return domObj.init(options);
    }
})(jQuery)