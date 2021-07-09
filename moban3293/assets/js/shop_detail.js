var vm = new Vue({
	el:'#shop_detail',
	data(){
		return {
			host,
			// username,
			shopdetail:'',
			sku_id:'',
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
            var re = /\/single-product.html\?sku_id=(\d)$/;
            this.sku_id = document.location.toString().match(re)[1];
        },
	}
})