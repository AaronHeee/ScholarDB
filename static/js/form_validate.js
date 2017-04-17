/**
 * Created by aucson on 17-4-6.
 */
function isSame(str1,str2) {
    return str1 == str2;
}

function isNumber(str)
{
    return !isNaN(str);
}

function isEmail(str)
{
    var reg=/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
    return reg.test(str);
}

function isNotNull(value)
{
    return !(value == "" || value == null);
}

/**
 * Create by aaron on 17-04-15
 */

function isNull(value)
{
    return (value == "") || (value == null) ;
}

function validate_required_txt(id,errtext)
{
        if(isNull(document.getElementById(id)).value)
        {
            document.getElementById("errortext").style.visibility = "visible";
            document.getElementById("errortext").innerHTML = errtext;
            return false;
        }
        else
            return true;
}

function validate_required_num(id,errtext)
{
        if(isNumber(document.getElementById(id)).value)
        {
            document.getElementById("errortext").style.visibility = "visible";
            document.getElementById("errortext").innerHTML = errtext;
            return false;
        }
        else
            return true;
}