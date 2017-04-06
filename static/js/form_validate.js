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

