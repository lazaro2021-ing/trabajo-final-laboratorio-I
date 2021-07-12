//------definición variables-------

const ventanaModal = document.getElementById('modal');
const btnComprar= document.getElementById('btnBuy');
const btnCancel= document.getElementById('btnCancel');
const btnConfirm= document.getElementById('btnConfirm');

const loading = document.querySelector('.loading');
const checked = document.querySelector('.check-buy');

//------envento boton comprar-------
btnComprar.addEventListener('click', (e)=>{
  e.preventDefault();
  ventanaModal.classList.add('active');
});

//------envento boton cancelar compra-------
btnCancel.addEventListener('click',(e)=>{
  ventanaModal.classList.remove('active');
});
