//import * as layout from "./layout_generation.js"
import * as layout from "./worker_dummycode.js";

   

    function funcString(fnc){
        var wstring = fnc.toString(); 
        return wstring.slice(wstring.indexOf("{") + 1, wstring.lastIndexOf("}"));
    }

function callWorker(theWindow){

    var body =
    funcString(layout.dummycode)
    + funcString(myworker);

    var blobURL = window.URL.createObjectURL(new Blob([body]));
    theWindow.worker = new Worker(blobURL);
    //this.worker = new Worker("./layout_worker.js");

    theWindow.worker.addEventListener("message", result(theWindow.worker), e=>console.error(e));

    var data= {words:[],
        groups:{},
    options:theWindow.options,
        WH:theWindow.WH,
        worldPerScreen:theWindow.worldPerScreen
    };

    for(var [_,n] of theWindow.Map.entries()){
        data.words.push( 
            {computed_position:n.computed_position,WH:n.WH,
            groups:n.groups,
            normalized_size:n.normalized_size}
        )
    }
    for(var key of Object.keys(theWindow.groups)){
        var g = theWindow.groups[key];
        data.groups[key] = {
            WH: g.WH
        }
    }

    theWindow.worker.postMessage( data );

    function result(worker){
        return (msg)=>{
            if(worker!=theWindow.worker) return; // every result but the last one is dropped.
            console.log("MAIN: got msg: "+msg.data);
        }
    }
}  


function myworker(){
      self.addEventListener('message', function(e) {
        //self.postmessage( solve.tostring() );
        
        var wordset = e.data;
        wordset.error = {clear:()=>null,post:(e)=>console.error(e)};
        wordset.screenToWorld_vector=(v2)=>scale2(v2, wordset.worldPerScreen);

        layoutWordcloudFormGroupsResolveOverlap( wordset );
        setTimeout(()=>
        self.postMessage(e.data)
        ,1000);  
      }, false);
    }

export { callWorker }