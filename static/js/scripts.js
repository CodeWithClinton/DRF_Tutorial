

let qty = document.getElementById('qty')
let items = document.getElementById('itemTotal')
let alertbox = document.getElementById('alert')
let alertmsg = document.getElementById('alertmsg')
let addBtn = document.getElementById('addToCart')
let updateBtn = document.getElementById('updateCart')

addBtn.addEventListener('click', addToCart, {capture:true})

function addToCart(e){
  e.stopPropagation()
  console.log(e.target)

    let product_id = addBtn.dataset.id
    let action = addBtn.dataset.action
    // addBtn.style.display='None'
    // updateBtn.style.display = 'flex'
   
    document.getElementById('spinner').style.display = 'block'
    // console.log(action)
    // console.log(product_id)




    

    addUserItem(product_id, action)

//     if (user == 'AnonymousUser'){
    
//     addCookieItem(product_id)
// }
// else{
//     addUserItem(product_id, action)
    
    

//     }
  

    
}


function addUserItem(product_id, action){
    
    let url = "/updatecart"

    const data = {p_id: product_id, action:action};

    fetch(url, {
    method: 'POST', // or 'PUT'
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
    console.log(data)
    // alertbox.style.cssText = 'display:flex !important'
    // alertmsg.innerText = 'Item added to cart'
    qty.innerText = data.num_of_items
    document.getElementById('spinner').style.display = 'none'
    
    })

    .catch((error) => {
    console.error('Error:', error);
    });
}

function saveAddress(){

    const data = { username: 'example' };

fetch('https://example.com/profile', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => {
  console.log('Success:', data);
})
.catch((error) => {
  console.error('Error:', error);
});


}
// for(let item of data){
//   cartitemContainer.innerHTML = `  <th scope="row"><div id = "cart_image"><img src = ${item.product.image.url}></div></th>
//   <td><h5>${item.product.name}</h5></td>
//   <td><h5>${parseFloat(item.product.price).toFixed(2)}</h5></td>
//   <td><input type = 'number' class = 'quantity' value = "${item.quantity}"  data-price = {{item.product.price}} data-p_id = {{item.product.id}} style = 'width: 50px; padding-left: 5px'></td>
//   <td><h5>${parseFloat(item.subTotal).toFixed(2)}</h5></td>
//   <td><h5><button class = 'btn btn-danger del'data-p_id = ${item.product.id} >Remove</button></h5></td> `
// }
