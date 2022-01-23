const buttons = document.getElementsByTagName("button");


for (const button of buttons) {
  
  button.addEventListener('click', () => {
    setTimeout(function() {
     var id = button.getAttribute("id");
    
     var layerClass = "." + id+ "-layer";
     var layers = document.querySelectorAll(layerClass);
     for (const layer of layers) {
       layer.classList.toggle("active");  
     }
    }, 1);
  }
  );
}

function getCookie(cName) {
  const name = cName + "=";
  const cDecoded = decodeURIComponent(document.cookie); //to be careful
  const cArr = cDecoded .split('; ');
  let res;
  cArr.forEach(val => {
      if (val.indexOf(name) === 0) res = val.substring(name.length);
  })
  return res;
}

function car_disp(val){
  var x = document.getElementById("out_car");
  x.innerHTML = val;
}

function dist_disp(val){
  var x = document.getElementById("out_dist");
  x.innerHTML = val;
  sessionStorage.setItem("distance",val);
}

function disp_up_tran(){
  var uptram = document.getElementById('uptran');
  uptram.style.display='block';
}

function unit(){
  var x = document.getElementById("dist_unit");
  if (x.innerHTML=='Km'){
    sessionStorage.setItem("unit",'Miles');
    sessionStorage.setItem("dist_mult",1.60934);
    x.innerHTML = "Miles";
  }else {
    sessionStorage.setItem("unit",'Km');
    sessionStorage.setItem("dist_mult",1);
    x.innerHTML = "Km";
  }
}

function carbon_calc(){
  var carbon = (parseFloat(sessionStorage.getItem("distance"))*parseFloat((sessionStorage.getItem("dist_mult")))*parseFloat((sessionStorage.getItem("CO2perkg")))*1000)
  var log = (localStorage.getItem("log")).split(",")
  var add_sec = [sessionStorage.getItem('car'),sessionStorage.getItem("distance"),sessionStorage.getItem("unit"),carbon]
  log.push(add_sec.toString())
  localStorage.setItem("log",log.toString())
}


