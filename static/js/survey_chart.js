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



