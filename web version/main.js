let canvas = document.getElementById("fen");
let context = canvas.getContext("2d"),
			W = window.innerWidth,
			H = window.innerHeight,
			ratio = window.devicePixelRatio;
let hmemel=document.getElementById("html");
canvas.width = W*ratio;
canvas.height = H*ratio;
canvas.style.width = W  + "px";
canvas.style.height = H  + "px";
context.scale(ratio,ratio);
document.addEventListener("wheel",scroll,false);
document.addEventListener("mousemove", bouge, false);
document.onmousedown = click;
document.onmouseup= function up(e) {
	mode=''
}
document.addEventListener("keydown", keydown, false);
function bouge(p){
	x = p.pageX;
	y = p.pageY;
	x=Math.round(x/SIZE)-1-depx/SIZE
    y=Math.round(y/SIZE)-1-depy/SIZE
}
function scroll(cb){
	if(cb.deltaY<0){
		SIZE+=5;
		depx-=x*5
		depy-=y*5
	}else if(cb.deltaY>0){
		SIZE-=5
		if(SIZE<0){
			size=1
		}else{
			depx+=x*5
			depy+=y*5
		}
	}
	nbsx=parseInt(W/SIZE)
	nbsy=parseInt(H/SIZE)
}
function click(e) {
	switch(e.buttons){
		case 1:
			mode='c'
			break;
		case 2:
			mode='take'
			sel=lieux[[x,y]]
			break;
		case 4:
			mode='e'
			break;
	}
}
function keydown(e){
	v=e.keyCode
	console.log(v)
	switch(v){
		case 81:
			depx+=10
			break;
		case 83:
			depy-=10
			break;
		case 68:
			depx-=10
			break;
		case 90:
			depy+=10
			break;
		case 87:
			sel+=0.1
			break;
		case 88:
			sel-=0.1
			break;
		case 27:
			depx=0
			depy=0
			break;
		case 67:
			sel=lieux[[x,y]]
			break;
		case 16:
			devmode= !devmode
			break;
		case 32:
			helpmode= !helpmode
	}
	sel=sel%1.2
	document.body.style.backgroundColor = coul(sel)
	//shell.textContent+=v+"\n";
	//context.fillStyle = "blue";
	//context.fillText(v,v*10,v*10);
}
let dep={'x':0,'y':0}
function find(xer,yer){
	return lieux[[xer,yer]]!=undefined
}
function coul(sel) {
	if(sel==1){
		return "white"
	}else{
		return "hsl("+sel*360+",100%,50%)";
	}
}
let lieux={}
let mode=''
let sel=1
let depx=0,depy=0;
let devmode=true;
let helpmode=true;
let x=10
let y=10
let i,j;
let SIZE =75
let fakeSIZE=75
let nbsx=W/SIZE
let nbsy=H/SIZE
context.font = "25px consolas";
context.textBaseline = "middle"

function bLoop() {
	if(devmode){
		context.beginPath()
		context.fillStyle=coul(sel)
		context.fillRect(0,0,W,H)
		context.fill()
		context.closePath()
		context.beginPath()
		context.fillStyle='black'
		context.fillRect(5,5,W-10,H-10)
		context.fill()
		context.closePath()
	}else{
		context.beginPath()
		context.fillStyle='black'
		context.fillRect(0,0,W,H)
		context.fill()
		context.closePath()
	}

	dep.x+=(depx-dep.x)/7
	dep.y+=(depy-dep.y)/7
	fakeSIZE+=(SIZE-fakeSIZE)/7
	if(mode=='c'){
		lieux[[x,y]]=sel
	}else if(mode=='e'){
		if(find(x,y)){
			lieux[[x,y]]=undefined
		}
	}
	for(clef in lieux){
		pos=clef.split(',')
		i=parseInt(pos[0])+0.5
		j=parseInt(pos[1])+0.5
		if(i>-depx/SIZE-1 && j>-depy/SIZE-2 && i<-depx/SIZE+nbsx+1 &&j<-depy/SIZE+nbsy+1 ){
			context.beginPath()
			context.fillStyle=coul(lieux[clef])
			context.fillRect(i*SIZE+dep.x,j*SIZE+dep.y,SIZE,SIZE)
			context.fill()
			context.closePath()
		}
	}
	if(helpmode){
		context.fillStyle="black"
		context.fillRect(0,0,W/2,7*25)
		context.fillStyle = "white";
		let decal=25
		let ls=['Maj -> masquer la bordure','Flèches -> se déplacer','Molette -> zoomer','W/X -> changer de couleur','Echap -> recentrer',"Espace -> cacher cette inutilité"]
		for(elem in ls ){
			context.fillText(ls[elem],0,decal);
			decal+=25
		}

	}
	requestAnimationFrame(bLoop)
}
bLoop()