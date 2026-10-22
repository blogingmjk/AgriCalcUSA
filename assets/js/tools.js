(function(root){
  'use strict';
  var N=function(x,d){return Number(x).toLocaleString('en-US',{maximumFractionDigits:d==null?2:d,minimumFractionDigits:0});};
  var USD=function(x){return Number(x).toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2});};
  var fail=function(m){return {error:m};};
  var SQM={acres:4046.8564224,hectares:10000,'square feet':0.09290304,'square yards':0.83612736,'square meters':1,'square miles':2589988.110336};
  var BUWT={corn:56,soybeans:60,wheat:60,barley:48,oats:32,sorghum:56,rye:56};
  var LB={bushels:null,pounds:1,'short tons':2000,'metric tonnes':2204.62262,'hundredweight (cwt)':100};
  var PRESETS={corn:{pop:34000,spl:1600,bag:80000},soybeans:{pop:120000,spl:2800,bag:140000},wheat:{pop:1200000,spl:14000,bag:0},custom:{}};

  var TOOLS={
    area:function(v){
      if(!(v.value>=0))return fail('Enter an area of zero or more.');
      var sqm=v.value*SQM[v.unit],rows=[];
      Object.keys(SQM).forEach(function(k){rows.push([k.charAt(0).toUpperCase()+k.slice(1),N(sqm/SQM[k],k==='square miles'?6:4)]);});
      return {big:N(sqm/SQM.acres,4)+' acres',sub:N(v.value,4)+' '+v.unit+' equals:',rows:rows};
    },
    seed:function(v){
      if(!(v.acres>0&&v.pop>0&&v.germ>0&&v.emerg>0&&v.spl>0))return fail('Acres, target population, germination, emergence and seeds per pound must all be greater than zero.');
      if(v.germ>100||v.emerg>100)return fail('Germination and emergence cannot exceed 100%.');
      var spa=v.pop/((v.germ/100)*(v.emerg/100)),tot=spa*v.acres,lbs=tot/v.spl,rows=[
        ['Seeds per acre to plant',N(spa,0)],['Total seeds needed',N(tot,0)],['Seed weight per acre',N(lbs/v.acres,1)+' lb'],['Total seed weight',N(lbs,0)+' lb']];
      if(v.bag>0){var bags=Math.ceil(tot/v.bag);rows.push(['Bags needed ('+N(v.bag,0)+' seeds each)',N(bags,0)]);if(v.price>0)rows.push(['Estimated seed cost',USD(bags*v.price)]);}
      else if(v.price>0)rows.push(['Estimated seed cost',USD(lbs*v.price)]);
      return {big:N(spa,0)+' seeds/acre',sub:'Planting rate needed to reach '+N(v.pop,0)+' plants/acre',rows:rows,note:'Typical defaults only. Use the germination % on your seed tag and your own planter and field conditions.'};
    },
    fert:function(v){
      if(!(v.acres>0))return fail('Enter the number of acres.');
      var g=function(s){return s.split('-').map(Number);},rows=[],nS=g(v.nsrc),pS=g(v.psrc),kS=g(v.ksrc),cost=0,hasCost=false;
      if(v.p2o5>0&&!(pS[1]>0))return fail('Pick a phosphate source to supply P2O5.');
      if(v.k2o>0&&!(kS[2]>0))return fail('Pick a potash source to supply K2O.');
      var pLb=v.p2o5>0?v.p2o5/(pS[1]/100):0,nFromP=pLb*pS[0]/100,remN=Math.max(0,v.n-nFromP),nLb=v.n>0&&remN>0?remN/(nS[0]/100):0,kLb=v.k2o>0?v.k2o/(kS[2]/100):0;
      var add=function(label,lbAc,price){if(lbAc<=0)return;var tons=lbAc*v.acres/2000;rows.push([label,N(lbAc,0)+' lb/ac',N(tons,2)+' tons']);if(price>0){cost+=tons*price;hasCost=true;}};
      var tbl=[];
      add(v.pname,pLb,v.pprice);add(v.nname,nLb,v.nprice);add(v.kname,kLb,v.kprice);
      if(!rows.length)return fail('Enter at least one nutrient target (N, P2O5 or K2O).');
      var out=rows.map(function(r){return [r[0],r[1]+' · '+r[2]];});
      if(nFromP>0)out.push(['Nitrogen supplied by phosphate product',N(Math.min(nFromP,v.n||nFromP),1)+' lb N/ac']);
      if(hasCost)out.push(['Estimated fertilizer cost',USD(cost)+' ('+USD(cost/v.acres)+'/ac)']);
      return {big:rows.map(function(r){return r[1];}).join(' + '),sub:'Product to apply per acre across '+N(v.acres,1)+' acres',rows:out,note:'Rates are nutrient targets converted to product weight. Base targets on a soil test and your state extension recommendations.'};
    },
    profit:function(v){
      if(!(v.acres>0&&v.yield>=0&&v.price>=0))return fail('Enter acres, expected yield and price.');
      var cost=v.seed+v.fert+v.chem+v.ins+v.mach+v.labor+v.rent+v.other,rev=v.yield*v.price,net=rev-cost,rows=[
        ['Revenue per acre',USD(rev)],['Total cost per acre',USD(cost)],['Net return per acre',USD(net)],['Total revenue',USD(rev*v.acres)],['Total cost',USD(cost*v.acres)],['Total net return',USD(net*v.acres)],
        ['Break-even price',v.yield>0?USD(cost/v.yield)+' /bu':'n/a'],['Break-even yield',v.price>0?N(cost/v.price,1)+' bu/ac':'n/a'],['Profit margin',rev>0?N(net/rev*100,1)+'%':'n/a']];
      return {big:USD(net)+' per acre',sub:net>=0?'Projected profit after all listed costs':'Projected loss after all listed costs',rows:rows};
    },
    irrigation:function(v){
      if(!(v.acres>0&&v.depth>0&&v.eff>0&&v.eff<=100))return fail('Enter acres, a depth above zero, and an efficiency between 1 and 100%.');
      var gross=v.depth/(v.eff/100),ai=gross*v.acres,gal=ai*27154,rows=[['Gross depth to pump',N(gross,2)+' in'],['Total water',N(ai,1)+' acre-inches'],['Total water',N(ai/12,2)+' acre-feet'],['Total water',N(gal,0)+' gallons']];
      if(v.gpm>0){var hrs=gal/(v.gpm*60);rows.push(['Pumping time at '+N(v.gpm,0)+' GPM',N(hrs,1)+' hours']);rows.push(['Pumping time (24 h/day)',N(hrs/24,1)+' days']);}
      return {big:N(gal/1e6,2)+' million gal',sub:'To apply '+N(v.depth,2)+' in net over '+N(v.acres,1)+' acres at '+N(v.eff,0)+'% efficiency',rows:rows,note:'1 acre-inch = 27,154 gallons. Check state and local water-use rules.'};
    },
    grain:function(v){
      var w=BUWT[v.crop];if(!(v.amount>=0))return fail('Enter an amount of zero or more.');
      var lb=v.unit==='bushels'?v.amount*w:v.amount*LB[v.unit],rows=[['Bushels',N(lb/w,2)],['Pounds',N(lb,0)],['Short tons',N(lb/2000,3)],['Metric tonnes',N(lb/2204.62262,3)],['Hundredweight (cwt)',N(lb/100,1)]];
      var big=N(lb/w,2)+' bushels',sub='Using '+w+' lb per bushel for '+v.crop;
      if(v.yield>0){rows.push(['Yield: '+N(v.yield,1)+' bu/ac in lb/ac',N(v.yield*w,0)]);rows.push(['Yield in kg/ha',N(v.yield*w*1.12085,0)]);rows.push(['Yield in metric tonnes/ha',N(v.yield*w*1.12085/1000,2)]);}
      return {big:big,sub:sub,rows:rows,note:'Uses standard test weights. Actual test weight and moisture vary by lot.'};
    },
    bin:function(v){
      if(!(v.dia>0&&v.depth>0&&v.peak>=0))return fail('Enter bin diameter and grain depth above zero.');
      var base=Math.PI*v.dia*v.dia/4,cyl=base*v.depth*0.8036,cone=base*v.peak/3*0.8036,tot=cyl+cone,lb=tot*BUWT[v.crop];
      return {big:N(tot,0)+' bushels',sub:'Estimated '+v.crop+' in a '+N(v.dia,0)+' ft bin',rows:[['Level grain (cylinder)',N(cyl,0)+' bu'],['Peak (cone)',N(cone,0)+' bu'],['Total bushels',N(tot,0)],['Weight (short tons)',N(lb/2000,1)],['Weight (metric tonnes)',N(lb/2204.62262,1)]],note:'Uses 1 bu = 1.2445 cu ft. Deep grain packs, so real capacity can run a few percent higher. Confirm with your bin manufacturer.'};
    },
    sprayer:function(v){
      if(!(v.gpm>0&&v.mph>0&&v.space>0))return fail('Enter nozzle flow, speed and nozzle spacing above zero.');
      var gpa=v.gpm*5940/(v.mph*v.space),rows=[['Application rate',N(gpa,2)+' GPA']];
      if(v.tank>0){var apt=v.tank/gpa;rows.push(['Acres per full tank',N(apt,1)]);if(v.rate>0)rows.push(['Product per full tank',N(v.rate*apt,2)+' (label units)']);
        if(v.acres>0){rows.push(['Tanks for '+N(v.acres,1)+' acres',N(v.acres/apt,2)]);if(v.rate>0)rows.push(['Total product',N(v.rate*v.acres,2)+' (label units)']);}}
      return {big:N(gpa,2)+' GPA',sub:'Gallons per acre applied',rows:rows,note:'Always follow the product label for rates, water volume and nozzle type. Verify with a catch test.'};
    },
    gdd:function(v){
      if(!(v.base>=0)&&v.base!==0)return fail('Enter a base temperature.');
      var lines=String(v.days||'').split(/\n/).map(function(s){return s.trim();}).filter(Boolean);
      if(!lines.length)return fail('Enter at least one day as "high, low".');
      var cum=0,rows=[],bad=0;
      lines.forEach(function(ln,i){
        var p=ln.split(/[\s,;\t]+/).map(Number);if(p.length<2||isNaN(p[0])||isNaN(p[1])){bad++;return;}
        var hi=p[0],lo=p[1];if(hi<lo){var x=hi;hi=lo;lo=x;}
        if(v.cap>0&&hi>v.cap)hi=v.cap;if(v.floor&&lo<v.base)lo=v.base;if(v.cap>0&&lo>v.cap)lo=v.cap;
        var g=Math.max(0,(hi+lo)/2-v.base);cum+=g;rows.push(['Day '+(i+1)+' ('+p[0]+'/'+p[1]+' °F)',N(g,1)+'  →  '+N(cum,1)]);
      });
      if(!rows.length)return fail('Could not read any days. Use one line per day like: 85, 62');
      return {big:N(cum,1)+' GDD',sub:'Accumulated over '+rows.length+' day'+(rows.length>1?'s':''),rows:rows,scroll:rows.length>8,note:(bad?bad+' line(s) skipped. ':'')+'Each row shows day GDD → running total.'};
    }
  };

  function read(form){
    var v={};Array.prototype.forEach.call(form.elements,function(e){
      if(!e.name)return;
      if(e.type==='number'){v[e.name]=e.value===''?0:parseFloat(e.value);}
      else if(e.type==='checkbox'){v[e.name]=e.checked;}
      else{v[e.name]=e.value;}
      if(e.tagName==='SELECT'){v[e.name+'_text']=e.options[e.selectedIndex].text;}
    });
    v.nname=v.nsrc_text;v.pname=v.psrc_text;v.kname=v.ksrc_text;return v;
  }
  function render(box,r){
    box.className='result';box.setAttribute('role','status');
    if(r.error){box.classList.add('err');box.textContent=r.error;return;}
    box.classList.add('ok');
    var h='<div class="big"></div><div class="sub"></div><div class="'+(r.scroll?'scroll':'')+'"><table><tbody></tbody></table></div>';
    box.innerHTML=h;box.querySelector('.big').textContent=r.big;box.querySelector('.sub').textContent=r.sub||'';
    var tb=box.querySelector('tbody');
    r.rows.forEach(function(x){var tr=document.createElement('tr'),a=document.createElement('td'),b=document.createElement('td');a.textContent=x[0];b.textContent=x[1];tr.appendChild(a);tr.appendChild(b);tb.appendChild(tr);});
    if(r.note){var n=document.createElement('p');n.className='note';n.textContent=r.note;box.appendChild(n);}
  }
  function init(){
    var form=document.getElementById('tool-form');if(!form)return;
    var key=form.getAttribute('data-tool'),box=document.getElementById('result');
    form.addEventListener('submit',function(e){e.preventDefault();render(box,TOOLS[key](read(form)));if(window.innerWidth<900)box.scrollIntoView({behavior:'smooth',block:'nearest'});});
    form.addEventListener('reset',function(){setTimeout(function(){box.className='result';box.textContent='Your results will appear here.';},0);});
    if(key==='seed'){var c=form.elements.crop;c.addEventListener('change',function(){var p=PRESETS[c.value];if(p&&p.pop){form.elements.pop.value=p.pop;form.elements.spl.value=p.spl;form.elements.bag.value=p.bag;}});}
    if(key==='gdd'){var m=form.elements.method;m.addEventListener('change',function(){var o=m.options[m.selectedIndex];if(o.dataset.base!=null){form.elements.base.value=o.dataset.base;form.elements.cap.value=o.dataset.cap;form.elements.floor.checked=o.dataset.floor==='1';}});}
  }
  if(typeof document!=='undefined'){document.addEventListener('DOMContentLoaded',init);}
  root.AgriTools=TOOLS;if(typeof module!=='undefined')module.exports=TOOLS;
})(typeof window!=='undefined'?window:globalThis);
