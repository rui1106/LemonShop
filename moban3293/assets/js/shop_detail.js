var vm = new Vue({
	el:'#shop_detail',
	data(){
		return {
			host,
			// username,
			shopdetail:'',
			sku_id:'',
      skuid:'',
      count:1,
		}
	},
	mounted(){
		let user = localStorage.username;    
        this.get_sku_id();
        // this.username = user;
        this.get_shop_detail();

	},
	methods:{
		 get_shop_detail:function(){
		 	// this.id = this.$route.query.sku_id;
        	var url = this.host + '/single_product/' + this.sku_id + '/'
        	axios.get(url, {
                responseType: 'json',
            })
              .then(response => {
                    this.shopdetail = response.data;
                
                })
                .catch(error => {
                    console.log(error.response);
                })
  		 },
  		 // 从路径中提取sku_id  single-product.html?sku_id=1
        get_sku_id: function(){
        	// console.log("document.location.pathname="+document.location.toString())
            var re = /\/single-product.html\?sku_id=(\d+)$/;
            this.sku_id = document.location.toString().match(re)[1];
        },
        add_cart:function(id){
            let token = localStorage.token;
            axios.post(this.host + '/carts/',{
                    "skuid":this.sku_id,
                    "count":this.count,
                   }, {
                   headers: {
                      'Authorization': 'JWT ' + token
                   },
                   responseType: 'json'     
            })
            .then(response => {
                  // console.log(response.data.code);
                  if(response.data.code==0){
                    alert('添加购物车成功');
                    this.cart_total_count += response.count;
                  }else{
                    alert(response.data.errmsg);
                  }
                  
            })
            .catch(error => {
                  console.log(error);
            })
        },
     
	}
})