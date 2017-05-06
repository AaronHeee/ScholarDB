/**
 * Created by aucson on 17-4-8.
 */


(function () {
     /// <summary>
     /// 引号转义符号
     /// </summary>
     String.EscapeChar = '\'';
     /// <summary>
     /// 替换所有字符串
     /// </summary>
     /// <param name="searchValue">检索值</param>
     /// <param name="replaceValue">替换值</param>
     String.prototype.replaceAll = function (searchValue, replaceValue) {
     var regExp = new RegExp(searchValue, "g");
     return this.replace(regExp, replaceValue);
     };
     /// <summary>
     /// 格式化字符串
     /// </summary>
     String.prototype.format = function () {
     var regexp = /\{(\d+)\}/g;
     var args = arguments;
     var result = this.replace(regexp, function (m, i, o, n) {
     return args[i];
     });
     return result.replaceAll('%', String.EscapeChar);
     }
})();

var choicenum = new Array(100);
for(i = 0;i<100;++i)
    choicenum[i]=1;
var inputtype = new Array(100);
for(i = 0;i<100;++i)
    inputtype[i]="text";

function get_mult_choice(id)
{
    var str = "";
    var o = document.getElementById(id);
    for(i=0;i<o.length;i++){
        if(o.options[i].selected){
            str+=o.options[i].value+",";
        }
    }
    return str;
}

function get_mult_choice_list(o)
{
    var l = [];
    for(var i = 0;i<o.childNodes.length;++i){
        if(o.childNodes[i].selected == true){
            l.push(o.childNodes[i].value);
        }
    }
    return l;
}

function add_qa(parent,qid){
    var qaele = document.getElementById("qa-ele");
    var ele = qaele.cloneNode(true);
    ele.id = qid;
    var ele_child = ele.childNodes;
    for(i = 0;i<ele_child.length;++i)
    {
        if(ele_child[i].id && ele_child[i].id!="")
            ele_child[i].id+=qid;
    }
    var title = ele.getElementsByTagName("h3")[0];
    title.innerHTML += qid;
    parent.appendChild(ele);
}

function add_radio(parent,qid){
    var qscele = document.getElementById("qsc-ele");
    var ele = qscele.cloneNode(true);
    var ele_child = ele.childNodes;
    ele.id = qid;
    for(i = 0;i<ele_child.length;++i)
    {
        if(ele_child[i].id && ele_child[i].id!="")
            ele_child[i].id+=qid;
    }
    var title = ele.getElementsByTagName("h3")[0];
    title.innerHTML += qid;
    parent.appendChild(ele);
}
function  add_choice(btn) {
    var par = btn.parentNode.parentNode;
    if(choicenum[par.id] >= 8)
        return false;
    else choicenum[par.id]++;
    par = par.getElementsByClassName("choice")[0];
    var ele = document.getElementById("choice").cloneNode(true);
    ele.id = "";
    par.appendChild(ele);
    return false;
}
function set_text_input(btn){
    var par = btn.parentNode.parentNode.parentNode;
    inputtype[par.id] = "text";
}
function set_number_input(btn)
{
    var par = btn.parentNode.parentNode.parentNode;
    inputtype[par.id] = "number";
}
function add_list_survey_item(json,parid){
    var parele = document.getElementById(parid);
    var ele = document.getElementById("list-item").cloneNode(true);
    ele.getElementsByClassName("name title")[0].innerHTML = json.title;
    ele.getElementsByClassName("name title")[0].href = "/project/view_questions/?sno=" + String(json.no);
    ele.getElementsByClassName("time")[0].innerHTML = json.opentime;
    ele.getElementsByClassName("help-block description")[0].innerHTML = json.description;
    ele.getElementsByClassName("payment")[0].innerHTML = json.payment;
    var restrict_par = ele.getElementsByClassName("align-right restrict")[0];
    if(json.gender_restrict!="无限制"){
        add_label(restrict_par,json.gender_restrict,"warning");
    }
    if(json.survey_restrict!="任何人"){
        add_label(restrict_par,json.survey_restrict,"warning");
    }
    if(json.min_age != 0){
        add_label(restrict_par,"至少"+String(json.min_age)+"岁","warning");
    }
    if(json.max_age!=200){
        add_label(restrict_par,"至多"+String(json.max_age)+"岁","warning");
    }
    var subject_par = ele.getElementsByClassName("text")[0];
    if(json.subject1 != ""){
        add_label(subject_par,json.subject1,"success")
    }
    if(json.subject2 != ""){
        add_label(subject_par,json.subject2,"success")
    }
    if(json.subject3 != ""){
        add_label(subject_par,json.subject3,"success")
    }
    parele.appendChild(ele);
    return ele;
}

function add_list_task_item(json,parid){
    var parele = document.getElementById(parid);
    var ele = document.getElementById("list-item").cloneNode(true);
    ele.getElementsByClassName("name title")[0].innerHTML = json.title;
    ele.getElementsByClassName("name title")[0].href = "/project/view_files/?tno=" + String(json.no);
    ele.getElementsByClassName("time")[0].innerHTML = json.opentime;
    ele.getElementsByClassName("help-block description")[0].innerHTML = json.description;
    ele.getElementsByClassName("payment")[0].innerHTML = json.payment;
    var subject_par = ele.getElementsByClassName("text")[0];
    if(json.datatype != ""){
        add_label(subject_par,json.datatype,"info")
    }
    parele.appendChild(ele);
    return ele;
}

function add_scholar_list_task_item(json,parid){
    var num = json.num,now = json.now,slice = json.slice;

    var parele = document.getElementById(parid);
    var ele = document.getElementById("scholar-list-item").cloneNode(true);
    if(json.publicity == "PUBLIC")
        ele.getElementsByClassName("icon-eye-close")[0].className = "icon-eye-open";
    ele.getElementsByClassName("name title")[0].innerHTML = json.title;
    ele.getElementsByClassName("name title")[0].href = "/project/manage_task/?tno=" + String(json.no);
    ele.getElementsByClassName("time")[0].innerHTML = json.opentime;
    ele.getElementsByClassName("help-block description")[0].innerHTML = json.description;
    ele.getElementsByClassName("payment")[0].innerHTML = json.payment;
    var subject_par = ele.getElementsByClassName("text")[0];
    if(json.datatype != ""){
        add_label(subject_par,json.datatype,"info");
    }
    ele.getElementsByClassName("processing")[0].innerHTML ="切割为"+slice+"份  "+ "回收"+now+"/"+num+"份";
    parele.appendChild(ele);

}

function add_scholar_list_survey_item(json,parid){
    var parele = document.getElementById(parid);
    var ele = document.getElementById("scholar-list-item").cloneNode(true);
    if(json.publicity == "PUBLIC") ele.getElementsByClassName("icon-eye-close")[0].className = "icon-eye-open";
    ele.getElementsByClassName("name title")[0].innerHTML = json.title;
    ele.getElementsByClassName("name title")[0].href = "/project/manage_survey/?sno=" + String(json.no);
    ele.getElementsByClassName("name title")[0].class = "icon-eye-open";
    ele.getElementsByClassName("time")[0].innerHTML = json.opentime;
    ele.getElementsByClassName("help-block description")[0].innerHTML = json.description;
    ele.getElementsByClassName("payment")[0].innerHTML = json.payment;
    var restrict_par = ele.getElementsByClassName("align-right restrict")[0];
    if(json.gender_restrict!="无限制"){
        add_label(restrict_par,json.gender_restrict,"warning");
    }
    if(json.survey_restrict!="任何人"){
        add_label(restrict_par,json.survey_restrict,"warning");
    }
    if(json.min_age != 0){
        add_label(restrict_par,"至少"+String(json.min_age)+"岁","warning");
    }
    if(json.max_age!=200){
        add_label(restrict_par,"至多"+String(json.max_age)+"岁","warning");
    }
    var subject_par = ele.getElementsByClassName("text")[0];
    if(json.subject1 != ""){
        add_label(subject_par,json.subject1,"success")
    }
    if(json.subject2 != ""){
        add_label(subject_par,json.subject2,"success")
    }
    if(json.subject3 != ""){
        add_label(subject_par,json.subject3,"success")
    }
    parele.appendChild(ele);
}

function add_list_item(json,parid){
    if (json.type == "SURVEY") {
        return add_list_survey_item(json, parid);
    }
    else {
        return add_list_task_item(json, parid);
    }
}

function add_scholar_list_item(json,parid){
    if (json.type == "SURVEY") {
        add_scholar_list_survey_item(json, parid);
    }
    else {
        add_scholar_list_task_item(json, parid);
    }
}


function add_label(par_ele,what,type){
    par_ele.innerHTML += "<label class = %label label-{0}%>".format(type)+what+"</label>  ";
}


function clear_list_item(parid){
    var parele = document.getElementById(parid);
    parele.innerHTML = "";
}

function load_questions(json_all,qid,eleid) {
    var l = [];
    for(var i = 0;i<json_all.length;++i) {
        if(json_all[i].type == "qa"){
            load_qa(json_all[i],qid,eleid);
        }
        else if(json_all[i].type == "qsc"){
            load_qsc(json_all[i],qid,eleid);
        }
        qid++;
        l.push(json_all[i].qno);
    }
    return l;
}

function load_qa(json,qid,eleid){
    var par = document.getElementById(eleid);
    var ele = document.getElementById("qa-ans").cloneNode(true);
    ele.id = qid;
    ele.getElementsByClassName("qa-des")[0].innerHTML = json.title;
    ele.getElementsByClassName("panel-title")[0].innerHTML += String(qid);
    if(json.supplement_type == "img") {
        var imgele = document.createElement("img");
        imgele.src = json.supplement;
        ele.getElementsByClassName("qa-det")[0].appendChild(imgele)
    }
    else{
        ele.getElementsByClassName("qa-det")[0].innerHTML = json.supplement;
    }
    ele.getElementsByClassName("span12")[0].type = json.inputtype;
    par.appendChild(ele);
}

function load_qsc(json,qid,eleid) {
    var par = document.getElementById(eleid);
    var ele = document.getElementById("qsc-ans").cloneNode(true);
    ele.id = qid;
    ele.getElementsByClassName("panel-title")[0].innerHTML += String(qid);
    ele.getElementsByClassName("qsc-des")[0].innerHTML = json.title;
    if(json.supplement_type == "img") {
        var imgele = document.createElement("img");
        imgele.src = json.supplement;
        ele.getElementsByClassName("qsc-det")[0].appendChild(imgele)
    }
    else{
        ele.getElementsByClassName("qsc-det")[0].innerHTML = json.supplement;
    }
    var choice_ele = ele.getElementsByClassName("span12")[0];
    for(var i = 0;i<json.choice.length;++i){
        var new_choice = document.createElement("option");
        new_choice.value = json.choice[i];
        new_choice.innerHTML = json.choice[i];
        choice_ele.appendChild(new_choice);
    }
    if(json.input_type == "single"){
        ele.getElementsByClassName("help-block")[0].innerHTML = "这是单选题"
    }
    else if(json.input_type == "multiple") {
        ele.getElementsByClassName("help-block")[0].innerHTML = "这是多选题";
        ele.getElementsByClassName("span12 select")[0].multiple = "multiple";
    }
    par.appendChild(ele);
}

var is_first_item = true;
function answer_group_by_user(parid,sno,json_list,project_type) {
    var par = document.getElementById(parid);
    for(var i =0;i<json_list.length;++i) {
        var uno = json_list[i].uno;
        var ele = document.getElementById("accordion").cloneNode(true);
        ele.getElementsByClassName("accordion-body collapse");
        ele.getElementsByClassName("accordion-body collapse")[0].id = 'u'+ uno;
        ele.getElementsByClassName("accordion-toggle")[0].name =  ele.getElementsByClassName("accordion-body collapse")[0].id = 'u'+ uno;
        ele.getElementsByClassName("accordion-toggle")[0].innerHTML = "用户于" + new Date(json_list[i].submit_time).toLocaleString();
        var list_ele = ele.getElementsByClassName("list-group")[0];
        if(project_type == 'SURVEY') {
            list_ele.innerHTML += "<li><strong>回答内容</strong></li>";
            for (var q in json_list[i].qa) {
                list_ele.innerHTML += "<li>{0}:{1}</li>".format(q, json_list[i].qa[q]);
            }
            list_ele.innerHTML += "<br/>";
            list_ele.innerHTML += "<li><strong>其他信息</strong></li>";
            for (var p in json_list[i].privacy) {
                list_ele.innerHTML += "<li>{0}:{1}</li>".format(p, json_list[i].privacy[p]);
            }
            list_ele.innerHTML += "<li>回答耗时：" + json_list[i].time_consumed / 1000 + "秒</li>";
        }
        else if(project_type == 'TASK'){
            list_ele.innerHTML += "<li><strong>完成任务组号</strong></li>";
            list_ele.innerHTML += "<li>{0}</li>".format(json_list[i].fsno);
        }

        var inner_ele = ele.getElementsByClassName("accordion-inner")[0];
        if(is_first_item) {
            ele.getElementsByClassName("accordion-body collapse")[0].className = "accordion-body collapse in";
            is_first_item = false;
        }
        par.appendChild(ele);
    }
}

function slice_group_by_user(parid,json_list,tno,project_type) {
    var par = document.getElementById(parid);
    console.log(json_list[0].fsno)
    for(var i =0;i<json_list.length;++i) {
        var uno = json_list[i].uno;
        var ele = document.getElementById("accordion").cloneNode(true);
        ele.getElementsByClassName("accordion-body collapse");
        ele.getElementsByClassName("accordion-body collapse")[0].id = 'u'+ uno;
        ele.getElementsByClassName("accordion-toggle")[0].name =  ele.getElementsByClassName("accordion-body collapse")[0].id = 'u'+ uno;
        ele.getElementsByClassName("accordion-toggle")[0].innerHTML = "用户于" + new Date(json_list[i].submit_time).toLocaleString();
        var list_ele = ele.getElementsByClassName("list-group")[0];
        if(project_type == 'SURVEY') {
            list_ele.innerHTML += "<li><strong>回答内容</strong></li>";
            for (var q in json_list[i].qa) {
                list_ele.innerHTML += "<li>{0}:{1}</li>".format(q, json_list[i].qa[q]);
            }
            list_ele.innerHTML += "<br/>";
            list_ele.innerHTML += "<li><strong>其他信息</strong></li>";
            for (var p in json_list[i].privacy) {
                list_ele.innerHTML += "<li>{0}:{1}</li>".format(p, json_list[i].privacy[p]);
            }
            list_ele.innerHTML += "<li>回答耗时：" + json_list[i].time_consumed / 1000 + "秒</li>";
        }
        else if(project_type == 'TASK'){
            list_ele.innerHTML += "<li><strong>完成任务组号</strong></li>";
            list_ele.innerHTML += "<li> {0}</li>".format(json_list[i].fsno);
            var filename = "/home/aaron/Desktop/Files/uno_1001/tno_58/receiver/1004/example.mp3";
            list_ele.innerHTML += "<a style='margin-top: 20px' href=" + filename + " download='1004'>下载数据</a>";

        }

        var inner_ele = ele.getElementsByClassName("accordion-inner")[0];
        if(is_first_item) {
            ele.getElementsByClassName("accordion-body collapse")[0].className = "accordion-body collapse in";
            is_first_item = false;
        }
        par.appendChild(ele);
    }
}

/*echarts*/
function echarts_date_number(parid,sno,json_list){
    var myChart = echarts.init(document.getElementById(parid));
    var type = "问卷日回收量";
    var date = json_list.date;
    var number = json_list.number;
    var option = {
           title: {
               text: '每日问卷回收量'
           },
           tooltip: {},
           legend: {
               data:[type]
           },
           xAxis: {
               data: date
           },
           yAxis: {},
           dataZoom: [
               {
                   type: 'slider',
                   start: 10,
                   end: 60
               }
           ],
           series: [{
               name: '问卷数',
               type: 'bar',
               data: number,
               itemStyle:{
                   normal:{
                       color: '#098b72'
                   }
               }
           }]
       };
       myChart.setOption(option);
}

function echarts_gender(parid,sno,json_list){
    var myChart = echarts.init(document.getElementById(parid));
    var gender = new Array();
    var Female = new Object();
    Female.name = "女性";
    Female.value = json_list.Female;
    gender[0] = Female;
    var Male = new Object();
    Male.name = "男性";
    Male.value = json_list.Male;
    gender[1] = Male;
    var option = {
           title: {
               text: '回答者男女比例'
           },
           tooltip: {},
           radius: '10%',
           series: [{
               name: '男女比例',
               type: 'pie',
               data: gender,
           }]
       };
       myChart.setOption(option);
}

function echarts_location(parid,sno,json_list){
    var myChart = echarts.init(document.getElementById("location"));
    var data = new Array();
    for (var i=0; i<json_list.length;i++){
        data[i] = json_list[i];
    }

var geoCoordMap = {
    '海门':[121.15,31.89],
    '鄂尔多斯':[109.781327,39.608266],
    '招远':[120.38,37.35],
    '舟山':[122.207216,29.985295],
    '齐齐哈尔':[123.97,47.33],
    '盐城':[120.13,33.38],
    '赤峰':[118.87,42.28],
    '青岛':[120.33,36.07],
    '乳山':[121.52,36.89],
    '金昌':[102.188043,38.520089],
    '泉州':[118.58,24.93],
    '莱西':[120.53,36.86],
    '日照':[119.46,35.42],
    '胶南':[119.97,35.88],
    '南通':[121.05,32.08],
    '拉萨':[91.11,29.97],
    '云浮':[112.02,22.93],
    '梅州':[116.1,24.55],
    '文登':[122.05,37.2],
    '上海':[121.48,31.22],
    '攀枝花':[101.718637,26.582347],
    '威海':[122.1,37.5],
    '承德':[117.93,40.97],
    '厦门':[118.1,24.46],
    '汕尾':[115.375279,22.786211],
    '潮州':[116.63,23.68],
    '丹东':[124.37,40.13],
    '太仓':[121.1,31.45],
    '曲靖':[103.79,25.51],
    '烟台':[121.39,37.52],
    '福州':[119.3,26.08],
    '瓦房店':[121.979603,39.627114],
    '即墨':[120.45,36.38],
    '抚顺':[123.97,41.97],
    '玉溪':[102.52,24.35],
    '张家口':[114.87,40.82],
    '阳泉':[113.57,37.85],
    '莱州':[119.942327,37.177017],
    '湖州':[120.1,30.86],
    '汕头':[116.69,23.39],
    '昆山':[120.95,31.39],
    '宁波':[121.56,29.86],
    '湛江':[110.359377,21.270708],
    '揭阳':[116.35,23.55],
    '荣成':[122.41,37.16],
    '连云港':[119.16,34.59],
    '葫芦岛':[120.836932,40.711052],
    '常熟':[120.74,31.64],
    '东莞':[113.75,23.04],
    '河源':[114.68,23.73],
    '淮安':[119.15,33.5],
    '泰州':[119.9,32.49],
    '南宁':[108.33,22.84],
    '营口':[122.18,40.65],
    '惠州':[114.4,23.09],
    '江阴':[120.26,31.91],
    '蓬莱':[120.75,37.8],
    '韶关':[113.62,24.84],
    '嘉峪关':[98.289152,39.77313],
    '广州':[113.23,23.16],
    '延安':[109.47,36.6],
    '太原':[112.53,37.87],
    '清远':[113.01,23.7],
    '中山':[113.38,22.52],
    '昆明':[102.73,25.04],
    '寿光':[118.73,36.86],
    '盘锦':[122.070714,41.119997],
    '长治':[113.08,36.18],
    '深圳':[114.07,22.62],
    '珠海':[113.52,22.3],
    '宿迁':[118.3,33.96],
    '咸阳':[108.72,34.36],
    '铜川':[109.11,35.09],
    '平度':[119.97,36.77],
    '佛山':[113.11,23.05],
    '海口':[110.35,20.02],
    '江门':[113.06,22.61],
    '章丘':[117.53,36.72],
    '肇庆':[112.44,23.05],
    '大连':[121.62,38.92],
    '临汾':[111.5,36.08],
    '吴江':[120.63,31.16],
    '石嘴山':[106.39,39.04],
    '沈阳':[123.38,41.8],
    '苏州':[120.62,31.32],
    '茂名':[110.88,21.68],
    '嘉兴':[120.76,30.77],
    '长春':[125.35,43.88],
    '胶州':[120.03336,36.264622],
    '银川':[106.27,38.47],
    '张家港':[120.555821,31.875428],
    '三门峡':[111.19,34.76],
    '锦州':[121.15,41.13],
    '南昌':[115.89,28.68],
    '柳州':[109.4,24.33],
    '三亚':[109.511909,18.252847],
    '自贡':[104.778442,29.33903],
    '吉林':[126.57,43.87],
    '阳江':[111.95,21.85],
    '泸州':[105.39,28.91],
    '西宁':[101.74,36.56],
    '宜宾':[104.56,29.77],
    '呼和浩特':[111.65,40.82],
    '成都':[104.06,30.67],
    '大同':[113.3,40.12],
    '镇江':[119.44,32.2],
    '桂林':[110.28,25.29],
    '张家界':[110.479191,29.117096],
    '宜兴':[119.82,31.36],
    '北海':[109.12,21.49],
    '西安':[108.95,34.27],
    '金坛':[119.56,31.74],
    '东营':[118.49,37.46],
    '牡丹江':[129.58,44.6],
    '遵义':[106.9,27.7],
    '绍兴':[120.58,30.01],
    '扬州':[119.42,32.39],
    '常州':[119.95,31.79],
    '潍坊':[119.1,36.62],
    '重庆':[106.54,29.59],
    '台州':[121.420757,28.656386],
    '南京':[118.78,32.04],
    '滨州':[118.03,37.36],
    '贵阳':[106.71,26.57],
    '无锡':[120.29,31.59],
    '本溪':[123.73,41.3],
    '克拉玛依':[84.77,45.59],
    '渭南':[109.5,34.52],
    '马鞍山':[118.48,31.56],
    '宝鸡':[107.15,34.38],
    '焦作':[113.21,35.24],
    '句容':[119.16,31.95],
    '北京':[116.46,39.92],
    '徐州':[117.2,34.26],
    '衡水':[115.72,37.72],
    '包头':[110,40.58],
    '绵阳':[104.73,31.48],
    '乌鲁木齐':[87.68,43.77],
    '枣庄':[117.57,34.86],
    '杭州':[120.19,30.26],
    '淄博':[118.05,36.78],
    '鞍山':[122.85,41.12],
    '溧阳':[119.48,31.43],
    '库尔勒':[86.06,41.68],
    '安阳':[114.35,36.1],
    '开封':[114.35,34.79],
    '济南':[117,36.65],
    '德阳':[104.37,31.13],
    '温州':[120.65,28.01],
    '九江':[115.97,29.71],
    '邯郸':[114.47,36.6],
    '临安':[119.72,30.23],
    '兰州':[103.73,36.03],
    '沧州':[116.83,38.33],
    '临沂':[118.35,35.05],
    '南充':[106.110698,30.837793],
    '天津':[117.2,39.13],
    '富阳':[119.95,30.07],
    '泰安':[117.13,36.18],
    '诸暨':[120.23,29.71],
    '郑州':[113.65,34.76],
    '哈尔滨':[126.63,45.75],
    '聊城':[115.97,36.45],
    '芜湖':[118.38,31.33],
    '唐山':[118.02,39.63],
    '平顶山':[113.29,33.75],
    '邢台':[114.48,37.05],
    '德州':[116.29,37.45],
    '济宁':[116.59,35.38],
    '荆州':[112.239741,30.335165],
    '宜昌':[111.3,30.7],
    '义乌':[120.06,29.32],
    '丽水':[119.92,28.45],
    '洛阳':[112.44,34.7],
    '秦皇岛':[119.57,39.95],
    '株洲':[113.16,27.83],
    '石家庄':[114.48,38.03],
    '莱芜':[117.67,36.19],
    '常德':[111.69,29.05],
    '保定':[115.48,38.85],
    '湘潭':[112.91,27.87],
    '金华':[119.64,29.12],
    '岳阳':[113.09,29.37],
    '长沙':[113,28.21],
    '衢州':[118.88,28.97],
    '廊坊':[116.7,39.53],
    '菏泽':[115.480656,35.23375],
    '合肥':[117.27,31.86],
    '武汉':[114.31,30.52],
    '大庆':[125.03,46.58]
};

var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var geoCoord = geoCoordMap[data[i].name];
        if (geoCoord) {
            res.push({
                name: data[i].name,
                value: geoCoord.concat("人数：", data[i].value)
            });
        }
    }
    return res;
};

var option = {
    backgroundColor: '#404a59',
    title: {
        text: '回答者地域分布',
        subtext: '仅限中国',
        // left: 'center',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip : {
        trigger: 'item'
    },
    legend: {
        orient: 'vertical',
        y: 'bottom',
        x:'right',
        data:['pm2.5'],
        textStyle: {
            color: '#fff'
        }
    },
    geo: {
        map: 'china',
        label: {
            emphasis: {
                show: false
            }
        },
        roam: true,
        itemStyle: {
            normal: {
                areaColor: '#323c48',
                borderColor: '#111'
            },
            emphasis: {
                areaColor: '#2a333d'
            }
        }
    },
    series : [
        {
            name: '回答者地域分布',
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: convertData(data),
            symbolSize: function (val) {
                return val[3] * 7;
            },
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
        {
            name: 'Top 5',
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: convertData(data.sort(function (a, b) {
                return b.value - a.value;
            }).slice(0, 6)),
            symbolSize: function (val) {
                return val[2]*7;
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        }
    ]
}
    myChart.setOption(option);
}

function echarts_choice(parid,i,sno,json_list){
    var myChart = echarts.init(document.getElementById(parid + i));
    console.log(json_list);
    var type = (json_list.type == "qsc single"?"单选":"多选") + "题：" + json_list.title;
    var choice = json_list.choice;
    var number = json_list.number;
    var option = {
           title: {
               text: type
           },
           tooltip: {},
           // legend: {
           //     data:[type]
           // },
           xAxis: {
               type:"value"
           },
           yAxis: {
               type:"category",
               data: choice
           },
           series: [{
               name: '选择次数',
               type: 'bar',
               data: number
           }]
       };
       myChart.setOption(option);
}

function create_series(length,type,name,data){
    var series = new Array();
    for (var i=0; i<length ; i++){
        var pattern = new Object();
        pattern.name=name[i];
        pattern.type=type;
        pattern.data=data[i];
        series[i] = pattern;
    }
    return series;
}

function echarts_correlation(parid,type,sno,json_list){
    var myChart = echarts.init(document.getElementById(parid));
    if (json_list.variable_1[0]!="选" && json_list.variable_2[0]!= "选"){
        var title = json_list.variable_1 + "-" + json_list.variable_2 + "相关性" + type;
    }

    else{
        var title = "相关性" + type;
    }
    type = type=="柱状图"?'bar':'line';
    var xAxis = json_list.xAxis;
    var data = json_list.yAxis_data;
    var series = create_series(data.length,type,json_list.yAxis_name,json_list.yAxis_data);
    console.log(series);
    var option = {
           title: {
               text: title
           },
           tooltip: {},
           legend: {
               data:json_list.yAxis_name
           },
           xAxis: {
               type:"category",
               data: xAxis
           },
           yAxis: {
               type:"value"
           },
           series: series
       };
       myChart.setOption(option);
}


function echarts_slice(parid,json_list){
    var myChart = echarts.init(document.getElementById(parid));

    var xAxis = json_list.xAxis;
    var send = json_list.send;
    var receive = json_list.receive;
    var option = {
           title: {
               text: "数据集切割回收情况"
           },
           tooltip: {},
           legend: {
               data:json_list.yAxis_name
           },
           xAxis: {
               type:"category",
               data: xAxis
           },
           yAxis: {
               type:"value"
           },
           series: [{
               name: '分发份数',
               type: 'line',
               data: send
           },
            {
               name: '回收份数',
               type: 'bar',
               data: receive
           }
           ]
       };
       myChart.setOption(option);
}

