url_server=""


//add las coin disponibles en el config.py al select
function coin_select() {
    let coin_list = Object.keys(data.coin)

    select = document.getElementById('coin');
    for (var i = 0; i < coin_list.length; i++) {
        let opt = document.createElement('option');
        opt.value = coin_list[i];
        opt.innerHTML = 'Coin ' + coin_list[i];
        select.appendChild(opt);
    }

}

//add las redes disponibles segun la coin el config.py
function red_select(coin) {
    let coin_list = Object.keys(data.coin)
    let red_list = Object.keys(data.coin[coin].red)
    let select = document.getElementById('red');

    for (var i = 0; i < red_list.length; i++) {
        let opt = document.createElement('option');
        opt.value = data.coin[coin].red[i];
        opt.innerHTML = 'Red ' + data.coin[coin].red[i];
        select.appendChild(opt);
    }
}

//llama al coin_select
coin_select();

const coin = document.querySelector('#coin');

//add event chaNge al coin select, al tocar las coin se actualiza las redes disponibles
coin.addEventListener('change', (event) => {
    let select = document.getElementById("red");
    let length = select.options.length;
    for (i = length - 1; i > 0; i--) {
        select.options[i] = null;
    }

    red_select(event.target.value);
});


const btn_buy = document.querySelector('#btnBuy');

//add event click al dar comprar consulta al server el precio de la coin, el fee network y el precio del dolar
btn_buy.addEventListener('click', (event) => {
    const select_coin = document.getElementById("coin").value;
    const select_red = document.getElementById("red").value;
    const input_amount = document.getElementById("input_amount").value;
    const input_address = document.getElementById("input_address").value;

    fetch(url_server+'/buy/get_info?coin=' + select_coin + '&network=' + select_red)
        .then(response => response.json())
        .then(res => {
            const fees = parseFloat(res['fees']);
            const withdraw_min = res['withdrawMin'];
            const price = parseFloat(res['price']).toFixed(2);
            const dolar = parseFloat(res['dolar']).toFixed(2);
            const monto=((1+data['ganancia'])*dolar*price * (parseFloat(input_amount) +fees)).toFixed(2);

          
            document.getElementById("info_buy_coin").value = select_coin + ' (precio:' + price + ' USDT)';
            document.getElementById("info_buy_red").value = select_red;
            document.getElementById("info_buy_address").value = input_address;
            document.getElementById("info_buy_amount").value = input_amount;
            document.getElementById("info_buy_fees").value = fees + ' ' + select_coin+'('+(price*fees).toFixed(2)+'USDT)';
            document.getElementById("info_buy_monto").value =monto ;
            document.getElementById("amount_pesos").value =monto ;
        }
        );

});

//send form
const form_buy = document.getElementById('confirm-form');
form_buy.addEventListener('submit', (event) => {

    event.preventDefault();

    const select_coin = document.getElementById("coin").value;
    const select_red = document.getElementById("red").value;
    const input_amount = document.getElementById("input_amount").value;
    const input_address = document.getElementById("input_address").value;
    const amount_pesos = document.getElementById("amount_pesos").value

    
    let formData=new FormData();
    formData.append('coin', select_coin);
    formData.append('red', select_red);
    formData.append('amount_coin', input_amount);
    formData.append('amount_pesos', amount_pesos);
    formData.append('address', input_address);

    console.log(formData)
    fetch(url_server+'/buy/pay',{
        method:'post',
        body:formData
    }).then(function(response){
        return response.json();
    }).then(function(text){
        window.location.replace(text.url_redirect);
    });

});



const btn_find = document.querySelector('#btnFind');
//add event click al dar comprar consulta al server el precio de la coin, el fee network y el precio del dolar
btn_find.addEventListener('click', (event) => {
    
    const address = document.getElementById("find_address").value;

    fetch(url_server+'/buy/historial?address=' + address)
        .then(response => response.json())
        .then(res => {
            let historial = document.getElementById('historial');

            const len_historial=res.historial.length;
            for (let index = 0; index < len_historial; index++) {
                const div = document.createElement('div');
                div.className = 'history__item';
                div.id=historial+index;

                const p = document.createElement('p');
                p.innerHTML="COIN/RED: "+res.historial[index].coin+"/"+res.historial[index].red+"<br /> CANTIDAD: "+res.historial[index].cantidad+" <br /> ESTADO: "+res.historial[index].status+"<br />";
                p.className="p_historial";

                const a = document.createElement('a');
                a.href=res.historial[index].tx_id
                a.innerText="Ver transacción."
                a.target="_blank"
                p.appendChild(a)
                div.appendChild(p);
                historial.appendChild(div);
            }
        });
});