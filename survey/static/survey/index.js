


document.addEventListener('DOMContentLoaded', function() {

  if(localStorage.getItem('block')){
    load_block(localStorage.getItem('block'))
  }else{
    load_block('#block_qu')
  }

  document.querySelector('#add_quest_block').onclick = () => document.querySelector('#add_q_bl').classList.toggle('none_display')
  document.querySelector('#add_new_surv').onclick = () => document.querySelector('#add_n_surv').classList.toggle('none_display')
  
  document.querySelector('#block_quest').addEventListener('click', () => load_block('#block_qu'));
  document.querySelector('#block_survey').addEventListener('click', () => load_block('#block_s'));
  document.querySelector('#block_library').addEventListener('click', () => load_block('#block_l'));

  let opnSurv = document.querySelectorAll('.open_surv');
  let openStartedSurv = document.querySelectorAll('.open_started_surv');
  let redo_surv = document.querySelectorAll('.redo_surv');
  let updSet = document.querySelectorAll('.upd_surv_bl');
  console.log(opnSurv, 'surv')

  for(let elem of opnSurv){
    elem.onclick = (e) => { 
      console.log(e.target, 'etarget')
      fetch('start_surv/'+e.target.dataset.survid)
      e.target.nextElementSibling.classList.toggle('none_display') };
    
  }


  for(let elem of redo_surv){
    elem.onclick = (e) => e.target.nextElementSibling.classList.toggle('none_display');
  }

  for(let elem of openStartedSurv){
    elem.onclick = (e) => e.target.nextElementSibling.classList.toggle('none_display');
  }

  for(let elem of updSet){
    elem.onclick = (e) => e.target.nextElementSibling.classList.toggle('none_display');
  }

  let linkSet = document.querySelectorAll('.upd_quest');
  
  for(let elem of linkSet){
    elem.onclick = (e) => e.target.nextElementSibling.classList.toggle('none_display');
  }

  let type = document.querySelector('#id_question_type');

  type.onclick = (e) => {
    if(type.options[type.selectedIndex].value != 'text_answ'){
      document.querySelector('#hidden_block').classList.remove('none_display')
    }else{
      document.querySelector('#hidden_block').classList.add('none_display')
    }
  }
})


function load_block(id){
  let list = ['#block_qu', '#block_s', '#block_l']
  localStorage.setItem('block', id);

  for(let el of list){
    let elem = document.querySelector(el);
    console.log(elem, 'elem')
    if(el == id){
      elem.classList.remove('none_display')
    }else{
      elem.classList.add('none_display')
    }

    console.log(el, 'el')
    console.log(id, 'id')
  }

  
}
