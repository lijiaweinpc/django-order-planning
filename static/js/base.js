
//页面IP加端口
var host = window.location.host;

RSC.Dialog.Div=function(option){// 成功
    var _option={
        //fromDiv: {
        //    "divMark": divMark
        //},
        width:0,
        height:0,
        active:[{ domTag: ".close", domEvent: "click", domDo: function (e) {
            e.data.close();
        } }]
    }
    if (option){
        _option = $.extend(_option, option);
    }
    var _dom = $(_option.fromDiv.divMark);
    
    var width = _option.width > 0 ? _option.width : _dom.width();
    var height = _option.height > 0 ? _option.height : _dom.height();
    _option = $.extend(_option, {width:width, height:height});
    return RSC.Dialog.CustomMessage.call(this,_option);
};

RSC.Dialog.Success=function(message,callback){// 成功
    $("#success .dialogContent .text,#success_bak .dialogContent .text").text(message);
    RSC.Dialog.Div({
        width:400,
        height:210,
        fromDiv: {
            "divMark": '#success'
        },
        time:1,
        closeCallback:callback,
        active:[
            { domTag: ".close", domEvent: "click", domDo: function (e) {
                e.data.close();
            }}
        ]
    });
};
RSC.Dialog.Error=function(message,height){// 错误
    $("#error .dialogContent .text,#error_bak .dialogContent .text").text(message);
    RSC.Dialog.Div({
        width:400,
        height:height || 210,
        fromDiv: {
            "divMark": '#error'
        },
        time:1,
        active:[
            { domTag: ".close", domEvent: "click", domDo: function (e) {
                e.data.close();
            }}
        ]
    });
};
//RSC.Dialog.Error("失败");

function createTimeLine(project){
    //初始加载数据列表
    $.ajax({
        url:"http://"+host+"/lab2/labprogress/listbyProject",
        data:{project:project},
        type:"get",
        success: function(data){
            if(data && data.length > 0){
                var jsonData = JSON.parse(data);
                create(jsonData);
            }
            
        }
    })
    
    //创建数据
    function create(jsonData){
        for(var i=0;i<jsonData.length;i++){
            var obj = jsonData[i];
            var dom = $('<div class="cd-timeline-block" labProgressID='+obj.labProgressID+'><div class="cd-timeline-img cd-picture"><img src="img/cd-icon-picture.svg" alt="Picture"></div><div class="cd-timeline-content"><div class="editCon"><h2>'+(obj.labProgressTitle || "")+'</h2><p>'+(obj.labProgressProgress || "")+'</p></div><div class="cd-read-more delete btn btn-primary" target="_blank">删除</div><div class="cd-read-more edit btn btn-primary" target="_blank">修改</div><span class="cd-date">'+obj.labProgressTime+'</span></div></div>');
            $("#cd-timeline").append(dom);
        }
    }
    //create();
    //修改
    $("#cd-timeline").delegate(".cd-read-more.edit","click",function(){
        var self = $(this);
        var parentObj = self.parents(".cd-timeline-block");
        var content = parentObj.find(".tareaContent").val();
        var time = parentObj.find(".cd-dateInput").val();
        var id = parentObj.attr("labprogressId");
        if(content == ""){
            alert("内容不能为空！");
            return;
        }
        if(time == ""){
            alert("时间不能为空！");
            return;
        }
        var items={
            project:project,
            title:parentObj.find(".title").val(),
            content:content,
            time:parentObj.find(".cd-dateInput").val()
        }
        //新增数据
        if(self.hasClass("new")){
            $.ajax({
                url:"http://"+host+"/lab2/labprogress/add",
                type:"get",
                data:{obj:JSON.stringify(items)},
                success: function(data){
                    data = JSON.parse(data);
                    if(data.ok){
                        var dataId = data.data;
                        RSC.Dialog.Success("新增数据成功！",function(){
                            var pDom = self.prevAll(".editCon");
                            var title = $("<h2>"+pDom.find(".title").val()+"</h2>");
                            var content = $("<p>"+pDom.find(".tareaContent").val()+"</p>");
                            var dateDom = $("<span class='cd-date'>"+self.parents(".cd-timeline-content").find(".cd-date").val()+"</span>");
                            pDom.empty();
                            pDom.append(title);
                            pDom.append(content);
                            self.parents(".cd-timeline-content").find(".cd-date").remove();
                            self.parents(".cd-timeline-content").append(dateDom);
                            self.text("修改");
                            self.parents(".cd-timeline-content").find(".new").removeClass("new");
                            parentObj.attr("labprogressId",dataId);
                        })
                    }else{
                        RSC.Dialog.Error(data.msg);
                    }
                }
            })
        }else{
            //修改数据
            var state = $(this).attr("state");
            if(state == "edit"){
                items.id = id;
                //修改数据接口
                $.ajax({
                    url:"http://"+host+"/lab2/labprogress/update",
                    type:"get",
                    data:{obj:JSON.stringify(items)},
                    success: function(data){
                        data = JSON.parse(data);
                        if(data.ok){
                            RSC.Dialog.Success("修改成功！",function(){
                                var pDom = self.prevAll(".editCon");
                                var title = $("<h2>"+pDom.find(".title").val()+"</h2>");
                                var content = $("<p>"+pDom.find(".tareaContent").val()+"</p>");
                                var dateDom = $("<span class='cd-date'>"+self.parents(".cd-timeline-content").find(".cd-date").val()+"</span>");
                                pDom.empty();
                                pDom.append(title);
                                pDom.append(content);
                                self.parents(".cd-timeline-content").find(".cd-date").remove();
                                self.parents(".cd-timeline-content").append(dateDom);
                                self.text("修改");
                                self.removeAttr("state");
                            });
                        }else{
                            RSC.Dialog.Error(data.msg);
                        }
                    }
                })
            }else{
                var pDom = $(this).prevAll(".editCon");
                var height = pDom.find("p").height();
                var title = $("<input class='title input' value='"+pDom.find("h2").text()+"' />");
                var content = $("<textarea class='tareaContent textarea'>"+pDom.find("p").text()+"</textarea>");
                var dateDom = $("<input class='cd-dateInput cd-date input' readonly='readonly' value='"+$(this).parents(".cd-timeline-content").find(".cd-date").text()+"' />");
                pDom.empty();
                content.height(height+15);
                pDom.append(title);
                pDom.append(content);
                $(this).parents(".cd-timeline-content").find(".cd-date").remove();
                $(this).parents(".cd-timeline-content").append(dateDom);
                $(this).text("保存");
                $(this).attr("state","edit");
                bindDate(dateDom);
            }
        }
    });
    
    //删除
    $("#cd-timeline").delegate(".cd-read-more.delete","click",function(){
        var self = $(this);
        var id = self.parents(".cd-timeline-block").attr("labprogressId");
        deletePop(function(){
            $.ajax({
                url:"http://"+host+"/lab2/labprogress/delete",
                data:{id:id},
                type:"post",
                success: function(data){
                    data = JSON.parse(data);
                    if(data.ok){
                        self.parents(".cd-timeline-block").fadeOut("slow",function(){
                            var that = $(this);
                            RSC.Dialog.Success("删除成功！",function(){
                                that.remove();
                            });
                            
                        });
                    }else{
                        RSC.Dialog.Error(data.msg);
                    }
                }
            })
        });
    });
    
    //新增
    $("#tab1 .add").click(function(){
        var dom = $('<div class="cd-timeline-block"><div class="cd-timeline-img cd-picture"><img src="img/cd-icon-picture.svg" alt="Picture"></div><div class="cd-timeline-content"><div class="editCon"><input class="title input" value="" placeholder="请输入标题"/><textarea class="tareaContent textarea" placeholder="请输入内容"></textarea></div><div class="cd-read-more delete btn btn-primary new" target="_blank">删除</div><div class="cd-read-more edit btn btn-primary new" target="_blank">保存</div><input class="cd-dateInput cd-date input" readonly="readonly" value="" /></div></div>');
        $("#cd-timeline").prepend(dom);
        bindDate(dom.find(".cd-dateInput"));
        
    });
    
    function bindDate(dom){
        // 日期限制
        var meetStart = dom;
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth()+1;
        var d = date.getDate();
        var hour = date.getHours();
        var m = date.getMinutes();
        var time = year+"-"+month+"-"+d;
        var date1 = meetStart.DatePicker({
            dateFmt:'yyyy-MM-dd',
            isTime:false,
            startDate:meetStart.val(),
            //minDate:time+" "+hour+":"+m,
            OKCallBack: function(self){
            },
            toDayCallBack: function(self){
            },
            clearCallBack: function(){
                
            }
        });
    }
    
    //删除确认弹窗
    function deletePop(fun){
        RSC.Dialog.Div({
            fromDiv:{
                divMark:"#confirm"
            },
            height:324,
            active:[
                { domTag: "#confirm .okBtn", domEvent: "click", domDo: function (e) {
                    if($.isFunction(fun)){
                        fun();
                    }
                    e.data.close();
                }},
                { domTag: "#confirm .close", domEvent: "click", domDo: function (e) {
                    e.data.close();
                }}]
        });
    }
}

//tab项点击做定位操作
$("#myTab").delegate("li","click",function(){
    var self = $(this);
    window.setTimeout(function(){
        var top = self.offset().top-85;
        $(window).scrollTop(top);
    },500);
})