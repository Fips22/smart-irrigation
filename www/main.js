
//siehe https://closure-compiler.appspot.com/home


// window.onload
window.onload = function() {

  let valveNumbers = [];
  let d = document

  function loadInitState(cb){

    var request = new XMLHttpRequest();

    request.open('POST', '/state.json', true);

      request.onload = function() {

        if (request.status >= 200 && request.status < 400) {
            // Success!
          //processInitState(JSON.parse(request.responseText));
          cb(JSON.parse(request.responseText));

          } 

      };

    request.send();
    
  }

  function processInitState(stateObj){

    d.getElementById("mois").innerHTML =stateObj.mois+ "%" ;
    d.getElementById("temp").innerHTML =stateObj.temp+"C°" ;
    d.getElementById("lev").innerHTML =stateObj.lev+"%" ;
    d.getElementById("selInputNum").setAttribute("max", stateObj.inputCannels);

    let plantTab = d.getElementById("plantTab");

    let i=0;

    for (let x in stateObj.plants) {

      let entry; 

      if(i==0)
      {
        entry = plantTab.children[0];

        for(let j=1 ; 1<plantTab.children.length ; j++){  //remove all-first childs
          plantTab.removeChild(plantTab.children[1]);
        }

      }else
      {
        entry = plantTab.children[0].cloneNode(true);
        plantTab.appendChild(entry);

      }  

      plantTab.appendChild(entry);
      
      entry.children[0].children[0].setAttribute("value", i);
      entry.children[0].children[0].setAttribute("plant_id", stateObj.plants[x].valve);
      valveNumbers.push(stateObj.plants[x].valve+"");
      entry.children[1].innerHTML=stateObj.plants[x].valve;
      entry.children[2].innerHTML=stateObj.plants[x].art;
      entry.children[3].innerHTML=stateObj.plants[x].mois +"%/"+ (stateObj.plants[x].mode > 0 ? " -":stateObj.plants[x].maxmois+"%");
      entry.children[4].innerHTML=stateObj.plants[x].consump + "ml/d";
      entry.children[5].innerHTML=stateObj.plants[x].mode > 0 ? "Interv":"Auto";

      i++;
            
    }

    function select(e){

      let x = e.target.attributes.getNamedItem("value").value;

      d.getElementById("selPlName").value = stateObj.plants[x].art;
      d.getElementById("selVtNum").value = stateObj.plants[x].valve;
      d.getElementById("ventmode").value = stateObj.plants[x].mode;
      d.getElementById("amount").value = stateObj.plants[x].consump;
      d.getElementById("maxmoisture").value = stateObj.plants[x].maxmois;
    }


    let elements = d.getElementsByClassName("plant");

    for (let x of elements) {
      x.addEventListener("click", select);
    }

  }

  function sendRequest(url,string,cb){

    let request = new XMLHttpRequest();

    request.open('POST', url, true);

      request.onload = ()=>{

        request.status >= 200 && request.status < 400? cb():console.log("send fail");

      };

      request.send(string);


  }

  function saveValve(e){ //speichert ventileintrag

    let changedValveEntry = JSON.stringify({
      "art" :  d.getElementById("selPlName").value,
      "id"  :  d.getElementById("selVtNum").value, 
      "mode":  d.getElementById("ventmode").value, 
      "consump": d.getElementById("amount").value, 
      "maxmois": d.getElementById("maxmoisture").value 

    });

    sendRequest("/updateValve", changedValveEntry,()=>loadInitState(processInitState)/*processInitState(json)*/);
     //loadInitState(processInitState);
  }

  function deleteValve(e){//löscht vertileintrag

    sendRequest("/delValve", d.getElementById("selVtNum").value,()=>loadInitState(processInitState)/*processInitState(json)*/);
    //loadInitState(processInitState);
  }

  function getSelectedRad(){

      let valverad = d.getElementsByClassName("valveRad");
      let selectedRad = false;
      for (let x of valverad){
        x.checked? selectedRad = x.attributes.plant_id.value: false; 
      }

      return selectedRad;
  }

  function sendCommand(amount){// seldet befehl zum vertil öffnen und wasser pumpen
    let getSelRad = getSelectedRad();

    getSelRad? sendRequest("/command",JSON.stringify({"v": getSelRad ,"am":amount }),console.log("send")):false
  }

  

  //form events
  d.getElementById("selVtNum").addEventListener("change", (e)=>{
    let selectedRad = getSelectedRad();
      // wenn value in array und value nicht selectet dann setze es zurück auf selected 
      valveNumbers.indexOf(e.target.value+"")>=0 && selectedRad!=e.target.value && selectedRad!=null ? e.target.value = selectedRad:null;
    });

  d.getElementById("saveval").addEventListener("click", (e)=>{e.preventDefault();saveValve();});
  d.getElementById("delval" ).addEventListener("click", (e)=>{e.preventDefault();deleteValve();});
  d.getElementById("opVent" ).addEventListener("click", (e)=>{e.preventDefault();sendCommand(0);});
  d.getElementById("50ml"   ).addEventListener("click", (e)=>{e.preventDefault();sendCommand(50);});

  d.getElementById("valUpdateForm").addEventListener("submit", (e)=>e.preventDefault());



//------------------------------------------------------------------------------------------
//production
loadInitState(processInitState);
//loadConfig(processConfig);

/*let json = {"lev": 40, "temp": 27, "mois": 70,"inputCannels":10,
 "plants": [
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 19, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 11, "mode": 1},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 10, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 9, "mode": 1},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 8, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 7, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 6, "mode": 1},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 5, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 4, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 3, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 2, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minze", "mois": 60, "valve": 0, "mode": 0},
 {"consump": 5, "maxmois": 80, "art": "Minzejj", "mois": 50, "valve": 1, "mode": 1}
 ]}*/

//test
//processInitState(json);


};


  