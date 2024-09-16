function ExecuteScript(strId)
{
  switch (strId)
  {
      case "5l0va8qNFXZ":
        Script1();
        break;
      case "63DpjbsbHYs":
        Script2();
        break;
  }
}

window.InitExecuteScripts = function()
{
var player = GetPlayer();
var object = player.object;
var addToTimeline = player.addToTimeline;
var setVar = player.SetVar;
var getVar = player.GetVar;
window.Script1 = function()
{
  const target = object('6f8fQKJrzeT');
const duration = 750;
const easing = 'ease-out';
const id = '6C5GPLVWc65';
const pulseAmount = 0.07;
player.addForTriggers(
id,
target.animate([
{ scale: '1' }, { scale: `${1 + pulseAmount}` },
{ scale: '1' }, { scale: `${1 + pulseAmount}` },
{ scale: '1' }
],
  { fill: 'forwards', duration, easing }
)
);
}

};
