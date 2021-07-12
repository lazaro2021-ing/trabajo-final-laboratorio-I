(()=>{
    let ws1 = new WebSocket('wss://stream.binance.com:9443/ws/ethusdt@trade'); 
    let ws2 = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@trade');
    let ws3 = new WebSocket('wss://stream.binance.com:9443/ws/ltcusdt@trade');
    let ws4 = new WebSocket('wss://stream.binance.com:9443/ws/eosusdt@trade'); 
  
    let priceEth = document.getElementById('priceEth');
    let priceBth = document.getElementById('priceBth');
    let priceLite = document.getElementById('priceLite');
    let priceEos = document.getElementById('priceEos');
  
    ws1.onmessage=(event)=>{
      let stockObject = JSON.parse(event.data);
      priceEth.innerText = parseInt(stockObject.p).toFixed(2);
    };
    ws2.onmessage=(event)=>{
      let stockObject2 = JSON.parse(event.data);
      priceBth.innerText = parseInt(stockObject2.p).toFixed(2);
    };
    ws3.onmessage=(event)=>{
      let stockObject3 = JSON.parse(event.data);
      priceLite.innerText = parseInt(stockObject3.p).toFixed(2);
    };
    ws4.onmessage=(event)=>{
      let stockObject4 = JSON.parse(event.data);
      priceEos.innerText = parseInt(stockObject4.p).toFixed(2);
    };
  })();
  