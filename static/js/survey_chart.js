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
function add_list_item(json,parid){
    var parele = document.getElementById(parid);
    var ele = document.getElementById("list-item-survey").cloneNode(true);
    ele.getElementsByClassName("name title")[0].innerHTML = json.title;
    ele.getElementsByClassName("name title")[0].href = "/project/view?sno=" + String(json.sno);
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
function add_label(par_ele,what,type){
    par_ele.innerHTML += "<label class = %label label-{0}%>".format(type)+what+"</label>  ";
}

function clear_list_item(parid){
    var parele = document.getElementById(parid);
    parele.innerHTML = "";
}

function load_questions(json_all,qid,eleid) {
    for(var i = 0;i<json_all.length;++i) {
        if(json_all[i].type == "qa"){
            load_qa(json_all[i],qid,eleid);
        }
        else if(json_all[i].type == "qsc"){
            load_qsc(json_all[i],qid,eleid);
        }
        qid++;
    }
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
    par.appendChild(ele);
}

