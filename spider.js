//去除弹框
document.getElementById("PNWHC000018_close").click()

//点击单程
document.getElementsByClassName("iCheck-helper")[1].click()


//设置出发地,参数传城市码,城市名都可以
function setchufa(cf){
    var chufa = cf
    //获得出发地列表
    var dep_list = document.getElementById("PNWHC00001_departure_list")
    var dep_list_a = dep_list.getElementsByTagName("a")

    //遍历网页可出发地列表,如果传的参数在可出发地列表中,则点击该出发地
    for (let i = 0; i < dep_list_a.length; i++) {
        const element = dep_list_a[i].text;
        if(element.indexOf(chufa)!= -1){
            dep_list_a[i].click()
            break
        }
    }
    //判断出发地是否被填写
    if(document.getElementById("PNWHC00001_departure_anchor").text == "选择出发城市"){
        console.log("没有此出发地")
    }else{
        console.log("设置出发地为:",chufa)
    }
}

//设置目的地,参数传城市码,城市名都可以
function setdaoda(dd){
    var daoda = dd
    //获得出发地列表
    var arr_list = document.getElementById("PNWHC00001_arrival_list")
    var arr_list_a = arr_list.getElementsByTagName("a")

    //遍历网页可到达地列表,如果传的参数在可到达地列表中,则点击该到达地
    for (let i = 0; i < arr_list_a.length; i++) {
        const element = arr_list_a[i].text;
        if(element.indexOf(daoda)!= -1){
            arr_list_a[i].click()
            break
        }
    }
    //判断出发地是否被填写
    if(document.getElementById("PNWHC00001_departure_anchor").text == "选择到达城市"){
        console.log("没有此到达地")
    }else{
        console.log("设置到达地为:",daoda)
    }
}

//设置时间
function settime(time){
    document.getElementById("PNWHC00001_departure_date").value = "2019-10-01"
    var m = document.getElementsByClassName("datepicker")[0]
    m.parentNode.removeChild(m);
    //设置时间
}




function main(){
    //设置出发地
    setchufa("仁川")
    //设置目的地延迟100毫秒
    setTimeout(() => {
        setdaoda("东京")
    }, 100);
}