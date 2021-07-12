var vm = new Vue({
	el:'#cart',
	data(){
		return{
			host,
			count:1,
			sku:'',
			cart_goods:[],
      result:0,
      total_prices:0,
		}
	},
	mounted(){
		this.show_cart();
	},
	methods:{
		show_cart:function(){
			let token = localStorage.token;
            axios.get(this.host + '/show_cart/', {
                   headers: {
                      'Authorization': 'JWT ' + token
                   },
                   responseType: 'json'     
            })
            .then(response => {
                  // console.log(response.data.code);
                  if(response.data.code==0){
                  	this.cart_goods = response.data.cart_skus;
                    this.cart = response.data.cart_skus;
                    for(var i=0; i<this.cart.length; i++){
                        // this.count = this.cart[i].count;
                        this.cart[i].amount = ((this.cart[i].price) * this.cart[i].count).toFixed(2);
                        this.result += Number(this.cart[i].amount);
                        console.log(this.result);
                    this.total_prices = parseFloat(this.result) + 10.00
                        // console.log(this.cart[i].amount);
                    // console.log(this.result);
                }
                  	console.log(response.data.errmsg);
                    // alert('添加购物车成功');
                    // this.cart_total_count += response.count;
                  }else{
                    alert(response.data.errmsg);

                  }
                  
            })
            .catch(error => {
                  console.log(error);
                  alert(error);
            })

		},
    on_delete:function(id){
      let token = localStorage.token;
            axios.delete(this.host + '/show_cart/', {
                  data: {
                        sku_id: id,
                    },
                  headers: {
                      'Authorization': 'JWT ' + token
                   },
                   responseType: 'json'     
            })
            .then(response => {
                  // console.log(response.data.code);
                  if(response.data.code==0){
                    alert('删除购物车成功')
                  }else{
                    alert(response.data.errmsg);
                  }
                  
            })
            .catch(error => {
                  console.log(error);
            })
    },
    update_cart:function(){
      let token = localStorage.token;
            axios.post(this.host + '/show_cart/',{
                    "shu_id":this.sku_id,
                    'count':this.count,
                   }, {
                   headers: {
                      'Authorization': 'JWT ' + token
                   },
                   responseType: 'json'     
            })
            .then(response => {
                  // console.log(response.data.code);
                  if(response.data.code==0){
                    alert('修改购物车成功');
                    this.cart_total_count += response.count;
                  }else{
                    alert(response.data.errmsg);
                  }
                  
            })
            .catch(error => {
                  console.log(error);
            })
    }
	}
})